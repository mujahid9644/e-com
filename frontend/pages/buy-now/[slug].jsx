import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import Image from 'next/image';
import { FiMinus, FiPlus } from 'react-icons/fi';
import Layout from '@/components/Layout';
import apiClient, { endpoints } from '@/utils/api';

export default function BuyNowPage() {
  const router = useRouter();
  const { slug } = router.query;

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [form, setForm] = useState({
    customer_name: '',
    phone_number: '',
    address: '',
    note: ''
  });

  const fetchProduct = useCallback(async () => {
    if (!slug) return;
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.get(endpoints.products.detail(slug));
      setProduct(response.data);
      setQuantity(1);
    } catch (err) {
      setError('Product not found.');
      setProduct(null);
    } finally {
      setLoading(false);
    }
  }, [slug]);

  useEffect(() => {
    fetchProduct();
  }, [fetchProduct]);

  const handleQuantity = (direction) => {
    if (!product) return;
    const next = quantity + direction;
    if (next >= 1 && next <= product.stock_quantity) {
      setQuantity(next);
    }
  };

  const effectiveUnitPrice = product ? Number(product.discounted_price ?? product.price) || 0 : 0;
  const totalPrice = effectiveUnitPrice * quantity;

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!product) {
      setError('No product selected.');
      return;
    }

    if (!form.customer_name || !form.phone_number || !form.address) {
      setError('Please complete all required fields.');
      return;
    }

    if (quantity < 1 || quantity > product.stock_quantity) {
      setError('Quantity is invalid or out of stock.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const payload = {
        product_id: product.id,
        quantity,
        customer_name: form.customer_name,
        phone_number: form.phone_number,
        address: form.address,
        note: form.note
      };
      const resp = await apiClient.post(endpoints.orders.create, payload);
      setSuccessMessage('Your order has been placed successfully! Order ID: ' + resp.data.order_id);
      setForm({ customer_name: '', phone_number: '', address: '', note: '' });
      setQuantity(1);
      setProduct((prev) => {
        if (!prev) return prev;
        const newStock = Math.max(prev.stock_quantity - quantity, 0);
        return { ...prev, stock_quantity: newStock, is_in_stock: newStock > 0 };
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to place order.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-100 py-16">
          <div className="max-w-5xl mx-auto p-6 bg-white rounded-xl shadow">
            <p>Loading product details...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-100 py-16">
          <div className="max-w-5xl mx-auto p-6 bg-white rounded-xl shadow text-center">
            <h2 className="text-2xl font-bold mb-4">Unable to load product</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <Link href="/products" className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded">Back to Products</Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-slate-800 py-12">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 px-4">
          <div className="bg-gray-900 rounded-xl p-6 shadow">
            <div className="relative w-full h-72 mb-4 bg-gray-700 overflow-hidden rounded-lg border border-gray-200">
              <Image
                src={product.featured_image_url || product.image_url || '/images/placeholder.jpg'}
                alt={product.name || 'Product Image'}
                fill
                className="object-contain"
                onError={(e) => {
                  e.target.src = '/images/placeholder.jpg';
                }}
              />
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight mb-2 text-gray-300">{product.name || 'Unnamed Product'}</h1>
            <p className="text-sm text-blue-600 font-semibold mb-1">{product.category?.name || product.brand?.name || 'No category'}</p>
            <p className="text-sm text-gray-600 mb-3 whitespace-pre-wrap">{product.short_description || product.description || 'No description available.'}</p>
            <div className="flex items-center gap-3 mb-4">
              <div className="text-3xl font-bold text-gray-300">${effectiveUnitPrice.toFixed(2)}</div>
              {Number(product.discounted_price) > 0 && Number(product.discounted_price) < Number(product.price) && (
                <div className="text-gray-400 line-through">${Number(product.price).toFixed(2)}</div>
              )}
            </div>

            <div className="mb-4">
              <span className={product.is_in_stock ? 'text-red-600' : 'text-red-600'}>
                {product.stock_status} ({product.stock_quantity} in stock)
              </span>
            </div>

            <div className="flex items-center gap-2 mb-4">
              <button onClick={() => handleQuantity(-1)} disabled={quantity === 1} className="p-2 bg-green-600 rounded">
                <FiMinus />
              </button>
              <span className="w-16 text-center text-lg">{quantity}</span>
              <button onClick={() => handleQuantity(1)} disabled={quantity >= product.stock_quantity} className="p-2 bg-green-600 rounded">
                <FiPlus />
              </button>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600">Total Price:</p>
              <p className="text-2xl text-gray-300 font-bold">${totalPrice.toFixed(2)}</p>
            </div>
          </div>

          <div className="bg-gray-300 rounded-xl p-6 shadow">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Guest Checkout</h2>
            {successMessage && <div className="mb-4 p-3 bg-green-50 text-green-700 rounded">{successMessage}</div>}
            {error && <div className="mb-4 p-3 bg-red-50 text-red-700 rounded">{error}</div>}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Full Name</label>
                <input required value={form.customer_name} onChange={(e) => setForm({...form, customer_name: e.target.value})} className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="Your name" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                <input required value={form.phone_number} onChange={(e) => setForm({...form, phone_number: e.target.value})} className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="01XXXXXXXXX" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Full Address</label>
                <textarea required value={form.address} onChange={(e) => setForm({...form, address: e.target.value})} rows={4} className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="Shipping address" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Note (optional)</label>
                <textarea value={form.note} onChange={(e) => setForm({...form, note: e.target.value})} rows={3} className="mt-1 block w-full border-gray-300 rounded-md shadow-sm" placeholder="Special instructions" />
              </div>

              <button disabled={isSubmitting || !product.is_in_stock} type="submit" className="w-full inline-flex justify-center items-center px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-base font-semibold disabled:opacity-50">
                {isSubmitting ? 'Placing Order...' : 'Confirm Order'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
}
