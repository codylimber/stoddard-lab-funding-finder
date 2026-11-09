#!/usr/bin/env python3
"""Print the weekly recheck worklist as Markdown.

Lists, from catalog/programs/*.json:
  1. rows with a posted deadline in the next 60 days (verify the date still holds)
  2. rows whose posted deadline has passed (roll to the next cycle or set to watch)
  3. rows tagged unconfirmed (`unv`)
  4. rows not checked in the last 30 days
Usage: python3 engine/recheck_report.py
"""
import glob, json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
today = datetime.date.today()
rows = []
for fp in sorted(glob.glob(os.path.join(ROOT, "catalog", "programs", "*.json"))):
    x = json.load(open(fp, encoding="utf-8"))
    rows.extend(x if isinstance(x, list) else [x])

def d(s):
    try:
        return datetime.date.fromisoformat(s)
    except Exception:
        return None

def line(r, extra=""):
    return f"- [{r['n']}]({r['u']}) · `{r['id']}`{extra}"

soon = [r for r in rows if d(r.get("d")) and 0 <= (d(r["d"]) - today).days <= 60]
past = [r for r in rows if d(r.get("d")) and d(r["d"]) < today]
unv = [r for r in rows if r.get("unv")]
stale = [r for r in rows if not d(r.get("checked")) or (today - d(r["checked"])).days > 30]

print(f"# Weekly recheck worklist ({today.isoformat()})\n")
for title, lst, fmt in [
    ("Deadline within 60 days: confirm the date", sorted(soon, key=lambda r: r["d"]), lambda r: f" · due {r['d']}"),
    ("Posted deadline has passed: find the next cycle or move to watch", past, lambda r: f" · was {r['d']}"),
    ("Tagged unconfirmed: read the funder's page", unv, lambda r: f" · {r['unv']}"),
    ("Not checked in 30+ days", stale, lambda r: f" · last checked {r.get('checked', 'never')}"),
]:
    print(f"## {title} ({len(lst)})\n")
    print("\n".join(line(r, fmt(r)) for r in lst) or "- none")
    print()
