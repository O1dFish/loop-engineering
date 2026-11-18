# Version notes

## 0.1.4

New Loops explicitly initialized with this version choose `gpt-6-luna` for suitable focused work or `gpt-6.2-sol` for higher complexity or risk, including independent review. Reasoning starts at `high` and uses a task-appropriate effort verified in the live catalog. Each execution attempt uses a fresh Executor with explicit native settings and preserves the work item's cumulative rework and budgets. A fresh read-only reviewer checks material changes. The original independent reviewer may recheck an exact, bounded diff under the review rules.

Frozen 0.1.3 Loops retain their original rules and fingerprints. `validation/check_task_fit_policy.py` checks this version's active files. The 0.1.3 checker and recorded results remain available at the original commit `db83ec05589666a8b0277143426aba8416e85d5b`.

## 0.1.3

This patch updates future `project-roadmap` recommendations, eligible execution retries, and independent review options from GPT-6 Sol to GPT-6.1 Sol, all at `high`. Human still chooses the main-session model, with no model-based entry gate and no global configuration changes. Execution index 0 and rework indexes 1–3 stay on `gpt-6-luna` + `high`; only index 4 and later may choose `gpt-6.1-sol` + `high`, with a recorded reason. Review remains independent and read-only. Stable work-item identity, fresh task identity, cumulative retry counts across resume, minimum context, and native spawning remain unchanged.

The previous 0.1.2 policy allowed GPT-6 Sol from rework index 4 and as an independent review option. That is historical context only; the operational files now direct future choices to GPT-6.1 Sol. This release note does not claim programmatic model routing or a real retry test.

The detailed original implementation and historical run evidence remain in the original source workspace. This minimal distribution snapshot does not include raw run records or missing historical validation documents.
