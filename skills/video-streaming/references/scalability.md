# Scalability, CDN & Auth Reference

## Signed CDN URL generation (Python)

Never expose your S3 origin or raw manifest URLs. Generate short-lived signed URLs at session start. For CloudFront:

```python
import boto3
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime, timedelta, timezone
import base64


def _rsa_signer(private_key_pem: bytes):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    def signer(message: bytes) -> bytes:
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())  # noqa: S303 — CloudFront requires SHA1

    return signer


def sign_stream_url(
    stream_key: str,
    private_key_pem: bytes,
    cf_key_id: str,
    cf_domain: str,
    ttl_seconds: int = 3600,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    cf_signer = CloudFrontSigner(cf_key_id, _rsa_signer(private_key_pem))

    manifest_url = f"https://{cf_domain}/live/{stream_key}/master.m3u8"
    signed_url = cf_signer.generate_presigned_url(manifest_url, date_less_than=expires_at)
    return signed_url
```

## Stream key issuance & validation (TypeScript)

Stream keys are random tokens stored in the database mapped to a user and a stream session. Validate on every RTMP `prePublish` event.

```typescript
import crypto from 'crypto';
import { db } from './db'; // any ORM / query builder

export async function issueStreamKey(userId: string): Promise<string> {
  const key = crypto.randomBytes(24).toString('hex'); // 48-char hex
  await db('stream_keys').insert({
    key,
    user_id: userId,
    created_at: new Date(),
    revoked: false,
  });
  return key;
}

export async function validateStreamKey(key: string): Promise<boolean> {
  const row = await db('stream_keys').where({ key, revoked: false }).first();
  return row !== undefined;
}

export async function revokeStreamKey(key: string): Promise<void> {
  await db('stream_keys').where({ key }).update({ revoked: true });
}
```

## Transcode job queue (Python + Redis / RQ)

Decouple ingest from transcoding so the ingest edge never blocks on FFmpeg startup.

```python
from redis import Redis
from rq import Queue
from transcode import start_transcode   # the function from ingest-transcode.md

redis_conn = Redis.from_url("redis://localhost:6379")
transcode_queue = Queue("transcode", connection=redis_conn)


def on_stream_start(stream_key: str) -> None:
    """Called by the ingest edge when a broadcaster goes live."""
    job = transcode_queue.enqueue(
        start_transcode,
        stream_key,
        job_timeout=7200,      # 2-hour max for a single live session
        result_ttl=600,
        failure_ttl=86400,
    )
    print(f"Transcode job enqueued: {job.id} for key={stream_key}")
```

Run workers on dedicated GPU/CPU instances that can scale independently of the ingest edge:

```bash
rq worker transcode --with-scheduler
```

## Health check endpoint (TypeScript / Express)

Load balancers use this to route traffic only to healthy instances.

```typescript
import express from 'express';

const app = express();

app.get('/health', async (_req, res) => {
  const checks = await Promise.allSettled([
    db.raw('SELECT 1'),          // database reachable
    redis.ping(),                // cache reachable
  ]);

  const healthy = checks.every((c) => c.status === 'fulfilled');
  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'ok' : 'degraded',
    checks: checks.map((c, i) => ({
      name: ['db', 'redis'][i],
      ok: c.status === 'fulfilled',
    })),
  });
});
```

## Horizontal scaling notes

| Component | Scaling strategy |
|-----------|-----------------|
| Ingest edge | DNS round-robin; each pod is stateless after handing the stream off to the queue |
| Transcode workers | Auto-scale on queue depth (CloudWatch / Keda metric) |
| Chat / WebSocket | Socket.IO Redis adapter handles fan-out across pods; scale behind an L4 load balancer |
| API servers | Stateless — scale behind any L7 load balancer (ALB, Nginx, Caddy) |
| Origin storage | S3 / GCS — effectively infinite; CDN absorbs viewer read load |

## CDN cache behavior

| Path | Cache-Control | Reason |
|------|--------------|--------|
| `*.ts` (segments) | `max-age=86400, immutable` | Segment content never changes once written |
| `*.m3u8` (live manifest) | `no-cache` | Must always reflect the latest segment list |
| `master.m3u8` | `max-age=60` | Rarely changes; short TTL is fine |
| Thumbnails | `max-age=30` | Updated every ~30 s; stale is acceptable |

## Monitoring checklist

* **Ingest bitrate drop** — alert if input bitrate falls >20 % below expected for >10 s (streamer network issue)
* **Segment upload lag** — alert if S3 upload lags more than one segment duration behind the live edge
* **Transcode queue depth** — alert if depth > 10 (workers can't keep up)
* **Chat message rate** — track p99 fan-out latency via Redis; alert if >500 ms
* **CDN error rate** — alert on >0.1 % 4xx/5xx across edge pops
* **Player rebuffering ratio** — instrument with hls.js `FRAG_BUFFERED` / `ERROR` events; target <0.5 %
