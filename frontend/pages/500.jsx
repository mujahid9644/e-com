import Link from 'next/link';
import { FiAlertTriangle, FiRefreshCw, FiHome } from 'react-icons/fi';
import Layout from '@/components/Layout';
import { useRouter } from 'next/router';

export default function ServerError() {
  const router = useRouter();

  const handleReload = () => {
    router.reload();
  };

  return (
    <Layout>
      <div className="min-h-screen flex items-center justify-center px-4 py-20">
        <div className="text-center max-w-md">
          {/* Error Icon */}
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-red-500/10 rounded-full">
              <FiAlertTriangle className="text-red-500 text-5xl" />
            </div>
          </div>

          {/* Error Code */}
          <h1 className="text-9xl font-bold text-red-500 mb-4">500</h1>

          {/* Message */}
          <h2 className="text-3xl font-bold text-white mb-2">
            Server Error
          </h2>
          <p className="text-gray-400 mb-8">
            Something went wrong on our end. Our team has been notified and is
            working to fix it. Please try again later.
          </p>

          {/* Error Info */}
          <div className="mb-8 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-left">
            <p className="text-red-300 text-sm mb-2">Error Code:</p>
            <p className="text-red-400 text-xs font-mono break-all">
              {new Date().toISOString()}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col gap-3">
            <button
              onClick={handleReload}
              className="flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition font-medium"
            >
              <FiRefreshCw size={18} />
              Try Again
            </button>

            <Link
              href="/"
              className="flex items-center justify-center gap-2 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition font-medium"
            >
              <FiHome size={18} />
              Go to Home
            </Link>
          </div>

          {/* Support */}
          <p className="text-center text-gray-500 text-sm mt-8">
            Need help?{' '}
            <a href="mailto:support@ecommerce.com" className="text-blue-400 hover:underline">
              Contact Support
            </a>
          </p>
        </div>
      </div>
    </Layout>
  );
}
