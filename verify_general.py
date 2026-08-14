#!/usr/bin/env python3
"""Verify both landing pages are the generalized version."""
import subprocess, re

for host, ip in [("qm.diazites.online", "2.25.93.230"), ("diazites.online", "2.25.93.230")]:
    r = subprocess.run(
        ["curl", "-s", "--resolve", f"{host}:443:{ip}", f"https://{host}/"],
        capture_output=True, text=True, timeout=60,
    )
    s = r.stdout
    title = re.search(r"<title>([^<]*)</title>", s)
    print(f"=== {host} ===")
    print(f"  size: {len(s)}")
    print(f"  title: {title.group(1) if title else '?'}")
    for t in ["Hire an AI employee", "never clocks out", "Roofing", "Dental", "Real estate",
              "Salons", "Veterinarians", "E-commerce", "SCENARIOS", "neat niches"]:
        print(f"  {t}: {s.count(t)}")
    q = 'action="/qm-checkout"'
    print(f"  checkout forms: {s.count(q)}")
    print()
