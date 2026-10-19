# Project TODO

This document tracks work adopted into the current project scope. Completed milestones are summarised here and described in greater detail in [Project History](PROJECT_HISTORY.md). Directions that have not been adopted belong in [Future Ideas](FUTURE_IDEAS.md); Git commit state is recorded separately.

## Status

- <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> (14): core workflows or decisions completed
- <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> (3): implementation exists, but required work remains
- <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> (0): committed work not yet started

## Contents

- [Current Work](#current-work)
- [Completed Foundations](#completed-foundations)
- [Verification Backlog](#verification-backlog)

## Current Work

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Expand automated test coverage**

Completed:

- The isolated SQLite suite discovers 39 Django tests: 37 pass and two PostgreSQL-only concurrency tests skip by design. Django system checks report no issues.
- A targeted `QuizAttempt`/`VocabRequest` suite discovers 12 tests: ten pass on SQLite; the two true multi-connection tests were subsequently confirmed passing with the dedicated PostgreSQL test role.
- Coverage now includes production SMTP validation, database-backed health checks, Redis cooldown failure policy, Sentry privacy filtering, per-IP rate limiting, single-use quiz attempts, and concurrent vocabulary approval. Fourteen Playwright browser cases exist but do not yet have a current pass result.

Remaining:

- Complete browser coverage for registration, activation, resend, and email delivery behaviour.
- Vocabulary request create/update/delete/restore and complete approval/rejection browser flows.
- User vocabulary synchronisation, `in_use` updates, ownership, active-state boundaries, weight, and streak calculations.
- Quiz answer comparison, filtered/full-pool decisions, initial/Next/Skip/Submit/resume paths, invalid current questions, and empty-pool termination.
- Event, feedback, logging, and management-command behaviour.

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Production settings and deployment hardening**

Completed:

- Application settings read secrets, PostgreSQL and SMTP credentials, hosts, and trusted origins from environment variables.
- `DEBUG=False` enables HTTPS redirect and secure session/CSRF cookies; Zoho SMTP and the no-reply alias have sent a real activation email.
- The current working tree adds production dependencies, `STATIC_ROOT`, SMTP fail-fast validation, Redis-backed shared cache with fail-open handling, trusted-proxy HTTPS metadata, a PostgreSQL-backed `/health/` endpoint, console logging, and Sentry privacy filtering.
- Registration and activation resend have shared, fail-open per-IP limits. Local production-like checks include migration drift, `check --deploy`, a two-worker Gunicorn Unix-socket health request, and the test evidence above.

Remaining before production:

- Update release metadata, complete the final dependency/secret/diff inventory, rerun release-candidate checks, produce the planned modification and verification reports, and commit/tag the application-preparation work.
- Supply separate production secrets, host/origin values, TLS proxy settings, Redis, and Nginx static-file serving on the VPS; verify the Cloudflare/Nginx/Gunicorn client-IP trust chain.
- Provision a least-privilege PostgreSQL role and database; implement backup, restore, migration, rollback, systemd/Gunicorn, logging, and monitoring operations.
- Rerun `python manage.py check --deploy` in production and verify DNS, SPF/DKIM/DMARC, activation links, SMTP failure handling, shared Redis behaviour, and Sentry alerts.

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Overdue UserVocab weight adjustment**

- The `adjust_user_vocab_weight` management command has argument and logging scaffolding.
- It does not yet select overdue records, apply a weight policy, or update database rows. Its dry run does not report candidates.

## Completed Foundations

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Reviewed vocabulary request workflow**

- Create, update, delete, and restore requests use one reviewed workflow.
- Approve and Reject are POST actions with permission checks, transactions, row locks, pending-state validation, readonly workflow fields, and separate request/review notes.
- Duplicate pending requests are protected by both service validation and database constraints.
- Approval revalidates final proposed data and the state of `original_vocab`.
- Delete requests retain a complete proposed snapshot.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Vocabulary model integrity**

- Public lists and direct user flows exclude inactive vocabulary.
- `VocabActionService` owns the official vocabulary mutation paths.
- General and katakana types create the appropriate detail record.
- Admin cannot directly add vocabulary or change an existing type in a way that bypasses service invariants.
- Unsupported multiple-choice types remain unavailable while their schema foundation is preserved.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **User vocabulary ownership and selection**

- `UserVocab` separates shared dictionary data from each user's learning state.
- List, detail, and bulk `in_use` operations are scoped to the authenticated owner.
- Candidate IDs are captured and validated consistently across GET and POST.
- Inactive vocabulary cannot enter the active learning or quiz pool.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Account activation and email identity**

- Registration creates inactive accounts and sends a time-limited activation link.
- Activation and resend flows use privacy-preserving responses and cooldown protection.
- Production cooldown state is shared through Redis and fails open with error logging if the cache is unavailable; registration and resend also apply permissive per-IP limits.
- Email is canonicalised to lowercase across manager, public forms, and admin forms.
- A case-insensitive database constraint is the final identity-uniqueness guard.
- Vocabulary synchronisation begins only after account activation.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Event notifications**

- `Event` and `UserEvent` separate shared event content from recipient read state.
- Request results, vocabulary synchronisation summaries, and feedback replies create user events.
- Event list/detail and read/history flows are operational.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Feedback workflow**

- Authenticated users can submit supported feedback types.
- Superusers can review and reply.
- Follow-up replies are allowed until `CLOSED`.
- Transactional row locking protects state transitions and reply side effects.
- Duplicate submission is guarded without relying on empty action forms.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz selection and explicit pool policy**

- Quiz filters, weighted random selection, and recent-question exclusion are operational.
- An empty filtered pool requires an explicit user decision; it never silently widens the selected scope.
- Full-pool choice persists across initial, Next, and Skip requests.
- Insufficient full-pool size returns the user to vocabulary management with a warning.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Quiz session recovery**

- Resume, Answer, and Skip revalidate the displayed question.
- Invalid questions do not mutate learning state.
- An invalid current question or empty next pool produces a reason-specific early summary.
- All terminal paths share summary rendering and `quiz_session` cleanup.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **QuizAttempt idempotency**

- Every displayed question has a unique, database-backed attempt token.
- Answer and Skip resolve the authoritative question from the attempt.
- PostgreSQL row locks and post-lock `PENDING` checks allow only one learning-state mutation.
- Answer and Skip use a consistent `QuizAttempt → UserVocab` lock order.
- Frontend submission guards improve UX but are not treated as the integrity boundary.
- A PostgreSQL-only test uses two threads and independent database connections to verify that concurrent processing applies the mutation once.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Bottom-up answer comparison**

- Replaced exponential recursive branching with `O(m × n)` dynamic programming.
- Preserved scoring, match preference, non-normal wrong preference, deterministic tie-breaking, and the response contract.
- Equivalence and worst-case performance were verified during implementation.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **PostgreSQL development backend**

- Development and test execution use PostgreSQL with Psycopg 3.
- The schema can be rebuilt from migrations on a fresh database.
- Application and test roles are separated; the application role remains without `CREATEDB`.
- The dedicated test role successfully runs the PostgreSQL-only `QuizAttempt` and `VocabRequest` concurrency tests.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Error handling, logging, and code hygiene**

- Global HTTP error handlers and structured Ajax error handling are in place.
- Account-side vocabulary synchronisation isolates retryable side-effect failures.
- Domain workflows use outcome-oriented, severity-based logging with daily rotation.
- Sensitive request content is excluded from logs.
- Obsolete commented code was removed while intentional post-v1.0.0 placeholders were retained.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Mobile UI and answer-comparison overlay**

- Major account, dictionary, event, feedback, quiz, and HTTP error pages use shared Django components and Tailwind CSS.
- The layout targets 320 CSS pixels, short viewports, safe areas, and a fixed action footer.
- The result partial overlays missing/extra markers on the corresponding kana image. The detailed judgement dialog is limited to superusers.
- Generated CSS, local Japanese fonts, background assets, and JavaScript interactions are committed; fourteen Playwright browser cases provide a verification foundation.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **QuizAttempt retention command**

- `clear_quiz_attempt` removes processed attempts older than a configurable number of days while retaining `PENDING` attempts.
- It supports `--dry-run`, validates the retention period, and logs the result. Scheduling and candidate-data automated coverage remain future operational work.

## Verification Backlog

The following checks belong to the test-expansion task rather than reopening completed features:

- Concurrent admin review and stale review-form submissions.
- Case-insensitive registration races.
- Concurrent vocabulary synchronisation and event generation.
- Broader Answer-versus-Answer and Answer-versus-Skip browser/integration combinations beyond the existing database concurrency test.
- Log routing, rotation, retention, and sensitive-data assertions.
- Execute and extend the fourteen Playwright cases for responsive layouts, Ajax focus management, and the result overlay.

