# Security Policy

## Supported Versions

| Version | Support Status | Notes                                 |
| ------- | -------------- | ------------------------------------- |
| v1.x    | Active support | Receive security patches              |
| v0.x    | End of life    | No security updates; upgrade required |

## Scope

- BrainXio GitHub repositories
- GitHub Actions workflows
- MCP servers (`brainxio-agent-*` packages)
- Published packages: npm (`@brainxio/*`), PyPI (`brainxio-*`), crates.io (`brainxio-*`)

## Out of Scope

- Social engineering or phishing attacks
- Denial-of-service attacks
- Third-party services or dependencies (report upstream)
- Vulnerabilities already disclosed via public CVE

## Reporting a Vulnerability

**Preferred: GitHub Security Advisories**
Open a draft advisory at `https://github.com/BrainXio/<repo>/security/advisories/new`.

**Backup: Email**
Contact github@brainxio.org. Encrypt if possible (PGP key available on keyserver).

**What to include:**

- Affected repository and version or commit SHA
- Description of the vulnerability
- Steps to reproduce
- Proof-of-concept or exploit (if any)
- Potential impact assessment

**Do not** open public issues or discuss vulnerabilities publicly until a patch is available.

## Response SLAs

| Severity | Initial Response | Triage          |
| -------- | ---------------- | --------------- |
| Critical | 24 hours         | 48 hours        |
| High     | 48 hours         | 5 business days |
| Medium   | 5 business days  | —               |
| Low      | 5 business days  | —               |

Severity is assessed by BrainXio based on CVSS scoring and blast radius.

## Coordinated Vulnerability Disclosure (CVD)

1. Reporter submits via GitHub Security Advisory or email.
1. BrainXio acknowledges within the SLA window.
1. BrainXio reproduces and validates, requests CVE number if applicable.
1. Fix is developed under embargo.
1. Patch is released publicly with credit (if agreed).
1. Public disclosure occurs **only after a fix is available**.
1. Full public advisory published within **90 days** of initial report, regardless of patch status.

## Safe Harbor

Good-faith security research performed in accordance with this policy will not result in legal action by BrainXio.

BrainXio reserves the right to update this policy. Substantive changes will be reflected in this file.
