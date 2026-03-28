import { useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import { useAuthStore } from '@/store/authStore';

export default function Dashboard() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <p className="text-white">Redirecting to login...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen p-6">
        <div className="max-w-3xl mx-auto bg-gray-900/70 border border-white/10 rounded-xl p-8">
          <h1 className="text-2xl font-bold text-white mb-4">Your Dashboard</h1>
          <p className="text-gray-300 mb-6">
            Welcome back, <strong>{user?.first_name || user?.username}</strong>!
          </p>

          <div className="space-y-3 text-gray-200">
            <p>
              <span className="font-semibold text-white">Email:</span> {user?.email}
            </p>
            <p>
              <span className="font-semibold text-white">Username:</span> {user?.username}
            </p>
            <p>
              <span className="font-semibold text-white">Registered:</span> {new Date(user?.created_at).toLocaleDateString()}
            </p>
          </div>

          {user?.is_staff && (
            <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <p className="text-sm text-blue-200 mb-2">Admin access granted.</p>
              <Link href="/admin" className="text-sm text-blue-400 hover:text-blue-300">
                Go to Django Admin Panel
              </Link>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
