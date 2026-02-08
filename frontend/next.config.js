/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Required for GitHub Pages
  trailingSlash: true, // Optional: adds trailing slashes to URLs
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