# BrainXio Framework & Setup

This is the central home for how we actually run BrainXio.

It describes the expected environment layout, our documentation framework, working attitudes, and the practical foundations that keep everything coherent across human, agents, local hardware, and cloud resources.

---

<p align="center">
  <a href="https://github.com/brainxio/.github/tree/main/docs/tutorials">Tutorials</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/tree/main/docs/how-to">How-to Guides</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/tree/main/docs/explanation">Explanation</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/tree/main/docs/reference">Reference</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=bug_report.md">Report Bug</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=feature_request.md&labels=enhancement">Request Feature</a>
</p>

---

## How We Expect the Environment to Be Set Up

We keep things intentionally simple, sovereign, and observable. Every development or runtime environment should follow the same baseline structure so agents and humans can move between machines without friction.

Core expectations:
- All projects live under a main workspace (usually `~/brainxio/` or `/opt/brainxio/`)
- Each repository follows the standard layout defined in our standards
- Local models and guardrails run where hardware allows
- Cloud sessions respect subscription tiers and never exceed them without explicit approval
- Everything stays local-first by default, with clear separation between development containers and runtime containers

We actively use three operating attitudes that adapt to both the human and the available resources:

- **F.R.E.E.** — our human mode: light, mindful, and always free  
- **P.R.O.** — our collaboration mode: balanced, professional, and realistic  
- **M.A.X.** — our exploration mode: deep, autonomous, and playful  

These combine into clear states such as FreePro, ProMax, or MaxFree so everyone always knows the current operating boundaries. Fun is never optional — even clean professional work must stay **fun**ctional.

## Our Documentation Framework (Diátaxis)

We organize all knowledge using the Diátaxis framework for maximum clarity and usability:

```bash
.github/
├── docs/
│   ├── index.md
│   ├── tutorials/                # Guided learning journeys
│   │   ├── getting-started.md
│   │   ├── first-sprint.md
│   │   ├── setting-up-your-environment.md
│   │   └── using-the-agents.md
│   ├── how-to/                   # Practical step-by-step solutions
│   │   ├── run-a-sprint.md
│   │   ├── add-a-new-agent-role.md
│   │   ├── configure-local-models.md
│   │   ├── handle-subscription-limits.md
│   │   └── contribute-to-the-project.md
│   ├── explanation/              # Understanding the “why”
│   │   ├── last-sprint-cpr-procedure.md
│   │   ├── next-sprint-aed-utility.md
│   │   ├── objective-pro-attitude.md
│   │   ├── idiot-playground.md
│   │   ├── neurodivergent-drivers.md
│   │   └── sovereignty-and-local-first.md
│   └── reference/                # Facts, specs, and quick lookups
│       ├── roles-overview.md
│       ├── acronyms-glossary.md
│       ├── standards-and-rules.md
│       ├── mcp-servers.md
│       └── hardware-requirements.md
├── README.md                     # This file – setup & overview
└── profile/
    └── README.md                 # Public welcome page
```

This structure keeps learning gentle, problem-solving fast, understanding deep, and reference quick.

---

We move at our own pace, with clarity, care, and a lot of quiet joy.

Welcome to the inside of BrainXio.