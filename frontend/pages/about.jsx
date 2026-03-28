// ============================================
// ABOUT PAGE
// ============================================
// About us page with company information and values

import Layout from '../components/Layout';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { FiArrowRight, FiCheckCircle, FiUsers, FiTrendingUp, FiHeart } from 'react-icons/fi';

export default function AboutPage() {
  const values = [
    {
      icon: FiHeart,
      title: 'Customer First',
      description: 'We prioritize customer satisfaction above everything else',
    },
    {
      icon: FiTrendingUp,
      title: 'Innovation',
      description: 'Continuously improving our platform with latest technologies',
    },
    {
      icon: FiCheckCircle,
      title: 'Quality',
      description: 'Only offering premium products from trusted suppliers',
    },
    {
      icon: FiUsers,
      title: 'Community',
      description: 'Building a vibrant community of shoppers and sellers',
    },
  ];

  const stats = [
    { number: '50K+', label: 'Products' },
    { number: '100K+', label: 'Customers' },
    { number: '50+', label: 'Categories' },
    { number: '99%', label: 'Satisfaction' },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
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
    <Layout>
      <div className="space-y-20">
        {/* Hero Section */}
        <motion.section
          className="py-20 px-4 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="max-w-3xl mx-auto space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold gradient-text">
              About Smart Commerce BD
            </h1>
            <p className="text-xl text-slate-300">
              Revolutionizing online shopping with premium products, exceptional service, and innovative technology
            </p>
          </div>
        </motion.section>

        {/* Story Section */}
        <motion.section
          className="max-w-5xl mx-auto px-4 py-16"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              className="glass-dark rounded-2xl h-96 bg-gradient-to-br from-neon-blue/20 via-transparent to-neon-pink/20"
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.3 }}
            />
            <div className="space-y-6">
              <h2 className="text-4xl font-bold gradient-text">Our Story</h2>
              <p className="text-slate-300 text-lg leading-relaxed">
                Smart Commerce BD was founded with a simple mission: to make online shopping accessible, affordable, and enjoyable for everyone in Bangladesh.
              </p>
              <p className="text-slate-300 text-lg leading-relaxed">
                We believe that quality products shouldn&apos;t be hard to find or expensive to buy. Our platform connects customers with thousands of verified sellers offering the best products at competitive prices.
              </p>
              <p className="text-slate-300 text-lg leading-relaxed">
                Today, we&apos;re proud to serve over 100,000 happy customers and continue to grow every day.
              </p>
              <Link href="/products" className="gradient-button inline-flex items-center gap-2 w-fit">
                Start Shopping
                <FiArrowRight />
              </Link>
            </div>
          </div>
        </motion.section>

        {/* Stats Section */}
        <motion.section
          className="max-w-5xl mx-auto px-4 py-16"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-center mb-16 gradient-text">By The Numbers</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                className="glass p-8 text-center rounded-2xl group hover:bg-white/15 transition-all"
                variants={itemVariants}
                whileHover={{ y: -8 }}
              >
                <div className="text-4xl md:text-5xl font-bold gradient-text mb-2">
                  {stat.number}
                </div>
                <div className="text-slate-400">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Values Section */}
        <motion.section
          className="max-w-5xl mx-auto px-4 py-16"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl font-bold text-center mb-16 gradient-text">Our Values</h2>
          <motion.div
            className="grid md:grid-cols-2 gap-6"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {values.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <motion.div
                  key={index}
                  className="glass-hover p-8 rounded-2xl space-y-4"
                  variants={itemVariants}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="w-16 h-16 rounded-full glass flex items-center justify-center">
                    <IconComponent size={32} className="text-neon-cyan" />
                  </div>
                  <h3 className="text-2xl font-bold text-slate-100">{value.title}</h3>
                  <p className="text-slate-400">{value.description}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </motion.section>

        {/* Team Section */}
        <motion.section
          className="max-w-5xl mx-auto px-4 py-16"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-4xl font-bold text-center mb-16 gradient-text">Why Choose Us?</h2>
          <div className="space-y-4">
            {[
              '✓ Curated collection of high-quality products',
              '✓ Fast and reliable delivery across Bangladesh',
              '✓ 24/7 customer support in Bengali',
              '✓ Secure payment with multiple options',
              '✓ Easy returns and refunds policy',
              '✓ Regular sales and exclusive offers',
            ].map((reason, index) => (
              <motion.div
                key={index}
                className="glass p-4 rounded-lg flex items-center gap-4"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.05 }}
              >
                <div className="w-6 h-6 rounded-full bg-gradient-neon flex items-center justify-center flex-shrink-0" />
                <span className="text-slate-200 text-lg">{reason}</span>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* CTA Section */}
        <motion.section
          className="glass-dark rounded-3xl mx-4 sm:mx-8 lg:mx-auto max-w-5xl py-16 px-8 mb-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="text-center space-y-6">
            <h2 className="text-3xl md:text-4xl font-bold gradient-text">
              Join Our Growing Community
            </h2>
            <p className="text-slate-300 text-lg max-w-2xl mx-auto">
              Experience the future of online shopping. Discover amazing products, enjoy exceptional service, and save big every day.
            </p>
            <div className="flex gap-4 justify-center flex-wrap pt-6">
              <Link href="/products" className="gradient-button inline-flex items-center gap-2">
                Start Shopping Now
                <FiArrowRight />
              </Link>
              <Link href="/contact" className="glass px-8 py-3 rounded-lg font-semibold hover:bg-white/15">
                Get in Touch
              </Link>
            </div>
          </div>
        </motion.section>
      </div>
    </Layout>
  );
}
