# Repository Instructions

## Project documentation sync

Do not invoke `project-status-sync` automatically during reviews, checks,
debugging, advice, ordinary project discussion, or commit inspection. Use the
skill in `.agents/skills/project-status-sync/SKILL.md` only when the user
explicitly invokes `$project-status-sync` or directly asks to update or
reconcile project status documentation.

## New Japanese vocabulary

When the user expresses a clear intent to add, save, collect, or record one or
more Japanese words, use the `japanese-vocab-csv` skill in
`.agents/skills/japanese-vocab-csv/SKILL.md`. Research and append valid entries
without requiring the user to request each enrichment or CSV step separately.
Do not treat a vocabulary question or comparison by itself as permission to
write the CSV.
