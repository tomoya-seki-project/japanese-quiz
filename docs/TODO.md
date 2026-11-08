# Project TODO

This document tracks work after v1.0.0; the next version number is undecided. Completed v1.0.0 items are archived in [TODO_v1_0_0.md](TODO_v1_0_0.md). Unadopted ideas belong in [Future Ideas](FUTURE_IDEAS.md).

## Status

- <span style="background:#1b5e20;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">DONE</span> (0): core workflows or decisions completed
- <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> (2): implementation exists, but required work remains
- <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> (8): committed work not yet started

## Contents

- [Post-v1.0.0 Multiple-Choice Quiz](#post-v100-multiple-choice-quiz)
- [Event Notifications](#event-notifications)
- [VocabRequest Review](#vocabrequest-review)
- [Current Work](#current-work)
- [Verification Backlog](#verification-backlog)

## Post-v1.0.0 Multiple-Choice Quiz

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Complete multiple-choice quiz flow**

- Re-enable `adverb`, `mimetic`, `conjunction`, and `colloquial` only after their complete question, option-generation, submission, checking, response, and rendering flow is implemented.
- Treat these values as project-specific learning categories rather than strict linguistic parts of speech. Resolve overlap in the order: inherent mimetic use, sentence-connecting role, modifier role, and finally colloquial recognition value. Send unresolved cases to an ambiguity queue with evidence instead of forcing a classification.
- Extend the CSV contract with `question1`, `question2`, `mc_answer1`, `mc_answer2`, and `mc_answer3` after `native_japanese`. Non-MC rows should use `---` for these fields.
- Give each sense two short, natural example questions. Hide the target with `____`, place inflection hints immediately after it, and normally limit each question to 50 Unicode characters, allowing up to 100 only when clarity requires it.
- Store the correct base form and three unique distractors. Every distractor must be clearly wrong for both questions and backed by verified natural usage.
- Validate blanks, literal `\n`, hints, length, grammar, inflection, semantics, and type. Randomise displayed options while preserving stable CSV roles.
- Keep one `Vocab` per `(word, kana)` and multiple `MCSense` records. Senses have independent meanings, questions, and distractors while sharing `UserVocab` learning state.
- Select MC questions in two random stages: first select a `Vocab` using the existing `UserVocab.weight` weighted random process, then select uniformly from that vocabulary's `MCSense` records. The number of senses must not increase the vocabulary's probability of being selected in the first stage.
- Enforce `sense_no >= 1`, define a stable `sense_key`, and use `(vocab, sense_no)` as the within-vocabulary duplicate guard.
- Decide whether type, level, and categories must remain consistent across senses or whether some data belongs on `MCSense`.
- Extend import, services, admin, requests, detail pages, and answer checking as one vertical slice. Conflicts must produce an explicit report rather than silent success.
- Existing monthly CSV files are test data and should not be automatically deleted, overwritten, or upgraded.
- Restore public MC choices only after end-to-end tests cover import, review, administration, quiz, and result rendering.

## Event Notifications

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Admin Create Event / site announcement page**

- Add an admin-only Create Event page for manually publishing site announcements such as system updates and new features. Its overall UI should follow Feedback Create with a fixed header, scrollable form area, fixed submit action, success toast, and unsaved-content confirmation. Define the final fields, recipient scope, and publication rules when the feature enters active design.

## VocabRequest Review

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **In-site admin vocabulary-request review page**

- Add an admin-only vocabulary-request review page within the site so admins can approve or reject requests without entering `/admin/`.
- Provide a request list and review details showing request type, requester, proposed data, request reason, and status, with a review-note field. Keep review notes mandatory for rejection.
- Reuse existing review services, validation, transactions/row locks, pending-state guards, and result notifications to preserve one review workflow and prevent duplicate processing.
- Enforce server-side admin review permissions on pages and actions; use POST with CSRF protection for state changes.
- Verify approval, rejection, permission boundaries, processed requests, and stale/duplicate submissions.

## Current Work

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **In-site admin user-data page**

- Add an admin-only page within the site for viewing other users’ data.
- Initial fields: email, answered-question count, and last login. Confirm additional fields and list/detail presentation during design.
- Enforce server-side admin permissions on both the page and data queries, including direct URL and data requests.
- Reuse the personal-statistics definition of answered-question count. Handle users who have never logged in and make the displayed time zone clear.
- Add a “Reset all UserVocab weights” button to each user detail page so an admin can reset every UserVocab weight belonging to that user without affecting other users.
- Define the reset target value before implementation. Require confirmation, POST/CSRF protection, and server-side admin permission checks; report the actual number of updated records.


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Password-reset flow**

- Add a password-reset flow using Django's built-in views, forms, and `default_token_generator`. Use a separate timeout policy if activation and password reset later require different expiry periods.


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Fix mobile layout of the three home footer buttons**

- User-reported issue: only a few mobile devices currently display all three home footer buttons on one row; other devices have wrapping/layout problems.
- Adjust the responsive footer layout so all three buttons fit on one row at supported mobile widths, with readable labels and adequate tap targets.
- Verify at 320 CSS px and other common mobile viewport widths, checking for clipped text, overlap, and horizontal overflow.


> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Post-v1.0.0 profile and home quiz statistics**

- Moved from Future Ideas into active scope to replace the under-construction sections.
- Profile: total answered questions, current correct streak, longest correct streak, and longest incorrect streak.
- Home: the signed-in user’s current correct streak, longest correct streak, and longest incorrect streak.
- Use consistent statistics across both pages. Define counting scope, the current-correct display after an incorrect answer, Skip behaviour, and historical backfill before implementation.
- The original idea also included the current incorrect streak; the requested page scope lists only the current correct streak. Decide storage representation during design.

> <span style="background:#0d47a1;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">TODO</span> **Post-v1.0.0 profile: ten most recent question results**

- Moved from Future Ideas into active scope to replace the profile / My Page under-construction section.
- Show the user’s ten most recent questions and results.
- Define displayed fields, ordering, Skip inclusion, empty/partial history states, and storage compatible with the existing QuizAttempt retention policy before implementation.

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Expand automated test coverage**

Completed:

- The production-aligned PostgreSQL suite discovers 40 Django tests and all 40 pass. Django system checks report no issues.
- A targeted `QuizAttempt`/`VocabRequest` suite discovers 12 tests: ten pass on SQLite; the two true multi-connection tests were subsequently confirmed passing with the dedicated PostgreSQL test role.
- Coverage now includes production SMTP validation, database-backed health checks, Redis cooldown failure policy, Sentry privacy filtering, per-IP rate limiting, single-use quiz attempts, and concurrent vocabulary approval. Fourteen Playwright browser cases exist but do not yet have a current pass result.

Remaining:

- Complete browser coverage for registration, activation, resend, and email delivery behaviour.
- Vocabulary request create/update/delete/restore and complete approval/rejection browser flows.
- User vocabulary synchronisation, `in_use` updates, ownership, active-state boundaries, weight, and streak calculations.
- Quiz answer comparison, filtered/full-pool decisions, initial/Next/Skip/Submit/resume paths, invalid current questions, and empty-pool termination.
- Event, feedback, logging, and management-command behaviour.

> <span style="background:#e65100;color:#ffffff;padding:2px 7px;border-radius:4px;font-weight:700;">WORKING</span> **Overdue UserVocab weight adjustment**

- The `adjust_user_vocab_weight` management command has argument and logging scaffolding.
- It does not yet select overdue records, apply a weight policy, or update database rows. Its dry run does not report candidates.

## Verification Backlog

The following checks belong to the test-expansion task rather than reopening completed features:

- Concurrent admin review and stale review-form submissions.
- Case-insensitive registration races.
- Concurrent vocabulary synchronisation and event generation.
- Broader Answer-versus-Answer and Answer-versus-Skip browser/integration combinations beyond the existing database concurrency test.
- Log routing, rotation, retention, and sensitive-data assertions.
- Execute and extend the fourteen Playwright cases for responsive layouts, Ajax focus management, and the result overlay.
