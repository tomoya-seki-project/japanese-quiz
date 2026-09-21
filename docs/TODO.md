# Project TODO

This document tracks committed work in the current project scope. Completed milestones are summarised here and described in greater detail in [Project History](PROJECT_HISTORY.md). Uncommitted directions belong in [Future Ideas](FUTURE_IDEAS.md).

## Status

- <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> (12): core workflows or decisions completed
- <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> (1): implementation exists, but required work remains
- <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> (2): committed work not yet started

## Contents

- [Current Work](#current-work)
- [Completed Foundations](#completed-foundations)
- [Verification Backlog](#verification-backlog)

## Current Work

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Expand automated test coverage**

Completed:

- Ten UI and language regression tests pass on an isolated PostgreSQL test database.
- Current coverage includes template compilation, public/admin language boundaries, built-in validation language, shared choices, kana keyboard values, output escaping, notification language, and key detail labels.
- Django system checks and migration drift checks pass.

Remaining:

- Account registration, activation, resend, and case-insensitive email identity.
- Vocabulary request create/update/delete/restore, duplicate pending requests, approval/rejection, and final approval validation.
- User vocabulary synchronisation, `in_use` updates, ownership, active-state boundaries, weight, and streak calculations.
- Quiz answer comparison, filtered/full-pool decisions, initial/Next/Skip/Submit/resume paths, invalid current questions, and empty-pool termination.
- True multi-connection tests for `QuizAttempt` Answer/Skip concurrency and duplicate processing.
- Event, feedback, logging, and management-command behaviour.

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Production settings and deployment hardening**

Required before production:

- Move `SECRET_KEY` and every environment-dependent secret out of source control.
- Use `DEBUG=False` and configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- Enforce HTTPS and secure cookie/proxy settings for the chosen hosting architecture.
- Configure production static-file handling.
- Provision the production PostgreSQL role/database with least privilege.
- Define backup, restore, migration, rollback, logging, and monitoring procedures.
- Run `python manage.py check --deploy` against the production environment.
- Verify real SMTP, domain DNS, sender identity, activation links, and error handling.

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Quiz answer-comparison overlay**

- The result partial currently renders `image_path` and `sub_image_path` sequentially.
- Use HTML/CSS positioning so missing/extra markers appear on the relevant kana image rather than occupying a separate layout position.
- Verify keyboard, screen-reader, responsive, and browser behaviour after the visual redesign.

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

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Bottom-up answer comparison**

- Replaced exponential recursive branching with `O(m × n)` dynamic programming.
- Preserved scoring, match preference, non-normal wrong preference, deterministic tie-breaking, and the response contract.
- Equivalence and worst-case performance were verified during implementation.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **PostgreSQL development backend**

- Development and test execution use PostgreSQL with Psycopg 3.
- The schema can be rebuilt from migrations on a fresh database.
- Application and test roles are separated; the application role remains without `CREATEDB`.
- Existing regression tests pass on an isolated test database.

> <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> **Error handling, logging, and code hygiene**

- Global HTTP error handlers and structured Ajax error handling are in place.
- Account-side vocabulary synchronisation isolates retryable side-effect failures.
- Domain workflows use outcome-oriented, severity-based logging with daily rotation.
- Sensitive request content is excluded from logs.
- Obsolete commented code was removed while intentional post-v1.0.0 placeholders were retained.

## Verification Backlog

The following checks belong to the test-expansion task rather than reopening completed features:

- Concurrent admin review and stale review-form submissions.
- Case-insensitive registration races.
- Concurrent vocabulary synchronisation and event generation.
- Multi-connection Answer-versus-Answer and Answer-versus-Skip races.
- Log routing, rotation, retention, and sensitive-data assertions.
- Full browser coverage for Japanese UI, Ajax focus management, and the final result overlay.

