// ============================================
// CART PAGE
// ============================================
// Shopping cart management

import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import ProductImage from '../components/ProductImage';
import { useCartStore } from '../store/cartStore';
import { motion } from 'framer-motion';
import { FiTrash2, FiArrowRight } from 'react-icons/fi';
import Link from 'next/link';
import { useAuthStore } from '../store/authStore';
import { useRouter } from 'next/router';

export default function CartPage() {
  const { items, totalPrice, totalItems, fetchCart, removeFromCart, updateQuantity } = useCartStore();
  const { isAuthenticated } = useAuthStore();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart().then(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [isAuthenticated, fetchCart]);

  const handleCheckout = () => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/checkout');
    } else {
      router.push('/checkout');
    }
  };

  if (!isAuthenticated) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto px-4 py-16 text-center">
          <h2 className="text-2xl font-bold mb-4">Please log in to view your cart</h2>
          <Link href="/login" className="gradient-button inline-block">
            Sign In
          </Link>
        </div>
      </Layout>
    );
  }

  if (isLoading) {
    return <Layout><div>Loading...</div></Layout>;
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold gradient-text mb-8">Shopping Cart</h1>

        {items.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-400 text-lg mb-6">Your cart is empty</p>
            <Link href="/products" className="gradient-button inline-flex items-center gap-2">
              Continue Shopping
              <FiArrowRight />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {items.map((item, index) => (
                <motion.div
                  key={item.id}
                  className="glass p-4 rounded-2xl flex gap-4"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {/* Product Image */}
                  <div className="w-24 h-24 rounded-lg overflow-hidden flex-shrink-0 bg-slate-700">
                    {item.product_detail?.image_url ? (
                      <ProductImage
                        src={item.product_detail.image_url}
                        alt={item.product_detail?.name}
                        width={96}
                        height={96}
                        className="w-full h-full object-cover"
                        fallbackSrc="/images/default-product.png"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-slate-500 text-xs">
                        No Image
                      </div>
                    )}
                  </div>

                  {/* Product Info */}
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-100 truncate">
                      {item.product_detail?.name}
                    </h3>
                    <p className="text-sm text-neon-cyan">
                      ${item.product_detail?.discounted_price || item.price_at_addition}
                    </p>

                    {/* Quantity Controls */}
                    <div className="flex items-center gap-2 mt-3">
                      <button
                        onClick={() => updateQuantity(item.product_detail.id, item.quantity - 1)}
                        className="px-2 py-1 glass rounded hover:bg-white/15"
                      >
                        −
                      </button>
                      <span className="w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.product_detail.id, item.quantity + 1)}
                        className="px-2 py-1 glass rounded hover:bg-white/15"
                      >
                        +
                      </button>
                    </div>
                  </div>

                  {/* Price & Remove */}
                  <div className="text-right flex flex-col justify-between">
                    <div className="text-lg font-bold text-neon-cyan">
                      ${item.total_price}
                    </div>
                    <button
                      onClick={() => removeFromCart(item.product_detail.id)}
                      className="p-2 text-red-400 hover:bg-red-900/20 rounded-lg transition-smooth"
                    >
                      <FiTrash2 />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Order Summary */}
            <div className="glass p-6 rounded-2xl h-fit sticky top-20 space-y-4">
              <h2 className="text-2xl font-bold text-slate-100">Order Summary</h2>

              <div className="space-y-3 border-t border-white/10 pt-4">
                <div className="flex justify-between text-slate-300">
                  <span>Subtotal ({totalItems} items)</span>
                  <span>${totalPrice?.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Shipping</span>
                  <span>$0.00</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Tax</span>
                  <span>${(totalPrice * 0.1).toFixed(2)}</span>
                </div>
              </div>

              <div className="border-t border-white/10 pt-4 flex justify-between text-lg font-bold">
                <span>Total</span>
                <span className="text-neon-cyan">${(totalPrice * 1.1).toFixed(2)}</span>
              </div>

              <button
                onClick={handleCheckout}
                className="w-full gradient-button py-3 rounded-lg font-semibold mt-4"
              >
                Proceed to Checkout
              </button>

              <Link href="/products" className="w-full block text-center glass py-2 rounded-lg hover:bg-white/15">
                Continue Shopping
              </Link>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
