// ============================================
// PRODUCTS PAGE
// ============================================
// Product listing with filters and search

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import ProductCard from '@/components/ProductCard';
import { SkeletonGrid } from '@/components/Skeleton';
import apiClient, { endpoints } from '@/utils/api';
import { FiFilter, FiX } from 'react-icons/fi';

export default function ProductsPage() {
  const router = useRouter();
  const { search, category, brand, page = 1 } = router.query;

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState(category || '');
  const [priceRange, setPriceRange] = useState({ min: 0, max: 10000 });
  const [showFilters, setShowFilters] = useState(false);

  // Fetch products
  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        const params = {
          page,
          page_size: 12,
        };

        if (search) params.search = search;
        if (selectedCategory) params.category__id = selectedCategory;
        if (priceRange.min) params.price__gte = priceRange.min;
        if (priceRange.max) params.price__lte = priceRange.max;

        const response = await apiClient.get(endpoints.products.list, { params });
        // Handle both paginated and non-paginated data
        setProducts(response.data.results || response.data || []);
        setTotalPages(response.data.count ? Math.ceil(response.data.count / 12) : 1);
      } catch (error) {
        console.error('Failed to fetch products:', error);
        setProducts([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [search, selectedCategory, priceRange, page]);

  // Fetch categories and brands
  useEffect(() => {
    const fetchCategoriesAndBrands = async () => {
      try {
        const [categoriesRes, brandsRes] = await Promise.all([
          apiClient.get(endpoints.products.categories),
          apiClient.get(endpoints.products.brands),
        ]);
        
        // Safety check for categories and brands data structure
        const catData = categoriesRes.data.results || categoriesRes.data;
        setCategories(Array.isArray(catData) ? catData : []);

        const brandData = brandsRes.data.results || brandsRes.data;
        setBrands(Array.isArray(brandData) ? brandData : []);
        
      } catch (error) {
        console.error('Failed to fetch categories/brands:', error);
        setCategories([]);
        setBrands([]);
      }
    };

    fetchCategoriesAndBrands();
  }, []);

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold gradient-text mb-2">Products</h1>
          <p className="text-slate-400">
            {search ? `Search results for "${search}"` : 'Browse our collection'}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className={`${showFilters ? 'block' : 'hidden'} lg:block lg:col-span-1`}>
            <div className="glass p-6 rounded-2xl space-y-6">
              {/* Filter Header */}
              <div className="flex items-center justify-between lg:hidden">
                <h3 className="text-lg font-semibold">Filters</h3>
                <button onClick={() => setShowFilters(false)} className="text-slate-400">
                  <FiX size={24} />
                </button>
              </div>

              {/* Category Filter */}
              <div>
                <h4 className="font-semibold text-slate-100 mb-3">Category</h4>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="category"
                      value=""
                      checked={!selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="w-4 h-4"
                    />
                    <span className="text-slate-300">All Categories</span>
                  </label>
                  
                  {/* categories.map fixed with Array check */}
                  {Array.isArray(categories) && categories.map((cat) => (
                    <label key={cat.id} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="category"
                        value={cat.id}
                        checked={selectedCategory === `${cat.id}`}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-4 h-4"
                      />
                      <span className="text-slate-300">{cat.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Price Range Filter */}
              <div>
                <h4 className="font-semibold text-slate-100 mb-3">Price Range</h4>
                <div className="space-y-3">
                  <div>
                    <label className="text-sm text-slate-400 mb-1 block">Min: ${priceRange.min}</label>
                    <input
                      type="range"
                      min="0"
                      max="10000"
                      value={priceRange.min}
                      onChange={(e) => setPriceRange({ ...priceRange, min: parseInt(e.target.value) })}
                      className="w-full"
                    />
                  </div>
                  <div>
                    <label className="text-sm text-slate-400 mb-1 block">Max: ${priceRange.max}</label>
                    <input
                      type="range"
                      min="0"
                      max="10000"
                      value={priceRange.max}
                      onChange={(e) => setPriceRange({ ...priceRange, max: parseInt(e.target.value) })}
                      className="w-full"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Products Grid */}
          <div className="lg:col-span-3">
            {/* Filter Toggle Button */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="lg:hidden mb-6 flex items-center gap-2 glass px-4 py-2 rounded-lg"
            >
              <FiFilter size={20} />
              Filters
            </button>

            {/* Products */}
            {isLoading ? (
              <SkeletonGrid count={12} />
            ) : products.length > 0 ? (
              <>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {products.map((product) => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="mt-12 flex justify-center gap-2">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                      <button
                        key={p}
                        onClick={() => router.push({ query: { ...router.query, page: p } })}
                        className={`px-4 py-2 rounded-lg transition-smooth ${
                          parseInt(page) === p
                            ? 'bg-gradient-neon text-white'
                            : 'glass hover:bg-white/15'
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-slate-400 text-lg">No products found</p>
                <button
                  onClick={() => router.push('/products')}
                  className="text-neon-cyan hover:text-neon-blue mt-4"
                >
                  View all products
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}