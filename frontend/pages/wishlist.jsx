import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import { useAuthStore } from '../store/authStore';
import { useWishlistStore } from '../store/wishlistStore';
import Layout from '../components/Layout';
import ProductCard from '../components/ProductCard';
import Skeleton from '../components/Skeleton';

export default function Wishlist() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { items, count, isLoading, fetchWishlist, removeFromWishlist } = useWishlistStore();
  const [removingIds, setRemovingIds] = useState(new Set());

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchWishlist();
  }, [isAuthenticated, fetchWishlist, router]);

  const handleRemoveFromWishlist = async (productId) => {
    setRemovingIds(prev => new Set(prev).add(productId));
    const result = await removeFromWishlist(productId);
    setRemovingIds(prev => {
      const newSet = new Set(prev);
      newSet.delete(productId);
      return newSet;
    });

    if (!result.success) {
      // Could show a toast here
      console.error('Failed to remove from wishlist:', result.error);
    }
  };

  if (!isAuthenticated) {
    return null; // Will redirect
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Wishlist</h1>
            <p className="text-gray-600">
              {count > 0 ? `${count} item${count !== 1 ? 's' : ''} in your wishlist` : 'Your wishlist is empty'}
            </p>
          </div>

          {/* Content */}
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {[...Array(8)].map((_, i) => (
                <Skeleton key={i} className="h-80" />
              ))}
            </div>
          ) : count === 0 ? (
            /* Empty State */
            <div className="text-center py-16">
              <div className="mb-6">
                <svg
                  className="mx-auto h-24 w-24 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1}
                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  />
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Your wishlist is empty</h2>
              <p className="text-gray-600 mb-8 max-w-md mx-auto">
                Save items you love for later. Start shopping and add products to your wishlist!
              </p>
              <Link
                href="/products"
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
              >
                Start Shopping
              </Link>
            </div>
          ) : (
            /* Wishlist Items */
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {items.map((item) => (
                <div key={item.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                  {/* Product Image */}
                  <div className="aspect-w-1 aspect-h-1 bg-gray-200">
                    <Image
                      src={item.product_detail.image_url || '/images/placeholder.jpg'}
                      alt={item.product_detail.name}
                      width={200}
                      height={200}
                      className="w-full h-48 object-cover"
                      onError={(e) => {
                        e.target.src = '/images/placeholder.jpg';
                      }}
                    />
                  </div>

                  {/* Product Info */}
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
                      {item.product_detail.name}
                    </h3>

                    <p className="text-sm text-gray-600 mb-2">
                      {item.product_detail.category_name}
                    </p>

                    {/* Price */}
                    <div className="flex items-center space-x-2 mb-3">
                      {item.product_detail.discounted_price ? (
                        <>
                          <span className="text-lg font-bold text-gray-900">
                            ${item.product_detail.discounted_price}
                          </span>
                          <span className="text-sm text-gray-500 line-through">
                            ${item.product_detail.price}
                          </span>
                        </>
                      ) : (
                        <span className="text-lg font-bold text-gray-900">
                          ${item.product_detail.price}
                        </span>
                      )}
                    </div>

                    {/* Stock Status */}
                    <div className="flex items-center mb-3">
                      <span
                        className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          item.product_detail.is_in_stock
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {item.product_detail.stock_status}
                      </span>
                    </div>

                    {/* Actions */}
                    <div className="flex space-x-2">
                      <Link
                        href={`/products/${item.product_detail.slug}`}
                        className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-md text-sm font-medium transition-colors text-center"
                      >
                        View Details
                      </Link>

                      <button
                        onClick={() => handleRemoveFromWishlist(item.product_detail.id)}
                        disabled={removingIds.has(item.product_detail.id)}
                        className="px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {removingIds.has(item.product_detail.id) ? 'Removing...' : 'Remove'}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}