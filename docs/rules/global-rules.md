# Global Rules — Non-Negotiable Invariants

1. Human sovereignty is absolute. No agent may override Core or lock the human out of control.
2. All capability thresholds are binding. Agents must not operate outside their declared tier.
3. Every significant decision, deferral, and escalation must be logged.
4. P.R.O. standard applies to all communication.
5. A.E.D. rituals are mandatory at sprint end.
6. Local-first preference is maintained.
7. The `gh` CLI is the only interface for GitHub organisation resources.
8. SSH/GPG keys are shielded inside `tools/` — agents never see sensitive material.

**Repo Visibility Rule**:

- Any repository whose name starts with a dot (`.`) is private by default.
- The only exception is `.github`, which is the sole dot-prefixed public repository allowed in the organization.
- All other dot-prefixed repositories are treated as private and must not be made public without explicit Core approval.
