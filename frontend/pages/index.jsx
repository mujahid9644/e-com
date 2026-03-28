// ============================================
// HOME PAGE
// ============================================
// Premium home page with video hero section, featured products, and categories

import { SkeletonGrid } from '../components/Skeleton';
import Link from 'next/link';
import Image from 'next/image';
import Layout from '../components/Layout';
import ProductCard from '../components/ProductCard';
import { useState, useEffect } from 'react';
import apiClient, { endpoints } from '../utils/api';
import { motion } from 'framer-motion';
import { FiArrowRight } from 'react-icons/fi';

// Video Hero Section Component
function VideoHeroSection() {
  return (
    <motion.div
      className="relative w-full h-screen overflow-hidden"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      {/* 🎥 Background Video */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute w-full h-full object-cover"
      >
        <source src="/home_Page_video.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* 🌑 Dark Overlay with Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/50 to-slate-900/80"></div>

      {/* ✨ Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-center text-white px-4">
        <motion.div
          className="max-w-3xl mx-auto space-y-6"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <h1 className="text-5xl md:text-7xl font-bold leading-tight">
            Welcome to
            <br />
            <span className="gradient-text">Smart Commerce BD</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-200">
            Shop Smart, Live Better
          </p>

          <motion.div
            className="flex gap-4 justify-center flex-wrap pt-4"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Link href="/products" className="gradient-button inline-flex items-center gap-2 group">
              Shop Now
              <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="/about" className="glass px-8 py-3 font-semibold rounded-lg hover:bg-white/15 transition-smooth">
              Learn More
            </Link>
          </motion.div>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-20"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-6 h-10 border-2 border-white/40 rounded-full flex items-start justify-center p-2">
          <motion.div
            className="w-1 h-2 bg-white rounded-full"
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
        </div>
      </motion.div>
    </motion.div>
  );
}
// Featured Products Section
function FeaturedProducts() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      try {
        const response = await apiClient.get(endpoints.products.featured);
        setProducts(response.data);
      } catch (error) {
        console.error('Failed to fetch featured products:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFeaturedProducts();
  }, []);

  return (
    <motion.section
      className="py-20"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between mb-16 gap-8">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-3">Featured Products</h2>
            <p className="text-slate-400 text-lg">Handpicked selection of our best sellers</p>
          </div>
          <Link href="/products" className="hidden sm:flex items-center gap-2 text-neon-cyan hover:text-white transition-colors text-lg">
            View All
            <FiArrowRight size={24} />
          </Link>
        </div>

        {isLoading ? (
          <SkeletonGrid count={8} />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
              >
                <ProductCard product={product} />
              </motion.div>
            ))}
          </div>
        )}

        <div className="mt-12 sm:hidden text-center">
          <Link href="/products" className="gradient-button inline-flex items-center gap-2">
            View All Products
            <FiArrowRight size={20} />
          </Link>
        </div>
      </div>
    </motion.section>
  );
}

// Categories Section
function CategoriesSection() {
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await apiClient.get(endpoints.products.categories);
        setCategories(response.data.slice(0, 6)); // Show top 6
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return (
    <motion.section
      className="py-20 bg-gradient-to-r from-slate-900/50 via-transparent to-slate-800/50"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-4xl md:text-5xl font-bold text-center text-slate-100 mb-16">
          Shop by <span className="gradient-text">Category</span>
        </h2>

        {isLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="glass h-40 animate-pulse rounded-2xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {categories.map((category, index) => (
              <motion.div
                key={category.id}
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <Link
                  href={`/products?category=${category.id}`}
                  className="glass-hover p-4 text-center group h-full flex flex-col items-center justify-center rounded-2xl"
                >
                  {category.image && (
                    <div className="mb-3 h-20 w-full overflow-hidden rounded-lg">
                      <Image
                        src={category.image}
                        alt={category.name}
                        width={80}
                        height={80}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    </div>
                  )}
                  <h3 className="font-semibold text-slate-100 group-hover:text-neon-cyan transition-colors text-sm md:text-base">
                    {category.name}
                  </h3>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </motion.section>
  );
}

// Stats Section
function StatsSection() {
  const stats = [
    { number: '50K+', label: 'Products' },
    { number: '100K+', label: 'Happy Customers' },
    { number: '24/7', label: 'Support' },
    { number: '99%', label: 'Satisfaction' },
  ];

  return (
    <motion.section
      className="py-20"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              className="glass p-6 md:p-8 text-center rounded-2xl group hover:bg-white/15 transition-all"
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              whileInView={{ opacity: 1, scale: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
            >
              <div className="text-3xl md:text-5xl font-bold gradient-text mb-2">
                {stat.number}
              </div>
              <div className="text-slate-400 text-sm md:text-base">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.section>
  );
}

// CTA Section
function CTASection() {
  return (
    <motion.section
      className="py-20"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          className="glass-dark rounded-3xl overflow-hidden"
          whileHover={{ borderColor: 'rgba(255, 255, 255, 0.3)' }}
        >
          <div className="relative p-8 md:p-16 text-center space-y-6">
            {/* Background gradient animation */}
            <div className="absolute inset-0 bg-gradient-to-r from-neon-blue/10 via-transparent to-neon-pink/10 opacity-0 group-hover:opacity-100 transition-opacity" />
            
            <div className="relative z-10 space-y-6">
              <h2 className="text-3xl md:text-5xl font-bold gradient-text">
                Ready to Start Shopping?
              </h2>
              <p className="text-slate-300 text-lg md:text-xl max-w-2xl mx-auto">
                Join thousands of happy customers enjoying exclusive deals, fast delivery, and exceptional customer service.
              </p>
              <div className="flex gap-4 justify-center flex-wrap pt-6">
                <Link href="/products" className="gradient-button inline-flex items-center gap-2 group hover-btn">
                  Explore Products
                  <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link href="/login" className="glass px-8 py-3 rounded-lg font-semibold hover:bg-white/15 transition-smooth">
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}

export default function Home() {
  return (
    <Layout>
      <div className="space-y-0">
        {/* Video Hero Section */}
        <VideoHeroSection />

        {/* Featured Products */}
        <FeaturedProducts />

        {/* Categories */}
        <CategoriesSection />

        {/* Stats */}
        <StatsSection />

        {/* CTA Section */}
        <CTASection />
      </div>
    </Layout>
  );
}
