# AGENT.md

## Python tooling
- Use `uv` for Python workflow and commands.
- Use `uv sync` to install/sync dependencies.
- Use `uv run ...` to execute project commands.

## Type checking requirement
- After each completed task, run the `ty` type checker via `uv`:
  - `uv run ty check`
- A task is only complete after this type check passes.
