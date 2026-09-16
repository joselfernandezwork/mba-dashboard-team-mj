import json

# Check courses
d = json.load(open("data/courses.json"))
print("=== COURSES ===")
print("Total:", d["totalCourses"])
for c in d["courses"]:
    print("  " + c["name"][:45].ljust(45) + " | " + c["code"][:20].ljust(20) + " | " + c["instructor"][:20].ljust(20) + " | " + c["term"][:15].ljust(15) + " | " + c["status"])

print()

# Check calendar
d = json.load(open("data/calendar.json"))
print("=== CALENDAR ===")
print("Total entries:", d["totalEntries"])
for e in d["entries"][:10]:
    am = e.get("amCourse", "")[:28]
    pm = e.get("pmCourse", "")[:28]
    print("  " + e["date"] + " | " + e["term"][:15].ljust(15) + " | " + e["weekday"][:10].ljust(10) + " | " + e["location"][:20].ljust(20) + " | " + e["group"][:4].ljust(4) + " | AM=" + am.ljust(28) + " | PM=" + pm)
print("  ...")
for e in d["entries"][-5:]:
    am = e.get("amCourse", "")[:28]
    pm = e.get("pmCourse", "")[:28]
    print("  " + e["date"] + " | " + e["term"][:15].ljust(15) + " | " + e["weekday"][:10].ljust(10) + " | " + e["location"][:20].ljust(20) + " | " + e["group"][:4].ljust(4) + " | AM=" + am.ljust(28) + " | PM=" + pm)

print()

# Check team
d = json.load(open("data/team.json"))
print("=== TEAM ===")
print("Members:", len(d["members"]))
for m in d["members"]:
    print("  " + m["name"] + " (" + m["role"] + ") - " + m["location"] + " - " + m["email"])
print("TeamChange:", d.get("teamChangeNote", "N/A"))

print()

# Check projects
d = json.load(open("data/projects.json"))
print("=== PROJECTS ===")
print("Total:", d["totalProjects"])
for p in d["projects"]:
    team = str(p.get("team", "N/A"))
    print("  " + p["name"][:35].ljust(35) + " | " + p["type"][:10].ljust(10) + " | status=" + p["status"][:12].ljust(12) + " | team=" + team)
