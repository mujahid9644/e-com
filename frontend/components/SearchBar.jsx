// ============================================
// Search Bar Component
// ============================================
// Search functionality for products

import { useState } from 'react';
import { useRouter } from 'next/router';
import { FiSearch } from 'react-icons/fi';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/products?search=${encodeURIComponent(query)}`);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSearch} className="w-full">
      <div className="relative">
        <input
          type="text"
          placeholder="Search products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full px-4 py-2 pl-10 glass text-slate-100 placeholder-slate-500"
        />
        <button
          type="submit"
          className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-neon-cyan"
        >
          <FiSearch size={18} />
        </button>
      </div>
    </form>
  );
}
