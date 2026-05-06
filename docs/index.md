# Diataxis Framework for BrainXio — Agent Edition

Primary reference for all agents and human engineers.

**Navigation**:

- `reference/` — Authoritative rules and role definitions
- `how-to/` — Step-by-step execution protocols
- `roles/` — Individual role contracts
- `rules/` — Global + role-specific invariants
- `skills/` — Executable skills for common operations
- `thresholds/` — Capability gates

All agents must load the `reference/` documents as the single source of truth.

**Capability Gate**: Agents with context windows below 32k or running on Free-tier subscriptions must immediately acknowledge they cannot perform high-autonomy Core or Trainer tasks.
