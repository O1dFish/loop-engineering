# Loop Core

- project-roadmap-chatgpt owns project decisions.
- Launcher owns Stage lifecycle.
- Executor owns bounded Task execution.
- Task completion does not equal Stage completion.
- Only explicit structured control changes lifecycle.
- Projects consume Loop Contract and cannot directly modify it.
- Role definitions do not assign roles; roles must be assigned explicitly.
- Each role receives only the minimum contract projection required for its responsibility; further contract material is limited to what that responsibility requires.
- Official terms and prohibited ambiguous alternatives are defined only in [Terminology](TERMINOLOGY.md).
- Collaboration messages are defined only in [Collaboration](COLLABORATION.md) and follow these role, projection, and control boundaries.
- In this collaboration exchange, Executor returns its Result directly to project-roadmap-chatgpt.
- When project-roadmap-chatgpt decides to Continue and another Task must be executed, it must produce a new PROJECT_EXECUTION_REQUEST for that successor Task.

## Stage

Stage is a Loop lifecycle concept. project-roadmap-chatgpt defines the Stage and Launcher maintains its lifecycle. Both know the Stage context. Executor receives only the current Task context; Stage information is provided only when strictly required for that Task, never as full Stage context.

Stage metadata may include `stage_id`, `objective`, `created_at`, and `status`. These describe the Stage and are not new collaboration message fields. This Contract does not define Stage messages, a Stage protocol, or a Stage state machine.

## Loop lifecycle

```text
project-roadmap-chatgpt initialization
  ↓
Stage creation
  ↓
Launcher initialization
  ↓
Task execution request
  ↓
Executor execution
  ↓
TASK_EXECUTION_RESULT
  ↓
project-roadmap-chatgpt decision
  ↓
continue or STOP
```

project-roadmap-chatgpt owns the project goal, Stage definition, Task definition, acceptance, Result evaluation, and the continuation or termination decision. Launcher reads collaboration rules and Stage context, creates Executor, maintains the Stage lifecycle, and handles STOP. Executor executes and validates the Task and generates its Result.

The Task execution request uses the existing request exchange defined in [Collaboration](COLLABORATION.md#role-and-control-boundaries). Executor returns TASK_EXECUTION_RESULT directly to project-roadmap-chatgpt. Launcher does not inspect Result content, judge execution quality, or make project decisions. Executor does not decide the next Task.

Continuation requires an explicit decision by project-roadmap-chatgpt within existing structured control boundaries. When that decision is Continue and another Task must be executed, project-roadmap-chatgpt must express the successor Task by producing a new PROJECT_EXECUTION_REQUEST. A successor Task description or natural-language discussion is not an execution request. Launcher consumes PROJECT_EXECUTION_REQUEST only and must not infer a Task from natural language. Task completion or receipt of a Result does not independently continue or terminate the Stage. Launcher handles STOP without evaluating the Result. This lifecycle description adds no collaboration message or control format.

During an active Stage lifecycle, Launcher must establish and maintain an effective listening mechanism. The mechanism checks for new structured collaboration control, consumes PROJECT_EXECUTION_REQUEST, consumes explicit STOP, and maintains the Stage lifecycle. The Contract does not prescribe how this mechanism is implemented; an automation, scheduler, or other runtime mechanism may be used. This requirement does not introduce an additional role, host concept, lifecycle state, or runtime dependency.

## Initialization information

Each role receives two categories of initialization information:

| Role | Collaboration bootstrap | Context |
| --- | --- | --- |
| project-roadmap-chatgpt | Explicit role assignment and the applicable collaboration rules and Contract material. | Project context needed to define the project goal, Stage, Tasks, and acceptance and make project decisions. |
| Launcher | Explicit role assignment and the applicable collaboration rules and Contract material. | Stage context needed to maintain the Stage lifecycle, create Executor, and handle STOP. |
| Executor | Explicit role assignment and the applicable collaboration rules and Contract material. | Task context needed for bounded execution, validation, and Result generation. |

Collaboration bootstrap follows the [minimum contract projection](COLLABORATION.md#minimum-contract-projection). Executor is not supplied full Stage context or project history. These categories clarify document usage; they do not define a runtime bootstrap implementation or new message fields.

## Structured interaction

Natural language discussion is not an execution command. Discussion and informal instructions do not substitute for structured collaboration messages. Only structured collaboration messages can trigger execution behavior, subject to explicitly assigned roles and existing control boundaries, as defined in [Collaboration](COLLABORATION.md#structured-interaction-boundary).

## Optional observability capability

The LoopFeishu Notification Skill, when used, is an optional observability capability. It is not part of the Loop Contract, is not a collaboration message, does not own lifecycle control, and does not affect Task execution. Launcher or Executor may use a Notification Skill for observability. Notification failure must not prevent Task execution, Result generation, or the Stage decision.
