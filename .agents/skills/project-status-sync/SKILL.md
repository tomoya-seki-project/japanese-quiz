---
name: project-status-sync
description: Keep the Japanese Quiz repository's TODO, future ideas, learning points, and project history synchronized while reviewing or discussing project work. Use after code checks, verification, debugging, technical explanations, roadmap discussions, and when reconciling undocumented Git commits.
---

# Project Status Sync

Keep the project status documents accurate as part of the current task. Apply
TODO and project history updates directly. Future ideas and learning points
require the user's explicit approval before writing.

## Sources of truth

Before editing status documents, read
[`references/project-doc-format.md`](references/project-doc-format.md). Treat it
as authoritative for document roles, formatting, headings, badges, counts, and
classification rules.

Inspect only the status documents relevant to the current evidence:

- `docs/status/TODO.md`
- `docs/status/FUTURE_IDEAS.md`
- `docs/status/LEARNING_POINTS.md`
- `docs/status/PROJECT_HISTORY.md`

Use the conversation, inspected code and tests, the working-tree diff, and Git
history as evidence. Do not infer completion merely from the user's intention.

## When to run

Run the classification and sync check before finishing a response when:

- reviewing or checking whether the user's implementation works;
- verification changes from failing or uncertain to passing;
- debugging or advice establishes a new required task or resolves an existing
  one;
- the user identifies a possible future feature or roadmap direction, in which
  case ask whether to record it after the discussion settles;
- a concept may be a learning point, in which case ask whether it is already
  familiar before recording it;
- important commits may exist after the newest commit represented in
  `PROJECT_HISTORY.md`.

Do not require the user to say "update the docs".

## Classify evidence

### TODO

Update `TODO.md` for work inside the current project scope.

- Mark an item complete only when code inspection and proportionate
  verification support that conclusion.
- If a review fails, keep the item unfinished and add only concrete remaining
  work that belongs to the existing scope.
- Do not turn optional suggestions into required TODOs.
- Move an idea from future ideas into TODO when the user actually adopts it into
  current scope.

### Future ideas

Treat a concrete project direction outside the current scope as a candidate,
not as permission to edit `FUTURE_IDEAS.md`. After the idea discussion reaches
a natural stopping point, immediately before changing topic, or at the end of a
response that wraps up the discussion, ask the user once whether to record the
idea. Write it only after an explicit yes.

A passing thought, alternative mentioned only to explain a tradeoff, or
speculative edge case is not enough to ask about. Avoid duplicates and merge
with an existing idea when appropriate. If the user does not answer the
question, treat the candidate as not approved and do not repeatedly ask during
the same discussion.

### Learning points

Treat a possible learning need or outcome as a candidate when:

- the user asks how or why a non-obvious mechanism works;
- a review exposes a misconception or missing concept;
- a technical explanation resolves or materially advances an existing learning
  point.

Before adding or changing `LEARNING_POINTS.md`, ask whether the user wants the
candidate recorded. The user may already understand a technology even when it
has not appeared in this repository. Write only after an explicit yes, and ask
only once for the same candidate during the same discussion. No answer means no
update unless the user returns to it later.

Do not propose an entry merely because a package, API, or technique is new in
the repository. Preserve the document's checklist semantics: record the concept
and current understanding honestly rather than marking it learned without
evidence.

### Project history

Reconcile important undocumented commits during review work:

1. Inspect recent Git history and the newest commit hashes already named in
   `PROJECT_HISTORY.md`.
2. Examine the relevant commit diff or files before describing it; do not write
   history from the subject line alone.
3. Add entries for meaningful features, architecture or schema changes,
   important fixes, or project milestones.
4. Skip documentation-only commits, wording cleanup, and minor mechanical
   changes unless they form part of a larger milestone.
5. Use the actual commit hash and commit date. Never describe uncommitted work
   as committed.

It is acceptable for project history to catch up on the user's next interaction;
this skill does not claim to monitor Git in the background.

## Editing safeguards

- Preserve existing user-authored content unless new evidence supersedes it.
- Avoid duplicate items across documents; choose the document matching the
  current commitment level.
- Keep tables of contents, anchors, TODO status badges, and status counts in
  sync after edits.
- Do not add entries merely recording that documentation was updated.
- Keep documentation edits scoped to facts established in the current task or
  verified Git history.
- Summarize which status documents changed in the final response. If none
  changed, say so only when that information is useful to the user.
