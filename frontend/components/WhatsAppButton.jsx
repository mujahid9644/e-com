// ============================================
// WhatsApp Floating Button Component
// ============================================
// Premium floating WhatsApp button with glassmorphism

import { motion } from 'framer-motion';
import { FaWhatsapp } from 'react-icons/fa';

export default function WhatsAppButton() {
  const whatsappNumber = '8801533827434';
  const defaultMessage = 'Hello, I want to know more about your products.';
  
  // URL encode the message
  const encodedMessage = encodeURIComponent(defaultMessage);
  const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;

  return (
    <motion.a
      href={whatsappUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-8 right-8 z-40 group"
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
    >
      {/* Pulse Background Animation */}
      <motion.div
        className="absolute inset-0 rounded-full bg-green-500/30"
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ duration: 2, repeat: Infinity }}
      />

      {/* Glow Effect */}
      <motion.div
        className="absolute inset-0 rounded-full bg-gradient-to-r from-green-400 to-emerald-500 opacity-0 group-hover:opacity-30 blur-lg transition-opacity duration-300"
      />

      {/* Main Button */}
      <motion.div
        className="relative w-14 h-14 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 backdrop-blur-md border border-white/20 shadow-lg flex items-center justify-center cursor-pointer"
        whileHover={{
          boxShadow: '0 0 30px rgba(34, 197, 94, 0.6)',
        }}
      >
        {/* WhatsApp Icon */}
        <FaWhatsapp className="text-white text-2xl" />
      </motion.div>

      {/* Tooltip on Hover */}
      <motion.div
        className="absolute bottom-16 right-0 whitespace-nowrap"
        initial={{ opacity: 0, y: 10 }}
        whileHover={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        <div className="glass px-4 py-2 rounded-lg text-sm text-slate-100 font-semibold">
          Chat with us!
        </div>
      </motion.div>
    </motion.a>
  );
}
