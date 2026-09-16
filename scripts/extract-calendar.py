#!/usr/bin/env python3
"""Extract cohort 27 calendar data from schedule Excel.

Parses the 'Class of 27' sheet from the schedule Excel file.
The sheet uses merged cells, causing column alignment to vary between rows.
This parser tracks state (term, month, year, location) across rows and
reconstructs dates using month/year markers and day-number rollover detection.
"""
import openpyxl
import json
import os
from datetime import datetime, date

SCHEDULE_FILE = "/Users/joselfernandezperera/Documents/Cornell/Administration/Schedule/EMBAA+Co27+course+schedule_7.17.26.xlsx"

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
MONTH_LOOKUP = {m.lower(): i + 1 for i, m in enumerate(MONTH_NAMES)}

TERM_MONTH_YEAR = {
    "SUMMER 25 TERM": ("Summer 2025", 6, 2025),
    "FALL 25 TERM": ("Fall 2025", 8, 2025),
    "SPRING 26 TERM": ("Spring 2026", 1, 2026),
    "SUMMER 26 TERM": ("Summer 2026", 6, 2026),
    "FALL 26 TERM": ("Fall 2026", 8, 2026),
}

LOCATION_MAP = {
    "CORNELL": "Cornell",
    "TORONTO": "Toronto",
    "NEW YORK CITY": "New York City",
    "QUEEN'S/CORNELL": "Queen's/Cornell",
    "KINGSTON": "Kingston (Queen's)",
    "ITHACA": "Ithaca (Cornell)",
    "Class at Cornell": "Cornell",
}

WEEKDAYS = {"Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}


def is_day_number(val):
    if isinstance(val, int) and 1 <= val <= 31:
        return True
    if isinstance(val, str):
        try:
            n = int(val.strip())
            return 1 <= n <= 31
        except ValueError:
            return False
    return False


def to_day_number(val):
    if isinstance(val, int):
        return val
    return int(val.strip())


def check_month(val):
    if not val:
        return None
    s = val.strip().rstrip()
    for m in MONTH_NAMES:
        if s.lower() == m.lower():
            return MONTH_LOOKUP[m.lower()]
    return None


def check_year(val):
    if not val:
        return None
    s = str(val).strip()
    if len(s) == 4 and s.isdigit() and s.startswith("20"):
        return int(s)
    return None


def check_location(val):
    if not val:
        return None
    s = val.strip()
    if s in LOCATION_MAP:
        return LOCATION_MAP[s]
    return None


def advance_month(month_num, year_num):
    """Advance 1-indexed month by one, handling year rollover."""
    next_month = month_num + 1
    next_year = year_num
    if next_month > 12:
        next_month = 1
        next_year += 1
    return next_month, next_year


def main():
    wb = openpyxl.load_workbook(SCHEDULE_FILE, data_only=True)
    ws = wb["Class of 27"]

    entries = []
    current_term = None
    current_month = None
    current_year = None
    current_location = None
    last_day = 0

    SKIP_COL1_VALUES = {"Opening  Onsite Session"}

    for row in ws.iter_rows(min_row=5, values_only=True):
        if not row or all(v is None for v in row):
            continue

        col0 = str(row[0]).strip() if row[0] else ""
        col1 = row[1]
        col2 = row[2]
        col3 = row[3]
        col4 = row[4]
        col5 = str(row[5]).strip() if row[5] else ""
        col6 = str(row[6]).strip() if row[6] else ""
        col7 = str(row[7]).strip() if row[7] else ""
        col8 = str(row[8]).strip() if row[8] else ""

        col1_str = str(col1).strip() if col1 else ""

        # --- Skip section headers and special rows ---
        if col1_str in SKIP_COL1_VALUES:
            continue
        if col1_str:
            lower = col1_str.lower()
            if "onsite session" in lower:
                if "final" in lower:
                    current_location = "Queen's/Cornell"
                elif "2nd" in lower:
                    current_location = "Toronto"
                elif "3rd" in lower:
                    current_location = "New York City"
                else:
                    current_location = "Cornell"
                continue
            if "videoconferencing" in lower or "videoconf" in lower:
                current_location = "Video Conferencing"
                continue
            if col1_str == "Class Dates":
                continue
            if col1_str in ("Final Onsite Session", "Final VIDEOCONFERENCING BLOCK"):
                current_location = "Video Conferencing"
                continue
            if col1_str == "Opening":
                continue

        # --- Term headers ---
        if col1_str in TERM_MONTH_YEAR:
            term_label, month_num, year = TERM_MONTH_YEAR[col1_str]
            current_term = term_label
            current_month = month_num
            current_year = year
            last_day = 0
            continue

        # --- Month/year/location markers in col1 ---
        if col1_str:
            m = check_month(col1_str)
            if m is not None:
                current_month = m
                continue
            y = check_year(col1_str)
            if y is not None:
                current_year = y
                continue
            loc = check_location(col1_str)
            if loc is not None:
                current_location = loc
                continue
            # col1 has a non-marker value -- skip
            continue

        # --- Data row: extract day number or datetime from col2/col3 ---
        day_num = None
        date_value = None
        location_override = current_location
        weekday = None
        group = ""

        if is_day_number(col2):
            day_num = to_day_number(col2)
            if col3 is not None:
                c3 = str(col3).strip()
                if c3 in WEEKDAYS:
                    weekday = c3
                else:
                    loc = check_location(c3)
                    if loc is not None:
                        location_override = loc
            if col4 is not None:
                group = str(col4).strip()
        elif isinstance(col2, datetime):
            date_value = col2
            if col3 is not None:
                c3 = str(col3).strip()
                if c3 in WEEKDAYS:
                    weekday = c3
                else:
                    loc = check_location(c3)
                    if loc is not None:
                        location_override = loc
            if col4 is not None:
                group = str(col4).strip()
        elif isinstance(col3, datetime):
            # GBP row where col2 is "GBP" string
            date_value = col3
            if col4 is not None:
                c4 = str(col4).strip()
                if c4 in WEEKDAYS:
                    weekday = c4
            if col5 is not None:
                group = str(col5).strip()
        else:
            continue

        if day_num is None and date_value is None:
            continue

        # Advance month if day number rolled over
        if day_num is not None and day_num < last_day and current_month is not None and current_year is not None:
            current_month, current_year = advance_month(current_month, current_year)

        # Build date string
        if date_value is not None:
            year_override = current_year if current_year else date_value.year
            actual_date = date(year_override, date_value.month, date_value.day)
            date_str = actual_date.strftime("%Y-%m-%d")
            day_name = actual_date.strftime("%A")
            if weekday is None:
                weekday = day_name
            current_month = date_value.month
            current_year = year_override
            last_day = date_value.day
        else:
            if current_month is None or current_year is None:
                continue
            actual_date = date(current_year, current_month, day_num)
            date_str = actual_date.strftime("%Y-%m-%d")
            day_name = actual_date.strftime("%A")
            if weekday is None:
                weekday = day_name
            last_day = day_num

        # Skip rows without actual course data
        am_course = col5
        pm_course = col7
        skip_words = {"", "N/A", "Departure", "Departure Day", "Arrival Day", "Arrival"}
        has_course = am_course not in skip_words or pm_course not in skip_words
        if not has_course:
            continue

        # Collect notes
        notes_parts = []
        if col6 and col6 not in ("", " ", "TEAM ME"):
            notes_parts.append(col6)
        if col8 and col8 not in ("", " ", "NOTES"):
            notes_parts.append(col8)
        notes = " ".join(notes_parts)

        entry = {
            "term": current_term or "Unknown",
            "date": date_str,
            "weekday": weekday or day_name,
            "location": location_override or "Unknown",
            "group": group,
            "amCourse": am_course,
            "pmCourse": pm_course,
            "notes": notes,
        }
        entries.append(entry)

    output = {
        "source": SCHEDULE_FILE,
        "sheet": "Class of 27",
        "generatedAt": datetime.now().isoformat(),
        "cohort": "EMBA Americas 27",
        "totalEntries": len(entries),
        "terms": ["Summer 2025", "Fall 2025", "Spring 2026", "Summer 2026", "Fall 2026"],
        "residencies": [
            {"name": "Opening Onsite", "location": "Cornell", "term": "Summer 2025"},
            {"name": "Toronto Residency", "location": "Toronto", "term": "Fall 2025"},
            {"name": "NYC Residency", "location": "New York City", "term": "Spring 2026"},
            {"name": "Final Onsite: Kingston", "location": "Kingston (Queen's)", "term": "Fall 2026"},
            {"name": "Final Onsite: Ithaca", "location": "Ithaca (Cornell)", "term": "Fall 2026"},
        ],
        "finalOnsite": {
            "dates": "Friday, October 30 - Sunday, November 8, 2026",
            "locations": "Kingston (Queen's University) then Ithaca (Cornell University)",
            "lodging": "Delta Hotels Kingston Waterfront (Kingston); Statler Hotel / Ithaca Commons (Ithaca)",
            "dressCode": "Business casual (business attire required for formal dinner on November 7)",
            "travelNotes": "Depart Cornell Oct 30 at 1:00 p.m. EDT (bus picks up Syracuse Airport 2:30 p.m.). Return Nov 8 at ~7:00 a.m. EDT from Ithaca (stops Syracuse Airport 8:30 a.m.).",
            "source": "Canvas announcement emails from Executive MBA Americas Resources 27 (July 6 and August 28, 2026)"
        },
        "entries": entries,
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "calendar.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print("Written {} calendar entries to {}".format(len(entries), out_path))

if __name__ == "__main__":
    main()
