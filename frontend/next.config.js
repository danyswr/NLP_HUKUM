/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  allowedDevOrigins: [
    'localhost',
    '127.0.0.1',
    '*.replit.dev',
    '*.repl.co',
    '*.pike.replit.dev',
  ],
};

module.exports = nextConfig;
