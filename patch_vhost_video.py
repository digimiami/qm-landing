#!/usr/bin/env python3
"""Add demo video + poster static locations to the qm nginx vhost on PROD."""
import subprocess, sys

VHOST = "/etc/nginx/sites-enabled/qm.diazites.online"
ANCHOR = """    location = /og-image.png {
        root /var/www/qm-landing;
        add_header Cache-Control "public, max-age=86400";
    }
"""
INSERT = """    location = /og-image.png {
        root /var/www/qm-landing;
        add_header Cache-Control "public, max-age=86400";
    }

    # hero demo video + poster (serve from landing dir)
    location = /demo_web.mp4 {
        root /var/www/qm-landing;
        add_header Cache-Control "public, max-age=86400";
    }
    location = /demo-poster.jpg {
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
if "demo_web.mp4" in s:
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
