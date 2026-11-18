#!/usr/bin/env python3
"""Check the active Loop Codex Skill 0.1.4 policy text."""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_FILES = (
    "SKILL.md",
    "README.md",
    "references/EXECUTOR.md",
    "references/REVIEW_AND_RECORDS.md",
    "agents/openai.yaml",
)
STALE_POLICY = re.compile(
    r"\bgpt-6(?:\.1)?-sol\b|前三次返工|前四次(?:执行|尝试|返工)|第四次返工|"
    r"(?:必须|一律)(?:使用|请求|选择)[^。\n]{0,24}(?:Luna|gpt-6-luna)|"
    r"所有执行[^。\n]{0,25}默认使用[^。\n]{0,24}(?:Luna|gpt-6-luna)|"
    r"\bfirst (?:3|three|4|four) (?:attempts|retr(?:y|ies)|reworks?)\b|"
    r"\b(?:fourth|4th) (?:retry|rework)\b|`4\+`",
    re.IGNORECASE,
)


def has(text, *phrases):
    return all(phrase in text for phrase in phrases)


def checks(files):
    skill, readme, executor, review, agent = (files[name] for name in ACTIVE_FILES)
    _, _, routing = skill.partition("\n### 按任务选型与原生派发\n")
    routing = routing.partition("\n## 审核、记录与停止\n")[0]
    _, _, review_rules = review.partition("\n## 独立审核实际候选\n")
    review_rules = review_rules.partition("\n## 原生记录\n")[0]
    return {
        "0.1.4 requires explicit initialization and preserves frozen 0.1.3": (
            has(skill, "Skill 版本为 `0.1.4`", "冻结的 `0.1.3` Loop 继续遵循",
                "五个运行文件的哈希集合", "显式重新加载 Skill 并初始化新的 `0.1.4` Loop",
                "停止受影响的新委派", "在 PAC 或任何其他流程中获委派的 Executor",
                "不得初始化 `project-roadmap`、创建下级代理")
            and "冻结的 `0.1.3` Loop 延续原规则" in readme
            and re.search(r"^  allow_implicit_invocation:\s*false\s*$", agent, re.MULTILINE) is not None
        ),
        "Human controls the parent model and effort": has(
            skill, "主会话模型和推理级别完全由用户选择", "不构成初始化或执行资格条件",
            "不得自动切换主会话模型或修改全局默认值",
        ),
        "task-fit routing covers direct checks, focused Luna and complex Sol from the first attempt": (
            has(routing, "确定性的微小检查", "无需派发", "集中或可重复任务，优先考虑 `gpt-6-luna`",
                "实质歧义、权限边界敏感或失误代价高", "可直接选择 `gpt-6.2-sol`", "初选 `high`",
                "首次尝试和每次返工", "选型与 `rework_index` 解耦", "无固定模型配额")
            and all(has(text, "gpt-6-luna", "gpt-6.2-sol", "high") for text in (readme, executor, review_rules))
        ),
        "live catalog, callable spawn and effective agent settings gate explicit native parameters": has(
            routing, "原生 `model/list`", "`supportedReasoningEfforts`", "当前可调用的原生 spawn",
            '每次显式传 `model`、`reasoning_effort` 和 `fork_turns: "none"`', "包括独立审核",
            "`[agents]` 默认值或继承主会话", "`model` 和 `model_reasoning_effort` 优先于对应的 spawn 值",
            "会改写所选值时，报告具体受阻", "不得静默降级", "任务提示中的模型文字无法设置原生配置",
        ),
        "native readback separates request, visible configuration and backend evidence": has(
            routing, "精确代理 ID 或 canonical name", "turn metadata", "客户端可见配置及其来源",
            "可见配置不符时报告差异，无法核对时标记未知", "服务端实际路由与用量仅凭各自证据报告",
        ),
        "fresh compact execution preserves cumulative rework, budgets and resume configuration": (
            has(routing, "每次有界执行尝试创建新的通用 Executor", "原生调用明确支持逐 turn 模型和推理级别覆盖",
                "且回读证实生效", "获准的安全边界新建适合的子会话", "保留工作项与累计返工计数")
            and has(skill, "稳定的 `work_item_id`", "新的 `task_id`", "累计的 `rework_index`",
                    "既定时间、费用和次数预算", "不得重置 `work_item_id`、`rework_index`")
            and has(executor, "完整 Roadmap", "完整 Stage", "历史聊天", "未来 Task", '`fork_turns: "none"`')
        ),
        "material candidates get fresh independent read-only review, with an exact narrow recheck path": has(
            review_rules, "审核自身的复杂度和风险", "审核者不得修改被审核候选", "实质变化",
            "新的 fresh 审核 Executor", "已独立审核的基线和当前候选都能精确定位", "差异有限且完整可查",
            "验收和审核范围保持一致", "原审核者始终独立且未参与实现", "精确的窄差异复核",
            "审核轮次和审核模型不决定执行模型或返工计数",
        ),
        **{f"no obsolete model or retry floor in {path}": not STALE_POLICY.search(files[path])
           for path in ACTIVE_FILES},
    }


def main():
    files = {name: (ROOT / name).read_text(encoding="utf-8") for name in ACTIVE_FILES}
    results = checks(files)
    for label, ok in results.items():
        print(f"{'PASS' if ok else 'FAIL'}: {label}")
    print("LIMIT: static checks of active files only. Model dispatch, installation and runtime are unverified.")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
