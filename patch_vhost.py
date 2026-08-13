#!/usr/bin/env python3
"""Add favicon.svg + og-image.png static locations to the qm nginx vhost on PROD."""
import subprocess, sys

VHOST = "/etc/nginx/sites-enabled/qm.diazites.online"
ANCHOR = """    location = /index.html {
        root /var/www/qm-landing;
        add_header Cache-Control "no-store";
    }
"""
INSERT = """    location = /index.html {
        root /var/www/qm-landing;
        add_header Cache-Control "no-store";
    }

    # static brand assets (serve from landing dir, not proxied to portal)
    location = /favicon.svg {
        root /var/www/qm-landing;
        add_header Cache-Control "public, max-age=86400";
    }
    location = /og-image.png {
        root /var/www/qm-landing;
        add_header Cache-Control "public, max-age=86400";
    }
"""

script = f'''
import re
p = "{VHOST}"
s = open(p).read()
anchor = """{ANCHOR}"""
insert = """{INSERT}"""
if "og-image.png" in s:
    print("already patched")
else:
    assert anchor in s, "anchor not found"
    s = s.replace(anchor, insert, 1)
    open(p, "w").write(s)
    print("vhost patched")
'''
r = subprocess.run(["sshpass", "-e", "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
                    "root@2.25.93.230", "python3 -"], input=script, capture_output=True, text=True, timeout=90)
print(r.stdout.strip() or r.stderr.strip())
sys.exit(r.returncode)
