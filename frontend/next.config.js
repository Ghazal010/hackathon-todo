/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: 'https://ghazakshaikh1-to-do-app.hf.space',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://ghazakshaikh1-to-do-app.hf.space/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig