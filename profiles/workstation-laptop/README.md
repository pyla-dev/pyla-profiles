# Workstation laptop

**Target**: the Ubuntu laptop you carry to hotels, conferences and home Wi-Fi every week.
**PYLA tested**: 0.2.6 · **Risk level**: medium (balanced for daily use)

## What it does

- **Nothing breaks**: full outbound, all inbound return traffic (established/related)
  works — this is the baseline you can enable on a working machine without calling it a day.
- Inbound is default-deny: no port listens to the network unless you switch something on.
- Two **quiet-mode** rules (mDNS 5353, SSDP 1900) ship disabled: enable them on untrusted
  networks to stop Avahi/Bonjour announcing your hostname on every hotel access point.
- SSH exists as a disabled rule: one toggle in PYLA when you need it, never silently open.

## What it mitigates

Attack-surface reduction for the mobile-machine threat model:

- **LAN-based opportunistic attacks** (evil-twin Wi-Fi, rogue devices on the same segment):
  nothing inbound answers, so the laptop is invisible to the `avahi-browse`/`ssdp` scans
  that map guest networks in seconds.
- **Discovery of the machine for targeted exploitation** — the CVE comes to you on the road;
  this profile means the attacker has to guess, not enumerate.
- Not a CVE patch: kernel CVEs are PYLA's CVE panel job (with reversible mitigations);
  this profile removes the reachability that makes them remotely exploitable.

## Verify

In PYLA after apply: **Exposure check** → only loopback listeners. From another host on
the same network: `ping` unanswered, `avahi-browse -arp` no longer lists your machine
(with quiet-mode rules on). On the host:
`sudo nft list ruleset | head -30` → default policy drop, loopback allows, final deny.

## Trade-offs

- File sharing / AirPlay-style discovery to this laptop stops working (by design; enable
  the specific rule when you're on a trusted LAN).
- Deliberately **no outbound restrictions**: a laptop baseline that breaks the VPN or the
  captive portal gets disabled by its owner in ten minutes — then there is no firewall at
  all. Use the `stealth` profile when you want egress control too.
