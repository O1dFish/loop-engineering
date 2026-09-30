# loop-engineering-codex

版本：`0.1.2`（Codex 原生 MVP）

这是 Loop Engineering 的独立 Codex 原生实验 Skill。用户在任意主会话显式调用 `$loop-engineering-codex`；主会话作为 `project-roadmap`，通过原生参数创建 fresh 通用 Executor。主会话模型和推理级别由用户选择，并作为已知观察或未知记录。执行 Task 的首次执行与前三次返工使用 `gpt-6-luna` + `high`；同一执行工作项第四次及后续返工可由 project-roadmap 结合实际返工结果与任务情况选择 Luna 或 Sol，并记录理由。独立审核可由主会话按审核复杂度选择 Luna 或 Sol。它没有 Launcher、隐藏启动器、定时调度、日志平台或自动恢复机制。

路由要求由 Skill 指令和 spawn 请求参数落实，当前没有程序化 router 或返工状态库；请求配置与服务端实际路由须分开记录。

Skill 版本与运行文件哈希集合分别冻结每个 Loop 的规则身份。主会话模型或推理级别可由用户在 Loop 中更改，记录变化并核对当前目标、候选和待办动作后继续。要采用更新版 Skill，显式重新加载并初始化更新后的规则；不要求特定主会话模型或仅因模型变化而新建会话。

仓库中的源码目录与运行时安装目录是两个不同位置。源码存在不代表客户端已经发现 Skill；安装后必须在目标入口重新核对发现与调用。

## 安装或更新

先从源码仓库根目录运行下面唯一的安装/更新块，并显式核对三个输入。`$TrustedPreviousManifest` 必须来自安装前已经信任的旧版本，不能从新候选临时生成；仓库现有 `validation/gpt6-routing-manifest.json` 描述当前已安装的 `0.1.1` 基线。当前环境的目标是 `C:\Users\Monster\.codex\skills`，其他入口应改成其实际技能目录。

此块在任何写入前预检全部五个运行文件。已安装文件若已等于候选，可安全重复运行；否则它必须匹配可信旧基线。目标缺文件、基线缺记录、哈希未知、reparse 路径或窄范围内存在第三份同名 Skill 时都会拒绝整次操作。目标中的非白名单文件保持不变，也不修改任何全局配置。

```powershell
# INSTALL/UPDATE INPUTS — 从 loop-engineering 仓库根目录运行；执行前核对三条绝对路径。
$Source = [IO.Path]::GetFullPath((Join-Path $PWD 'skills\loop-engineering-codex'))
$Target = [IO.Path]::GetFullPath((Join-Path $env:USERPROFILE '.codex\skills\loop-engineering-codex'))
$TrustedPreviousManifest = [IO.Path]::GetFullPath((Join-Path $Source 'validation\gpt6-routing-manifest.json'))

# GUARD + ACTION — 不要跳过 guard，也不要把 baseline 改成由当前候选生成的清单。
$ErrorActionPreference = 'Stop'
$RuntimeFiles = @(
    'SKILL.md',
    'agents\openai.yaml',
    'references\EXECUTOR.md',
    'references\REVIEW_AND_RECORDS.md',
    'README.md'
)

function Normalize-FullPath([string]$Path) {
    return [IO.Path]::GetFullPath($Path).TrimEnd([char[]]@('\', '/'))
}
function Assert-NotReparse([string]$Path, [string]$Label) {
    if (Test-Path -LiteralPath $Path) {
        $Item = Get-Item -LiteralPath $Path -Force
        if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Refusing reparse $Label`: $($Item.FullName)"
        }
    }
}

$Source = Normalize-FullPath $Source
$Target = Normalize-FullPath $Target
$TargetRoot = Normalize-FullPath (Split-Path $Target -Parent)
$TrustedPreviousManifest = Normalize-FullPath $TrustedPreviousManifest

if ((Split-Path $Target -Leaf) -ne 'loop-engineering-codex') {
    throw "Unexpected target leaf: $Target"
}
if ($Source -eq $Target) {
    throw 'Source and target must be different directories.'
}
if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
    throw "Source directory missing: $Source"
}
if (-not (Test-Path -LiteralPath $TargetRoot -PathType Container)) {
    throw "Target root missing; resolve it explicitly before install: $TargetRoot"
}
Assert-NotReparse $Source 'source directory'
Assert-NotReparse $TargetRoot 'target root'
Assert-NotReparse $Target 'target directory'
if ((Test-Path -LiteralPath $Target) -and -not (Test-Path -LiteralPath $Target -PathType Container)) {
    throw "Existing target is not a directory: $Target"
}

# Detect a third active-looking copy only in the repo and the known user skill roots.
$RepoRoot = Normalize-FullPath (Split-Path (Split-Path $Source -Parent) -Parent)
$KnownSkillRoots = @(
    (Split-Path $Source -Parent),
    (Join-Path $RepoRoot '.agents\skills'),
    (Join-Path $env:USERPROFILE '.codex\skills'),
    (Join-Path $env:USERPROFILE '.agents\skills')
) | ForEach-Object { Normalize-FullPath $_ } | Select-Object -Unique
foreach ($Root in $KnownSkillRoots) {
    $SameName = Normalize-FullPath (Join-Path $Root 'loop-engineering-codex')
    if ((Test-Path -LiteralPath $SameName) -and $SameName -ne $Source -and $SameName -ne $Target) {
        throw "Refusing duplicate same-name Skill: $SameName"
    }
}

$CandidateHashes = @{}
foreach ($RelativePath in $RuntimeFiles) {
    $SourceFile = Join-Path $Source $RelativePath
    if (-not (Test-Path -LiteralPath $SourceFile -PathType Leaf)) {
        throw "Candidate runtime file missing: $RelativePath"
    }
    Assert-NotReparse (Split-Path $SourceFile -Parent) "source parent for $RelativePath"
    Assert-NotReparse $SourceFile "source file $RelativePath"
    $CandidateHashes[$RelativePath] = (Get-FileHash -LiteralPath $SourceFile -Algorithm SHA256).Hash
}

$TargetExists = Test-Path -LiteralPath $Target -PathType Container
$BaselineByFile = @{}
# Full preflight: no directory or file writes occur until every target file is accepted.
$PreflightErrors = @()
$TargetHashes = @{}
$NeedsBaseline = $false
if ($TargetExists) {
    foreach ($RelativePath in $RuntimeFiles) {
        $TargetFile = Join-Path $Target $RelativePath
        if (-not (Test-Path -LiteralPath $TargetFile -PathType Leaf)) {
            $PreflightErrors += "Existing install is missing runtime file: $RelativePath"
            continue
        }
        Assert-NotReparse (Split-Path $TargetFile -Parent) "target parent for $RelativePath"
        Assert-NotReparse $TargetFile "target file $RelativePath"
        $CurrentHash = (Get-FileHash -LiteralPath $TargetFile -Algorithm SHA256).Hash.ToUpperInvariant()
        $TargetHashes[$RelativePath] = $CurrentHash
        $CandidateHash = $CandidateHashes[$RelativePath].ToUpperInvariant()
        if ($CurrentHash -ne $CandidateHash) { $NeedsBaseline = $true }
    }
}
if ($NeedsBaseline) {
    if (-not (Test-Path -LiteralPath $TrustedPreviousManifest -PathType Leaf)) {
        $PreflightErrors += "Trusted previous manifest missing: $TrustedPreviousManifest"
    } else {
        Assert-NotReparse $TrustedPreviousManifest 'trusted previous manifest'
        foreach ($Entry in (Get-Content -LiteralPath $TrustedPreviousManifest -Raw | ConvertFrom-Json)) {
            $BaselineByFile[([string]$Entry.file -replace '/', '\')] = ([string]$Entry.sha256).ToUpperInvariant()
        }
    }
}
if ($TargetExists) {
    foreach ($RelativePath in $RuntimeFiles) {
        if (-not $TargetHashes.ContainsKey($RelativePath)) { continue }
        $CurrentHash = $TargetHashes[$RelativePath]
        $CandidateHash = $CandidateHashes[$RelativePath].ToUpperInvariant()
        if ($CurrentHash -eq $CandidateHash) { continue }
        if (-not $BaselineByFile.ContainsKey($RelativePath)) {
            $PreflightErrors += "Trusted baseline has no entry for changed file: $RelativePath"
            continue
        }
        if ($CurrentHash -ne $BaselineByFile[$RelativePath]) {
            $PreflightErrors += "Unknown installed changes: $RelativePath"
        }
    }
}
if ($PreflightErrors.Count -gt 0) {
    throw ($PreflightErrors -join [Environment]::NewLine)
}

New-Item -ItemType Directory -Path $Target -Force | Out-Null
foreach ($RelativePath in $RuntimeFiles) {
    $SourceFile = Join-Path $Source $RelativePath
    $TargetFile = Join-Path $Target $RelativePath
    New-Item -ItemType Directory -Path (Split-Path $TargetFile -Parent) -Force | Out-Null
    $CurrentHash = if (Test-Path -LiteralPath $TargetFile -PathType Leaf) {
        (Get-FileHash -LiteralPath $TargetFile -Algorithm SHA256).Hash
    } else { $null }
    if ($CurrentHash -ne $CandidateHashes[$RelativePath]) {
        Copy-Item -LiteralPath $SourceFile -Destination $TargetFile -Force
    }
}

foreach ($RelativePath in $RuntimeFiles) {
    $InstalledHash = (Get-FileHash -LiteralPath (Join-Path $Target $RelativePath) -Algorithm SHA256).Hash
    if ($InstalledHash -ne $CandidateHashes[$RelativePath]) {
        throw "Post-copy verification failed: $RelativePath"
    }
}
```

安装后在当前客户端会话重新加载 Skill，或打开任意主会话并确认技能清单中出现 `loop-engineering-codex`，且不会因普通工程请求隐式加载。正在运行的 Loop 仍按初始化时记录的 Skill 版本与哈希集合执行；显式重新加载并初始化后方可采用更新规则。再显式输入：

```text
$loop-engineering-codex
```

预期只初始化，不创建 Executor、不修改业务文件。若初始化同时包含目标、范围与验收，则工作流可以直接开始。

安装或更新后核对至少以下内容：

- 源码与安装副本是不同路径，且安装副本内容与本版本一致。
- `agents/openai.yaml` 关闭隐式调用。
- 仅初始化不执行；带授权目标时才开始 Task。
- 创建 Executor 时原生请求参数真实包含所选模型、`high` 和 fresh 上下文设置。
- 审核能读取 dirty/untracked 候选，修改后旧审核失效。
- 停止回执区分已终止、仍运行与未知，不把一次中断当作进程静止证明。

## 卸载

卸载前把目标解析到绝对路径并确认末级目录名精确为 `loop-engineering-codex`。只删除该安装副本；源码仓库不会受影响：

```powershell
$RuntimeHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$SkillsRootItem = Get-Item -LiteralPath (Resolve-Path (Join-Path $RuntimeHome 'skills')).Path -Force
$SkillsRoot = $SkillsRootItem.FullName
$Target = Join-Path $SkillsRoot 'loop-engineering-codex'
$ResolvedTarget = (Resolve-Path $Target).Path
$TargetItem = Get-Item -LiteralPath $ResolvedTarget -Force

if (
    (Split-Path $ResolvedTarget -Leaf) -ne 'loop-engineering-codex' -or
    (Split-Path $ResolvedTarget -Parent) -ne $SkillsRoot -or
    ($SkillsRootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
    ($TargetItem.Attributes -band [IO.FileAttributes]::ReparsePoint)
) {
    throw "Refusing to remove unexpected target: $ResolvedTarget"
}
Remove-Item -LiteralPath $ResolvedTarget -Recurse
```

## 使用示例

只初始化：

```text
$loop-engineering-codex
```

初始化并执行：

```text
$loop-engineering-codex

目标：修复导入 CSV 时空行导致的崩溃。
允许范围：解析器、相关测试和必要文档。
禁止事项：不修改公共 API，不升级依赖。
验收：复现测试先失败；修复后相关测试和完整测试通过；独立审核实际工作区候选。
```

日常执行不需要用户逐 Task 输入“继续”。`project-roadmap` 在授权边界内根据真实结果接受、返工、继续或停止。

只读复盘：完成若干真实 Loop 后，由 `project-roadmap` 新建 fresh Executor，复制 [references/REVIEW_AND_RECORDS.md](references/REVIEW_AND_RECORDS.md) 中的“可复制的只读复盘 Task”，填入用户指定的真实 Loop 与产物位置。缺少成功、失败/阻塞或人工接管样本时如实写样本不足。

## 与 v0.1.5 Contract 的差异

根 Contract `0.1.5` 由 Launcher 维护 Stage 生命周期并创建 Executor。本 Skill 把这些 Codex 原生编排职责放到用户显式初始化的 `project-roadmap` 主会话，不创建 Launcher，也不修改 `core/`、`roles/`、根 `VERSION` 或根 README。因此它继承部分工程原则，但不是旧 Contract 的兼容实现。

角色与上下文边界主要由指令、fresh 创建参数和证据检查建立；代理仍可能共享文件系统。这不是安全沙箱。无法确认模型实际路由、子进程终止或记录位置时，必须如实标为未知。

## 验证范围

静态校验只能证明技能结构和元数据可解析。一次模拟冒烟可以证明当前入口能够加载和派发，却不能证明真实项目价值。交付时分别报告：候选是否实现；当前目标入口是否实测；真实项目价值是否经过实际 Loop 验证。

| 入口 | 已有证据 |
| --- | --- |
| 历史本机 Codex CLI/app-server 记录（`0.155.0-alpha.9.2`） | 记录使用 gpt-5.6 配置，不能证明本版 gpt-6 请求或路由；其中原生发现、仅初始化、fresh 实例和最小闭环证据仍仅适用于当时的候选与环境；服务端实际路由未知 |
| 用户目标的桌面新主会话入口 | NOT_RUN：未对本次对齐候选执行完整桌面流程；CLI 证据不能替代该入口 |

完整原始设计与实现 prompt 现已从用户提供的本地文件取得并用于本次对齐：`loop-engineering-codex-design.md` 与 `loop-engineering-codex-implementation-prompt.md`。`validation/SOURCE_DESIGN.md` 和既有 `validation/RESULTS.md` 中“独立附件当时未取得”的说法是首次实现时的历史限制，仍按当时事实保留；它不再描述本次对齐的来源状态。验证材料不属于安装白名单。
