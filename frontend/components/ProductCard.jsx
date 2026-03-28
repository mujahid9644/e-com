// ============================================
// Product Card Component  
// ============================================
// Reusable product card with glassmorphism

import Link from 'next/link';
import { useRouter } from 'next/router';
import ProductImage from './ProductImage';
import { FiShoppingCart, FiHeart } from 'react-icons/fi';
import { useState, useEffect } from 'react';
import { useCartStore } from '../store/cartStore';
import { useWishlistStore } from '../store/wishlistStore';
import { useAuthStore } from '../store/authStore';

// Star Rating Component
function StarRating({ rating, reviews, sold, productId }) {
  // Generate deterministic rating and sold count based on product ID
  const generateDeterministicValue = (productId, min, max, seed) => {
    const hash = productId.toString().split('').reduce((a, b) => {
      a = ((a << 5) - a) + b.charCodeAt(0);
      return a & a;
    }, 0);
    const seededRandom = (Math.sin(hash + seed) + 1) / 2;
    return Math.floor(seededRandom * (max - min + 1)) + min;
  };

  // Use provided values or generate deterministic ones
  const displayRating = rating || (4.0 + generateDeterministicValue(productId, 0, 10) / 10).toFixed(1);
  const displayReviews = reviews || generateDeterministicValue(productId, 10, 100, 1);
  const displaySold = sold || generateDeterministicValue(productId, 1, 999, 2);
  
  const stars = Array(5).fill(0).map((_, i) => i < Math.round(displayRating));
  
  return (
    <div className="flex items-center gap-2 text-xs">
      <div className="flex gap-1">
        {stars.map((filled, i) => (
          <span key={i} className={filled ? 'text-yellow-400' : 'text-slate-600'}>
            ★
          </span>
        ))}
      </div>
      <span className="text-slate-400">({displayReviews})</span>
      <span className="text-slate-500">• {displaySold} sold</span>
    </div>
  );
}

export default function ProductCard({ product }) {
  const router = useRouter();
  const [isHovering, setIsHovering] = useState(false);
  const { addToCart, isLoading } = useCartStore();
  const { isAuthenticated } = useAuthStore();
  const { toggleWishlist, isInWishlist } = useWishlistStore();
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const [isInWishlistState, setIsInWishlistState] = useState(false);
  const [wishlistLoading, setWishlistLoading] = useState(false);

  // Check if product is in wishlist
  useEffect(() => {
    if (isAuthenticated) {
      isInWishlist(product.id).then(setIsInWishlistState);
    }
  }, [isAuthenticated, product.id, isInWishlist]);

  const handleAddToCart = async (e) => {
    e.preventDefault();
    setIsAddingToCart(true);
    await addToCart(product.id, 1);
    setIsAddingToCart(false);
  };

  const handleWishlistToggle = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    setWishlistLoading(true);
    const result = await toggleWishlist(product.id);
    if (result.success) {
      setIsInWishlistState(!isInWishlistState);
    }
    setWishlistLoading(false);
  };

  const discount = product.discount_percentage || 0;
  const discountedPrice = Number.parseFloat(product.discounted_price || 0);
  const price = Number.parseFloat(product.price || 0);
  const displayPrice = Number.isFinite(discountedPrice) && discountedPrice > 0 ? discountedPrice : price;

  const handleBuyNow = (e) => {
    e.preventDefault();
    e.stopPropagation();
    router.push(`/buy-now/${product.slug}`);
  };

  return (
    <Link href={`/products/${product.slug}`}>
      <div
        className="glass-hover h-full overflow-hidden cursor-pointer group animate-fade-in"
        onMouseEnter={() => setIsHovering(true)}
        onMouseLeave={() => setIsHovering(false)}
      >
        {/* Image Container */}
        <div className="relative h-48 overflow-hidden bg-gradient-to-br from-slate-700 to-slate-800">
          {product.image_url ? (
            <ProductImage
              src={product.image_url}
              alt={product.name}
              fill={true}
              className="object-cover group-hover:scale-110 transition-transform duration-300"
              fallbackSrc="/images/default-product.png"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-slate-500">
              No Image Available
            </div>
          )}
          
          {/* Discount Badge */}
          {discount > 0 && (
            <div className="absolute top-3 right-3 bg-gradient-neon text-white px-3 py-1 rounded-lg text-sm font-bold">
              -{discount}%
            </div>
          )}

          {/* Featured Badge */}
          {product.is_featured && (
            <div className="absolute top-3 left-3 bg-neon-blue text-slate-900 px-3 py-1 rounded-lg text-xs font-bold">
              Featured
            </div>
          )}

          {/* Hover Actions */}
          {isHovering && (
            <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center gap-3">
              <button
                onClick={handleAddToCart}
                disabled={isAddingToCart || !product.is_in_stock}
                className="bg-gradient-neon text-white p-3 rounded-full hover:shadow-neon-pink disabled:opacity-50"
              >
                <FiShoppingCart size={20} />
              </button>
              <button
                onClick={handleWishlistToggle}
                disabled={wishlistLoading}
                className={`p-3 rounded-full hover:bg-white/20 transition-colors ${
                  isInWishlistState ? 'text-red-500' : 'text-white'
                }`}
              >
                <FiHeart size={20} fill={isInWishlistState ? 'currentColor' : 'none'} />
              </button>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Category */}
          <p className="text-xs text-neon-cyan mb-2">{product.category_name}</p>

          {/* Name */}
          <h3 className="text-sm font-semibold text-slate-100 line-clamp-2 mb-2">
            {product.name}
          </h3>

          {/* Rating */}
          <StarRating rating={product.average_rating} reviews={product.reviews_count} sold={product.sold_count} productId={product.id} />

          {/* Price */}
          <div className="mt-3 flex items-center gap-2">
            <span className="text-lg font-bold text-neon-cyan">
              ${displayPrice.toFixed(2)}
            </span>
            {discount > 0 && price > 0 && (
              <span className="text-sm text-slate-500 line-through">
                ${price.toFixed(2)}
              </span>
            )}
          </div>

          {/* Stock Status */}
          <p className={`text-xs mt-2 ${product.is_in_stock ? 'text-green-400' : 'text-red-400'}`}>
            {product.stock_status}
          </p>

          <button
            onClick={handleBuyNow}
            className="w-full mt-3 py-2 bg-neon-cyan text-slate-900 font-semibold rounded-lg hover:bg-neon-blue"
          >
            Buy Now
          </button>
        </div>
      </div>
    </Link>
  );
}
