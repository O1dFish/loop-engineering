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
- Receive [TASK_EXECUTION_RESULT](../core/COLLABORATION.md#task_execution_result) and produce [TASK_RESULT_RETURN](../core/COLLABORATION.md#task_result_return), returning a reference to the original Result without interpreting, changing, judging, or replacing it.
- Use the applicable [shared rules and field semantics](../core/COLLABORATION.md#shared-rules-and-field-semantics) through the [minimum contract projection](../core/COLLABORATION.md#minimum-contract-projection).
