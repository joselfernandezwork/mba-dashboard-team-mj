#!/usr/bin/env python3
"""Extract individual and team project data from EMBA program sources."""
import json
import os
from datetime import datetime

CLASSES_ROOT = "/Users/joselfernandezperera/Documents/Cornell/Classes"

# Team 2 project metadata (from directory structure + MASTER_CONTEXT.md + Team2_CFP_Review_Rundown.md)
# Note: Team 2 roster was reduced to 2 members (Jose Luis Fernandez Perera and Dr. Marian Hanna) as of September 15, 2026.
# All projects in progress or upcoming from this date forward are handled by these 2 members.
TEAM_PROJECTS = {
    "Corporate Financial Policy": {
        "course": "Corporate Financial Policy",
        "courseCode": "NBAB 5580 / MBQC 822",
        "instructor": "Steven A. Carvell",
        "team": "Team 2",
        "parts": [
            {"name": "Part One: Company Positioning Statement", "weight": "15%", "status": "completed"},
            {"name": "Part Two: Individual Advocacy Document", "weight": "25%", "status": "completed"},
            {"name": "Part Three: Company Selection Framework", "weight": "10%", "dueDate": "2026-09-14", "status": "in-progress"},
            {"name": "Part Four: Group Discussion with Professor", "weight": "15%", "dueDate": "2026-09-25", "status": "pending"},
            {"name": "Part Five: Final Written Project", "weight": "35%", "dueDate": "2026-10-14/15", "status": "pending"},
        ],
        "selectedCompany": "Pfizer (pending team vote)",
        "advocates": ["Jose Luis (NVIDIA)", "Marian (CSW Industrials)"],
        "status": "Part Three in progress",
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to Jose Luis Fernandez Perera and Dr. Marian Hanna. Going forward, all CFP parts are handled by these 2 members.",
    },
    "Critical Thinking for Business Leaders": {
        "course": "Critical Thinking for Business Leaders",
        "courseCode": "NBAB 5880",
        "instructor": "Risa Mish",
        "team": "Team 2",
        "deliverable": "American Girl Case Group Project",
        "status": "submitted",
        "dueDate": "Spring 2026",
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members (Jose Luis Fernandez Perera and Dr. Marian Hanna). This project was completed under the original team roster.",
    },
    "Business Strategy": {
        "course": "Business Strategy",
        "courseCode": "NCCB 5090 / MBQC 901",
        "instructor": "Faculty TBD",
        "team": "Team 2",
        "deliverable": "Hulu Reorganization Strategy",
        "status": "in-progress",
        "subgroups": ["Jose Luis", "Dr. Marian Hanna"],
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members.",
    },
    "Global Business Project": {
        "course": "Global Business Project",
        "courseCode": "NBAB 5970 / MBQC 907",
        "instructor": "Shai Dubey",
        "team": "Team 2",
        "status": "in-progress",
        "phase": "Strategy & Validation to Project Execution",
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members.",
    },
    "Marketing Strategy": {
        "course": "Marketing Strategy",
        "courseCode": "NBAB 6220 / MBQC 932",
        "instructor": "Monica LaBarge",
        "team": "Team 2",
        "status": "in-progress",
        "subgroups": ["JTBD Analysis (Jose Luis)", "Strategy & Visual Communication (Dr. Marian)"],
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members.",
    },
    "Investment Banking Essentials": {
        "course": "Investment Banking Essentials",
        "courseCode": "TBD",
        "instructor": "Drew Pascarella",
        "team": "Team 2",
        "status": "in-progress",
        "deliverable": "LBO Group Assignment (ServiceTitan)",
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members.",
    },
    "Managing Operations": {
        "course": "Managing Operations",
        "courseCode": "NCCB 5080 / MBQC 941",
        "instructor": "Yao Cui",
        "team": "Team 2",
        "status": "completed",
        "deliverables": ["Littlefield Technologies Simulation (5th of 20 teams, $2M final cash)", "Lean Operations Presentation", "National Cranberry Cooperative"],
        "teamNote": "As of September 15, 2026, Team 2 roster reduced to 2 members (Jose Luis Fernandez Perera and Dr. Marian Hanna). This project was completed under the original team roster.",
    },
}

INDIVIDUAL_PROJECT = {
    "name": "EduCollab",
    "course": "Individual Project (NMI 5001 / MBQC 808)",
    "description": "EdTech startup focused on collaborative learning platforms for higher education",
    "status": "Phase 1 submitted (April 27, 2026); Final Project due June 1, 2026",
    "deliverables": [
        {"name": "Business Plan", "sections": 15, "status": "submitted"},
        {"name": "Financial Model", "tabs": 5, "status": "submitted"},
        {"name": "Pitch Deck", "status": "submitted"},
        {"name": "Final Project", "status": "in-progress", "dueDate": "2026-06-01"},
    ],
    "marketAnalysis": ["US", "Canada", "Europe", "LATAM"],
    "research": ["Research & Analysis", "Research Audit", "Competitive Analysis", "Business Model Analysis"],
    "app": "eduCClab MVP (HTML/CSS/JS prototype at Classes/Individual-Project/App/educollab-mvp/)",
}

def main():
    projects = []
    for name, data in TEAM_PROJECTS.items():
        projects.append({
            "type": "team",
            "name": name,
            **data,
        })
    projects.append({
        "type": "individual",
        **INDIVIDUAL_PROJECT,
    })

    output = {
        "source": "Generated from Team 2 shared folder and Individual-Project directory",
        "generatedAt": datetime.now().isoformat(),
        "cohort": "EMBA Americas 27",
        "totalProjects": len(projects),
        "individualProjects": [p for p in projects if p["type"] == "individual"],
        "teamProjects": [p for p in projects if p["type"] == "team"],
        "projects": projects,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "projects.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print("Written {} projects to {}".format(len(projects), out_path))

if __name__ == "__main__":
    main()
