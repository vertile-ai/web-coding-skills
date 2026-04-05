# Queue Management - implementation references

Use this source audit format to keep guidance authentic and code-backed.

| Source type | URL | Code/example anchor | Rationale link |
|---|---|---|---|
| Official docs | [source](https://www.twilio.com/docs/taskrouter) | TaskRouter queues/workers/workflows model | Queue systems need explicit queue, worker, and routing primitives for lane assignment |
| Official docs | [source](https://www.twilio.com/docs/taskrouter/workflow-configuration) | Workflow expressions and task routing rules | Priority lanes and no-show handling should be policy-driven, not hardcoded branches |
| Official docs | [source](https://www.postgresql.org/docs/current/functions-window.html) | Window functions for rolling averages/percentiles | Wait-time estimation should be computed from historical service-time distributions |
| Official docs | [source](https://socket.io/docs/v4/rooms/) | Room-targeted broadcast patterns | Called/served state should fan out in realtime to the right counter/lane displays |

## Category-specific notes

- Category: `queue-management`
- Family: `field-scheduling`
- Tier: `Tier 1`
- Keep recommendations opinionated and list rejected alternatives when they materially affect architecture.
