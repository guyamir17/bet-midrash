#!/bin/bash
# Build and push. Usage: ./deploy.sh "commit message"
set -e
cd "$(dirname "$0")"
python3 build.py
cd ..
git add -A
git -c user.name="guyamir17" -c user.email="guyamir17@users.noreply.github.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || true
git -c push.negotiate=true push -q origin main 2>&1 | tail -2
git log --oneline -1
