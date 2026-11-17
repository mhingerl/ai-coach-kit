#!/usr/bin/env bash
# Consistency checks for the kit repo. Run from the repo root: bash scripts/check-kit.sh
set -u
fail=0
bad() { echo "FAIL: $1"; fail=1; }
ver=$(tr -d '[:space:]' < VERSION)
top=$(grep -m1 '^## ' CHANGELOG.md | sed 's/^## //')
[ "$ver" = "$top" ] || bad "VERSION ($ver) differs from the newest changelog entry ($top)"
for f in kit/ai-coach-setup-prompt.md kit/coach-kit-checkin-skill.md; do
  grep -q "Kit version: $ver\." "$f" || bad "$f: footer does not say 'Kit version: $ver.'"
done
python3 - <<'PY' || fail=1
import re,sys
t=open('CHANGELOG.md').read()
parts=re.split(r'\n(?=## \d{4}-\d{2}-\d{2})',t)[1:]
ok=True
for p in parts:
    h=p.split('\n',1)[0][3:]
    if h<'2026-11-05': continue
    if '*Touches:*' not in p: print('FAIL: changelog',h,'has no *Touches:* line'); ok=False
    if '*If you already use the kit' not in p: print('FAIL: changelog',h,'has no *If you already use the kit* line'); ok=False
    for line in p.split('\n'):
        if line.startswith('*If you already use the kit') and line.count('*')%2: print('FAIL: changelog',h,'unclosed italic'); ok=False
sys.exit(0 if ok else 1)
PY
for f in kit/routecoach/tools/*.py; do python3 -I -m py_compile "$f" 2>/dev/null || bad "$f does not compile"; done
rm -rf kit/routecoach/tools/__pycache__
[ "$fail" = 0 ] && echo "kit checks passed ($ver)"
exit $fail
