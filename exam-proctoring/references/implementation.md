# Exam Proctoring - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) | Camera/mic capture API usage | Proctoring sessions need controlled media capture with explicit permission handling |
| Official docs | [source](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API/Using_Screen_Capture) | Screen capture setup and lifecycle | Exam integrity workflows often require monitored screen-share events |
| Official docs | [source](https://www.w3.org/TR/webauthn-2/) | WebAuthn ceremonies and assertion model | Candidate identity checks benefit from standards-based strong authentication |
| OSS repo | [source](https://github.com/openedx/edx-proctoring) | Proctoring workflow service in production LMS ecosystem | Violation events and review queues require explicit proctoring domain workflows |

## Category-specific notes

- Category: `exam-proctoring`
- Family: `people-learning-engagement`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
