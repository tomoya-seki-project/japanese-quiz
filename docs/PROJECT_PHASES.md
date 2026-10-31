# WordLoop — Development Phases

This document presents WordLoop's product evolution and engineering decisions as a portfolio-oriented overview. For commit-level chronology and database changes, see [Project History](PROJECT_HISTORY.md).

## Project Snapshot

WordLoop is a Django-based Japanese vocabulary learning system. It began as a simple dictionary and evolved into a reviewed shared vocabulary workflow, user-specific learning state, weighted quizzes, Ajax interaction, notifications, feedback, resilient error handling, logging, PostgreSQL row locking, and idempotent quiz actions.

The architecture is guided by five principles:

- Separate shared `Vocab` master data from each user's `UserVocab` learning state.
- Route shared dictionary mutations through a reviewed `VocabRequest` workflow.
- Centralise cross-model transactions and domain rules in services.
- Select questions from the user's own active state, weight, streak, and recent history.
- Use Django Templates and vanilla JavaScript for server-rendered Ajax partials.

## Phase Overview

| Phase | Period | Main outcome |
| --- | --- | --- |
| [1](#phase-1-project-foundation-and-account-system) | 2026-05-20 to 2026-05-29 | Django foundation, custom user, authentication |
| [2](#phase-2-dictionary-and-reviewed-vocabulary-workflow) | 2026-06-02 to 2026-06-22 | Dictionary, requests, admin review, transactions |
| [3](#phase-3-personal-vocabulary-data-operations-and-notifications) | 2026-06-23 to 2026-07-19 | User vocabulary, CSV operations, categories, events |
| [4](#phase-4-quiz-core-and-ajax-interaction) | 2026-07-20 to 2026-07-30 | Weighted quiz and Ajax Answer/Next/Skip |
| [5](#phase-5-visual-learning-feedback) | 2026-08-01 to 2026-08-11 | Kana assets and answer-difference feedback |
| [6](#phase-6-user-facing-workflows-and-domain-hardening) | 2026-08-13 to 2026-08-22 | Feedback, ownership, active-state safeguards |
| [7](#phase-7-extensibility-and-application-resilience) | 2026-08-24 to 2026-08-28 | MC schema, error recovery, logging foundation |
| [8](#phase-8-workflow-observability-and-project-review) | 2026-08-31 | Domain logging and whole-project review |
| [9](#phase-9-quiz-performance-and-interface-language) | 2026-09-02 to 2026-09-06 | Bottom-up DP, Japanese UI, initial tests |
| [10](#phase-10-explicit-quiz-pool-choice-and-review-context) | 2026-09-07 to 2026-09-08 | Explicit pool fallback and request/review reasons |
| [11](#phase-11-account-verification-and-email-identity-integrity) | 2026-09-09 to 2026-09-12 | Email activation and canonical identity |
| [12](#phase-12-quiz-session-terminal-recovery) | 2026-09-12 | Invalid-question and empty-pool recovery |
| [13](#phase-13-postgresql-and-quiz-attempt-idempotency) | 2026-09-15 to 2026-09-16 | PostgreSQL and single-use quiz attempts |
| [14](#phase-14-production-settings-foundation) | 2026-09-17 | Environment-based security and SMTP configuration |
| [15](#phase-15-mobile-vocabulary-navigation) | 2026-09-22 to 2026-09-25 | Filter/result navigation, multi-select filters, Japanese labels |
| [16](#phase-16-maintenance-command-foundation) | 2026-09-30 | Kana asset tooling and QuizAttempt retention |
| [17](#phase-17-workflow-navigation-and-state-refinement) | 2026-10-04 | Notification, feedback, vocabulary, and quiz controls |
| [18](#phase-18-tailwind-mobile-ui) | 2026-10-07 | Tailwind UI, shared components, and browser-test foundation |
| [19](#phase-19-production-readiness-and-application-preparation) | 2026-10-17 to 2026-10-20 | Readiness review, production hardening, and deployment-test foundation |
| [20](#phase-20-first-production-deployment-and-recovery-verification) | 2026-10-23 to 2026-10-31 | VPS deployment, public HTTPS, monitoring, backup/restore, and rollback verification |

## Phase 1: Project Foundation and Account System

**Period:** 2026-05-20 to 2026-05-29

### Objective

Create a maintainable Django foundation and a stable identity boundary for later dictionary, quiz, and personal-learning features.

### Outcomes

- Created the `accounts`, `dictionary`, `quiz`, and `core` application boundaries.
- Implemented a custom email-based `User` and custom manager.
- Added registration, login, logout, remember-me sessions, profiles, and `UserProfile`.
- Established initial templates, URL routing, and model relationships.

### Key decisions

- Adopt a custom user model at project start rather than migrate away from Django's default user later.
- Keep account-wide profile data separate from authentication fields.
- Treat email as the login identity.

## Phase 2: Dictionary and Reviewed Vocabulary Workflow

**Period:** 2026-06-02 to 2026-06-22

### Objective

Build a shared dictionary that users can propose changes to without directly mutating master data.

### Outcomes

- Added `Vocab` with type-specific `VocabDetail` and `KatakanaDetail` records.
- Built create, update, delete, and restore `VocabRequest` flows.
- Added POST-based Approve and Reject controls to Django Admin.
- Moved vocabulary mutations into `VocabActionService`.
- Added atomic request creation and review, row locks, pending-state checks, and duplicate-request constraints.
- Added an authenticated CSV import command.

### Key decisions

- Shared dictionary changes require review.
- Soft deletion is the normal removal path.
- Services own multi-model mutations; forms and views own input and presentation.
- Application checks provide clear feedback while database constraints remain the final concurrency guard.

## Phase 3: Personal Vocabulary, Data Operations, and Notifications

**Period:** 2026-06-23 to 2026-07-19

### Objective

Create independent learning state for each user and support bulk data and notification workflows.

### Outcomes

- Added user-specific `UserVocab` state and the `in_use` learning selection.
- Added synchronisation between active shared vocabulary and user records.
- Migrated categories to a model-backed many-to-many relationship.
- Added category seeding, development reset, and improved CSV import reporting.
- Introduced `Event`, `UserEvent`, notification history, and vocabulary-request result events.
- Added Ajax pagination to vocabulary lists.

### Key decisions

- Never store user progress on the shared `Vocab` row.
- Keep import and seeding operations behind management commands.
- Separate an event's shared content from each recipient's read state.

## Phase 4: Quiz Core and Ajax Interaction

**Period:** 2026-07-20 to 2026-07-30

### Objective

Build a session-driven quiz with weighted selection and responsive interaction while retaining server-rendered templates.

### Outcomes

- Added filters by type, level, and category.
- Implemented weighted random selection and recent-question exclusion.
- Added session tracking for question state and summary counts.
- Implemented Answer, Result, Next, and Skip through Ajax partial responses.
- Added a reusable payload layer for quiz partials and errors.
- Added the first custom kana keyboard and hint flow.

### Key decisions

- The server remains authoritative for question and learning state.
- Ajax replaces page fragments rather than introducing a separate SPA API.
- Skip is a learning outcome and updates weight, streak, and last quiz time.

## Phase 5: Visual Learning Feedback

**Period:** 2026-08-01 to 2026-08-11

### Objective

Turn answer checking into clear, kana-level learning feedback.

### Outcomes

- Added kana image assets and generation tools.
- Added match, wrong, missing, and extra answer operations.
- Added wrong subtypes for dakuten, handakuten, and small kana.
- Rendered visual answer-difference feedback through quiz result partials.
- Expanded kana keyboard and answer-display behaviour.

### Key decisions

- Keep comparison output independent of presentation assets.
- Represent differences as deterministic operations that templates can render.
- Store source artwork separately from generated runtime assets.

## Phase 6: User-Facing Workflows and Domain Hardening

**Period:** 2026-08-13 to 2026-08-22

### Objective

Complete user support workflows and strengthen server-side ownership and data-integrity boundaries.

### Outcomes

- Added feedback submission, administrator review, replies, and result notifications.
- Added detailed `UserVocab` management.
- Protected inactive vocabulary from public lists, direct URLs, and quiz pools.
- Added ownership checks for user-specific detail views.
- Preserved complete delete-request snapshots.
- Added additional vocabulary-type schema groundwork.

### Key decisions

- Normal UI paths are not security boundaries; ownership and active-state checks belong on the server.
- Feedback can receive follow-up replies until it reaches terminal `CLOSED` state.
- Request snapshots must retain enough data for meaningful review.

## Phase 7: Extensibility and Application Resilience

**Period:** 2026-08-24 to 2026-08-28

### Objective

Prepare extensible multiple-choice data while improving failure recovery and operational visibility.

### Outcomes

- Added the `MCSense` schema foundation for ordered senses, questions, and distractors.
- Added global `400`, `403`, `404`, and `500` handlers.
- Standardised Ajax success and validation-error contracts.
- Added resilient vocabulary synchronisation at account entry points.
- Added severity-based console and rotating-file logging.
- Added a minimal custom 500-rendering path with fewer dependencies.

### Key decisions

- Schema groundwork does not make an unfinished feature available to users.
- Expected validation failures, HTTP errors, and unexpected exceptions require different contracts.
- Retryable side effects should not unnecessarily block login or registration.
- Logs must avoid credentials and complete request payloads.

## Phase 8: Workflow Observability and Project Review

**Period:** 2026-08-31

### Objective

Extend logging across domain workflows and use a whole-project review to separate defects from unfinished features.

### Outcomes

- Added outcome-oriented logging to requests, review, user-vocabulary sync, quizzes, accounts, events, feedback, and management commands.
- Standardised log context around operations, IDs, counts, and results.
- Added the `MCSense` migration.
- Reviewed the project from learner, content, data-integrity, and product/UX perspectives.
- Identified answer-comparison performance, filter fallback, unsupported MC paths, and automated testing as priority areas.

### Key decisions

- An unfinished feature is a defect only when users can enter an unsupported path or it breaks an existing flow.
- Logging should cover meaningful state changes and rejections without producing query-level noise.

## Phase 9: Quiz Performance and Interface Language

**Period:** 2026-09-02 to 2026-09-06

### Objective

Remove the answer-comparison worst case, isolate unsupported vocabulary types, and establish a Japanese user interface with English administration.

### Outcomes

- Replaced exponential recursive answer comparison with `O(m × n)` bottom-up dynamic programming.
- Verified old/new equivalence across 24,336 input pairs up to three characters; a 25-by-25 full mismatch completed in about 0.0018 seconds.
- Disabled unfinished `adverb`, `mimetic`, `conjunction`, and `colloquial` choices while preserving schema groundwork.
- Localised user-facing templates, forms, validation, events, and quiz output into Japanese.
- Added request-level `ja`/`en-us` language routing.
- Added ten initial UI and language regression tests.

### Key decisions

- Store only the DP state required to choose the best next operation, then reconstruct the result path.
- Preserve stable database values and JavaScript contracts while translating display labels.
- Select language by page responsibility rather than only by user role.

## Phase 10: Explicit Quiz Pool Choice and Review Context

**Period:** 2026-09-07 to 2026-09-08

### Objective

Respect the user's quiz filters and preserve the reasoning from both request submitters and reviewers.

### Outcomes

- Replaced silent out-of-scope quiz fallback with an explicit full-pool confirmation page.
- Persisted the choice in the session for initial, Next, and Skip requests.
- Redirected users to vocabulary management when the full pool is below the minimum size.
- Added optional `request_reason` and separate `review_note` fields.
- Required a review note for Reject while keeping it optional for Approve.
- Included review notes in result notifications.

### Key decisions

- User-selected quiz scope must not be silently widened.
- Request and review reasons represent different actors and moments, so they require separate fields.

## Phase 11: Account Verification and Email Identity Integrity

**Period:** 2026-09-09 to 2026-09-12

### Objective

Turn email from a simple identifier into a verified, canonical, database-protected account identity.

### Outcomes

- Added inactive registration and a 24-hour, single-use activation link.
- Added activation confirmation, success, invalid-link, sent-email, and resend screens.
- Added resend cooldown and privacy-preserving responses.
- Deferred vocabulary synchronisation until activation succeeds.
- Centralised lowercase email canonicalisation in the custom manager and all account/admin forms.
- Added a case-insensitive `Lower("email")` unique constraint.

### Key decisions

- Activation tokens depend on password, email, and active state so identity changes invalidate old links.
- Form validation provides clear errors; the database remains the final duplicate-identity guard.
- Real SMTP, shared cache, HTTPS, and secret management are deployment concerns.

## Phase 12: Quiz Session Terminal Recovery

**Period:** 2026-09-12

### Objective

Terminate quiz sessions consistently when the displayed question becomes invalid or the pool becomes empty.

### Outcomes

- Revalidated ownership, `in_use`, and active state during resume, Answer, and Skip.
- Prevented invalid questions from changing learning state.
- Added a terminal `quiz_ended` signal from the pool builder.
- Added shared summary construction and session cleanup.
- Added distinct `question_unavailable` and `no_question_pool` reason codes.

### Key decisions

- If the displayed question becomes invalid, explain and end the session instead of silently replacing it.
- Changes to undisplayed questions are reflected naturally when the next pool is built.
- Expected domain absence should use a controlled terminal response rather than break the Ajax contract with a 404.

## Phase 13: PostgreSQL and Quiz Attempt Idempotency

**Period:** 2026-09-15

### Objective

Use a database with real row-level locking and give every Answer or Skip operation a single-use database identity.

### Outcomes

- Migrated the development backend from SQLite to PostgreSQL with Psycopg 3.
- Rebuilt the schema from migrations and explicitly reimported foundation data.
- Added `QuizAttempt` with a unique UUID token and `PENDING`, `ANSWERED`, and `SKIPPED` states.
- Created an attempt for every displayed question and carried its token through the session and hidden forms.
- Resolved the authoritative question from the attempt instead of trusting a client-provided update target.
- Locked `QuizAttempt` and then `UserVocab` in a fixed order inside one transaction.
- Returned `already_processed` after a duplicate request waits for the first transaction.
- Added a separate PostgreSQL test role and verified all ten existing tests against an isolated test database.

### Key decisions

- A row lock makes concurrent transactions wait; the status check after the lock enforces single use.
- Answer and Skip must share the same lock order to reduce deadlock risk.
- `select_for_update(of=("self",))` avoids accidentally locking a read-only related vocabulary row.
- A stale request must not clear a newer attempt from the session.
- Attempt history remains available for audit; a retention command was added later, while scheduling remains future work.

## Phase 14: Production Settings Foundation

**Period:** 2026-09-17

### Objective

Make application settings configurable for deployment without storing credentials in source files.

### Outcomes

- Moved the Django secret, hosts, trusted origins, PostgreSQL connection, and SMTP settings to environment variables.
- Added HTTPS redirect, secure cookies, and configurable HSTS when `DEBUG=False`.
- The configured Zoho sender alias was subsequently verified with a real activation email.

### Remaining work

Hosting, TLS proxy configuration, static-file serving, least-privilege production database setup, backup, and `check --deploy` still require deployment-environment verification.

## Phase 15: Mobile Vocabulary Navigation

**Period:** 2026-09-22 to 2026-09-25

### Objective

Make vocabulary filtering and return navigation practical on narrow screens.

### Outcomes

- Separated vocabulary and personal-vocabulary filter pages from paginated results.
- Preserved GET filters and page number when entering and returning from detail pages, with validated return URLs.
- Added multi-select type, JLPT level, category, and applicable in-use filters.
- Completed Japanese labels across project-owned user interfaces.

### Key decision

Filter state stays in the URL so pagination and detail navigation share one source of truth.

## Phase 16: Maintenance Command Foundation

**Period:** 2026-09-30

### Objective

Prepare repeatable kana asset conversion and safe QuizAttempt retention.

### Outcomes

- Added kana palette tooling and generated 389 preview assets with a conversion report.
- Added `clear_quiz_attempt` with configurable retention, `--dry-run`, logging, and protection for `PENDING` attempts.
- Created an `adjust_user_vocab_weight` command scaffold; overdue selection and weight mutation remain unfinished.

## Phase 17: Workflow Navigation and State Refinement

**Period:** 2026-10-04

### Objective

Clarify navigation and action guards before applying the new UI.

### Outcomes

- Added notification read/unread controls and service-backed bulk updates.
- Added feedback status filtering and safer return paths.
- Let quiz settings load the previous selection and blocked Next or Finish before answering.
- Improved post-submit vocabulary-request navigation, vocabulary query loading, and bulk in-use feedback.

### Key decision

A validated return URL guides navigation; server-side checks remain responsible for workflow state changes.

## Phase 18: Tailwind Mobile UI

**Period:** 2026-10-07

### Objective

Apply the mobile design to actual Django pages.

### Outcomes

- Rebuilt account, dictionary, event, feedback, quiz, and HTTP error pages with Tailwind CSS and shared Django components.
- Added local Japanese fonts, backgrounds, logo, UI JavaScript, mobile input states, and a kana answer overlay.
- Committed generated CSS and added fourteen Playwright browser cases with isolated browser-test settings.
- Increased the Django regression suite to eleven tests.

### Verification and limits

System and migration checks and eleven Django tests passed. Browser cases were not run during the documentation sync because Playwright CLI was unavailable. Multiple-choice flows, core domain and concurrency tests, and production deployment remain unfinished.

## Phase 19: Production Readiness and Application Preparation

**Period:** 2026-10-17 to 2026-10-20

**Status:** Complete.

### Objective

Convert a repository-wide production-readiness review into the smallest application-side changes and repeatable checks required before provisioning a VPS.

### Outcomes so far

- Completed a read-only readiness review that classified six high-priority and four medium-priority findings into application work, local verification, VPS validation, and post-v1.0.0 work.
- Added production dependencies, `STATIC_ROOT`, SMTP fail-fast validation, Redis-backed shared cache with fail-open handling, trusted-proxy HTTPS metadata, a PostgreSQL-backed `/health/` endpoint, console logging, and Sentry integration with privacy filtering.
- Added permissive per-IP limits for registration and activation resend. Production uses only the `X-Real-IP` value overwritten by the controlled Nginx proxy; cache failure follows the documented fail-open availability policy.
- Expanded the Django suite to 39 discovered tests. The isolated SQLite run passes 37 and skips two PostgreSQL-only cases; the two true multi-connection concurrency tests were subsequently confirmed passing with the dedicated PostgreSQL test role.
- Completed migration-drift and whitespace checks, a production-like `check --deploy` review, and a two-worker Gunicorn Unix-socket request to `/health/` with graceful shutdown.

### Key decisions

- Redis shares cooldown and rate-limit state across Gunicorn workers. If Redis is unavailable, email flows remain available and errors are logged, accepting that both abuse-control layers pause during the outage.
- `/health/` uses `SELECT 1` to verify the Django-to-PostgreSQL path; Redis is deliberately not a hard-fail health dependency.
- Django's `HTTP_X_FORWARDED_PROTO` setting name represents the WSGI mapping of the incoming `X-Forwarded-Proto` header. Its safety still depends on the Cloudflare, Nginx, and Gunicorn trust boundary.
- Sentry initialises only outside debug mode when a DSN exists, and strips activation tokens, cookies, headers, and request bodies before transmission.
- Per-IP thresholds were adopted as a Phase 2 implementation decision on 20 October rather than retroactively treated as part of the original deployment plan.

### Result

The application-side blockers were implemented, committed, and carried into the VPS deployment. Infrastructure verification remained a separate phase so local readiness evidence was not presented as proof of production operation.

## Phase 20: First Production Deployment and Recovery Verification

**Period:** 2026-10-23 to 2026-10-31

**Status:** Complete; this phase defines the verified `v1.0.0` release baseline.

### Outcomes

- Provisioned an Ubuntu 24.04 LTS VPS with key-based administration, firewalling, intrusion protection, unattended security updates, and a non-login application user.
- Deployed Nginx, systemd-managed Gunicorn, PostgreSQL, loopback-only Redis, collected static assets, and Cloudflare Origin CA TLS at `https://wordloop.silent-mori.com/`.
- Configured proxied DNS, Full (strict) encryption, an origin boundary limited to Cloudflare traffic, trusted client-IP restoration, and cache bypass for dynamic application responses.
- Connected Sentry, UptimeRobot, and Netdata and verified error delivery, sensitive activation-path filtering, availability email alerts, node offline/recovery notifications, and resource baselines.
- Passed all 40 Django tests against PostgreSQL and completed manual production smoke checks for accounts, activation email, vocabulary review operations, quizzes, and error pages.
- Implemented local and Cloudflare R2 off-site database backups with retention and scheduling, then restored into an isolated database and compared schema, migrations, row counts, and sequences.
- Performed a real rollback to the previous commit and roll-forward to release candidate `af7513a`; both health checks returned `200` after restart retry handling.

### Post-release operations

- Confirm the first naturally scheduled 03:20 JST backup and complete the initial 24–72-hour observation window.
- Keep the 14 Playwright cases visible as incomplete automated browser evidence; manual smoke checks do not replace them.

## Current Architecture

```text
Browser / Django Templates / Tailwind CSS / Vanilla JavaScript
                    |
             Forms and CBV Views
                    |
      +-------------+--------------+
      |             |              |
Vocab services  Quiz service   Core services
      |             |         Event / Feedback
      +-------------+--------------+
                    |
 Django ORM / PostgreSQL Transactions / Row Locks
                    |
Accounts | Dictionary | UserVocab | QuizAttempt | Events | Feedback
```

Responsibility boundaries:

- **Middleware, views, and forms:** interface language, HTTP input, validation presentation, redirects, and JSON responses.
- **Services:** domain rules, multi-model orchestration, transactions, and side effects.
- **Models and constraints:** persistence, uniqueness, relationships, and basic integrity.
- **Templates and JavaScript:** server-rendered UI, Ajax partial replacement, and kana input.
- **Management commands:** bulk imports, category seeding, QuizAttempt retention, and development resets.

## Engineering Themes Demonstrated

- Custom Django authentication and admin customisation.
- Service-layer separation and reusable mutation paths.
- Transactions, row locks, conditional constraints, and concurrency control.
- Foreign keys, many-to-many modelling, and separation of master data from user state.
- Session-driven quiz lifecycle, weighted selection, and learning statistics.
- Server-rendered Ajax partials with structured frontend recovery.
- Domain-specific answer comparison and visual asset tooling.
- Permission, ownership, active-state, and soft-delete boundaries.
- Severity-based logging, daily rotation, retention, and sensitive-data limits.

## Current State and Remaining Work

The v1.0.0 application is publicly deployed at `https://wordloop.silent-mori.com/`. Production PostgreSQL, Redis, Nginx/Gunicorn, TLS, monitoring, off-site backup/restore, and rollback have direct verification evidence. Important remaining work includes:

- Expand browser and integration coverage for complete account, vocabulary-review, quiz-pool, answer, navigation, and operational flows. The production-aligned PostgreSQL suite currently passes all 40 tests, including the `QuizAttempt` and `VocabRequest` concurrency cases.
- Complete the first scheduled-backup observation and early production monitoring window; continue practising restore and rollback procedures.
- Finish multiple-choice import, admin, request, and quiz flows before re-enabling their vocabulary types.
- Run and expand browser-level visual checks for the implemented mobile layout and answer-comparison overlay.
- Consider a durable outbox/retry design only if best-effort post-commit notifications later require guaranteed delivery.

See [TODO](TODO.md) for committed work and [Future Ideas](FUTURE_IDEAS.md) for uncommitted directions.

