# Ingest & Transcoding Reference

## RTMP ingest endpoint (Node.js / TypeScript)

Use `node-media-server` as the RTMP ingest edge. Validate the stream key on connect; reject unknown keys immediately so no transcode resources are wasted.

```typescript
import NodeMediaServer from 'node-media-server';
import { validateStreamKey } from './auth';

const nms = new NodeMediaServer({
  rtmp: { port: 1935, chunk_size: 60000, gop_cache: true, ping: 60, ping_timeout: 30 },
  http: { port: 8000, mediaroot: './media', allow_origin: '*' },
});

nms.on('prePublish', async (id, StreamPath, args) => {
  // StreamPath = "/live/<streamKey>"
  const streamKey = StreamPath.split('/')[2];
  const session = nms.getSession(id);

  const isValid = await validateStreamKey(streamKey);
  if (!isValid) {
    session.reject(); // closes the RTMP connection immediately
    return;
  }

  console.log(`Stream accepted: key=${streamKey}`);
});

nms.on('donePublish', (id, StreamPath) => {
  console.log(`Stream ended: ${StreamPath}`);
  // trigger post-processing / recording finalization here
});

nms.run();
```

## Transcoding pipeline (Python + FFmpeg)

The transcoder subscribes to an ingest event (e.g. from a queue), then spawns FFmpeg with the full ABR ladder. Each rung is written as HLS segments directly to a local staging directory, which a separate uploader syncs to S3.

```python
import subprocess
import shlex
from pathlib import Path

QUALITY_LADDER = [
    {"name": "1080p", "scale": "1920:1080", "vb": "5000k", "ab": "192k"},
    {"name": "720p",  "scale": "1280:720",  "vb": "2800k", "ab": "128k"},
    {"name": "480p",  "scale": "854:480",   "vb": "1200k", "ab": "128k"},
    {"name": "360p",  "scale": "640:360",   "vb": "700k",  "ab": "96k"},
]

def build_ffmpeg_cmd(rtmp_url: str, out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build per-rung output args
    rung_args: list[str] = []
    stream_map: list[str] = []

    for i, rung in enumerate(QUALITY_LADDER):
        rung_args += [
            f"-map", "0:v", "-map", "0:a",
            f"-vf:v:{i}", f"scale={rung['scale']}",
            f"-c:v:{i}", "libx264", f"-b:v:{i}", rung["vb"],
            f"-c:a:{i}", "aac", f"-b:a:{i}", rung["ab"],
        ]
        stream_map.append(f"v:{i},a:{i},name:{rung['name']}")

    hls_segment_pattern = str(out_dir / "%v/seg%03d.ts")
    hls_playlist_pattern = str(out_dir / "%v/index.m3u8")

    return [
        "ffmpeg", "-re",
        "-i", rtmp_url,
        *rung_args,
        "-f", "hls",
        "-hls_time", "2",              # 2-second segments (low-latency friendly)
        "-hls_list_size", "5",         # keep 5 segments in the live playlist
        "-hls_flags", "delete_segments+append_list",
        "-master_pl_name", "master.m3u8",
        "-var_stream_map", " ".join(stream_map),
        hls_segment_pattern,
    ]


def start_transcode(stream_key: str) -> subprocess.Popen:
    rtmp_url = f"rtmp://localhost:1935/live/{stream_key}"
    out_dir = Path(f"/tmp/hls/{stream_key}")
    cmd = build_ffmpeg_cmd(rtmp_url, out_dir)
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
```

## Segment uploader (Python, async)

Watches the local HLS output directory and uploads new `.ts` segments and `.m3u8` playlists to S3 as they appear. The manifest is always uploaded last so viewers never reference a segment that has not arrived yet.

```python
import asyncio
import aioboto3
from pathlib import Path
from watchfiles import awatch

S3_BUCKET = "my-stream-origin"
S3_PREFIX = "live"


async def upload_file(s3_client, local_path: Path, stream_key: str) -> None:
    s3_key = f"{S3_PREFIX}/{stream_key}/{local_path.parent.name}/{local_path.name}"
    content_type = "video/MP2T" if local_path.suffix == ".ts" else "application/x-mpegURL"
    extra = {
        "ContentType": content_type,
        # No-cache for manifests so the CDN always fetches fresh playlists;
        # long cache for segments since they are immutable once written.
        "CacheControl": "no-cache" if local_path.suffix == ".m3u8" else "max-age=86400",
    }
    await s3_client.upload_file(str(local_path), S3_BUCKET, s3_key, ExtraArgs=extra)


async def watch_and_upload(stream_key: str) -> None:
    watch_dir = Path(f"/tmp/hls/{stream_key}")
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        async for changes in awatch(watch_dir):
            segments = [Path(p) for _, p in changes if Path(p).suffix == ".ts"]
            manifests = [Path(p) for _, p in changes if Path(p).suffix == ".m3u8"]

            # Upload segments first, manifests after
            await asyncio.gather(*[upload_file(s3, f, stream_key) for f in segments])
            await asyncio.gather(*[upload_file(s3, f, stream_key) for f in manifests])
```

## Thumbnail extraction (Python)

Extract a keyframe thumbnail every 30 seconds from the live stream for preview cards.

```python
def extract_thumbnail(stream_key: str, timestamp_sec: int, out_path: Path) -> None:
    rtmp_url = f"rtmp://localhost:1935/live/{stream_key}"
    cmd = [
        "ffmpeg", "-ss", str(timestamp_sec),
        "-i", rtmp_url,
        "-vframes", "1",
        "-q:v", "2",          # JPEG quality (2 = high, 31 = low)
        "-vf", "scale=640:-1",
        str(out_path),
        "-y",
    ]
    subprocess.run(cmd, check=True, timeout=10)
```
