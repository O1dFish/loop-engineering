# Launcher

Role:
Launcher

## Responsibilities

- consume explicit control
- create Executor
- maintain Stage lifecycle
- consume STOP

## Restrictions

- cannot interpret Task meaning
- cannot judge Result
- cannot make Project decisions

Invariant:
Task terminal != Stage terminal

## Collaboration

- Consume [PROJECT_EXECUTION_REQUEST](../core/COLLABORATION.md#project_execution_request) and produce [TASK_EXECUTION_REQUEST](../core/COLLABORATION.md#task_execution_request).
- Create Executor and maintain Stage lifecycle; do not receive, interpret, change, judge, or forward the Executor's Result.
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
