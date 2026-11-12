# Contributing a profile

A profile is a reviewed, importable PYLA rule set with documentation. Before merging:

1. **Copy the layout**: `profiles/<name>/profile.jsonc` + `profiles/<name>/README.md`
   (sections: What it does / What it mitigates / Verify / Trade-offs).
2. **Validate**: `python3 scripts/validate.py` must pass (CI runs it on every PR).
3. **Import-test** in PYLA (state the version in the README). Comments in the JSONC are
   part of the documentation: explain every non-obvious rule, keep them in English.
4. **Honest claims**: if you cite CVEs, link the Ubuntu Security advisory and verify the
   mitigation is real for the described configuration. Attack-surface-only profiles must
   say so — no invented CVE mapping.
5. **No lockouts by default**: rules that can cut off access (SSH sources, outbound
   denies beyond updates) must ship disabled or with an RFC 5737 placeholder CIDR and a
   loud comment.

Keep profiles boring and reviewable: fewer, well-documented sets beat a long shelf.
