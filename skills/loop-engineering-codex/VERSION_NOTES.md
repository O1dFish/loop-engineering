# Version notes

## 0.1.3

This patch updates future `project-roadmap` recommendations, eligible execution retries, and independent review options from GPT-6 Sol to GPT-6.1 Sol, all at `high`. Human still chooses the main-session model, with no model-based entry gate and no global configuration changes. Execution index 0 and rework indexes 1–3 stay on `gpt-6-luna` + `high`; only index 4 and later may choose `gpt-6.1-sol` + `high`, with a recorded reason. Review remains independent and read-only. Stable work-item identity, fresh task identity, cumulative retry counts across resume, minimum context, and native spawning remain unchanged.

The previous 0.1.2 policy allowed GPT-6 Sol from rework index 4 and as an independent review option. That is historical context only; the operational files now direct future choices to GPT-6.1 Sol. This release note does not claim programmatic model routing or a real retry test.

The detailed original implementation and historical run evidence remain in the original source workspace. This minimal distribution snapshot does not include raw run records or missing historical validation documents.
