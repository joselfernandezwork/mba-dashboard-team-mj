#!/usr/bin/env python3
"""Extract course data from EMBA Americas Classes directory."""
import os
import json
from pathlib import Path
from datetime import datetime

CLASSES_ROOT = "/Users/joselfernandezperera/Documents/Cornell/Classes"

COURSE_DETAILS = {
    "Accounting": {"code": "NBCB 5200 / MBQC 806", "instructor": "Brian White", "term": "Fall 2025", "status": "completed"},
    "Applied AI": {"code": "Elective", "instructor": "TBD", "term": "Summer 2026", "status": "completed"},
    "Applied Microeconomics": {"code": "MBQC 882", "instructor": "Ricard Gill", "term": "Spring 2026", "status": "completed"},
    "Business Decision Models": {"code": "NCCB 5010 / MBQC 862", "instructor": "Faculty TBD", "term": "Fall 2025", "status": "completed"},
    "Business Strategy": {"code": "NCCB 5090 / MBQC 901", "instructor": "Faculty TBD", "term": "Spring 2026", "status": "in-progress"},
    "Career Development": {"code": "TBD", "instructor": "TBD", "term": "All terms", "status": "active"},
    "Corporate Financial Policy": {"code": "NBAB 5580 / MBQC 822", "instructor": "Steven A. Carvell", "term": "Fall 2026", "status": "in-progress"},
    "Corporate Governance": {"code": "TBD", "instructor": "Adrian Corum", "term": "Fall 2026", "status": "in-progress"},
    "Cornell Management Simulation": {"code": "TBD", "instructor": "Steve Sauer / Tom Schryver", "term": "Fall 2026", "status": "completed"},
    "Critical Thinking for Business Leaders-NBAB 5880": {"code": "NBAB 5880", "instructor": "Risa Mish", "term": "Spring 2026", "status": "completed"},
    "Fintech Innovation & Technology": {"code": "TBD", "instructor": "TBD", "term": "Spring 2026", "status": "completed"},
    "Global Business Project": {"code": "NBAB 5970 / MBQC 907", "instructor": "Shai Dubey", "term": "Spring 2027", "status": "in-progress"},
    "Global Macroeconomics": {"code": "TBD", "instructor": "TBD", "term": "Fall 2025", "status": "completed"},
    "Global Strategy": {"code": "TBD", "instructor": "Michael Sartor", "term": "Fall 2026", "status": "in-progress"},
    "Individual-Project": {"code": "NMI 5001 / MBQC 808", "instructor": "TBD", "term": "Spring 2026", "status": "in-progress"},
    "Investment Banking Essentials": {"code": "TBD", "instructor": "Drew Pascarella", "term": "Fall 2026", "status": "in-progress"},
    "Leadership and High Perf Teams": {"code": "NBAB 6050", "instructor": "Beta Mannix", "term": "Summer 2025", "status": "completed"},
    "Management Accounting": {"code": "TBD", "instructor": "Danny Szpiro", "term": "Summer 2026", "status": "in-progress"},
    "Management Information Systems": {"code": "NBAB 601 / MBQC 917", "instructor": "Salman Mufti", "term": "Fall 2025", "status": "completed"},
    "Managerial Finance": {"code": "NCCB 5060 / MBQC 821", "instructor": "Mao Ye", "term": "Spring 2026", "status": "completed"},
    "Managing Operations": {"code": "NCCB 5080 / MBQC 941", "instructor": "Yao Cui", "term": "Spring 2026", "status": "completed"},
    "Managing, Leading in Org": {"code": "NBCB 5040 / MBQC 851", "instructor": "Goce Andrevski", "term": "Summer 2025", "status": "completed"},
    "Marketing": {"code": "NBCB 5030", "instructor": "Bahriye Goren", "term": "Fall 2025", "status": "completed"},
    "Marketing Strategy": {"code": "NBAB 6220 / MBQC 932", "instructor": "Monica LaBarge", "term": "Summer 2026", "status": "in-progress"},
    "Negotiation": {"code": "NBAB 6660 / MBQC 952", "instructor": "Shai Dubey", "term": "Spring 2026", "status": "completed"},
    "New Venture Management": {"code": "TBD", "instructor": "Elspeth Murray", "term": "Fall 2025", "status": "completed"},
    "Role of the GM": {"code": "NBAB 5630 / MBQC 800", "instructor": "Goce Andrevski", "term": "Summer 2025", "status": "completed"},
    "Strategies for Sustainability": {"code": "TBD", "instructor": "Mark Milstein", "term": "Fall 2026", "status": "upcoming"},
    "Team 1 Files": {"code": "N/A", "instructor": "N/A", "term": "All terms", "status": "completed"},
    "Team 2": {"code": "N/A", "instructor": "N/A", "term": "All terms", "status": "active"},
    "Transformational Leadership": {"code": "TBD", "instructor": "Julian Barling", "term": "Fall 2026", "status": "upcoming"},
    "VC BVR": {"code": "TBD", "instructor": "TBD", "term": "Spring 2026", "status": "completed"},
    "Valuation": {"code": "NBAB 6560 / MBQC 804", "instructor": "Pamela Moulton", "term": "Spring 2026", "status": "completed"},
}

SKIP_DIRS = {"_Flagged", "_Training", "sora_deal_desk"}
# Directories to skip as they're organizational, not courses
EXCLUDE_NAMES = {"Team 1 Files"}

def main():
    courses = []
    seen_names = set()
    for entry in sorted(os.listdir(CLASSES_ROOT)):
        path = os.path.join(CLASSES_ROOT, entry)
        if not os.path.isdir(path) or entry in SKIP_DIRS:
            continue
        # Strip leading/trailing whitespace for lookup (some dirs have leading spaces)
        clean_name = entry.strip()
        if clean_name in EXCLUDE_NAMES:
            continue
        # Skip duplicates (e.g., both " Managerial Finance" and "Managerial Finance")
        if clean_name in seen_names:
            continue
        seen_names.add(clean_name)
        details = COURSE_DETAILS.get(clean_name, {})
        file_count = sum(1 for f in Path(path).rglob("*") if f.is_file() and f.name != ".DS_Store")
        courses.append({
            "name": clean_name,
            "code": details.get("code", "TBD"),
            "instructor": details.get("instructor", "TBD"),
            "term": details.get("term", "TBD"),
            "status": details.get("status", "unknown"),
            "fileCount": file_count,
            "team": details.get("team", "Team 2"),
        })

    # Sort by term order, then by name within each term
    term_order = ["Summer 2025", "Fall 2025", "Spring 2026", "Summer 2026", "Fall 2026", "Spring 2027", "All terms"]
    def sort_key(c):
        t = c["term"]
        idx = term_order.index(t) if t in term_order else len(term_order)
        return (idx, c["name"])
    courses.sort(key=sort_key)

    output = {
        "source": "Generated from /Users/joselfernandezperera/Documents/Cornell/Classes/",
        "generatedAt": datetime.now().isoformat(),
        "cohort": "EMBA Americas 27",
        "totalCourses": len(courses),
        "termOrder": term_order,
        "courses": courses,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "courses.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print("Written {} courses to {}".format(len(courses), out_path))

if __name__ == "__main__":
    main()
