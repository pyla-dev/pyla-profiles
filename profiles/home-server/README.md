# Home server

**Target**: a small Ubuntu server at home that must expose exactly SSH and HTTPS — and
SSH only to your management network.
**PYLA tested**: 0.2.6 · **Risk level**: hard

## What it does

- **Two doors, one of them addressed**: HTTPS to the world (switch it off if the service
  sits behind a reverse proxy/tunnel), SSH **only from the management CIDR**.
- Everything else inbound is **denied silently** — closed ports never confirm the host
  exists (no RST, no ICMP unreachable to fingerprint).
- Outbound allow-listed to DNS/NTP/updates: an unattended box should not dial home.
- Loopback untouched: local databases, agents and proxies keep working.

## ⚠ Before applying

Edit the SSH source `192.0.2.0/24` (an RFC 5737 documentation range — it matches nothing)
to **your** LAN or VPN pool, from the set detail in PYLA. Applying as-is locks you out of
remote SSH: console access remains.

## What it mitigates

Attack-surface reduction for an internet-adjacent box:

- **Brute-force and exploit attempts against every service that is not SSH/HTTPS** —
  admin panels, databases, Docker-exposed ports, printer daemons: unreachable by default,
  regardless of what the application binds to 0.0.0.0.
- **Scanning and targeting**: silent drops make the host indistinguishable from absent to
  mass scanners (the reason this is `deny`, not `reject`).
- **Outbound containment** for compromised services: a web app exploited via 443 cannot
  open arbitrary outbound connections (updates/DNS only).
- Not a CVE patch: kernel CVEs are PYLA's CVE panel job; this removes reachability.

## Verify

In PYLA after apply: **Exposure check** → SSH shows *blocked* outside the management net,
HTTPS *exposed*. From outside the management net:
`nc -w2 <host> 22` → timeout (not refused). From inside: SSH connects.
Evidence: `sudo nft list ruleset | grep -E "22|443|drop"`.

## Trade-offs

- Wrong/missing CIDR edit = locked out remotely (console saves you; plan before apply).
- Any service you add later (new site, game server) needs an explicit rule — that's the
  model working: changes are visible in the rule list, audit-ready.
