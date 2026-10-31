# Project History

This document records significant implementation milestones, architectural decisions, schema changes, and verification checkpoints. Minor wording and documentation-only changes are intentionally omitted.

## 2026-05 — Foundation and Accounts

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-05-20 | `ad4deee` | Created the Django project and the initial application boundaries. |
| 2026-05-20 | `adf7f9e` | Added the initial data model and custom email-based user manager. |
| 2026-05-25 | `be08b3d` | Implemented registration, login, logout, and core authentication views. |
| 2026-05-29 | `c67a9d0` | Added the user area, profile foundation, and initial vocabulary-creation path. |

### Engineering direction

- Adopted a custom user model before building domain features.
- Separated authentication data, profile data, shared vocabulary, and user-specific learning state.
- Established Django apps as responsibility boundaries rather than organising all behaviour in one module.

## 2026-06 — Reviewed Vocabulary and User Learning State

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-06-02 | `e8b7bb8` | Added the `VocabRequest` foundation. |
| 2026-06-02 | `cdcd761` | Completed create requests and expanded account metadata. |
| 2026-06-04 | `bc37573` | Added restore requests and separated request-related modules. |
| 2026-06-06 | `259ce8e` | Added the update-request workflow. |
| 2026-06-07 | `0280a4d` | Expanded vocabulary browsing and refined request schema. |
| 2026-06-09 | `99e7214` | Added the user vocabulary list and nullable request proposal fields. |
| 2026-06-10 | `144c719` | Completed create and delete request paths. |
| 2026-06-12 | `d16bdd6` | Added dictionary admin foundations and redesigned type-specific detail data. |
| 2026-06-14 | `80c655f` | Cleaned admin data presentation and schema labels. |
| 2026-06-15 | `244c793` | Established the custom admin review architecture. |
| 2026-06-17 | `d65b3df` | Made request creation transaction-safe. |
| 2026-06-19 | `c1979dc` | Added custom `UserAdmin` groundwork and prepared vocabulary services. |
| 2026-06-20 | `913e765` | Completed admin user creation and introduced `VocabActionService`. |
| 2026-06-20 | Working-tree checkpoint | Designed quiz filtering and the kana keyboard. |
| 2026-06-21 | `b483c51` | Added transactional Approve/Reject processing with state checks. |
| 2026-06-22 | `567adc4` | Added superuser-authenticated CSV vocabulary import. |
| 2026-06-23 | `595ad0b` | Added `UserVocab` selection and normalised service naming. |
| 2026-06-27 | Working-tree checkpoint | Added `UserVocab.in_use` and hardened admin review. |
| 2026-06-28 | Working-tree checkpoint | Drafted login-time vocabulary synchronisation and bulk in-use updates. |
| 2026-06-29 | `5cdf658` | Stabilised the normal dictionary workflow before full-flow testing. |

### Engineering direction

- Shared vocabulary became review-controlled master data.
- Create, update, restore, and delete converged on reusable service operations.
- Transactions, row locks, pending-state checks, and constraints progressively replaced UI-only assumptions.
- `UserVocab` became the owner of per-user learning state and activation.

## 2026-07 — Events, Categories, and Ajax Quiz Foundation

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-07-01 | `f51693a` | Added `Event` and `UserEvent` data-model foundations. |
| 2026-07-02 | `9a746a1` | Added kanji CSV resources and hardened dictionary admin. |
| 2026-07-02 | `e1e56df` | Added Ajax partial pagination for the vocabulary list. |
| 2026-07-06 | `e61baea` | Added UserVocab Ajax pagination and verified the dictionary workflow. |
| 2026-07-10 | `bf579ac` | Migrated categories to a model-backed many-to-many relationship. |
| 2026-07-11 | `0d8b401` | Connected vocabulary-request results to notifications. |
| 2026-07-14 | `14c04a6` | Added vocabulary-sync summary events. |
| 2026-07-19 | `f616e5c` | Improved event and admin management. |
| 2026-07-20 | `615dc9f` | Added the initial quiz-question flow. |
| 2026-07-23 | `3beeeb3` | Restructured quiz partial endpoints. |
| 2026-07-25 | `7cc32df` | Added fallback handling and active-vocabulary guards. |
| 2026-07-28 | `41db40d` | Added the Ajax quiz interface and kana input panel. |
| 2026-07-30 | `726517e` | Completed the first usable Ajax quiz-play interface. |
| 2026-07-30 | `23b8327` | Added Skip and shared Ajax payload helpers. |

### Engineering direction

- Events separate shared notification content from per-recipient read state.
- Categories moved from fixed fields to relational data.
- Quiz interaction remained server-rendered while Ajax replaced only the changing fragments.
- Question selection introduced user filters, weights, recent-question exclusion, and session state.

## 2026-08 — Visual Feedback, Support Workflows, and Resilience

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-08-01 | `7af87d6` | Added kana visual assets and image-generation tools. |
| 2026-08-11 | `a8af3c5` | Added kana-by-kana visual answer comparison. |
| 2026-08-11 | `f41fe5d` | Added active-vocabulary safeguards and an image-resizing helper. |
| 2026-08-13 | `ea9ab55` | Added the user feedback workflow. |
| 2026-08-14 | `4d14a87` | Added UserVocab detail and learning controls. |
| 2026-08-18 | `c8ee779` | Hardened feedback, events, permissions, and vocabulary review. |
| 2026-08-22 | `5bc6f06` | Added vocabulary-type groundwork and an August import dataset. |
| 2026-08-24 | `8295da5` | Added the multiple-choice sense model foundation and repository safeguards. |
| 2026-08-25 | `11634f6` | Added global error handling and resilient vocabulary synchronisation. |
| 2026-08-28 | `300ab7c` | Added application logging and a safer 500 fallback. |
| 2026-08-31 | `f47ece0` | Extended logging across domain workflows. |
| 2026-08-31 | `3ad1709` | Improved synchronisation consistency and complete request snapshots. |

### Engineering direction

- Answer differences became explicit operations: match, wrong, missing, and extra.
- Ownership, active state, and workflow state were enforced on the server.
- Multiple-choice schema was introduced without exposing an incomplete runtime path.
- Expected validation failures, HTTP errors, and unexpected exceptions received different response and logging contracts.
- Retryable side effects were isolated from critical account operations.

## 2026-09 — Performance, Identity, Recovery, and Concurrency

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-09-02 | `a5b071b` | Isolated unsupported vocabulary types from active workflows. |
| 2026-09-05 | `e78408e` | Replaced recursive answer comparison with bottom-up DP and tightened type isolation. |
| 2026-09-06 | `ee31424` | Localised the user interface into Japanese and added request-level language boundaries. |
| 2026-09-08 | `012ae67` | Added explicit full-pool confirmation and separate request/review context. |
| 2026-09-09 | `9062a2e` | Added account email activation. |
| 2026-09-12 | `89d3030` | Added canonical email identity and quiz terminal recovery. |
| 2026-09-16 | `10f6dd2` | Migrated development to PostgreSQL and committed `QuizAttempt` idempotency. |
| 2026-09-17 | `236784f` | Moved security and SMTP settings to the environment and added HTTPS defaults. |
| 2026-09-22 | `e87ac95` | Split vocabulary filtering from results and preserved return navigation. |
| 2026-09-25 | `7bc9b5e` | Added multi-select vocabulary filters and completed Japanese interface labels. |
| 2026-09-30 | `69b3c87` | Added kana palette tooling, QuizAttempt retention, and weight-command scaffolding. |

## Detailed September Decisions

### Bottom-up answer comparison

The previous recursive branch search had exponential worst-case behaviour. The replacement fills an `O(m × n)` dynamic-programming table, ranks candidate operations by cost, matches, and non-normal wrongs, then reconstructs the selected result path. It preserves the existing result contract and deterministic tie-breaking.

Verification compared the old and new algorithms across 24,336 input pairs of length zero to three without a mismatch. A 25-character full mismatch completed in approximately 0.0018 seconds.

### Interface-language boundary

Project-built pages, including staff feedback screens, use Japanese; Django Admin uses English. Request-level middleware activates the appropriate language and restores the previous language after the response. Database choice values and JavaScript contracts remain stable; only display labels change.

The first ten regression tests cover template compilation, language routing, built-in validation language, shared choices, keyboard values, output escaping, notifications, and detail labels.

### Explicit quiz-pool choice

An empty filtered pool no longer silently selects out-of-scope questions. The user must return to settings or POST an explicit full-pool confirmation. The session remembers this decision across initial, Next, and Skip requests. If even the full pool is below the minimum size, the user returns to vocabulary management with a warning.

### Vocabulary review context

`VocabRequest` now stores an optional submitter `request_reason` separately from the reviewer's `review_note`. Reject requires a note; Approve keeps it optional. The note is included in the result notification.

### Email activation and identity integrity

Registration creates an inactive account. A 24-hour, single-use token confirms the email before activation and initial vocabulary synchronisation. Resend uses uniform responses and cooldown protection.

Email canonicalisation is centralised in the user manager and applied by account and admin forms. A functional unique constraint on `Lower("email")` prevents case-only duplicates at the database boundary.

### Quiz terminal recovery

Resume, Answer, and Skip revalidate the displayed `UserVocab` owner, `in_use` state, and related vocabulary active state. If the current question is invalid, the quiz ends without mutating learning state. If the next pool is empty, the pool builder emits a terminal signal and a shared summary helper renders the result and clears the session.

### PostgreSQL and QuizAttempt idempotency

The development backend moved from SQLite to PostgreSQL 16 with Psycopg 3 so row-level locking semantics match the concurrency design.

Each displayed question creates a `QuizAttempt` with a unique UUID and `PENDING` state. Answer and Skip:

1. start one atomic transaction;
2. resolve and lock the attempt;
3. verify that it is still `PENDING`;
4. resolve the authoritative question from the attempt;
5. lock only the required `UserVocab` row;
6. apply the learning-state mutation;
7. mark the attempt `ANSWERED` or `SKIPPED`.

Concurrent duplicates wait at the row lock and then observe the completed state, so they return `already_processed` without repeating side effects. Both operations use the same `QuizAttempt → UserVocab` lock order to reduce deadlock risk.

PostgreSQL 16.15, the migration graph, 24 database tables, transactional rollback behaviour, Answer/Skip single-use smoke checks, and the ten existing regression tests were verified. A dedicated test role may create and delete isolated test databases; the application role remains `NOCREATEDB`.

The PostgreSQL and QuizAttempt work was committed as `10f6dd2` on 16 September 2026.

## 2026-10 — Workflow Refinement and Mobile UI

| Date | Commit | Milestone |
| --- | --- | --- |
| 2026-10-04 | `8e77709` | Added notification return paths, quiz settings restore, and unanswered-question guards. |
| 2026-10-04 | `314c866` | Refined feedback filtering, notification bulk updates, vocabulary requests, and query loading. |
| 2026-10-07 | `a909a7e` | Applied Tailwind UI across the application and added browser-test scaffolding. |
| 2026-10-12 | `32ac5c8` (`v0.9.6`) | Kept the current question visible inside the mobile quiz keyboard dialog and synchronised it across Ajax question changes. |
| 2026-10-20 | `40124f3` | Hardened application settings, shared cache, health, logging, Sentry privacy, rate limiting, and deployment tests. |
| 2026-10-22 | `eb92d3e` | Strengthened vocabulary collection/import tooling and prepared the deployment candidate. |
| 2026-10-31 | `af7513a` | Made the `400` handler resilient to errors raised before URL resolution completes. |

### Engineering direction

- Navigation preserves a validated return URL, while state-changing actions keep server-side guards.
- Quiz settings, full-pool choice, and active-session state have distinct responsibilities.
- Shared Django components, Tailwind CSS, and vanilla JavaScript provide the mobile UI without introducing a separate frontend application.
- The result view positions missing and extra markers over the relevant kana images.
- Quiz question context is duplicated inside the keyboard dialog deliberately; Ajax state changes update both the page and dialog to prevent stale prompts.
- Eleven Django tests passed with isolated SQLite settings on 7 October 2026. Fourteen Playwright cases exist, but the CLI was unavailable for this documentation sync.

## 2026-10-23 to 2026-10-31 — First Production Deployment

WordLoop was deployed to an Ubuntu 24.04 LTS VPS at `https://wordloop.silent-mori.com/` behind Cloudflare and Nginx. Gunicorn runs under systemd with PostgreSQL and loopback-only Redis. Static assets, SMTP activation, proxy/client-IP trust, Sentry privacy filtering, uptime monitoring, resource monitoring, and public error boundaries were verified in the deployed environment.

All 40 Django tests passed against PostgreSQL. PostgreSQL backups were configured locally and in private Cloudflare R2 storage with retention and scheduling. A restore into an isolated database matched tables, migrations, row counts, and sequences. A real rollback to `eb92d3e` and roll-forward to `af7513a` both returned a healthy response after restart retry handling.

This infrastructure work is recorded as operational evidence alongside the repository release history. The verified application and documentation state forms the `v1.0.0` release baseline.

## Current Position

By the end of October 2026, WordLoop has operational end-to-end paths for accounts, reviewed vocabulary, personal learning state, notifications, feedback, and kana quizzes, and v1.0.0 is publicly deployed. Application code was verified at `af7513a`; the final release baseline adds the completed project documentation. Remaining work includes broader automated browser coverage, ongoing operational checks, and a complete multiple-choice vertical slice.

