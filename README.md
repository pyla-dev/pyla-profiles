# PYLA Profiles

Ready-made, reviewed firewall rule sets for [PYLA](https://github.com/pyla-dev/pyla), the
open-source firewall and CVE-aware hardening tool for Ubuntu.

The idea is borrowed from the way hardening guidance worked in the NIST / USGCB world for
Active Directory: a **published baseline** you can read line by line, **import** in one click,
then **verify** against your own machine — no faith required.

> Import, verify, own it.

## How it works

1. **Pick a profile** below, read its README (what it does, what it mitigates, what it breaks).
2. **Import it** in PYLA: *Import from file…* → select the `.jsonc`. Every rule shows up with
   its state and comment; nothing is applied until you preview and apply.
3. **Verify**: each profile ships a *Verify* section — PYLA's Exposure check plus the exact
   `nft`/`ss` commands to prove the result yourself. This is the gpresult moment: you see what
   is enforced on *your* machine, not what the docs promise.

## Profiles

| Profile | One-liner | PYLA tested |
|---|---|---|
| [`stealth`](profiles/stealth/) | Silent machine: no inbound port answers anything, no ICMP replies, outbound limited to system services. Access via console or VPN only. | 0.2.6 |
| [`workstation-laptop`](profiles/workstation-laptop/) | Sensible daily-driver baseline: full outbound, nothing inbound except established/related, management SSH off by default. | 0.2.6 |
| [`home-server`](profiles/home-server/) | Small exposed server: SSH and HTTPS only, from your management network, everything else discarded silently. | 0.2.6 |

## House rules

A profile is merged only if:

- **Import-tested**: the JSONC imports cleanly in the PYLA version listed in its README
  (CI runs the schema check; the import test is part of review).
- **CVE claims are verified or absent**: if a profile says it mitigates a CVE, the README links
  the Ubuntu Security advisory and the mitigation is true for the described configuration.
  Profiles that only reduce attack surface say so plainly — no invented CVE mapping.
- **Trade-offs documented**: what stops working after applying it, always.
- **Least surprise**: profiles never enable destructive actions, never touch default policies
  behind your back, and ship disabled rules (like management SSH) switched *off*.

## Format

Profiles are PYLA rule-set exports in JSONC (JSON with comments — the comments are the
documentation, keep them). The accepted schema is in [`schema/profile.schema.json`](schema/profile.schema.json);
`scripts/validate.sh` checks every profile against it.

## License

MIT — same as PYLA. Rules are configuration, not code: use them, fork them, adapt them.
