const PASSWORD = process.env.DASHBOARD_PASSWORD || 'emba2026';

module.exports = (req, res) => {
  if (req.method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      const params = new URLSearchParams(body);
      const password = params.get('password');

      if (password && password === PASSWORD) {
        res.writeHead(302, {
          'Set-Cookie': 'token=authenticated; HttpOnly; SameSite=Lax; Path=/; Max-Age=86400',
          'Location': '/',
          'Content-Type': 'text/html',
        });
        res.end('Redirecting to dashboard...');
      } else {
        res.writeHead(401, { 'Content-Type': 'text/html' });
        res.end(`
          <!DOCTYPE html>
          <html>
          <head><title>Invalid Password</title></head>
          <body style="font-family: -apple-system, sans-serif; background: #002452; color: white; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="background: white; padding: 40px; border-radius: 12px; max-width: 420px; text-align: center;">
              <h1 style="color: #B31B1B;">Invalid Password</h1>
              <p style="color: #666; margin: 12px 0;">Please try again.</p>
              <a href="/" style="display: inline-block; padding: 10px 24px; background: #002452; color: white; text-decoration: none; border-radius: 6px;">Back</a>
            </div>
          </body>
          </html>
        `);
      }
    });
  } else {
    res.writeHead(405, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Method not allowed' }));
  }
};
