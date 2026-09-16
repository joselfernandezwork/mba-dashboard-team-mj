/* EMBA Americas Dashboard - data-driven view */
const DATA_BASE = '/data/';

async function loadData(endpoint) {
  const res = await fetch(DATA_BASE + endpoint + '?t=' + Date.now());
  return res.json();
}

function showTab(tabName) {
  document.querySelectorAll('.tab-content').forEach(el => {
    el.classList.remove('active');
  });
  document.querySelectorAll('.nav-tab').forEach(el => {
    el.classList.remove('active');
  });
  document.getElementById(tabName + '-tab').classList.add('active');
  document.querySelector('[onclick="showTab(\'' + tabName + '\')"]').classList.add('active');
}

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
  const [label, cls] = labels[status] || [status, ''];
  return '<span class="badge ' + cls + '">' + label + '</span>';
}

async function initCourses() {
  const data = await loadData('courses.json');
  document.getElementById('updated-at').textContent = new Date(data.generatedAt).toLocaleString();
  const grid = document.getElementById('courses-grid');
  grid.innerHTML = data.courses.map(c =>
    '<div class="card course-card">' +
    '  <div class="flex-between">' +
    '    <h3>' + c.name + '</h3>' +
    '    ' + statusBadge(c.status) +
    '  </div>' +
    '  <p class="course-code">' + c.code + '</p>' +
    '  <p class="course-instructor">' + c.instructor + '</p>' +
    '  <p class="course-term">' + c.term + ' * ' + c.fileCount + ' files</p>' +
    '</div>'
  ).join('');
}

async function initProjects() {
  const data = await loadData('projects.json');
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
  data.teamProjects.forEach(p => {
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

async function initCalendar() {
  const data = await loadData('calendar.json');
  const container = document.getElementById('calendar-container');

  // Residencies summary
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

  // Calendar table
  html += '<h3 style="color: var(--queens-blue); margin-bottom: 12px;">Full Schedule</h3>';
  html += '<table class="table">';
  html += '<thead><tr><th>Term</th><th>Date</th><th>Day</th><th>AM Course</th><th>PM Course</th><th>Notes</th></tr></thead><tbody>';

  // Group by term
  const terms = {};
  data.entries.forEach(e => {
    if (!terms[e.term]) terms[e.term] = [];
    terms[e.term].push(e);
  });

  Object.entries(terms).forEach(function(item) {
    var term = item[0];
    var entries = item[1];
    html += '<tr><td colspan="6" style="background: var(--pale-blue); font-weight: 700; color: var(--queens-blue);">' + term + '</td></tr>';
    entries.forEach(function(e) {
      html += '<tr>' +
        '<td></td>' +
        '<td>' + e.date + '</td>' +
        '<td>' + (e.day || '-') + '</td>' +
        '<td>' + e.amCourse + '</td>' +
        '<td>' + e.pmCourse + '</td>' +
        '<td>' + (e.notes || '-') + '</td>' +
        '</tr>';
    });
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

async function initTeam() {
  const data = await loadData('team.json');
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
  data.members.forEach(function(m) {
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

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  Promise.all([initCourses(), initProjects(), initCalendar(), initTeam()]);
});
