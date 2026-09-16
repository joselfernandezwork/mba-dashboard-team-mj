import json
import urllib.request

base = "https://mba-dashboard-team-mj.vercel.app"

def fetch(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())

# Team
team = fetch(base + "/data/team.json")
print("=== TEAM ===")
print("Members:", len(team["members"]))
for m in team["members"]:
    print("  " + m["name"] + " | " + m["location"] + " | " + m["email"] + " | " + m["role"])
print("TeamChange:", team.get("teamChangeNote", "N/A")[:80])
print("TeamChangeDate:", team.get("teamChangeDate", "N/A"))

# Courses
courses = fetch(base + "/data/courses.json")
print("\n=== COURSES ===")
print("Total:", courses["totalCourses"])
terms = {}
for c in courses["courses"]:
    t = c["term"]
    terms[t] = terms.get(t, 0) + 1
for t, cnt in sorted(terms.items()):
    print("  " + t + ": " + str(cnt))

# Calendar
cal = fetch(base + "/data/calendar.json")
print("\n=== CALENDAR ===")
print("Total entries:", cal["totalEntries"])
print("Terms:", cal["terms"])
print("Residencies:", len(cal["residencies"]))
for r in cal["residencies"]:
    print("  " + r["name"] + " | " + r["location"] + " | " + r["term"])
print("First entry:", cal["entries"][0]["date"], cal["entries"][0]["term"], cal["entries"][0]["amCourse"][:40])
print("Last entry:", cal["entries"][-1]["date"], cal["entries"][-1]["term"], cal["entries"][-1]["amCourse"][:40])

# Projects
projects = fetch(base + "/data/projects.json")
print("\n=== PROJECTS ===")
print("Total:", projects["totalProjects"])
for p in projects["projects"]:
    note = p.get("teamNote", "")
    print("  " + p["name"][:35].ljust(35) + " | " + p["type"][:10].ljust(10) + " | " + p["status"][:12].ljust(12) + " | " + ("HAS NOTE" if note else "no note"))

# HTML check
with urllib.request.urlopen(base + "/") as resp:
    html = resp.read().decode()
print("\n=== HTML ===")
print("Length:", len(html))
print("Has EMBA Americas:", "EMBA Americas" in html)
print("Has TEAM Mj:", "TEAM Mj" in html)
print("Has 4 nav tabs:", "showTab('courses')" in html and "showTab('projects')" in html and "showTab('calendar')" in html and "showTab('team')" in html)
