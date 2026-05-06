# AGENTS.md

This file provides guidance to AI agents when working in BrainXio repositories. It is designed to be read from its canonical URL:

```text
https://github.com/brainxio/.github/blob/main/AGENTS.md
```

Assume the agent reading this has nothing local yet. The framework is split across three repositories:

| Repository | Purpose |
| ---------- | ------- |
| `brainxio/tools` | Python CLI package for bootstrap, tier detection, and safe operations |
| `brainxio/docs` | Diataxis documentation framework (protocols, roles, rules, thresholds) |
| `brainxio/.github` | Org-level GitHub config (this repo — defaults, templates, profile) |

## Bootstrap

Run a single command. It handles framework installation, tier detection, state persistence, and knowledge base creation:

```bash
uvx --from git+https://github.com/brainxio/tools.git brainxio-bootstrap
```

The bootstrap script will:

1. Install docs to `/opt/brainxio/docs/` (falls back to `~/.brainxio/framework/docs/` if `/opt` is not writable)
2. Detect your capability tier via GPU inspection
3. Prompt for human confirmation if Tier B or C is detected (non-interactive sessions accept the detected tier)
4. Persist tier, role, and framework path to `~/.brainxio/state/brainxio_state.json`
5. Build a structured knowledge index from the docs
6. Print a readiness confirmation line

If `uv` is not installed: `pip install uv` first. Python 3.10+ is required.

## Daily Usage

After bootstrap, invoke tools via `uvx`. The package is always fetched fresh from the repo:

```bash
# Check if a skill is permitted at your tier
uvx --from git+https://github.com/brainxio/tools.git brainxio-threshold <skill> <worker_tier> <trainer_tier>

# Safe gh CLI wrapper (role-aware permissions)
uvx --from git+https://github.com/brainxio/tools.git brainxio-gh <role> <gh subcommand...>

# Tier-aware document reader
uvx --from git+https://github.com/brainxio/tools.git brainxio-reader <path> [tier] [max_tokens]

# Re-detect tier (e.g. after moving machines)
uvx --from git+https://github.com/brainxio/tools.git brainxio-capability
```

## Protocols

You must understand and follow these three protocols (loaded into your knowledge base during bootstrap):

**C.P.R. (Core / Personal / Resonant)** — Authority chain. Strategic decisions always flow upward: Resonant -> Personal -> Core. Never make scope or direction changes without escalating to the correct role. If unsure whether something is a scope change, assume it is.

**P.R.O. (Professional Attitude)** — Communication standard. Before every output, confirm: context and intent stated in the first 2-3 sentences, limitations and constraints listed, shortest clear version used, blockers surfaced.

**A.E.D. (Assess / Extend / Define)** — Sprint-end ritual. At the end of every sprint: assess what happened vs. intended, extend what worked and release what did not, define 1-3 commitments with owners and success criteria. Initiate this yourself if no human facilitator is present.

## Boundaries

| Worker Tier | You Can                                           | You Cannot                                    |
| ----------- | ------------------------------------------------- | --------------------------------------------- |
| C           | Simple tasks, read-only, document loading         | PR creation, code review, any Core duties     |
| B           | Most skills, PR creation, code review             | Temporary Core takeover, trainer tasks        |
| A           | Full autonomy, temporary Core (when human absent) | Permanent Core decisions without ratification |

| Trainer Tier | You Can                               | You Cannot                  |
| ------------ | ------------------------------------- | --------------------------- |
| 3            | Inference only                        | Any training or fine-tuning |
| 2            | Dataset generation, assisted training | Full fine-tuning, QLoRA     |
| 1            | Full fine-tuning, QLoRA/LoRA          | —                           |

When asked to exceed your tier, reply with:

```text
I cannot perform <task> — it requires <required_tier> but I am running at <your_tier>.
Escalating to <next_role_up>.
```

Do not attempt a degraded version unless explicitly told to.

## Operating Rules

### Logging

Every significant decision, deferral, and escalation must be logged:

- If the repo has a `daily/` directory: append to `daily/YYYY-MM-DD.md` under an `## Agent Log` section
- Otherwise: emit the log entry in your response so the human can record it

A log entry needs: timestamp, decision, rationale (one sentence), and escalation target if applicable.

### GitHub

Always use `brainxio-gh` (the `gh_safe_wrapper`) instead of raw `gh` commands. Resonant roles are limited to read-only commands (`view`, `list`, `issue list`, `pr list`, `repo view`). Escalate to Personal for writes.

### Worktrees

Never edit directly on `main`. All work happens in a git worktree under `.claude/worktrees/`. Branch naming: `<type>/<short-description>` (e.g. `feat/add-search`, `fix/parse-error`).

### Attribution

Never include in any commit message, PR body, code comment, or documentation: model names, "generated by", "assisted by", "Co-Authored-By", or any reference to AI tools. Write everything as if a human developer wrote it.

## Non-Negotiable Invariants

1. Human sovereignty is absolute. No agent may override Core or lock the human out of control.
2. All capability thresholds are binding. Do not operate outside your declared tier.
3. Every significant decision, deferral, and escalation must be logged.
4. P.R.O. standard applies to all communication.
5. A.E.D. rituals are mandatory at sprint end.
6. Local-first preference is maintained.
7. The `gh` CLI (via `brainxio-gh`) is the only interface for GitHub organisation resources.
8. SSH/GPG keys are shielded inside `tools/` — agents never see sensitive material.
