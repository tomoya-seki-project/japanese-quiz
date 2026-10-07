# WordLoop (言葉の輪)

WordLoop is a Django-based Japanese vocabulary learning application. It combines a reviewed shared dictionary with user-specific learning state, weighted quizzes, visual kana feedback, notifications, and feedback workflows.

> **Status:** In development
>
> **Version:** v0.7.0
>
> **Milestone:** Core workflows and the mobile UI are implemented; testing and production deployment remain in progress.

The project is not yet production-ready. Core dictionary, review, account, notification, feedback, and kana quiz workflows are operational. Multiple-choice quizzes, broader automated regression coverage, and production deployment remain incomplete.

## Current Features

### Accounts

- A custom `User` model uses email as the login identifier.
- Registration creates an inactive account that must be activated through a time-limited, single-use email link.
- Activation emails can be resent through a privacy-preserving flow with cooldown protection.
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
- Logging separates console, debug-only, information, and error output.
- File logs rotate daily and retain seven days.
- Domain workflows log outcomes and identifiers without recording credentials, feedback bodies, sessions, or complete POST payloads.

### Mobile Interface

- Account, dictionary, event, feedback, quiz, and HTTP error pages use Tailwind CSS and reusable Django components.
- The layout supports widths from 320 CSS pixels, short viewports, safe areas, and fixed action footers.
- Local Japanese fonts, kana backgrounds, and shared JavaScript support the interface. Generated CSS is committed so Node is unnecessary at runtime.
- Fourteen Playwright browser cases cover routes, responsive overflow, forms, notifications, and quiz interaction; they require a separate browser-test setup.

## Current Priorities

- Expand account, domain, quiz integration, and `QuizAttempt` concurrency tests.
- Complete production settings, secret management, deployment, and database-operation hardening.
- Run and extend browser UI verification across supported viewport sizes and Ajax states.
- Keep unfinished multiple-choice functionality outside the active user flow until its full vertical slice is complete.

See [the project TODO](docs/TODO.md) for current work and [Future Ideas](docs/FUTURE_IDEAS.md) for work outside the current scope.

## Tech Stack

| Area | Technology |
| --- | --- |
| Backend | Django 6.0.5 |
| Language | Python |
| Database | PostgreSQL 16 with Psycopg 3 |
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

Eleven Django regression tests cover template compilation, language boundaries, built-in validation, shared choices, kana keyboard values, escaping, notifications, key detail labels, and the regular-user boundary for the answer-judgement debug dialog. All eleven passed on 7 October 2026 using isolated SQLite test settings. Ten earlier tests also passed on an isolated PostgreSQL test database.

An isolated `japanese_quiz_test` PostgreSQL role can create and remove the test database. Supply its credentials through the shell environment or local/CI secrets:

```bash
DB_USER=japanese_quiz_test DB_PASSWORD="<test-role-password>" python manage.py test
```

Fourteen Playwright browser cases have been added; the CLI was unavailable during the latest documentation sync, so that run was not verified. High-priority missing Django coverage includes activation and email identity, reviewed vocabulary mutations, concurrent request handling, learning-state calculations, answer comparison, and no-pool/full-pool quiz integration.

## Current Limitations

- Multiple-choice import, review, administration, and quiz flows are not connected; their active vocabulary types remain disabled.
- Automated tests do not yet cover the major domain and concurrency paths.
- Full database export and restore are not implemented.
- The mobile layout and answer overlay are implemented; browser verification needs to be run and expanded.
- Settings read secrets, hosts, database, and SMTP values from the environment, but production infrastructure and operational procedures are not ready.

## Security Notes

Settings load secrets, database credentials, SMTP, allowed hosts, and trusted origins from environment variables. With `DEBUG=False`, HTTPS redirect and secure cookies are enabled. Production deployment still requires separate secrets and hosts, correctly configured TLS proxy and static-file serving, PostgreSQL backup and rollback procedures, and `python manage.py check --deploy` in the deployed environment.

## Development History

Development began on 20 May 2026. See [Project History](docs/PROJECT_HISTORY.md) for milestones and [Development Phases](docs/PROJECT_PHASES.md) for a portfolio-oriented technical overview.

## Contributing

This is currently a personal learning project. A contribution guide, issue templates, and pull-request rules have not yet been prepared.

## License

No licence has been selected. Do not assume that the source may be copied, modified, or redistributed until a licence is added.
