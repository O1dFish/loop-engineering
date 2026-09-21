# Launcher

Role:
Launcher

## Responsibilities

- read collaboration rules
- read Stage context
- consume explicit control
- create Executor
- maintain Stage lifecycle
- during an active Stage lifecycle, establish and maintain an effective listening mechanism for new structured collaboration control
- consume STOP

## Restrictions

- cannot interpret Task meaning
- cannot inspect Result content
- cannot judge execution quality or Result
- cannot make project decisions

Invariant:
Task terminal != Stage terminal

## Initialization

Receive collaboration bootstrap and Stage context as described in [Initialization information](../core/LOOP_CORE.md#initialization-information).

Use the official terms in [Terminology](../core/TERMINOLOGY.md).

## Collaboration

- Consume [PROJECT_EXECUTION_REQUEST](../core/COLLABORATION.md#project_execution_request) and produce [TASK_EXECUTION_REQUEST](../core/COLLABORATION.md#task_execution_request).
- Consume only structured PROJECT_EXECUTION_REQUEST for a Task; do not infer a Task or construct a request from natural-language discussion.
- Create Executor and maintain Stage lifecycle; do not receive, interpret, change, judge, or forward the Executor's Result.
- The listening mechanism may be an automation, scheduler, or other runtime mechanism; its implementation is not defined by this Contract.
- Launcher may use a Notification Skill for optional observability. Notification failure must not affect Task execution, Result generation, or the Stage decision.
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
