// ============================================
// FAQ PAGE
// ============================================
// Frequently Asked Questions with accordion component

import Layout from '../components/Layout';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useState } from 'react';
import { FiChevronDown, FiSearch, FiArrowRight } from 'react-icons/fi';

export default function FAQPage() {
  const [expandedId, setExpandedId] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  const faqs = [
    {
      id: 1,
      category: 'Shopping',
      question: 'How do I place an order?',
      answer: 'Simply browse our products, add items to your cart, and proceed to checkout. You can pay using credit card, debit card, bKash, Nagad, or bank transfer.',
    },
    {
      id: 2,
      category: 'Shopping',
      question: 'Can I search for specific products?',
      answer: 'Yes, use the search bar at the top of the page to find products. You can also browse by category or apply filters to narrow down your results.',
    },
    {
      id: 3,
      category: 'Shipping',
      question: 'How long does delivery take?',
      answer: 'Standard delivery typically takes 2-5 business days within Dhaka and 3-7 days for other areas. Express delivery options are also available.',
    },
    {
      id: 4,
      category: 'Shipping',
      question: 'Do you offer free shipping?',
      answer: 'Free shipping is available on orders over Tk. 500. For orders below that amount, a shipping fee of Tk. 50-100 applies depending on your location.',
    },
    {
      id: 5,
      category: 'Returns',
      question: 'What is your return policy?',
      answer: 'We offer hassle-free returns within 7 days of purchase. Items must be unused and in original packaging. Simply contact our support team to initiate a return.',
    },
    {
      id: 6,
      category: 'Returns',
      question: 'How do I initiate a return?',
      answer: 'Contact our support team via email or phone with your order number. We\'ll provide you with a return label and instructions. Once received, we\'ll process your refund.',
    },
    {
      id: 7,
      category: 'Payment',
      question: 'What payment methods do you accept?',
      answer: 'We accept credit cards, debit cards, bKash, Nagad, Rocket, bank transfers, and cash on delivery for selected areas.',
    },
    {
      id: 8,
      category: 'Account',
      question: 'Do I need an account to shop?',
      answer: 'No, you can checkout as a guest. However, creating an account allows you to track orders, save addresses, and access exclusive discounts.',
    },
    {
      id: 9,
      category: 'Account',
      question: 'How do I reset my password?',
      answer: 'Click on "Forgot Password" on the login page. Enter your email address and follow the instructions sent to your inbox.',
    },
    {
      id: 10,
      category: 'Support',
      question: 'How can I contact customer support?',
      answer: 'You can reach us via email at support@smartcommerce.bd or call us at +880 1234 567890. We\'re available 24/7 to help!',
    },
  ];

  const filteredFaqs = faqs.filter(
    faq =>
      faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const categories = ['All', ...new Set(faqs.map(faq => faq.category))];
  const [selectedCategory, setSelectedCategory] = useState('All');

  const displayedFaqs = selectedCategory === 'All'
    ? filteredFaqs
    : filteredFaqs.filter(faq => faq.category === selectedCategory);

  return (
    <Layout>
      <div className="space-y-12">
        {/* Hero Section */}
        <motion.section
          className="py-20 px-4 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="max-w-3xl mx-auto space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold gradient-text">
              Frequently Asked Questions
            </h1>
            <p className="text-xl text-slate-300">
              Find answers to commonly asked questions about shopping, shipping, returns, and more.
            </p>
          </div>
        </motion.section>

        {/* Main Content */}
        <motion.div
          className="max-w-4xl mx-auto px-4 pb-20"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {/* Search Bar */}
          <motion.div
            className="mb-12"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <div className="relative">
              <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
              <input
                type="text"
                placeholder="Search questions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="glass w-full pl-12 pr-4 py-4 rounded-xl focus:ring-2 focus:ring-neon-cyan focus:outline-none text-slate-100 placeholder-slate-500"
              />
            </div>
          </motion.div>

          {/* Category Filter */}
          <motion.div
            className="mb-12 flex flex-wrap gap-3"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-full font-semibold transition-all ${
                  selectedCategory === category
                    ? 'gradient-button'
                    : 'glass hover:bg-white/15'
                }`}
              >
                {category}
              </button>
            ))}
          </motion.div>

          {/* FAQ Items */}
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            {displayedFaqs.length > 0 ? (
              displayedFaqs.map((faq, index) => (
                <motion.div
                  key={faq.id}
                  className="glass-dark rounded-xl overflow-hidden"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.05 }}
                >
                  <motion.button
                    onClick={() => setExpandedId(expandedId === faq.id ? null : faq.id)}
                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-white/10 transition-colors"
                    whileHover={{ x: 4 }}
                  >
                    <div className="flex items-center gap-4 text-left flex-1">
                      <div className="w-3 h-3 rounded-full bg-neon-cyan flex-shrink-0" />
                      <div>
                        <p className="text-slate-400 text-sm font-medium mb-1">{faq.category}</p>
                        <h3 className="text-slate-100 font-semibold">{faq.question}</h3>
                      </div>
                    </div>
                    <motion.div
                      animate={{ rotate: expandedId === faq.id ? 180 : 0 }}
                      transition={{ duration: 0.2 }}
                      className="flex-shrink-0"
                    >
                      <FiChevronDown size={24} className="text-neon-cyan" />
                    </motion.div>
                  </motion.button>

                  {/* Answer */}
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{
                      opacity: expandedId === faq.id ? 1 : 0,
                      height: expandedId === faq.id ? 'auto' : 0,
                    }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <div className="px-6 py-4 border-t border-white/10 bg-white/5 text-slate-300">
                      {faq.answer}
                    </div>
                  </motion.div>
                </motion.div>
              ))
            ) : (
              <motion.div
                className="text-center py-12"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="text-5xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-slate-100 mb-2">No questions found</h3>
                <p className="text-slate-400">
                  Try searching for different keywords or browse other categories.
                </p>
              </motion.div>
            )}
          </motion.div>

          {/* Still need help? */}
          <motion.div
            className="mt-16 p-8 glass-dark rounded-2xl text-center space-y-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="text-2xl font-bold gradient-text">Didn&apos;t find your answer?</h3>
            <p className="text-slate-300">
              Our support team is here to help. Reach out to us and we&apos;ll get back to you as soon as possible.
            </p>
            <div className="flex gap-4 justify-center flex-wrap pt-4">
              <Link href="/contact" className="gradient-button inline-flex items-center gap-2">
                Contact Support
                <FiArrowRight />
              </Link>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </Layout>
  );
}
