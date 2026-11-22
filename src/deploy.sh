#!/bin/bash
# build standalone single file and push to GitHub
set -e
cd /home/claude
python3 - <<'PY'
s=open('/home/claude/app/index.html').read()
d=open('/home/claude/app/data.json').read()
old='fetch("data.json").then(r => r.json()).then(d => { DATA = d; render(); })'
assert old in s
s=s.replace(old,'Promise.resolve(JSON.parse(document.getElementById("bm-data").textContent)).then(d => { DATA = d; render(); })')
s=s.replace('<script>\n"use strict";','<script type="application/json" id="bm-data">'+d.replace('</','<\\/')+'</script>\n<script>\n"use strict";')
open('/home/claude/bet-midrash/index.html','w').write(s)
PY
cd /home/claude/bet-midrash
git add -A
git -c user.name="guyamir17" -c user.email="guyamir17@users.noreply.github.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_011bakAc9hLhWZkkhiryKc8q" || true
git -c push.negotiate=true push -q origin main 2>&1 | tail -2
git log --oneline -1
