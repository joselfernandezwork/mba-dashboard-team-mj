const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');

const FILE_MAP = {
  team: 'team.json',
  courses: 'courses.json',
  calendar: 'calendar.json',
  projects: 'projects.json',
};

module.exports = (req, res) => {
  if (req.method !== 'GET') {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  const url = new URL(req.url, 'http://localhost');
  const dataType = url.searchParams.get('type');

  const file = FILE_MAP[dataType];

  if (!file) {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Invalid or missing ?type= parameter. Use: team, courses, calendar, projects' }));
    return;
  }

  try {
    const dataPath = path.join(DATA_DIR, file);
    const content = fs.readFileSync(dataPath, 'utf-8');
    const parsed = JSON.parse(content);

    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=300, stale-while-revalidate=60',
    });
    res.end(JSON.stringify(parsed));
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Failed to load data' }));
  }
};
