// ============================================
// Next.js Configuration
// ============================================
// Configuration for the Next.js application

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for development
  reactStrictMode: true,

  // Image optimization
  images: {
    unoptimized: true, // For static export
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        hostname: 'yourdomain.com',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
        pathname: '/**',
      },
    ],
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },

  // Trailing slashes
  trailingSlash: false,

  // SWR Config for data fetching
  swcMinify: true,

  // ESLint
  eslint: {
    ignoreDuringBuilds: false,
  },

  // Allow build with warnings
  typescript: {
    ignoreBuildErrors: false,
  },
};

module.exports = nextConfig;
