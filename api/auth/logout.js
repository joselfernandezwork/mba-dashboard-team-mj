module.exports = (req, res) => {
  res.writeHead(302, {
    'Set-Cookie': 'token=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0',
    'Location': '/',
    'Content-Type': 'text/html',
  });
  res.end('Logged out. <a href="/">Return to login</a>');
};
