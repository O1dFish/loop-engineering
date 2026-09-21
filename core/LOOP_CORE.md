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

Continuation requires an explicit decision by project-roadmap-chatgpt within existing structured control boundaries. Task completion or receipt of a Result does not independently continue or terminate the Stage. Launcher handles STOP without evaluating the Result. This lifecycle description adds no collaboration message or control format.

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
