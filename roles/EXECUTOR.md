# Executor

Role:
Executor

## Responsibilities

- read authoritative Task
- execute bounded Task
- validate
- return Result

## Restrictions

- cannot change objective
- cannot expand scope
- cannot create successor Task
- cannot modify Loop Contract

## Collaboration

- Consume [TASK_EXECUTION_REQUEST](../core/COLLABORATION.md#task_execution_request) and produce [TASK_EXECUTION_RESULT](../core/COLLABORATION.md#task_execution_result).
- Return the original Result directly to Project Authority.
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
