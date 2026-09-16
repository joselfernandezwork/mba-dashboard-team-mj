#!/usr/bin/env python3
"""Extract Team 2 roster and information from EMBA program sources."""
import json
import os
from datetime import datetime

# Source: MASTER_CONTEXT.md (Managing Operations), Team 2 contract, meeting agendas
# Two core members for this dashboard (team restructured September 15, 2026)
TEAM_MEMBERS = [
    {"name": "Jose Luis Fernandez Perera", "nickname": "joseluis", "location": "Menlo Park, CA", "timeZone": "PT", "email": "jlf348@cornell.edu", "role": "Team 2 member"},
    {"name": "Dr. Marian Hanna", "nickname": "Marian", "location": "San Diego, CA", "timeZone": "PT", "email": "mh2635@cornell.edu", "role": "Team 2 member"},
]

TEAM_INFO = {
    "program": "EMBA Americas 27",
    "teamName": "Team 2",
    "nickname": "the awesome team",
    "established": "April 2026 (restructured September 15, 2026)",
    "members": TEAM_MEMBERS,
    "teamChangeDate": "2026-09-15",
    "teamChangeNote": "Team 2 roster reduced to 2 members (Jose Luis Fernandez Perera and Dr. Marian Hanna) as of September 15, 2026. All projects in progress or upcoming from this date forward are handled by these 2 members.",
    "recentActivity": {
        "lastMeeting": "August 25, 2026",
        "lastMeetingAgenda": "Team 2 Working Meeting - Investment Banking project discussion, Global Business Project discussion",
        "nextStandingMeeting": "Tuesdays, 6:30 PM ET",
        "currentFocus": "Corporate Financial Policy Part Three, Investment Banking team project, Global Business Project, Marketing Strategy team project",
    },
    "discAssessments": True,
    "discAssessmentsPath": "Classes/Team 2/Copy From OneDrive/Second Copy/DISC Assessments/",
    "meetingRecordings": True,
    "meetingRecordingsPath": "Classes/Team 2/Copy From OneDrive/Second Copy/Meetings/Meeting Recordings/",
    "boardroomGroup": "Team 2 boardroom group information available at Administration/Board Rooms/",
}

def main():
    output = {
        "source": "MASTER_CONTEXT.md (Managing Operations), Team 2 contract, meeting agendas",
        "generatedAt": datetime.now().isoformat(),
        **TEAM_INFO,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "team.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print("Written Team 2 info to {}".format(out_path))

if __name__ == "__main__":
    main()
