# Infrastructure

Deployment configuration. The API Dockerfile lives in `apps/api/Dockerfile` because it
builds from that folder.

The exact hosting providers are chosen when the first deployment happens (open question
Q15). Everything is configured by environment variables, so the choice is a deployment
detail and not a code change (ADR-013).
