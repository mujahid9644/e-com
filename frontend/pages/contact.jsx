// ============================================
// CONTACT PAGE
// ============================================
// Contact us page with contact form and information

import Layout from '../components/Layout';
import { motion } from 'framer-motion';
import { useState } from 'react';
import Link from 'next/link';
import { FiMail, FiPhone, FiMapPin, FiClock, FiSend } from 'react-icons/fi';

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Simulate form submission
      await new Promise(resolve => setTimeout(resolve, 1500));
      setSubmitStatus('success');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setTimeout(() => setSubmitStatus(null), 3000);
    } catch (error) {
      setSubmitStatus('error');
      setTimeout(() => setSubmitStatus(null), 3000);
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactInfo = [
    {
      icon: FiMail,
      title: 'Email',
      value: 'support@smartcommerce.bd',
      href: 'mailto:support@smartcommerce.bd',
    },
    {
      icon: FiPhone,
      title: 'Phone',
      value: '+880 1234 567890',
      href: 'tel:+880123456789',
    },
    {
      icon: FiMapPin,
      title: 'Location',
      value: 'Dhaka, Bangladesh',
      href: '#',
    },
    {
      icon: FiClock,
      title: 'Hours',
      value: '24/7 Available',
      href: '#',
    },
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
              Get in Touch
            </h1>
            <p className="text-xl text-slate-300">
              We&apos;d love to hear from you. Send us a message and we&apos;ll respond as soon as possible.
            </p>
          </div>
        </motion.section>

        {/* Main Content */}
        <motion.div
          className="max-w-6xl mx-auto px-4 pb-20"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Contact Info */}
            <motion.div
              className="space-y-6"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {contactInfo.map((info, index) => {
                const IconComponent = info.icon;
                return (
                  <motion.a
                    key={index}
                    href={info.href}
                    className="glass-hover p-6 rounded-2xl block group"
                    variants={itemVariants}
                    whileHover={{ x: 8 }}
                  >
                    <div className="flex gap-4">
                      <div className="w-12 h-12 rounded-full glass flex items-center justify-center flex-shrink-0">
                        <IconComponent size={24} className="text-neon-cyan" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-slate-100 mb-1">{info.title}</h3>
                        <p className="text-slate-400 group-hover:text-neon-cyan transition-colors">
                          {info.value}
                        </p>
                      </div>
                    </div>
                  </motion.a>
                );
              })}

              {/* FAQ Link */}
              <motion.div
                className="glass-dark rounded-2xl p-6 space-y-3"
                variants={itemVariants}
              >
                <h3 className="font-semibold text-slate-100 text-lg">Have Questions?</h3>
                <p className="text-slate-400 text-sm">
                  Check out our FAQ page for quick answers to common questions.
                </p>
                <Link
                  href="/faq"
                  className="inline-block text-neon-cyan hover:text-white transition-colors font-semibold text-sm"
                >
                  View FAQ →
                </Link>
              </motion.div>
            </motion.div>

            {/* Contact Form */}
            <motion.form
              onSubmit={handleSubmit}
              className="lg:col-span-2 glass-dark rounded-2xl p-8 space-y-6"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="grid md:grid-cols-2 gap-4">
                <motion.div
                  className="space-y-2"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.1 }}
                >
                  <label className="block text-slate-200 font-medium">Full Name</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="glass w-full px-4 py-3 rounded-lg focus:ring-2 focus:ring-neon-cyan focus:outline-none text-slate-100 placeholder-slate-500"
                    placeholder="Your name"
                  />
                </motion.div>
                <motion.div
                  className="space-y-2"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.15 }}
                >
                  <label className="block text-slate-200 font-medium">Email Address</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="glass w-full px-4 py-3 rounded-lg focus:ring-2 focus:ring-neon-cyan focus:outline-none text-slate-100 placeholder-slate-500"
                    placeholder="your@email.com"
                  />
                </motion.div>
              </div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
              >
                <label className="block text-slate-200 font-medium">Subject</label>
                <input
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="glass w-full px-4 py-3 rounded-lg focus:ring-2 focus:ring-neon-cyan focus:outline-none text-slate-100 placeholder-slate-500"
                  placeholder="How can we help?"
                />
              </motion.div>

              <motion.div
                className="space-y-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.25 }}
              >
                <label className="block text-slate-200 font-medium">Message</label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={6}
                  className="glass w-full px-4 py-3 rounded-lg focus:ring-2 focus:ring-neon-cyan focus:outline-none text-slate-100 placeholder-slate-500 resize-none"
                  placeholder="Tell us more about your inquiry..."
                />
              </motion.div>

              {/* Status Messages */}
              {submitStatus === 'success' && (
                <motion.div
                  className="p-4 rounded-lg bg-green-500/20 border border-green-500/50 text-green-300"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  ✓ Message sent successfully! We&apos;ll get back to you soon.
                </motion.div>
              )}
              {submitStatus === 'error' && (
                <motion.div
                  className="p-4 rounded-lg bg-red-500/20 border border-red-500/50 text-red-300"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  ✗ Error sending message. Please try again.
                </motion.div>
              )}

              <motion.button
                type="submit"
                disabled={isSubmitting}
                className="gradient-button w-full py-3 rounded-lg font-semibold flex items-center justify-center gap-2 disabled:opacity-50"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isSubmitting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Sending...
                  </>
                ) : (
                  <>
                    Send Message
                    <FiSend />
                  </>
                )}
              </motion.button>
            </motion.form>
          </div>
        </motion.div>

        {/* Additional Info */}
        <motion.section
          className="glass-dark rounded-3xl mx-4 sm:mx-8 lg:mx-auto max-w-5xl py-16 px-8 mb-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
        >
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold gradient-text">Response Times</h2>
            <p className="text-slate-300 max-w-2xl mx-auto">
              Our support team typically responds to emails within 2-4 hours during business hours.
              For urgent issues, please call us directly.
            </p>
          </div>
        </motion.section>
      </div>
    </Layout>
  );
}
