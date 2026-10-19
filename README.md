# WordLoop (言葉の輪)

WordLoop is a Django-based Japanese vocabulary learning application. It combines a reviewed shared dictionary with user-specific learning state, weighted quizzes, visual kana feedback, notifications, and feedback workflows.

> **Status:** In development
>
> **Latest tagged version:** v0.9.6
>
> **Target release:** v1.0.0
>
> **Milestone:** Production-readiness Phase 1 is complete. Phase 2 application preparation is in progress and remains uncommitted.

The project is not yet deployed or ready for public production use. Core dictionary, review, account, notification, feedback, and kana quiz workflows are operational. The current v1.0.0 candidate work adds application-side production safeguards and tests, while release finalisation, VPS infrastructure, live monitoring, backup/recovery, browser verification, and multiple-choice quizzes remain incomplete.

## Current Features

### Accounts

- A custom `User` model uses email as the login identifier.
- Registration creates an inactive account that must be activated through a time-limited, single-use email link.
- Activation emails can be resent through a privacy-preserving flow with cooldown protection. Production cooldown state is shared through Redis and fails open with error logging if the cache is unavailable.
- Registration and resend apply permissive per-IP limits. Production accepts the client IP only from the value overwritten by the controlled Nginx proxy.
- Registration, login, resend, and admin forms canonicalise email addresses to lowercase.
- A case-insensitive database constraint prevents duplicate identities that differ only by letter case.
- Login, logout, profile, and optional remember-me sessions are supported.

### Dictionary and Personal Vocabulary

- The public dictionary lists active vocabulary and supports word, kana, multi-select type, JLPT level, and category filters.
- General vocabulary and katakana-specific vocabulary are supported.
- Each user has independent `UserVocab` learning state, including `in_use`, weight, answer counts, streak, and last quiz time.
- Users can manage personal learning data without directly modifying shared vocabulary records. Vocabulary and personal-vocabulary filters have separate mobile pages; result links preserve the filtered page when returning from details.

### Reviewed Vocabulary Requests

- Authenticated users can request vocabulary creation, update, deletion, or restoration.
- Request creation is transactional and protected against duplicate pending requests by service checks and database constraints.
- Users may provide an optional request reason; reviewers may add a separate review note.
- Django Admin provides POST-based Approve and Reject actions.
- Approval executes the appropriate domain service. Rejection changes request state without modifying vocabulary and requires a review note.
- Review uses `transaction.atomic()`, row locks, pending-state checks, permission checks, and readonly workflow fields.
- Result notifications include the review note.

The `MCSense` schema foundation exists, but its import, request, admin, and quiz runtime flows are intentionally not exposed yet.

### Quiz

- Quiz settings filter by vocabulary type, JLPT level, and category.
- Questions come from the current user's active, in-use vocabulary.
- Weighted random selection favours higher-weight items and avoids the ten most recently used records.
- An empty filtered pool never silently ignores the user's settings. The user can return to settings or explicitly confirm a full active/in-use pool.
- Resume, Answer, and Skip revalidate ownership, `in_use`, and vocabulary active state.
- If the current question becomes invalid or the pool becomes empty, the quiz ends through a shared summary and session-cleanup path.
- The play screen uses server-rendered Ajax partials for Answer, Result, Next, Skip, and Summary.
- Every displayed question creates a `QuizAttempt` with a unique UUID token.
- Answer and Skip lock the attempt and `UserVocab` in one transaction and allow only a `PENDING` attempt to mutate learning state.
- A frontend in-flight guard reduces ordinary double clicks; database idempotency remains the authoritative protection.
- A custom kana keyboard and hint counter feed the normal backend validation flow.
- Answer feedback distinguishes match, wrong, missing, and extra kana, including dakuten, handakuten, and small-kana subtypes.
- Answer comparison uses an `O(m × n)` bottom-up dynamic-programming algorithm with deterministic tie-breaking.
- The summary tracks answered, correct, incorrect, skipped, and hint counts. The result UI overlays missing and extra markers on the corresponding kana image.

### Interface Language

- User-facing screens are in Japanese.
- Django Admin remains in English; project-built pages, including staff feedback screens, use Japanese.
- Request-level middleware selects `ja` or `en-us` by page responsibility and restores the previous language after the response.
- Stored values, keyboard data attributes, and JavaScript event contracts remain language-independent.

### Events and Feedback

- `Event` and `UserEvent` provide per-user notification history and read state.
- Vocabulary request results, vocabulary synchronisation summaries, and feedback replies generate events.
- Authenticated users can submit vocabulary suggestions, bulk requests, bug reports, and feature requests.
- Superusers can review and reply to feedback; replies notify the submitter.
- Follow-up replies are permitted until feedback reaches its terminal `CLOSED` state. Staff can filter feedback by status, and notification details support read/unread controls.

### Error Handling and Logging

- Global `400`, `403`, `404`, and `500` handlers are registered.
- Quiz Ajax actions return structured validation errors and the client handles non-JSON, network, and parsing failures.
- Account entry points use a resilient vocabulary-sync wrapper so retryable side-effect failures do not unnecessarily block login or registration.
- Development logging separates console, debug-only, information, and error output; development file logs rotate daily and retain seven days.
- Non-debug production logging uses console output only so Gunicorn/systemd can collect it without competing application file handlers.
- Domain workflows log outcomes and identifiers without recording credentials, feedback bodies, sessions, or complete POST payloads.

### Mobile Interface

- Account, dictionary, event, feedback, quiz, and HTTP error pages use Tailwind CSS and reusable Django components.
- The layout supports widths from 320 CSS pixels, short viewports, safe areas, and fixed action footers.
- Local Japanese fonts, kana backgrounds, and shared JavaScript support the interface. Generated CSS is committed so Node is unnecessary at runtime.
- Fourteen Playwright browser cases cover routes, responsive overflow, forms, notifications, and quiz interaction; they require a separate browser-test setup.

### Production-Readiness Foundation

- Production dependencies include Gunicorn, the Redis client, and the Django Sentry SDK integration.
- `STATIC_ROOT` supports `collectstatic`; generated `staticfiles/` output is not committed and is intended to be served by Nginx.
- Non-debug startup validates required SMTP configuration instead of silently falling back to development email behaviour.
- Non-debug requests use trusted-proxy HTTPS metadata, secure cookies, HTTPS redirect, and configurable HSTS.
- `/health/` performs a lightweight PostgreSQL `SELECT 1` check and returns `200` or `503`; Redis is deliberately not a hard-fail health dependency.
- Production logging writes to stdout/stderr for Gunicorn and systemd journal collection. Sentry is enabled only outside debug mode when a DSN is supplied and filters activation credentials, cookies, headers, request bodies, and other sensitive context.
- Local production-like verification has covered migration drift, Django deployment warnings, a two-worker Gunicorn Unix-socket health request, and graceful shutdown. These checks do not replace VPS validation.

## Current Priorities

- Finalise v1.0.0 release metadata, review the dependency/secret/diff inventory, rerun release-candidate checks, and commit/tag the application-preparation work.
- Expand browser and integration coverage for complete account, vocabulary-review, quiz-pool, answer, navigation, and operational flows.
- Provision and verify the VPS, Nginx, systemd/Gunicorn, PostgreSQL, Redis, TLS/proxy trust, static files, Sentry, monitoring, backup/restore, and rollback procedures.
- Run and extend browser UI verification across supported viewport sizes and Ajax states.
- Keep unfinished multiple-choice functionality outside the active user flow until its full vertical slice is complete.

See [the project TODO](docs/TODO.md) for current work and [Future Ideas](docs/FUTURE_IDEAS.md) for work outside the current scope.

## Tech Stack

| Area | Technology |
| --- | --- |
| Backend | Django 6.0.5 |
| Language | Python |
| Database | PostgreSQL 16 with Psycopg 3 |
| Shared cache | Redis in production; local-memory cache in development |
| Application server | Gunicorn sync workers behind Nginx (planned deployment) |
| Error monitoring | Sentry SDK integration; live project configuration remains pending |
| Frontend | Django Templates, Tailwind CSS, and vanilla JavaScript |
| Authentication | Django Auth with a custom `User` model |
| Time zone | Asia/Tokyo |

## Main Data Models

### Accounts

- `User`: custom email-based user.
- `UserProfile`: account profile extension.

### Dictionary

- `Vocab`: shared word, kana, meaning, type, level, category, and active state.
- `VocabDetail`: detail extension for general vocabulary.
- `KatakanaDetail`: katakana-specific data such as the native Japanese equivalent.
- `UserVocab`: user-specific learning state for shared vocabulary.
- `VocabRequest`: reviewed create, update, delete, and restore request.
- `MCSense`: foundation for ordered multiple-choice senses, questions, and distractors.

### Core

- `TimeStampedModel`: reusable creation and update timestamps.
- `Event`: notification master record.
- `UserEvent`: per-user event assignment and read state.
- `Feedback`: user submission, handling state, and administrator reply metadata.

### Quiz

- `QuizAttempt`: authoritative, single-use state for one Answer or Skip operation.

## Project Structure

```text
accounts/      User model, authentication, activation, and account pages
assets/        Source and exported visual assets
config/        Django settings, root URLs, WSGI, and ASGI
core/          Shared models, events, feedback, and base templates
devtools/      Development-only tools, including image generators
dictionary/    Vocabulary models, forms, views, admin, and services
docs/          Public project documentation
errorHandler/  Global HTTP error handlers and templates
log/           Generated runtime logs; log files are ignored by Git
quiz/          Quiz settings, selection, attempts, and Ajax play flow
frontend/      Tailwind CSS source and isolated browser-test setup
```

Additional public documentation:

- [Development phases](docs/PROJECT_PHASES.md)
- [Project history](docs/PROJECT_HISTORY.md)
- [Project TODO](docs/TODO.md)
- [Future ideas](docs/FUTURE_IDEAS.md)

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/tomoya-seki-project/japanese-quiz.git
cd japanese-quiz
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Depending on the environment, use `py` or `python3` instead of `python`.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

### 4. Configure PostgreSQL

Create a local PostgreSQL role and database, then copy the example environment file:

```bash
cp .env.example .env
```

Set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`. The local `.env` contains credentials and must not be committed.

### 5. Initialise and run the application

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Development URLs:

- Application: `http://127.0.0.1:8000/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Main URLs

| URL | Purpose |
| --- | --- |
| `/` | Project home |
| `/accounts/` | Account home |
| `/accounts/user_regist/` | Registration |
| `/accounts/user_login/` | Login |
| `/accounts/user_detail/` | User profile |
| `/dictionary/` | Dictionary home |
| `/dictionary/vocab/list` | Active vocabulary list |
| `/dictionary/vocab/create` | Create-vocabulary request |
| `/dictionary/user_vocab/list` | Current user's vocabulary |
| `/quiz/` | Quiz home |
| `/quiz/setting` | Quiz settings |
| `/quiz/play` | Ajax quiz play |
| `/health/` | Django and PostgreSQL health check (`200`/`503`) |
| `/core/feedback/` | Role-based feedback entry |
| `/core/feedback/create/` | Submit feedback |
| `/core/feedback/list/` | Superuser feedback list |
| `/admin/` | Django Admin |

## Management Commands

### Import vocabulary

```bash
python manage.py import_vocab list.csv
```

The command authenticates a superuser, validates required headers, creates vocabulary through `VocabActionService`, supports up to three categories, continues after row-level validation or integrity errors, and prints a summary.

Expected headers:

```text
word,kana,meaning,type,level,category1,category2,category3,native_japanese
```

### Seed categories

```bash
python manage.py setup_categories resource/categories.csv
```

### Clear development vocabulary

```bash
python manage.py dev_clear_vocab
```

This destructive command is intended only for local development and testing. Full database export and restore remain planned work.

## Visual Assets and Development Tools

Source files live under `assets/source/`, exported assets under `assets/export/`, and helper scripts under `devtools/`.

Generate reusable kana background tiles with:

```bash
python devtools/image_generator/generate_kana_bg.py
```

## Frontend Development

Install the frontend tools with `npm ci`. Use `npm run css:watch` while developing and `npm run css:build` before reviewing or deploying changes. Edit `frontend/css/app.css`; `static/css/app.css` is generated and committed.

Browser-test setup and isolated fixtures are documented in [frontend/README.md](frontend/README.md).

## Testing

The isolated SQLite suite discovers 39 Django tests: 37 pass and two PostgreSQL-only concurrency tests skip by design. It covers the existing UI/language contracts plus production SMTP validation, the database-backed health endpoint, Redis cooldown failure policy, Sentry privacy filtering, per-IP rate limiting, single-use quiz attempts, and concurrent vocabulary approval.

An isolated `japanese_quiz_test` PostgreSQL role can create and remove the test database. Supply its credentials through the shell environment or local/CI secrets:

```bash
DB_USER=japanese_quiz_test DB_PASSWORD="<test-role-password>" python manage.py test
```

A targeted `QuizAttempt`/`VocabRequest` suite discovers 12 tests: ten pass with SQLite settings, and the two true multi-connection tests were subsequently confirmed passing with the dedicated PostgreSQL test role. Fourteen Playwright browser cases exist but do not yet have a current pass result. Important remaining coverage includes complete registration/activation and vocabulary-review browser flows, learning-state calculations, answer comparison, and no-pool/full-pool quiz integration.

## Current Limitations

- Multiple-choice import, review, administration, and quiz flows are not connected; their active vocabulary types remain disabled.
- Automated coverage has expanded, including two PostgreSQL concurrency cases, but complete browser and integration coverage is still missing.
- Full database export and restore are not implemented.
- The mobile layout and answer overlay are implemented; browser verification needs to be run and expanded.
- Application-side production hardening exists in the current uncommitted working tree, but release finalisation, production infrastructure, and operational procedures are not complete.

## Security Notes

Settings load secrets, database credentials, SMTP, Redis, allowed hosts, trusted origins, and optional Sentry configuration from environment variables. With `DEBUG=False`, HTTPS redirect, secure cookies, trusted-proxy HTTPS handling, HSTS, Redis cache, SMTP fail-fast validation, and optional Sentry initialisation are enabled. Production deployment still requires separate secrets and hosts, a verified Cloudflare/Nginx/Gunicorn trust boundary, Nginx static-file serving, least-privilege PostgreSQL, backup/restore and rollback procedures, monitoring, and a fresh `python manage.py check --deploy` review in the deployed environment.

## Development History

Development began on 20 May 2026. See [Project History](docs/PROJECT_HISTORY.md) for milestones and [Development Phases](docs/PROJECT_PHASES.md) for a portfolio-oriented technical overview.

## Contributing

This is currently a personal learning project. A contribution guide, issue templates, and pull-request rules have not yet been prepared.

## License

No licence has been selected. Do not assume that the source may be copied, modified, or redistributed until a licence is added.
