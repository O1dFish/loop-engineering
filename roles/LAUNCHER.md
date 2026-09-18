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
