# Composite Actions

These actions are consumed by the reusable workflows in `workflows/`.

Do not call them directly from consumer repositories — they are implementation details of the reusable workflows.

## Available Actions

| Action | Purpose |
|---|---|
| `setup-python-deps` | Install Python with uv, caching, and optional dependency groups |
| `setup-node-deps` | Install Node.js with npm/pnpm/yarn, caching, and script runner |
| `setup-go-deps` | Install Go with module and build caching |
| `setup-rust-deps` | Install Rust toolchain with rust-cache |

## Cache Best Practices

See [cache-best-practices.md](cache-best-practices.md) for the restore-keys pattern used across all actions.
