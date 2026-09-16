/**
 * User store for TEAM Mj dashboard.
 * Passwords are sourced from Vercel env vars (DASHBOARD_PASSWORD_JOSE,
 * DASHBOARD_PASSWORD_MARIAN).  Fallback values are provided so the
 * dashboard works locally without env vars.
 */
const USERS = [
  {
    id: 'jose',
    name: 'Jose Luis Fernandez Perera',
    email: 'jlf348@cornell.edu',
    envVar: 'DASHBOARD_PASSWORD_JOSE',
    fallback: 'EMBA_Mj_Jose_2026!Secure#Access',
  },
  {
    id: 'marian',
    name: 'Dr. Marian Hanna',
    email: 'mh2635@cornell.edu',
    envVar: 'DASHBOARD_PASSWORD_MARIAN',
    fallback: 'EMBA_Mj_Marian_2026!Secure#Access',
  },
];

/**
 * Validate credentials.
 * Returns the user object on success, null on failure.
 */
function authenticateByName(name, password) {
  if (!name || !password) return null;
  const user = USERS.find(u => u.name === name);
  if (!user) return null;
  const expected = process.env[user.envVar] || user.fallback;
  if (expected === password) {
    return { id: user.id, name: user.name, email: user.email };
  }
  return null;
}

module.exports = { USERS, authenticateByName };
