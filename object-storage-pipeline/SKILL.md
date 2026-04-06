---
name: web-coding-skills-object-storage-pipeline
description: Used when building object-storage ingestion and retrieval modules for web applications with signed URLs and metadata workflows.
---

# Object Storage Pipeline playbook

## Purpose / category boundary

Application-layer object storage module for upload validation, signed URL lifecycle, metadata indexing, and retrieval workflow consistency.

## When to use

- Your products rely on document/media/file uploads and controlled retrieval.
- You need one reusable coding pattern across many business categories.
- You need deterministic file metadata + storage-key lifecycle.

## When not to use

- You are designing bucket/network/infrastructure provisioning.
- You only store tiny blobs directly in transactional tables.
- You need a broad “data platform” umbrella without upload/retrieval boundaries.

## Baseline stack

| Layer | Opinionated default |
|---|---|
| API | Upload-init, upload-complete, and retrieve endpoints |
| Backend (Python) | FastAPI/Flask service with storage adapter |
| Backend (JS) | Hono/Express service with storage adapter |
| Storage | S3-compatible object storage via app-owned abstraction |
| Data | PostgreSQL metadata + integrity state |
| Security | Signed URL issuance + content-type/size validation |

## Module split

- `ingest/` - upload initialization and validation policy
- `storage-adapter/` - provider-agnostic put/get/delete operations
- `metadata/` - object metadata persistence and search keys
- `access/` - signed URL issuance and expiry rules
- `processing/` - optional post-upload processing triggers
- `audit/` - object lifecycle and access trail

## Data / workflow model

`upload-init -> signed-upload -> upload-complete -> metadata-commit -> retrieve/expire -> audit`.

Core entities:

- `object_record`
- `object_access_token`
- `object_processing_task`
- `object_event`

## Strong opinions / defaults

- Decouple storage provider API from domain objects with an adapter boundary.
- Never trust client MIME or size metadata without server-side validation.
- Keep metadata state machine explicit (`pending`, `active`, `quarantined`, `deleted`).

## Overengineering warnings

- Do not build custom CDN/cache invalidation orchestration in v1.
- Avoid coupling virus-scan infra details into core upload domain logic.
- Do not prematurely split media and document pipelines unless policies diverge.

## TS/Python example note

Use TypeScript/Python only.

```ts
type UploadTicket = { key: string; expiresAt: string };
const isExpired = (t: UploadTicket, nowIso: string) => nowIso > t.expiresAt;
```

```python
def is_expired(expires_at: str, now_iso: str) -> bool:
    return now_iso > expires_at
```

## References / local reference links

- [Implementation references](references/implementation.md)
- See `docs/skill-authoring-policy.md` for evidence requirements.
