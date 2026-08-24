---
name: project-status-sync
description: Explicitly requested synchronization of the Japanese Quiz repository's TODO, future ideas, learning points, and project history. Use only when the user invokes $project-status-sync or directly asks to update or reconcile project status documentation; do not invoke automatically during reviews, debugging, advice, ordinary discussion, or commit inspection.
---

# Project Status Sync

Keep the project status documents accurate as part of the current task. Apply
TODO and project history updates directly. Future ideas and learning points
require the user's explicit approval before writing.

## Repository root resolution

Before reading or writing project files, resolve the active workspace's Git
root with `git rev-parse --show-toplevel`. Treat every path in this skill as
relative to that resolved root; never reuse an absolute path or working
directory remembered from an earlier turn or another clone.

Verify that the resolved root contains this repository's `AGENTS.md`,
`.agents/skills/`, and the target status files before writing. A skill locator
may show where a copy of the skill was discovered, but it is not permission to
switch the task to that clone. If the user identifies a different clone or the
active tool workspace and intended editor workspace disagree, stop all writes,
report both canonical paths, and continue only after the target workspace has
been confirmed and is writable.

## Sources of truth

Before editing status documents, read
[`references/project-doc-format.md`](references/project-doc-format.md). Treat it
as authoritative for document roles, formatting, headings, badges, counts, and
classification rules.

Inspect only the status documents relevant to the current evidence:

- `docs/status/TODO.md`
- `docs/status/FUTURE_IDEAS.md`
- `docs/status/CODING_REFERENCE.md`
- `docs/status/PROJECT_HISTORY.md`

Use the conversation, inspected code and tests, the working-tree diff, and Git
history as evidence. Do not infer completion merely from the user's intention.

## When to run

Run only when the user explicitly invokes `$project-status-sync` or directly
asks to update, synchronize, or reconcile one or more project status documents.
Do not run merely because a review passes, debugging establishes work, a future
idea or learning point appears, or Git contains undocumented commits.

When explicitly invoked, apply the classification, approval, evidence, and
editing rules below. Otherwise do not inspect or modify the status documents
and do not ask whether ideas or learning points should be recorded.

## Classify evidence

### TODO

Update `TODO.md` for work inside the current project scope.

- Mark an item complete only when code inspection and proportionate
  verification support that conclusion.
- Keep detailed task and progress bullets while a subtag is `TODO` or
  `WORKING`, because they are still needed to show what remains and what has
  already been attempted.
- When a subtag becomes `DONE`, compress its implementation diary into a short
  outcome-oriented summary. Also compact an existing `DONE` subtag when a sync
  reveals that it has accumulated excessive chronological or repetitive
  detail.
- A compact `DONE` summary should normally use about 3-6 bullets and preserve
  the final user-visible behavior, important architecture decisions, security
  or data-integrity safeguards, and meaningful verification evidence. Keep an
  `改良` section separate when it still describes optional follow-up work.
- Remove superseded approaches, incremental wiring steps, repeated facts, and
  low-level form/template/field chronology from a `DONE` subtag. Do not remove
  a current limitation merely to make the entry look complete, and do not
  relabel a subtag `DONE` while required work remains.
- Do not repeatedly rewrite an already concise and accurate `DONE` summary.
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

### Coding reference

Treat a possible learning need or outcome as a candidate when:

- the user asks how or why a non-obvious mechanism works;
- a review exposes a misconception or missing concept;
- a technical explanation resolves or materially advances an existing learning
  point.

Before adding or changing `CODING_REFERENCE.md`, ask whether the user wants the
candidate recorded. The user may already understand a technology even when it
has not appeared in this repository. Write only after an explicit yes, and ask
only once for the same candidate during the same discussion. No answer means no
update unless the user returns to it later.

Do not propose an entry merely because a package, API, or technique is new in
the repository. Preserve the document's reference semantics: record the concept
and current understanding as reusable guidance rather than treating it as a
learning task without evidence.

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
