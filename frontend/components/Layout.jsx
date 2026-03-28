// ============================================
// Layout Component
// ============================================
// Main layout wrapper for all pages

import Header from './Header';
import Footer from './Footer';
import WhatsAppButton from './WhatsAppButton';
import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export default function Layout({ children }) {
  const { initAuth } = useAuthStore();

  useEffect(() => {
    // Initialize auth from localStorage
    initAuth();
  }, [initAuth]);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header Navigation */}
      <Header />

      {/* Main Content */}
      <main className="flex-grow">
        {children}
      </main>

      {/* Footer */}
      <Footer />

      {/* WhatsApp Button */}
      <WhatsAppButton />
    </div>
  );
}
