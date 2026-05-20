# Cache Best Practices

All setup composite actions use explicit `restore-keys` fallbacks to maximize cache-hit rate across branch boundaries and partial dependency changes.

## Pattern

```yaml
- uses: actions/cache/restore@v4
  with:
    path: <ecosystem-cache-paths>
    key: ${{ runner.os }}-<ecosystem>-<hash-of-lockfile>
    restore-keys: |
      ${{ runner.os }}-<ecosystem>-

- uses: <built-in-setup-action>
  with:
    cache: true  # built-in cache handles primary save / restore
```

The `actions/cache/restore@v4` step provides a broader fallback key family **before** the built-in setup step runs. The built-in step then manages its own primary cache save/restore with a more specific key. This gives two chances for a cache hit without double-saving.

## Ecosystem-Specific Keys

| Action | Fallback Key | Lockfiles |
|---|---|---|
| `setup-go-deps` | `${{ runner.os }}-go-` | `go.sum`, `go.mod` |
| `setup-node-deps` | `${{ runner.os }}-${{ inputs.package-manager }}-` | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` |
| `setup-python-deps` | `${{ runner.os }}-uv-` | `pyproject.toml`, `uv.lock`, `requirements*.txt` |
| `setup-rust-deps` | `${{ runner.os }}-cargo-` | `Cargo.lock` |

## Why Not `actions/cache@v4` (Save + Restore)?

Using the full `actions/cache` action in a composite alongside a built-in cache would create **two** save steps and potential cache key conflicts. `actions/cache/restore` is restore-only, so the built-in step remains the single source of truth for cache saves while the manual step only broadens the restore key family.
