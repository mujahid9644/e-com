import { useState } from 'react';
import Image from 'next/image';

/**
 * ProductImage Component
 * 
 * Handles product image display with:
 * - Fallback on error
 * - Loading state
 * - Error boundary
 * - Responsive sizing
 * - Proper alt text
 */
export default function ProductImage({ 
  src, 
  alt = 'Product Image',
  fill = false,
  width = null,
  height = null,
  className = 'object-cover',
  fallbackSrc = '/images/default-product.png',
  priority = false,
}) {
  const [imageSrc, setImageSrc] = useState(src);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const handleImageError = () => {
    console.warn(`Failed to load image: ${src}`);
    setHasError(true);
    setImageSrc(fallbackSrc);
  };

  const handleImageLoad = () => {
    setIsLoading(false);
  };

  // If no image source provided, show placeholder immediately
  if (!src) {
    return (
      <div
        className={`relative bg-gray-200 flex items-center justify-center ${
          fill ? 'w-full h-full' : ''
        } ${className}`}
        style={!fill && width && height ? { width, height } : {}}
      >
        <div className="text-center">
          <div className="text-gray-400 text-sm">No Image</div>
        </div>
      </div>
    );
  }

  // If fill prop is used (for container-based sizing)
  if (fill) {
    return (
      <div className="relative w-full h-full">
        <Image
          src={imageSrc}
          alt={alt}
          fill
          className={`${className} ${isLoading ? 'animate-pulse' : ''}`}
          onError={handleImageError}
          onLoadingComplete={handleImageLoad}
          priority={priority}
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        {hasError && (
          <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400 text-sm">Image not available</span>
          </div>
        )}
      </div>
    );
  }

  // If specific width/height is provided
  if (width && height) {
    return (
      <div className="relative" style={{ width, height, overflow: 'hidden' }}>
        <Image
          src={imageSrc}
          alt={alt}
          width={width}
          height={height}
          className={`${className} ${isLoading ? 'animate-pulse' : ''}`}
          onError={handleImageError}
          onLoadingComplete={handleImageLoad}
          priority={priority}
        />
        {hasError && (
          <div
            className="absolute inset-0 bg-gray-200 flex items-center justify-center"
            style={{ width, height }}
          >
            <span className="text-gray-400 text-sm">Image not available</span>
          </div>
        )}
      </div>
    );
  }

  // Default: return plain Image component with error handling
  return (
    <Image
      src={imageSrc}
      alt={alt}
      width={200}
      height={200}
      className={`${className} ${isLoading ? 'animate-pulse' : ''}`}
      onError={handleImageError}
      onLoadingComplete={handleImageLoad}
      priority={priority}
    />
  );
}
