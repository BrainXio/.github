# How to Detect Your Capability Tier

Run this at the start of every session or before any high-impact task.

```bash
uv run --directory .github/tools python detect_capability_tier.py
```

**Example output:**

```json
{
  "worker_tier": "B",
  "trainer_tier": "2",
  "note": "Detected Worker Tier B | Trainer Tier 2"
}
```

## Interpreting the Result

- **Worker Tier A**: Full autonomy, may temporarily assume Core when human absent
- **Worker Tier B**: Standard collaboration mode (most common)
- **Worker Tier C**: Light / cautious mode — escalate early

- **Trainer Tier 1**: Can perform full fine-tuning
- **Trainer Tier 2**: Assisted training only
- **Trainer Tier 3**: No training tasks

Agents should store this result and reference it before accepting complex work.
