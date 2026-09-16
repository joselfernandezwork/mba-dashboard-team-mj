/* EMBA Americas Dashboard - data-driven view with auth + dynamic API */
const DATA_BASE = '/api/data?type=';
const AUTH_TOKEN = null; // Token managed via cookie by middleware

// ---- Auth-aware data loading ----
async function loadData(endpoint) {
  const res = await fetch(DATA_BASE + endpoint + '&t=' + Date.now(), {
    credentials: 'include',
  });
  if (res.status === 401) {
    // Middleware returned login form — redirect to it
    window.location.href = '/';
    return null;
  }
  if (!res.ok) {
    console.error('Failed to load ' + endpoint + ':', res.statusText);
    return null;
  }
  return res.json();
}

// ---- Search / filter helpers ----
function filterItems(items, query) {
  if (!query) return items;
  const q = query.toLowerCase().trim();
  return items.filter(item => {
    const text = Object.values(item).join(' ').toLowerCase();
    return text.includes(q);
  });
}

function setupSearch(inputId, listId, renderFn, items) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);
  if (!input || !list) return;

  input.addEventListener('input', function () {
    const filtered = filterItems(items, this.value);
    list.innerHTML = renderFn(filtered);
  });

  // Return the current items for external re-render
  return items;
}

// ---- Tab navigation ----
function showTab(tabName) {
  document.querySelectorAll('.tab-content').forEach(el => {
    el.classList.remove('active');
  });
  document.querySelectorAll('.nav-tab').forEach(el => {
    el.classList.remove('active');
  });
  document.getElementById(tabName + '-tab').classList.add('active');
  // Update nav tab active state
  const navTabs = document.querySelectorAll('.nav-tab');
  navTabs.forEach(t => {
    if (t.getAttribute('onclick') && t.getAttribute('onclick').includes("'" + tabName + "'")) {
      t.classList.add('active');
    }
  });
}

// ---- Badge helper ----
function statusBadge(status) {
  const labels = {
    completed: ['Completed', 'badge-blue'],
    in_progress: ['In Progress', 'badge-gold'],
    pending: ['Pending', ''],
    upcoming: ['Upcoming', 'badge-red'],
    active: ['Active', 'badge-gold'],
    submitted: ['Submitted', 'badge-blue'],
    unknown: ['Unknown', ''],
  };
  const [label, cls] = labels[status] || [status || 'Unknown', ''];
  return '<span class="badge ' + cls + '">' + label + '</span>';
}

// ---- Courses ----
let coursesData = null;

function renderCourses(courses) {
  const grid = document.getElementById('courses-grid');
  grid.innerHTML = courses.map(c =>
    '<a href="class.html?course=' + encodeURIComponent(c.name) + '" class="card course-card">' +
    '  <div class="flex-between">' +
    '    <h3>' + c.name + '</h3>' +
    '    ' + statusBadge(c.status) +
    '  </div>' +
    '  <p class="course-code">' + c.code + '</p>' +
    '  <p class="course-instructor">' + c.instructor + '</p>' +
    '  <p class="course-term">' + c.term + ' * ' + c.fileCount + ' files</p>' +
    '</a>'
  ).join('');
}

async function initCourses() {
  const data = await loadData('courses');
  if (!data) return;
  coursesData = data.courses;
  document.getElementById('updated-at').textContent = 'Updated: ' + new Date(data.generatedAt).toLocaleString();
  renderCourses(coursesData);
  setupSearch('courses-search', 'courses-grid', renderCourses, coursesData);
}

// ---- Projects ----
let projectsData = null;

function renderProjects(data) {
  const container = document.getElementById('projects-container');
  let html = '';

  // Individual project
  html += '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Individual Project</h3>';
  const ind = data.individualProjects[0];
  html += '<div class="card" style="margin-bottom: 20px;">' +
    '  <div class="flex-between">' +
    '    <h3>' + ind.name + '</h3>' +
    '    ' + statusBadge('in-progress') +
    '  </div>' +
    '  <p class="course-code">' + ind.course + '</p>' +
    '  <p>' + ind.description + '</p>' +
    '  <p><strong>Status:</strong> ' + ind.status + '</p>' +
    '  <table class="table">' +
    '    <thead><tr><th>Deliverable</th><th>Status</th><th>Due</th></tr></thead>' +
    '    <tbody>' + ind.deliverables.map(d =>
      '      <tr><td>' + d.name + '</td><td>' + d.status + '</td><td>' + (d.dueDate || '-') + '</td></tr>'
    ).join('') +
    '    </tbody>' +
    '  </table>' +
    '</div>';

  // Team projects
  html += '<h3 style="color: var(--queens-blue); margin: 24px 0 12px;">Team Projects</h3>';
  html += '<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px;">';
  const filteredProjects = filterItems(data.teamProjects, document.getElementById('projects-search')?.value || '');
  filteredProjects.forEach(p => {
    html += '<div class="card">' +
      '  <h3>' + p.name + '</h3>' +
      '  <p class="course-code">' + p.courseCode + ' - ' + p.instructor + '</p>' +
      '  <p><strong>Status:</strong> ' + p.status + '</p>';
    if (p.parts) {
      html += '<table class="table" style="font-size: 0.78rem;">' +
        '  <thead><tr><th>Part</th><th>Weight</th><th>Status</th></tr></thead>' +
        '  <tbody>' + p.parts.map(pt =>
          '    <tr><td>' + pt.name + '</td><td>' + pt.weight + '</td><td>' + pt.status + '</td></tr>'
        ).join('') +
        '  </tbody>' +
        '</table>';
    }
    if (p.deliverable) {
      html += '<p><strong>Deliverable:</strong> ' + p.deliverable + '</p>';
    }
    if (p.teamNote) {
      html += '<p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 8px;">' + p.teamNote + '</p>';
    }
    html += '</div>';
  });
  html += '</div>';
  container.innerHTML = html;
}

async function initProjects() {
  const data = await loadData('projects');
  if (!data) return;
  projectsData = data;
  renderProjects(data);
  // Setup search for team projects (re-render on input)
  const searchInput = document.getElementById('projects-search');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      renderProjects(projectsData);
    });
  }
}

// ---- Calendar ----
let calendarData = null;

function renderCalendar(data) {
  const container = document.getElementById('calendar-container');

  // Residencies summary — updated with Kingston and Ithaca split
  let html = '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Residencies</h3>';
  html += '<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; margin-bottom: 24px;">';
  data.residencies.forEach(r => {
    html += '<div class="card" style="text-align: center;">' +
      '  <h4>' + r.name + '</h4>' +
      '  <p style="color: var(--text-secondary);">' + r.location + '</p>' +
      '  <p style="font-size: 0.8rem; color: var(--text-secondary);">' + r.term + '</p>' +
      '</div>';
  });
  html += '</div>';

  // Final onsite details card
  if (data.finalOnsite) {
    const fo = data.finalOnsite;
    html += '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Final Onsite Session — Kingston &amp; Ithaca</h3>';
    html += '<div class="card" style="margin-bottom: 24px;">';
    html += '<p><strong>Dates:</strong> ' + fo.dates + '</p>';
    html += '<p><strong>Locations:</strong> ' + fo.locations + '</p>';
    html += '<p><strong>Lodging:</strong> ' + fo.lodging + '</p>';
    html += '<p><strong>Dress Code:</strong> ' + fo.dressCode + '</p>';
    html += '</div>';
  }

  // Calendar table — filtered by search
  html += '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Full Schedule</h3>';
  html += '<table class="table">';
  html += '<thead><tr><th>Term</th><th>Date</th><th>Day</th><th>AM Course</th><th>PM Course</th><th>Location</th><th>Notes</th></tr></thead><tbody>';

  // Group by term
  const terms = {};
  data.entries.forEach(e => {
    if (!terms[e.term]) terms[e.term] = [];
    terms[e.term].push(e);
  });

  const searchInput = document.getElementById('calendar-search')?.value || '';
  const q = searchInput.toLowerCase().trim();

  Object.entries(terms).forEach(function (item) {
    var term = item[0];
    var entries = item[1];
    var visibleEntries = entries.filter(function (e) {
      if (!q) return true;
      var text = (e.date + ' ' + e.amCourse + ' ' + e.pmCourse + ' ' + (e.location || '') + ' ' + (e.notes || '')).toLowerCase();
      return text.includes(q);
    });
    if (visibleEntries.length === 0) return;
    html += '<tr><td colspan="7" style="background: var(--pale-blue); font-weight: 700; color: var(--queens-blue);">' + term + '</td></tr>';
    entries.forEach(function (e) {
      var visible = true;
      if (q) {
        var text = (e.date + ' ' + e.amCourse + ' ' + e.pmCourse + ' ' + (e.location || '') + ' ' + (e.notes || '')).toLowerCase();
        visible = text.includes(q);
      }
      html += '<tr style="' + (visible ? '' : 'display:none;') + '">' +
        '<td>' + e.date + '</td>' +
        '<td>' + (e.day || '-') + '</td>' +
        '<td>' + e.amCourse + '</td>' +
        '<td>' + e.pmCourse + '</td>' +
        '<td>' + (e.location || '-') + '</td>' +
        '<td>' + (e.notes || '-') + '</td>' +
        '</tr>';
    });
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

async function initCalendar() {
  const data = await loadData('calendar');
  if (!data) return;
  calendarData = data;
  renderCalendar(data);
  // Re-render on search
  const searchInput = document.getElementById('calendar-search');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      renderCalendar(calendarData);
    });
  }
}

// ---- Team ----
let teamData = null;

function renderTeam(data) {
  const container = document.getElementById('team-container');
  let html = '';

  // Team header
  html += '<div class="card" style="margin-bottom: 20px;">' +
    '  <h3>' + data.teamName + ' - ' + data.nickname + '</h3>' +
    '  <p style="color: var(--text-secondary);">Program: ' + data.program + ' * Established: ' + data.established + '</p>' +
    '</div>';

  // Members table
  html += '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Team Members</h3>';
  html += '<table class="table">';
  html += '<thead><tr><th>Name</th><th>Nickname</th><th>Location</th><th>Time Zone</th><th>Email</th></tr></thead><tbody>';
  data.members.forEach(function (m) {
    html += '<tr>' +
      '<td>' + m.name + '</td>' +
      '<td>' + m.nickname + '</td>' +
      '<td>' + m.location + '</td>' +
      '<td>' + m.timeZone + '</td>' +
      '<td><a href="mailto:' + m.email + '">' + m.email + '</a></td>' +
      '</tr>';
  });
  html += '</tbody></table>';

  // Team information
  const ra = data.recentActivity;
  html += '<h3 style="color: var(--queens-blue); margin: 24px 0 12px;">Team Information</h3>';
  html += '<div class="card">' +
    '  <p><strong>Team Change:</strong> ' + (data.teamChangeNote || 'No changes') + '</p>' +
    '  <hr style="margin: 12px 0; border: none; border-top: 1px solid #e5e7eb;">' +
    '  <p><strong>Last Meeting:</strong> ' + ra.lastMeeting + '</p>' +
    '  <p><strong>Agenda:</strong> ' + ra.lastMeetingAgenda + '</p>' +
    '  <p><strong>Standing Meeting:</strong> ' + ra.nextStandingMeeting + '</p>' +
    '  <p><strong>Current Focus:</strong> ' + ra.currentFocus + '</p>' +
    '</div>';

  container.innerHTML = html;
}

async function initTeam() {
  const data = await loadData('team');
  if (!data) return;
  teamData = data;
  renderTeam(data);
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', function () {
  Promise.all([
    initCourses(),
    initProjects(),
    initCalendar(),
    initTeam(),
  ]);
});
