/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: 'https://ghazakshaikh1-to-do-app.hf.space',
  },
  images: {
    unoptimized: true, // Required for Vercel deployment
  },
}

module.exports = nextConfig