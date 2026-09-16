import json

d = json.load(open("data/calendar.json"))
print("=== RESIDENCIES ===")
for r in d["residencies"]:
    print(json.dumps(r, indent=2))

print("\n=== FINAL ONSITE ENTRIES ===")
for e in d["entries"]:
    if "2026-10" in e["date"] or "2026-11" in e["date"]:
        print(e["date"], e["term"], e["location"], e["amCourse"][:30], e.get("pmCourse","")[:30])
