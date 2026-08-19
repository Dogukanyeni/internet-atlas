## What and why

<!-- One or two sentences. What does this change, and which user problem does it serve? -->

**Phase:**
**Closes:**

## Definition of Done

Tick every line, or write why it does not apply.

- [ ] Code reviewed (by yourself with fresh eyes if working alone)
- [ ] Tests written and passing in CI
- [ ] Authorization and validation in place for every new endpoint
- [ ] Loading, empty, error, unauthorized and archived states handled (UI changes)
- [ ] Logs, metrics or events added where they will be needed
- [ ] Documentation updated (README, ADR, or the phase document)
- [ ] Migration has a working rollback (database changes)
- [ ] `make check` passes locally

## Vision guardrails

Only tick the ones this change touches.

- [ ] Makes the graph **denser or more trustworthy**, not only bigger
- [ ] The user can still see **where to go next** from every screen touched
- [ ] No AI output reaches public data without human review
- [ ] Every new fact carries provenance, confidence and a verified date

## How to test

<!-- Exact steps a reviewer can follow. -->

## Risk

<!-- What could break? What is the rollback plan? -->
