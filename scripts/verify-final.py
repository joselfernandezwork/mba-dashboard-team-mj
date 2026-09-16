import json
import urllib.request

base = "https://mba-dashboard-team-mj.vercel.app"

def fetch(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())

team = fetch(base + "/data/team.json")
print("TEAM: " + str(len(team["members"])) + " members")
for m in team["members"]:
    print("  " + m["name"] + " | " + m["role"])
print("Change date: " + team.get("teamChangeDate", "N/A"))

projects = fetch(base + "/data/projects.json")
print("PROJECTS: " + str(projects["totalProjects"]))
has_note = 0
no_note = 0
for p in projects["projects"]:
    if p["type"] == "team":
        if "teamNote" in p:
            has_note += 1
        else:
            no_note += 1
            print("  MISSING NOTE: " + p["name"])
print("  Team projects with teamNote: " + str(has_note))
print("  Team projects without teamNote: " + str(no_note))

cal = fetch(base + "/data/calendar.json")
print("CALENDAR: " + str(cal["totalEntries"]) + " entries, " + str(len(cal["residencies"])) + " residencies")

courses = fetch(base + "/data/courses.json")
print("COURSES: " + str(courses["totalCourses"]))

with urllib.request.urlopen(base + "/") as resp:
    html = resp.read().decode()
print("HTML: " + str(len(html)) + " bytes, has EMBA Americas: " + str("EMBA Americas" in html))
