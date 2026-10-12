# Planning

This directory holds the planning records for changes to this repository: one
folder per initiative, containing its plan, checkpoint-based runbook(s) and
validation evidence.

## Conventions

- **One folder per initiative.** Each initiative keeps its plan, runbook(s) and
  evidence together.
- **Active work** lives under `active/<initiative>/`. Keep an initiative active
  while it is in progress, awaiting review, or blocked on a required gate.
- **Archive** a completed, reviewed initiative by moving its whole folder to
  `archive/YYYY-MM-<initiative>/`, using the actual completion year and month.
- **Cancelled or superseded** initiatives also go to the archive, clearly labelled
  **Cancelled** or **Superseded**, never Completed.
- Before archiving, record the outcome: completion date, final implementation
  commit references (or explicitly pending commit status), delivered work, known
  limitations and follow-up links.
- A commit title alone is not proof that every gate passed; reconcile archived
  statuses against the validation evidence and Git history.
- Archived documents are historical references. Their recorded commands, paths,
  versions and failures describe the state at the time; current operating
  instructions live in [`DEVELOPMENT.md`](../DEVELOPMENT.md).
- No archiving automation is used; folder moves are manual.

## Active initiatives

| Initiative | Status | Location |
| --- | --- | --- |
| MDClassics documentation consolidation and v1.3 | Active — checkpoints 1-3 passed; awaiting the v1.3 release date and final review | [`active/mdclassics-documentation-v1.3/`](active/mdclassics-documentation-v1.3/) |

## Archived initiatives

| Initiative | Status | Completed | Location |
| --- | --- | --- | --- |
| MDClassic_games modernization (uv / KivyMD 2 / Android) | Completed | 2026-10-12 | [`archive/2026-10-mdclassics-modernization/`](archive/2026-10-mdclassics-modernization/) |

The modernization archive's entry point is its
[master plan](archive/2026-10-mdclassics-modernization/mdclassic_games_upgrade_plan.md),
which opens with a completion summary linking the delivered work, implementation
commits, limitations and this follow-up initiative.
