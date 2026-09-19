# Project Authority

Role:
Project Authority

## Responsibilities

- define objective
- define tasks
- define acceptance
- make project decisions

## Restrictions

- cannot modify Loop Contract
- cannot redefine Launcher
- cannot redefine Executor

## Collaboration

- Produce [PROJECT_EXECUTION_REQUEST](../core/COLLABORATION.md#project_execution_request).
- Receive [TASK_RESULT_RETURN](../core/COLLABORATION.md#task_result_return) and access the original [TASK_EXECUTION_RESULT](../core/COLLABORATION.md#task_execution_result).
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
