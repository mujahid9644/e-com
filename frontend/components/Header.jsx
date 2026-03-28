// ============================================
// Header / Navigation Component
// ============================================
// Main navigation header with glassmorphism

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { FiSearch, FiShoppingCart, FiHeart, FiUser, FiMenu, FiX } from 'react-icons/fi';
import { useAuthStore } from '../store/authStore';
import { useCartStore } from '../store/cartStore';
import { useWishlistStore } from '../store/wishlistStore';
import SearchBar from './SearchBar';

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuthStore();
  const { totalItems, fetchCart } = useCartStore();
  const { count: wishlistCount, fetchWishlist } = useWishlistStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart();
      fetchWishlist();
    }
  }, [isAuthenticated, fetchCart, fetchWishlist]);

  return (
    <header className="sticky top-0 z-50 glass-dark border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-lg bg-gradient-neon flex items-center justify-center">
              <span className="text-white font-bold text-lg">E</span>
            </div>
            <span className="hidden sm:inline font-bold text-xl gradient-text">
              ECommerceHub
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-slate-300 hover:text-neon-cyan transition-smooth">
              Home
            </Link>
            <Link href="/products" className="text-slate-300 hover:text-neon-cyan transition-smooth">
              Products
            </Link>
            <Link href="/categories" className="text-slate-300 hover:text-neon-cyan transition-smooth">
              Categories
            </Link>
            <Link href="/about" className="text-slate-300 hover:text-neon-cyan transition-smooth">
              About
            </Link>
            <Link href="/contact" className="text-slate-300 hover:text-neon-cyan transition-smooth">
              Contact
            </Link>
          </nav>

          {/* Right Icons */}
          <div className="flex items-center gap-4">
            {/* Search - Desktop */}
            <button
              onClick={() => setIsSearchOpen(!isSearchOpen)}
              className="hidden sm:flex text-slate-300 hover:text-neon-cyan transition-smooth"
            >
              <FiSearch size={20} />
            </button>

            {/* Cart */}
            <Link
              href="/cart"
              className="relative text-slate-300 hover:text-neon-cyan transition-smooth"
            >
              <FiShoppingCart size={20} />
              {totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-gradient-neon text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>

            {/* Wishlist */}
            <Link
              href="/wishlist"
              className="relative text-slate-300 hover:text-neon-cyan transition-smooth hidden sm:block"
            >
              <FiHeart size={20} />
              {wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-gradient-neon text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>

            {/* User Menu */}
            {isAuthenticated ? (
              <div className="relative group hidden sm:block">
                <button className="flex items-center gap-2 text-slate-300 hover:text-neon-cyan transition-smooth">
                  <FiUser size={20} />
                  <span className="text-sm">{user?.username}</span>
                </button>
                {/* Dropdown */}
                <div className="absolute right-0 mt-0 w-48 glass rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                  <Link
                    href="/dashboard"
                    className="block px-4 py-2 text-sm hover:bg-white/10 first:rounded-t-lg"
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/profile"
                    className="block px-4 py-2 text-sm hover:bg-white/10"
                  >
                    Profile
                  </Link>
                  <Link
                    href="/orders"
                    className="block px-4 py-2 text-sm hover:bg-white/10"
                  >
                    My Orders
                  </Link>
                  <button
                    onClick={logout}
                    className="w-full text-left px-4 py-2 text-sm hover:bg-white/10 last:rounded-b-lg text-red-400"
                  >
                    Logout
                  </button>
                </div>
              </div>
            ) : (
              <Link href="/login" className="hidden sm:block text-slate-300 hover:text-neon-cyan transition-smooth">
                <FiUser size={20} />
              </Link>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden text-slate-300 hover:text-neon-cyan"
            >
              {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>

        {/* Search Bar - Desktop */}
        {isSearchOpen && (
          <div className="pb-4">
            <SearchBar />
          </div>
        )}

        {/* Mobile Menu */}
        {isOpen && (
          <nav className="md:hidden pb-4 space-y-2">
            <Link href="/" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              Home
            </Link>
            <Link href="/products" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              Products
            </Link>
            <Link href="/categories" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              Categories
            </Link>
            <Link href="/about" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              About
            </Link>
            <Link href="/contact" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              Contact
            </Link>
            <Link href="/faq" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
              FAQ
            </Link>
            {isAuthenticated && (
              <>
                <Link href="/dashboard" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
                  Dashboard
                </Link>
                <button
                  onClick={logout}
                  className="w-full text-left px-4 py-2 hover:bg-white/10 rounded-lg text-red-400"
                >
                  Logout
                </button>
              </>
            )}
            {!isAuthenticated && (
              <Link href="/login" className="block px-4 py-2 hover:bg-white/10 rounded-lg text-slate-300 hover:text-neon-cyan transition-smooth">
                Login
              </Link>
            )}
          </nav>
        )}
      </div>
    </header>
  );
}
