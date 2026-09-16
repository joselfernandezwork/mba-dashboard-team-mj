export default async function middleware(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Allow access without authentication
  const publicPaths = [
    '/api/auth/',
    '/styles/',
    '/scripts/',
    '/assets/',
    '/favicon.svg',
    '/favicon.ico',
  ];

  for (const publicPath of publicPaths) {
    if (path.startsWith(publicPath)) {
      return;
    }
  }

  // Check for auth token cookie
  const cookie = request.headers.get('cookie') || '';
  const match = cookie.match(/(?:^|;\s*)token=([^;]+)/);
  const token = match ? match[1] : null;

  if (token === 'authenticated') {
    return;
  }

  // Return login form for unauthenticated requests
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login - EMBA Americas Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #002452;
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .login-box {
      background: white;
      color: #002452;
      padding: 40px;
      border-radius: 12px;
      width: 100%;
      max-width: 420px;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    .login-box h1 {
      font-size: 1.4rem;
      margin-bottom: 8px;
      color: #002452;
    }
    .login-box p {
      font-size: 0.85rem;
      color: #666;
      margin-bottom: 24px;
    }
    .login-box .cornell-gold {
      color: #B31B1B;
      font-weight: 700;
    }
    input[type="password"] {
      width: 100%;
      padding: 12px 16px;
      margin: 12px 0;
      border: 1px solid #ddd;
      border-radius: 6px;
      font-size: 1rem;
      font-family: inherit;
    }
    button {
      width: 100%;
      padding: 12px;
      background: #002452;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
      transition: background 0.2s;
    }
    select {
      width: 100%;
      padding: 12px 16px;
      margin: 12px 0;
      border: 1px solid #ddd;
      border-radius: 6px;
      font-size: 1rem;
      font-family: inherit;
      background: #f9f9f9;
    }
    button:hover { background: #B31B1B; }
    .error { color: #B31B1B; font-size: 0.85rem; margin-top: 8px; }
  </style>
</head>
<body>
  <div class="login-box">
    <h1>EMBA Americas • TEAM Mj</h1>
    <p>Select your name and enter your password to access the Cornell EMBA Americas (Cohort 27) dashboard.</p>
    <form method="POST" action="/api/auth/login" id="loginForm">
      <select name="name" required autofocus>
        <option value="">Select your name...</option>
        <option value="Jose Luis Fernandez Perera">Jose Luis Fernandez Perera</option>
        <option value="Dr. Marian Hanna">Dr. Marian Hanna</option>
      </select>
      <input type="password" name="password" placeholder="Password" required
             autocomplete="current-password">
      <button type="submit">Access Dashboard</button>
    </form>
  </div>
</body>
</html>`;

  return new Response(html, {
    status: 401,
    headers: {
      'Content-Type': 'text/html',
    },
  });
}
