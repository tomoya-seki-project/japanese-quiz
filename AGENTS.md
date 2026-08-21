# Repository Instructions

## Project documentation sync

When reviewing, checking, debugging, or advising on project work, use the
`project-status-sync` skill in `.agents/skills/project-status-sync/SKILL.md`.

Run its documentation sync before finishing the response when any of these
conditions apply:

- the review or verification passes;
- the user approves recording a concrete future project idea;
- the user approves recording or updating a learning point;
- Git contains important commits not yet represented in project history.

Update TODO and project history directly without asking for confirmation. Ask
before adding or changing future ideas or learning points, as required by the
skill.
Do not mark work complete when the review still has unresolved correctness
issues. Documentation-only edits do not by themselves justify status or history
entries.

## New Japanese vocabulary

When the user expresses a clear intent to add, save, collect, or record one or
more Japanese words, use the `japanese-vocab-csv` skill in
`.agents/skills/japanese-vocab-csv/SKILL.md`. Research and append valid entries
without requiring the user to request each enrichment or CSV step separately.
Do not treat a vocabulary question or comparison by itself as permission to
write the CSV.
