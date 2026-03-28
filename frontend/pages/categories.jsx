// ============================================
// CATEGORIES PAGE
// ============================================

import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { motion } from 'framer-motion';
import Link from 'next/link';
import Image from 'next/image';
import { FiArrowRight, FiGrid, FiList } from 'react-icons/fi';
import apiClient, { endpoints } from '../utils/api';

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await apiClient.get(endpoints.products.categories);

        // Django Rest Framework এর ডাটা ফরম্যাট চেক করা হচ্ছে
        if (Array.isArray(response.data)) {
          setCategories(response.data);
        } else if (response.data && Array.isArray(response.data.results)) {
          setCategories(response.data.results);
        } else {
          setCategories([]);
        }
      } catch (error) {
        console.error('Failed to fetch categories:', error);
        setCategories([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900">
        <div className="space-y-12">
          {/* Hero Section */}
          <motion.section
            className="py-16 md:py-20 px-4 text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="max-w-4xl mx-auto space-y-6">
              <h1 className="gradient-text text-4xl md:text-5xl font-extrabold ">
                Shop by Category
              </h1>
              <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto">
                Explore our comprehensive collection of products organized by category
              </p>
            </div>
          </motion.section>

          {/* Main Content */}
          <motion.div
            className="max-w-7xl mx-auto px-4 pb-20"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Controls */}
            <div className="flex items-center justify-between mb-12 flex-wrap gap-4">
              <div>
                <h2 className="text-2xl md:text-3xl font-bold text-slate-100">All Categories</h2>
                <p className="text-slate-400 mt-1">
                  {Array.isArray(categories) ? categories.length : 0} categories available
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-3 rounded-lg transition-all duration-200 ${
                    viewMode === 'grid'
                      ? 'bg-white/20 backdrop-blur-md border border-white/30 text-white'
                      : 'bg-white/10 backdrop-blur-md border border-white/20 text-slate-300 hover:bg-white/15'
                  }`}
                >
                  <FiGrid size={20} />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-3 rounded-lg transition-all duration-200 ${
                    viewMode === 'list'
                      ? 'bg-white/20 backdrop-blur-md border border-white/30 text-white'
                      : 'bg-white/10 backdrop-blur-md border border-white/20 text-slate-300 hover:bg-white/15'
                  }`}
                >
                  <FiList size={20} />
                </button>
              </div>
            </div>

            {/* Categories Grid */}
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="bg-white/10 backdrop-blur-md border border-white/20 h-64 rounded-2xl animate-pulse"
                  />
                ))}
              </div>
            ) : (
              <div
                className={`grid gap-6 ${
                  viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'
                }`}
              >
                {/* নিরাপদভাবে Map করা হচ্ছে */}
                {Array.isArray(categories) && categories.map((category, index) => (
                  <motion.div
                    key={category.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.05 }}
                    whileHover={{ y: -8, scale: 1.02 }}
                    className="h-full"
                  >
                    <Link href={`/products?category=${category.id}`}>
                      <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl overflow-hidden group cursor-pointer h-full hover:bg-white/15 hover:border-white/30 transition-all duration-300 shadow-lg hover:shadow-xl">
                        <div className="relative h-48 overflow-hidden bg-gradient-to-br from-blue-500/10 to-purple-500/10">
                          <Image
                            src={category.image || '/images/placeholder-product.jpg'}
                            alt={category.name}
                            fill
                            className="object-cover group-hover:scale-110 transition-transform duration-500"
                            onError={(e) => {
                              e.target.src = '/images/placeholder-product.jpg';
                            }}
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-6">
                            <h3 className="text-xl md:text-2xl font-bold text-white drop-shadow-lg">
                              {category.name}
                            </h3>
                          </div>
                        </div>
                        <div className="p-6 space-y-4">
                          <p className="text-slate-400 text-sm md:text-base">
                            {category.description || 'Explore our collection in this category'}
                          </p>
                          <div className="flex items-center justify-between">
                            <span className="text-slate-400 text-sm">
                              {category.product_count || 0} products
                            </span>
                            <FiArrowRight className="text-cyan-400 group-hover:translate-x-2 transition-transform duration-200" />
                          </div>
                        </div>
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </div>
            )}

            {/* Empty State */}
            {!isLoading && (!categories || categories.length === 0) && (
              <motion.div
                className="text-center py-20"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div className="text-6xl mb-4">📁</div>
                <h3 className="text-2xl font-bold text-slate-100 mb-2">No categories found</h3>
                <p className="text-slate-400 mb-8">
                  Please check back later or visit our products page
                </p>
                <Link
                  href="/products"
                  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all inline-flex items-center gap-2 shadow-lg hover:shadow-xl"
                >
                  Browse All Products
                  <FiArrowRight />
                </Link>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </Layout>
  );
}