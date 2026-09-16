/* Test: verify dashboard data files are valid and contain expected content */
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const errors = [];

function check(condition, message) {
  if (!condition) errors.push(message);
}

// Check courses.json
const coursesRaw = fs.readFileSync(path.join(DATA_DIR, 'courses.json'), 'utf8');
const courses = JSON.parse(coursesRaw);
check(courses.totalCourses >= 20, `Expected >=20 courses, got ${courses.totalCourses}`);
check(courses.cohort === 'EMBA Americas 27', `Wrong cohort: ${courses.cohort}`);

// Check calendar.json
const calRaw = fs.readFileSync(path.join(DATA_DIR, 'calendar.json'), 'utf8');
const cal = JSON.parse(calRaw);
check(cal.totalEntries >= 30, `Expected >=30 calendar entries, got ${cal.totalEntries}`);
check(cal.residencies.length === 5, `Expected 5 residencies, got ${cal.residencies.length}`);

// Check projects.json
const projRaw = fs.readFileSync(path.join(DATA_DIR, 'projects.json'), 'utf8');
const proj = JSON.parse(projRaw);
check(proj.totalProjects >= 7, `Expected >=7 projects, got ${proj.totalProjects}`);
check(proj.individualProjects.length === 1, `Expected 1 individual project`);
check(proj.teamProjects.length >= 6, `Expected >=6 team projects`);

// Check team.json
const teamRaw = fs.readFileSync(path.join(DATA_DIR, 'team.json'), 'utf8');
const team = JSON.parse(teamRaw);
check(team.members.length === 2, `Expected 2 team members, got ${team.members.length}`);

if (errors.length > 0) {
  console.error('FAIL:');
  errors.forEach(e => console.error('  - ' + e));
  process.exit(1);
} else {
  console.log('PASS: All dashboard data files are valid.');
}
