# Future Ideas

This document stores possible future directions that are not committed to the current development scope. When an idea becomes active work, it should move to `TODO.md` with an appropriate status.

## Contents

- [Event Notifications](#event-notifications)
- [User Messages and Admin Inbox](#user-messages-and-admin-inbox)
- [Quiz](#quiz)
- [User Analytics / Ranking](#user-analytics--ranking)
- [Vocabulary Data Model](#vocabulary-data-model)
- [Database Export and Restore](#database-export-and-restore)
- [CSV Import and Logging](#csv-import-and-logging)
- [Post-v1.0.0 Operations and Infrastructure](#post-v100-operations-and-infrastructure)

## Event Notifications

- Extend site announcements with publication time, expiry time, importance, active state, and target user groups.
- Include a reviewer reason or a more detailed result message in vocabulary-request result events.
- Add a one-to-many relationship from `Feedback` to its reply `Event` records so the feedback detail page can show the complete reply-content history in chronological order. The current `Feedback.reply_by` and `reply_at` fields describe only the latest reply; decide later whether each event should store its actor or whether replies should use a dedicated `FeedbackReply` model.

## User Messages and Admin Inbox

- Preserve the relationship between a user message and its latest import batch so processing results remain traceable.
- If several users request vocabulary from the same import batch, notify every affected user of the result.

## Quiz

- Add the complete katakana answer flow.
- Implement a smartphone-style Japanese flick keyboard. Each key represents a kana row such as あ, か, さ, た, な, は, ま, や, or ら; holding and flicking selects another kana in that row.
- If recent-skip behaviour later needs greater precision, retain only the latest ten vocabulary IDs instead of introducing a complete question-history model.

## User Analytics / Ranking

- Analyse users’ learning and answer records to build a ranking page.
- Define ranking metrics, reporting periods, tie-breaking, minimum answer counts, participation, and publicly displayed data when adopted into scope. Account for bias from lifetime answer totals or accuracy based on very few answers.

## Vocabulary Data Model

- Add `Vocab.word_slug` after v1.0.0. Define its source fields, duplicate policy, update behaviour, and migration/backfill strategy first.

## Database Export and Restore

- After v1.0.0, consider `python manage.py export_whole <output_folder>` with separate model files, preserved keys and relationships, a manifest, and an explicit sensitive-data policy.
- Design the matching restore process around dependency order, schema/version preflight, dry-run support, and a single documented export contract.

## CSV Import and Logging

- Consider a database import-history model.
- Allow an admin-inbox/import report to update the originating user message with processing results.
- Duplicate rows currently produce terminal messages and logs. A future enhancement may export all duplicate rows to a separate CSV for review.

## Post-v1.0.0 Operations and Infrastructure

- Add CI that runs the PostgreSQL test suite, then evaluate automated deployment only after rollback and secret-handling boundaries are explicit.
- Periodically restore an off-site backup into an isolated database and compare schema, migrations, row counts, and sequences; successful uploads alone are not recovery proof.
- Confirm scheduled backups and monitoring alerts through natural runs, not only manual invocation, and document retention/cost changes before increasing frequency.
- Replace or renew the Cloudflare Origin CA certificate before 27 October 2029; evaluate ACME/Certbot separately as a learning exercise.
- Increase HSTS duration only after HTTPS and subdomain policy remain stable. Do not enable preload or include-subdomains without reviewing every affected hostname.
- Consider Discord alerts in addition to email, while avoiding duplicate noise from Sentry, UptimeRobot, and Netdata.

