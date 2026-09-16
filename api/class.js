const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');

module.exports = (req, res) => {
  // Defense in depth: middleware already checks auth at the edge.
  const cookie = req.headers.cookie || '';
  if (!cookie.includes('token=authenticated')) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const courseName = url.searchParams.get('course') || '';

  if (!courseName) {
    res.status(400).json({ error: 'Course parameter required' });
    return;
  }

  const decoded = decodeURIComponent(courseName);

  // Load courses
  const coursesRaw = fs.readFileSync(path.join(DATA_DIR, 'courses.json'), 'utf-8');
  const coursesData = JSON.parse(coursesRaw);
  const course = coursesData.courses.find(c => c.name === decoded);

  if (!course) {
    res.status(404).json({ error: 'Course not found' });
    return;
  }

  // Load projects and filter to those matching this course
  const projRaw = fs.readFileSync(path.join(DATA_DIR, 'projects.json'), 'utf-8');
  const projData = JSON.parse(projRaw);
  const relatedProjects = projData.projects.filter(p =>
    p.course === decoded || p.courseCode === course.code
  );

  // Build subjects list from course description parts
  const subjects = course.description
    ? course.description.split(/\. |\n/).filter(s => s.trim().length > 10).map(s => s.trim())
    : [];

  res.status(200).json({
    course: course,
    subjects: subjects,
    projects: relatedProjects,
  });
};
