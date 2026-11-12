# Silent stealth

**Target**: machines that should offer nothing and confirm nothing — laptops left on
untrusted networks, jump hosts, machines you only ever touch from console or VPN.
**PYLA tested**: 0.2.6 · **Risk level**: hard

## What it does

- Inbound: **everything is dropped without replying** (deny, not reject — a closed port
  stays invisible: no RST, no ICMP unreachable for the prober to fingerprint).
- Pings die silently: ICMP echo requests hit the final deny, while the ICMP replies that
  protocols genuinely need (PMTUD, traceroute responses) come back as `related` state and
  UFW allows them on its own.
- Outbound: only DNS (UDP+TCP), NTP, HTTP/HTTPS updates, DHCP client (v4 and v6).
- LAN discovery (mDNS, DHCPv6) is present but **off**; management SSH is present but **off**.

## What it mitigates

This profile is attack-surface reduction, not a CVE patch. It is the "why weren't the
defenses up before?" answer:

- **Removes the remote entry point for every network-facing kernel CVE** while you wait
  for the patched kernel (e.g. MPTCP-class remote CVEs — PYLA's CVE panel offers the
  subsystem mitigation separately; this set removes the listener surface entirely).
- **Defeats scanning and OS fingerprinting** (nmap SYN scans and TTL probing get no answer
  at all — the host looks absent, not "firewalled").
- **Contains outbound C2/exfil channels** to the four egress paths listed (allow-list
  model; if you need another egress, add it and comment why).

## Verify (your gpresult moment)

In PYLA: import → apply → **Exposure check**: no listener should be reachable from outside
loopback. From another machine:

```sh
ping -c1 <host>              # no reply (silent)
nmap -Pn -p- --max-rate 500 <host>   # all ports "filtered"→ actually no response at all
nc -w2 <host> 22             # timeout, not connection refused
```

Evidence on the host: `sudo nft list ruleset | grep -E "drop|deny"` — the final inbound
rule is a drop, and there is no reject anywhere.

## Trade-offs

- **No remote access** unless you enable the SSH rule (and edit its source CIDR first) or
  come in over VPN. A locked door is the point.
- Services you start later (a dev web server, AirPlay, printing) will be silently
  unreachable — that is the profile working, not a bug.
- `ufw limit` rate limiting is not expressible in PYLA's model; if you expose SSH later,
  add `sudo ufw limit 22/tcp` by hand.
