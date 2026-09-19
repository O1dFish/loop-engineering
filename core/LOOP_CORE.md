# Loop Core

- Project Authority owns project decisions.
- Launcher owns stage lifecycle.
- Executor owns bounded task execution.
- Task completion does not equal Stage completion.
- Only explicit structured control changes lifecycle.
- Executor returns result to Project Authority.
- Projects consume Loop Contract and cannot directly modify it.
- Role definitions do not assign roles; roles must be assigned explicitly.
- Each role receives only the minimum contract projection required for its responsibility; further contract material is limited to what that responsibility requires.
