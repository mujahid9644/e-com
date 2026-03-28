// ============================================
// Footer Component
// ============================================
// Premium footer with glassmorphism design, social links, and navigation

import Link from 'next/link';
import { FiFacebook, FiInstagram, FiTwitter, FiMail, FiPhone, FiMapPin, FiArrowRight } from 'react-icons/fi';
import { motion } from 'framer-motion';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  return (
    <footer className="glass-dark border-t border-white/10 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Newsletter Section */}
        <motion.div
          className="py-12 border-b border-white/10"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold gradient-text mb-2">Subscribe to Our Newsletter</h3>
              <p className="text-slate-400">Get latest updates on products and exclusive offers</p>
            </div>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="Enter your email"
                className="glass flex-1 px-4 py-3 rounded-lg focus:ring-2 focus:ring-neon-cyan focus:outline-none"
              />
              <button className="gradient-button px-6 py-3 rounded-lg flex items-center gap-2">
                <FiArrowRight size={18} />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Main Footer Content */}
        <motion.div
          className="py-16"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
            {/* Company Info */}
            <motion.div variants={itemVariants}>
              <div className="mb-4">
                <h3 className="text-xl font-bold gradient-text mb-3 flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-gradient-neon flex items-center justify-center">
                    <span className="text-white font-bold">E</span>
                  </div>
                  Smart Commerce BD
                </h3>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed mb-4">
                Premium e-commerce platform delivering quality products with exceptional customer experience and fast shipping.
              </p>
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-slate-400 text-sm hover:text-neon-cyan transition-colors cursor-pointer">
                  <FiPhone size={16} />
                  <span>+880 1234 567890</span>
                </div>
                <div className="flex items-center gap-3 text-slate-400 text-sm hover:text-neon-cyan transition-colors cursor-pointer">
                  <FiMail size={16} />
                  <span>support@smartcommerce.bd</span>
                </div>
                <div className="flex items-center gap-3 text-slate-400 text-sm hover:text-neon-cyan transition-colors cursor-pointer">
                  <FiMapPin size={16} />
                  <span>Dhaka, Bangladesh</span>
                </div>
              </div>
            </motion.div>

            {/* Quick Links */}
            <motion.div variants={itemVariants}>
              <h4 className="font-bold text-slate-100 mb-6 text-lg">Quick Links</h4>
              <ul className="space-y-3">
                <li>
                  <Link href="/" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="/products" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Products
                  </Link>
                </li>
                <li>
                  <Link href="/categories" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Categories
                  </Link>
                </li>
                <li>
                  <Link href="/about" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    About Us
                  </Link>
                </li>
              </ul>
            </motion.div>

            {/* Support */}
            <motion.div variants={itemVariants}>
              <h4 className="font-bold text-slate-100 mb-6 text-lg">Support</h4>
              <ul className="space-y-3">
                <li>
                  <Link href="/contact" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Contact Us
                  </Link>
                </li>
                <li>
                  <Link href="/faq" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    FAQ
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Shipping Info
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Returns
                  </Link>
                </li>
              </ul>
            </motion.div>

            {/* Legal */}
            <motion.div variants={itemVariants}>
              <h4 className="font-bold text-slate-100 mb-6 text-lg">Legal</h4>
              <ul className="space-y-3">
                <li>
                  <Link href="#" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Terms of Service
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-slate-400 hover:text-neon-cyan transition-colors flex items-center gap-2 group">
                    <span className="inline-block w-1.5 h-1.5 bg-neon-cyan rounded-full opacity-0 group-hover:opacity-100 transition-all" />
                    Cookie Policy
                  </Link>
                </li>
              </ul>
            </motion.div>
          </div>

          {/* Divider */}
          <div className="border-t border-white/10 pt-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <p className="text-slate-400 text-sm">
                © {currentYear} Smart Commerce BD. All rights reserved.
              </p>

              {/* Social Media Icons */}
              <div className="flex gap-4">
                <motion.a
                  href="https://facebook.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full glass flex items-center justify-center text-slate-400 hover:text-neon-cyan hover:bg-white/15 transition-all"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FiFacebook size={18} />
                </motion.a>
                <motion.a
                  href="https://instagram.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full glass flex items-center justify-center text-slate-400 hover:text-neon-cyan hover:bg-white/15 transition-all"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FiInstagram size={18} />
                </motion.a>
                <motion.a
                  href="https://twitter.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full glass flex items-center justify-center text-slate-400 hover:text-neon-cyan hover:bg-white/15 transition-all"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FiTwitter size={18} />
                </motion.a>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </footer>
  );
}
