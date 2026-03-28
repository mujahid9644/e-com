// ============================================
// Hero Section Component
// ============================================
// Reusable hero section with video background and overlay

import { motion } from 'framer-motion';
import Link from 'next/link';
import { FiArrowRight } from 'react-icons/fi';

export function VideoHeroSection({
  title,
  subtitle,
  videoSrc,
  buttonText = 'Shop Now',
  buttonHref = '/products',
  showSecondaryButton = true,
  secondaryButtonText = 'Learn More',
  secondaryButtonHref = '/about',
}) {
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
        <source src={videoSrc} type="video/mp4" />
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
            {title}
            <br />
            <span className="gradient-text">{subtitle}</span>
          </h1>

          <motion.div
            className="flex gap-4 justify-center flex-wrap pt-4"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Link href={buttonHref} className="gradient-button inline-flex items-center gap-2 group">
              {buttonText}
              <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
            </Link>
            {showSecondaryButton && (
              <Link href={secondaryButtonHref} className="glass px-8 py-3 font-semibold rounded-lg hover:bg-white/15 transition-smooth">
                {secondaryButtonText}
              </Link>
            )}
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

// Simple text-based hero section
export function TextHeroSection({
  title,
  subtitle,
  description,
  buttonText = 'Get Started',
  buttonHref = '/',
}) {
  return (
    <motion.section
      className="py-20 px-4 text-center"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="max-w-3xl mx-auto space-y-6">
        <h1 className="text-5xl md:text-6xl font-bold gradient-text">
          {title}
        </h1>
        {subtitle && (
          <h2 className="text-2xl md:text-3xl text-slate-200">
            {subtitle}
          </h2>
        )}
        {description && (
          <p className="text-xl text-slate-300">
            {description}
          </p>
        )}
        {buttonText && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Link href={buttonHref} className="gradient-button inline-flex items-center gap-2">
              {buttonText}
              <FiArrowRight />
            </Link>
          </motion.div>
        )}
      </div>
    </motion.section>
  );
}

export default VideoHeroSection;
