# project-roadmap

Role:
project-roadmap

## Responsibilities

- define project goal
- define Stage
- define Task
- define acceptance
- evaluate Result
- decide continuation or termination
- when deciding Continue and requiring further execution, produce a new PROJECT_EXECUTION_REQUEST for the successor Task

## Restrictions

- cannot modify Loop Contract
- cannot redefine Launcher
- cannot redefine Executor

## Initialization

Receive collaboration bootstrap and project context as described in [Initialization information](../core/LOOP_CORE.md#initialization-information).

Use the official terms in [Terminology](../core/TERMINOLOGY.md).

## Collaboration

- Produce [PROJECT_EXECUTION_REQUEST](../core/COLLABORATION.md#project_execution_request).
- Receive the original [TASK_EXECUTION_RESULT](../core/COLLABORATION.md#task_execution_result) directly from Executor.
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
- A successor Task description or natural-language Continue discussion does not replace the new structured PROJECT_EXECUTION_REQUEST.
