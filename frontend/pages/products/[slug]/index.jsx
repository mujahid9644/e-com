import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import { FiShoppingCart, FiHeart, FiMinus, FiPlus, FiStar } from 'react-icons/fi';
import Layout from '@/components/Layout';
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';
import { useWishlistStore } from '@/store/wishlistStore';
import apiClient, { endpoints } from '@/utils/api';

export default function ProductDetail() {
  const router = useRouter();
  const { slug } = router.query;
  const { isAuthenticated } = useAuthStore();
  const { addToCart } = useCartStore();
  const { toggleWishlist, isInWishlist } = useWishlistStore();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [isInWishlistState, setIsInWishlistState] = useState(false);
  const [wishlistLoading, setWishlistLoading] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);

  const [showOrderForm, setShowOrderForm] = useState(false);
  const [orderForm, setOrderForm] = useState({
    customer_name: '',
    phone_number: '',
    whatsapp_number: '',
    address: '',
    note: '',
  });
  const [placingOrder, setPlacingOrder] = useState(false);
  const [orderSuccess, setOrderSuccess] = useState(false);

  const fetchProduct = useCallback(async () => {
    if (!slug) return;
    try {
      setLoading(true);
      const response = await apiClient.get(endpoints.products.detail(slug));
      setProduct(response.data);
      setError(null);
    } catch (err) {
      setError('Product not found');
      setProduct(null);
      console.error('Error fetching product:', err);
    } finally {
      setLoading(false);
    }
  }, [slug]);

  const checkWishlistStatus = useCallback(async () => {
    if (!product) return;
    try {
      const inWishlist = await isInWishlist(product.id);
      setIsInWishlistState(inWishlist);
    } catch (err) {
      console.error('Wishlist status error:', err);
    }
  }, [product, isInWishlist]);

  useEffect(() => {
    fetchProduct();
  }, [fetchProduct]);

  useEffect(() => {
    if (product && isAuthenticated) {
      checkWishlistStatus();
    }
  }, [product, isAuthenticated, checkWishlistStatus]);

  const handleWishlistToggle = async () => {
    if (!product) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    setWishlistLoading(true);
    const result = await toggleWishlist(product.id);
    if (result.success) setIsInWishlistState((prev) => !prev);
    setWishlistLoading(false);
  };

  const handleAddToCart = async () => {
    if (!product) return;
    setAddingToCart(true);
    const result = await addToCart(product.id, quantity);
    setAddingToCart(false);
    if (result.success) console.log('Added to cart');
  };

  const handleBuyNow = () => setShowOrderForm(true);

  const handleOrderSubmit = async (e) => {
    e.preventDefault();
    if (!product) return;
    setPlacingOrder(true);
    try {
      const orderData = {
        product_id: product.id,
        quantity,
        customer_name: orderForm.customer_name,
        phone_number: orderForm.phone_number,
        whatsapp_number: orderForm.whatsapp_number,
        address: orderForm.address,
        note: orderForm.note,
      };
      await apiClient.post(endpoints.orders.create, orderData);
      setOrderSuccess(true);
      setShowOrderForm(false);
      setOrderForm({ customer_name: '', phone_number: '', whatsapp_number: '', address: '', note: '' });
    } catch (err) {
      console.error('Order failed:', err);
      setError('Could not place order');
    } finally {
      setPlacingOrder(false);
    }
  };

  const updateQuantity = (change) => {
    setQuantity((current) => {
      const newQty = current + change;
      if (!product) return current;
      if (newQty < 1) return 1;
      if (newQty > product.stock_quantity) return product.stock_quantity;
      return newQty;
    });
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 py-8 px-4">Loading product...</div>
      </Layout>
    );
  }

  if (error || !product) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 py-16">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-3xl font-bold mb-2">Product Not Found</h1>
            <p className="text-gray-600 mb-6">The product you&apos;re looking for doesn&apos;t exist.</p>
            <Link href="/products" className="btn-primary">
              Browse Products
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  const discount = product.discount_percentage || 0;
  const discountedPrice = product.discounted_price || product.price;
  const originalPrice = product.price;

  return (
    <Layout>
      <div className="min-h-screen p-4 md:p-8 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Product Images Section */}
            <div className="space-y-4">
              {/* Main Image */}
              <div className="aspect-square bg-slate-800 rounded-lg overflow-hidden border border-slate-700">
                {product.featured_image_url ? (
                  <Image
                    src={product.featured_image_url}
                    alt={product.name}
                    width={500}
                    height={500}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-slate-700">
                    <p className="text-slate-400">No Image</p>
                  </div>
                )}
              </div>

              {/* Gallery Images */}
              {product.images && product.images.length > 0 && (
                <div className="flex gap-3 overflow-x-auto">
                  {product.images.map((img, idx) => (
                    <button
                      key={idx}
                      className="flex-shrink-0 w-20 h-20 rounded-lg bg-slate-700 border border-slate-600 overflow-hidden hover:border-neon-cyan transition"
                    >
                      <Image
                        src={img.image_url}
                        alt={`${product.name} ${idx + 1}`}
                        width={100}
                        height={100}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Details Section */}
            <div className="space-y-6">
              {/* Title & Category */}
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                  {product.name}
                </h1>
                {product.category && (
                  <p className="text-neon-cyan text-sm font-medium">
                    {product.category.name}
                  </p>
                )}
              </div>

              {/* Rating & Reviews */}
              <div className="flex items-center gap-4">
                <div className="flex gap-1">
                  {[...Array(5)].map((_, i) => (
                    <FiStar
                      key={i}
                      size={20}
                      className={
                        i < Math.round(product.average_rating)
                          ? 'text-yellow-400 fill-yellow-400'
                          : 'text-slate-600'
                      }
                    />
                  ))}
                </div>
                <span className="text-slate-300">
                  {product.average_rating || '4.5'} ({product.reviews_count || 0} reviews)
                </span>
              </div>

              {/* Price */}
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="text-3xl font-bold text-neon-cyan">
                    ${parseFloat(product.discounted_price || product.price).toFixed(2)}
                  </span>
                  {product.discount_percentage > 0 && (
                    <>
                      <span className="text-lg text-slate-500 line-through">
                        ${parseFloat(product.price).toFixed(2)}
                      </span>
                      <span className="bg-red-500 text-white px-3 py-1 rounded-lg text-sm font-bold">
                        -{product.discount_percentage}%
                      </span>
                    </>
                  )}
                </div>
              </div>

              {/* Stock Status */}
              <div>
                <p
                  className={`text-sm font-medium ${
                    product.is_in_stock ? 'text-green-400' : 'text-red-400'
                  }`}
                >
                  {product.stock_status || (product.is_in_stock ? 'In Stock' : 'Out of Stock')}
                </p>
              </div>

              {/* Description */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">Description</h3>
                <p className="text-slate-300 text-sm leading-relaxed">
                  {product.description || product.short_description || 'No description available'}
                </p>
              </div>

              {/* Quantity Selector */}
              <div className="space-y-3">
                <label className="text-sm font-medium text-slate-200">Quantity</label>
                <div className="flex items-center gap-3 w-32">
                  <button
                    onClick={() => updateQuantity(-1)}
                    disabled={quantity <= 1}
                    className="w-10 h-10 rounded-lg bg-slate-700 hover:bg-slate-600 disabled:opacity-50 flex items-center justify-center text-white"
                  >
                    <FiMinus size={18} />
                  </button>
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                    className="flex-1 bg-slate-700 border border-slate-600 rounded px-2 py-1 text-white text-center"
                  />
                  <button
                    onClick={() => updateQuantity(1)}
                    disabled={quantity >= product.stock_quantity}
                    className="w-10 h-10 rounded-lg bg-slate-700 hover:bg-slate-600 disabled:opacity-50 flex items-center justify-center text-white"
                  >
                    <FiPlus size={18} />
                  </button>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <button
                  onClick={handleAddToCart}
                  disabled={addingToCart || !product.is_in_stock}
                  className="flex-1 bg-gradient-to-r from-neon-cyan to-neon-blue text-slate-900 font-bold py-3 rounded-lg hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  <FiShoppingCart size={20} />
                  Add to Cart
                </button>
                <button
                  onClick={handleWishlistToggle}
                  disabled={wishlistLoading}
                  className={`w-12 h-12 rounded-lg border-2 flex items-center justify-center transition ${
                    isInWishlistState
                      ? 'bg-red-500/20 border-red-500 text-red-500'
                      : 'border-slate-600 text-slate-300 hover:border-slate-400'
                  }`}
                >
                  <FiHeart size={20} fill={isInWishlistState ? 'currentColor' : 'none'} />
                </button>
              </div>

              <button
                onClick={handleBuyNow}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-3 rounded-lg hover:opacity-90 transition"
              >
                Buy Now
              </button>

              {/* Quick Order Form */}
              {showOrderForm && (
                <div className="mt-6 p-4 bg-slate-800 rounded-lg border border-slate-700 space-y-4">
                  <h3 className="text-lg font-semibold text-white">Place Order</h3>
                  {orderSuccess && (
                    <div className="bg-green-500/20 border border-green-500 text-green-300 p-3 rounded">
                      Order placed successfully!
                    </div>
                  )}
                  <form onSubmit={handleOrderSubmit} className="space-y-3">
                    <input
                      type="text"
                      placeholder="Customer Name"
                      value={orderForm.customer_name}
                      onChange={(e) =>
                        setOrderForm({ ...orderForm, customer_name: e.target.value })
                      }
                      className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-400"
                    />
                    <input
                      type="tel"
                      placeholder="Phone Number"
                      value={orderForm.phone_number}
                      onChange={(e) =>
                        setOrderForm({ ...orderForm, phone_number: e.target.value })
                      }
                      className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-400"
                    />
                    <input
                      type="tel"
                      placeholder="WhatsApp Number"
                      value={orderForm.whatsapp_number}
                      onChange={(e) =>
                        setOrderForm({ ...orderForm, whatsapp_number: e.target.value })
                      }
                      className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-400"
                    />
                    <textarea
                      placeholder="Address"
                      value={orderForm.address}
                      onChange={(e) =>
                        setOrderForm({ ...orderForm, address: e.target.value })
                      }
                      rows={2}
                      className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-400"
                    />
                    <textarea
                      placeholder="Special Notes (Optional)"
                      value={orderForm.note}
                      onChange={(e) => setOrderForm({ ...orderForm, note: e.target.value })}
                      rows={2}
                      className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-white placeholder-slate-400"
                    />
                    <button
                      type="submit"
                      disabled={placingOrder}
                      className="w-full bg-gradient-to-r from-neon-cyan to-neon-blue text-slate-900 font-bold py-2 rounded-lg hover:opacity-90 disabled:opacity-50"
                    >
                      {placingOrder ? 'Processing...' : 'Confirm Order'}
                    </button>
                  </form>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}