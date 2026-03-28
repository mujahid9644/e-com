import Link from 'next/link';
import { FiArrowLeft, FiHome, FiSearch } from 'react-icons/fi';
import Layout from '@/components/Layout';

export default function NotFound() {
  return (
    <Layout>
      <div className="min-h-screen flex items-center justify-center px-4 py-20">
        <div className="text-center max-w-md">
          {/* 404 Text */}
          <h1 className="text-9xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent mb-4">
            404
          </h1>

          {/* Message */}
          <h2 className="text-3xl font-bold text-white mb-2">
            Page Not Found
          </h2>
          <p className="text-gray-400 mb-8">
            Sorry, the page you&apos;re looking for doesn&apos;t exist or has been moved.
          </p>

          {/* Search Suggestion */}
          <div className="mb-8 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <p className="text-blue-300 text-sm mb-3">
              Here are some helpful links:
            </p>
            <div className="flex flex-col gap-2">
              <Link
                href="/products"
                className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
              >
                <FiSearch size={18} />
                Browse Products
              </Link>
              <Link
                href="/"
                className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
              >
                <FiHome size={18} />
                Go to Home
              </Link>
            </div>
          </div>

          {/* Back Button */}
          <button
            onClick={() => window.history.back()}
            className="flex items-center justify-center gap-2 px-4 py-2 text-gray-400 hover:text-white transition"
          >
            <FiArrowLeft size={18} />
            Go Back
          </button>
        </div>
      </div>
    </Layout>
  );
}
