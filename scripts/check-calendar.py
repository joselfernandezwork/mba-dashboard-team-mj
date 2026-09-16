import json

d = json.load(open("data/calendar.json"))
# Show entries around transition points
for i, e in enumerate(d["entries"]):
    dt = e["date"]
    if e["term"] == "Summer 2025" and "2025-07-1" in dt:
        print("Summer VCR:", dt, e["location"], e["amCourse"][:40], e["pmCourse"][:40])
    if e["term"] == "Fall 2025" and "2025-09" in dt:
        print("Fall VCR:", dt, e["location"], e["amCourse"][:30], e["pmCourse"][:30])
    if e["term"] == "Spring 2026" and "2026-01-04" in dt:
        print("Spring VCR:", dt, e["location"], e["amCourse"][:30], e["pmCourse"][:30])
    if e["term"] == "Fall 2026" and "2026-09" in dt:
        print("Fall start:", dt, e["location"], e["amCourse"][:30], e["pmCourse"][:30])

# Count by term
terms = {}
for e in d["entries"]:
    t = e["term"]
    terms[t] = terms.get(t, 0) + 1
print()
print("Entries by term:")
for t, c in sorted(terms.items()):
    print("  " + t + ": " + str(c))
