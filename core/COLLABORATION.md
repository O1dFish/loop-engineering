# Collaboration

This document is the canonical source for the three collaboration message definitions and their shared field semantics.

## Shared rules and field semantics

### Role and control boundaries

The participants act as explicitly assigned project-roadmap-chatgpt, Launcher, and Executor. A participant name, message type, or receipt of a message does not assign a role or grant authority.

Official terms and prohibited ambiguous alternatives are defined in [Terminology](TERMINOLOGY.md).

The exchange is:

```text
project-roadmap-chatgpt --PROJECT_EXECUTION_REQUEST--> Launcher
Launcher --TASK_EXECUTION_REQUEST--> Executor
Executor --TASK_EXECUTION_RESULT--> project-roadmap-chatgpt
```

These messages operate within existing explicit control and role boundaries. They do not introduce lifecycle control. Message receipt or field values do not by themselves advance Stage lifecycle, authorize a retry, or create a successor Task. Launcher retains its existing responsibilities to consume explicit control, create Executor, maintain Stage lifecycle, and consume STOP.

When project-roadmap-chatgpt decides to Continue and another Task must be executed, it must produce a new PROJECT_EXECUTION_REQUEST for the successor Task. A successor Task definition, proposed next step, or natural-language discussion is not a PROJECT_EXECUTION_REQUEST. Launcher consumes PROJECT_EXECUTION_REQUEST only and must not infer or construct one from natural language. This reuses the existing message type and collaboration flow.

### Structured interaction boundary

Natural language discussion is not an execution command. Discussion, proposed instructions, examples, and natural-language content inside message fields do not independently authorize execution. Only structured collaboration messages, issued within explicitly assigned roles and existing control boundaries, can trigger execution behavior. An informal instruction does not substitute for a collaboration message.

The [Loop lifecycle and initialization requirements](LOOP_CORE.md#loop-lifecycle) do not add message types or fields. Stage context is initialization context for Launcher, not a Stage collaboration protocol. Stage information is supplied to Executor only when strictly required for its current Task; full Stage context is not supplied.

### Continuation and successor Task boundary

After receiving TASK_EXECUTION_RESULT, project-roadmap-chatgpt evaluates the Result and makes the continuation or termination decision. If it decides Continue and further execution is required, it defines the successor Task and emits a new PROJECT_EXECUTION_REQUEST. The successor Task definition alone is insufficient. Launcher waits for and consumes the structured request; it does not infer the successor Task from prose.

During an active Stage lifecycle, Launcher must establish and maintain an effective listening mechanism for new structured collaboration control, including PROJECT_EXECUTION_REQUEST and explicit STOP. The mechanism is an implementation concern and may use automation, a scheduler, or another runtime mechanism. It is not a new message, role, host concept, lifecycle state, or transport requirement.

### Common message fields

All three messages contain these fields:

| Field | Meaning |
| --- | --- |
| `type` | The exact message name defined below. It identifies message semantics, not a role, permission, or lifecycle command. |
| `version` | The collaboration message format version. Its value for these definitions is the string `"0.1"`; it is not the Contract, project, or implementation version. |
| `message_id` | A non-empty string identifying this message uniquely within the project collaboration context, supplied by its producer. Distinct messages use distinct identifiers. It supports reference and diagnosis, not deduplication, idempotency, or retry guarantees. |
| `created_at` | A string recording this message's creation time in ISO 8601 with an explicit timezone, such as `2026-09-19T09:30:00Z`. It does not define timeouts, scheduling, lifecycle transitions, or message ordering. |
| `task_id` | A non-empty string identifying one Task uniquely within the project context, supplied by project-roadmap-chatgpt. The same Task identity is preserved throughout the three-message exchange. It does not create a global task registry or execution scheduler. |

The project context is the existing collaboration context; no additional context field or global identifier service is defined.

### Task fields

These fields occur in both request messages:

| Field | Meaning |
| --- | --- |
| `objective` | The Task objective defined by project-roadmap-chatgpt. |
| `scope` | The Task execution boundary, including included and excluded work, defined by project-roadmap-chatgpt. |
| `acceptance` | The Task completion criteria defined by project-roadmap-chatgpt. |

Launcher carries `task_id`, `objective`, `scope`, and `acceptance` unchanged into TASK_EXECUTION_REQUEST. Executor executes and validates against that authoritative Task; neither execution context nor reporting changes its objective, scope, or acceptance.

### Execution iteration

`execution_iteration` is a positive integer identifying one bounded execution of a Task. Launcher supplies it in TASK_EXECUTION_REQUEST. Different bounded executions of the same Task use different iteration values. This document does not prescribe an allocation or scheduling mechanism.

Executor copies the request's `task_id` and `execution_iteration` unchanged into TASK_EXECUTION_RESULT.

The iteration supports diagnosis and correlation. It does not authorize another execution, automatic retry, or Executor initiation of a subsequent iteration.

### Field governance

Each message contains the fields shown in its definition. Examples illustrate populated values; they are not default Task instructions or an execution authorization.

Shared field names and meanings are governed by this Contract. Task-specific content in `objective`, `scope`, `acceptance`, `execution_context`, `summary`, and `evidence` does not redefine shared semantics or role boundaries. This document does not define an internal schema for structured Task content, execution context, or evidence items.

## Minimum contract projection

Canonical storage does not require every participant to read this entire document. Roles should receive only the applicable collaboration definitions and contract rules required for their responsibility.

| Role | Required collaboration material |
| --- | --- |
| project-roadmap-chatgpt | Applicable shared rules; PROJECT_EXECUTION_REQUEST; TASK_EXECUTION_RESULT. |
| Launcher | Applicable shared rules; PROJECT_EXECUTION_REQUEST; TASK_EXECUTION_REQUEST. Access does not grant Task interpretation or Result judgment. |
| Executor | Applicable shared rules; TASK_EXECUTION_REQUEST; TASK_EXECUTION_RESULT. |

Executor receives the authoritative Task, applicable restrictions and validation requirements, and the minimum contract rules needed to execute and report. Links identify canonical sources and do not require reading the entire repository or document. Projection preserves the meaning of its canonical source and does not create a separately maintained field definition.

Do not supply the full Stage context, project history, Roadmap, other roles' responsibility documents, or successor Tasks as Executor context. This is a document usage rule; no projection engine, loader, or new message field is defined.

## PROJECT_EXECUTION_REQUEST

Direction: project-roadmap-chatgpt to Launcher.

Purpose: express the project decision that a defined Task is to be executed within existing role and explicit control boundaries. This existing message is also the required structured output when a Continue decision requires execution of a successor Task.

```json
{
  "type": "PROJECT_EXECUTION_REQUEST",
  "version": "0.1",
  "message_id": "msg-001",
  "created_at": "2026-09-19T09:30:00Z",
  "task_id": "T001",
  "objective": "Review the supplied document.",
  "scope": "Read the supplied document and report findings; do not modify files.",
  "acceptance": "Return findings supported by references to the supplied document."
}
```

The common and Task fields are defined above. Launcher does not change or reinterpret the Task.

## TASK_EXECUTION_REQUEST

Direction: Launcher to Executor.

Purpose: pass the authoritative Task and necessary context for one bounded execution.

```json
{
  "type": "TASK_EXECUTION_REQUEST",
  "version": "0.1",
  "message_id": "msg-002",
  "created_at": "2026-09-19T09:31:00Z",
  "task_id": "T001",
  "execution_iteration": 1,
  "objective": "Review the supplied document.",
  "scope": "Read the supplied document and report findings; do not modify files.",
  "acceptance": "Return findings supported by references to the supplied document.",
  "execution_context": {}
}
```

`execution_context` is an object containing only the material needed for the current Task, such as its working location, input material, and necessary environment information. It does not change the authoritative Task or grant additional authority. No internal field schema is defined.

The empty object illustrates the outer shape only. An actual execution must receive the necessary input and contract material described under Minimum contract projection.

## TASK_EXECUTION_RESULT

Direction: Executor to project-roadmap-chatgpt.

Purpose: report facts about the bounded execution and its validation. Executor produces the original Result and returns it directly to project-roadmap-chatgpt. Launcher does not receive, interpret, change, judge, or forward the Result.

```json
{
  "type": "TASK_EXECUTION_RESULT",
  "version": "0.1",
  "message_id": "msg-003",
  "created_at": "2026-09-19T09:32:00Z",
  "task_id": "T001",
  "execution_iteration": 1,
  "status": "BLOCKED",
  "summary": "The required input document was unavailable. Review and validation could not be performed; no supporting evidence was obtained.",
  "evidence": []
}
```

| Field | Meaning |
| --- | --- |
| `status` | One of the exact strings `COMPLETED`, `FAILED`, or `BLOCKED`, reporting this bounded execution's outcome. |
| `summary` | Natural-language reporting of execution and validation facts, including relevant failure, blocking conditions, or missing evidence. |
| `evidence` | An array of material or references supporting the Result. No fixed item schema is defined. An empty array does not by itself establish completion. |

`COMPLETED` reports the Executor's completion of the bounded Task against its acceptance and applicable validation requirements. It does not mean project-roadmap-chatgpt has accepted the Result, the project objective has been achieved, or the Stage has completed.

`FAILED` reports failure of the bounded execution. `BLOCKED` reports that external conditions prevent Executor from continuing.

Report facts truthfully. Do not claim validation that was not performed or fabricate evidence. Status values report outcomes; they do not define a lifecycle state machine or transition policy.

## Scope limits

These definitions cover Task requests and an Executor-produced Result returned directly to project-roadmap-chatgpt. They do not define a complete lifecycle failure protocol for an Executor that was not created, an execution that produced no Result, or a Result that cannot be delivered or accessed.

No role or permission model, control protocol, lifecycle state machine, retry, scheduling, timeout, error model, evidence-item schema, storage service, or transport is added. No additional control message format is defined; existing explicit control and lifecycle responsibilities, including STOP handling, remain in force.

### Optional observability capability

Notification Skill is outside the Loop Contract and collaboration message set. It does not own lifecycle control or affect Task execution. Launcher or Executor may use it for observability, but a notification failure must not prevent Task execution, Result generation, or the Stage decision.
