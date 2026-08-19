# Worker

The worker has no code of its own. It runs the same package as the API
(`apps/api/src/atlas`) with a different entry point, which is the whole idea of
ADR-001: one codebase, more than one process.

Start it:

```bash
make worker
```

Job definitions live in `apps/api/src/atlas/jobs/`.
Nothing enqueues jobs directly — everything goes through `jobs.queue.enqueue()`
(see ADR-008).
