#!/usr/bin/env python3
"""Static wording checks for the 0.1.3 policy; not routing or runtime tests."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
files = {
    "skill": (ROOT / "SKILL.md").read_text(encoding="utf-8"),
    "executor": (ROOT / "references/EXECUTOR.md").read_text(encoding="utf-8"),
    "review": (ROOT / "references/REVIEW_AND_RECORDS.md").read_text(encoding="utf-8"),
    "readme": (ROOT / "README.md").read_text(encoding="utf-8"),
}
checks = {
    "project-roadmap recommends GPT-6.1 Sol/high while Human selects main model and no gate":
        "主会话模型和推理级别完全由用户选择" in files["skill"]
        and "不构成初始化或执行资格条件" in files["skill"]
        and "建议默认请求 `gpt-6.1-sol`、`high`" in files["skill"],
    "index 0 and rework 1-3 require Luna/high; index 4+ may choose GPT-6.1 Sol/high with reason":
        all(x in files["skill"] for x in ["`0`（首次尝试）", "`1`、`2`、`3`（前三次返工）", "`4+`（第四次及后续返工）", "gpt-6.1-sol", "记录理由"])
        and "`rework_index` 为 `0`、`1`、`2` 或 `3` 时必须请求 Luna" in files["skill"]
        and "`rework_index` 为 `0` 至 `3` 时必须请求 `gpt-6-luna` + `high`" in files["executor"],
    "stable work item, fresh task, cumulative rework and resume preserved":
        all(x in files["skill"] for x in ["稳定的 `work_item_id`", "新的 `task_id`", "累计的 `rework_index`", "不得重置 `work_item_id`、`rework_index`"]),
    "minimum context and explicit fork_turns none preserved":
        all(x in files["executor"] for x in ["不要发送完整", "完整 Roadmap", "历史聊天", "后续 Task"])
        and '`fork_turns: "none"`' in files["executor"],
    "review supports Luna or GPT-6.1 Sol/high and stays read-only":
        "`gpt-6-luna` 或 `gpt-6.1-sol`" in files["review"]
        and "审核者不得修改被审核候选" in files["review"],
    "no operational GPT-6 Sol driver remains":
        all(not re.search(r"gpt-6-sol", text, re.IGNORECASE) for text in files.values()),
}
for label, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
if not all(checks.values()):
    sys.exit(1)
print("LIMIT: wording/static check only; it does not invoke models, route requests, or test real retries.")
