// ============================================
// API Configuration & Utilities
// ============================================
// Configure axios and API endpoints

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API Endpoints
export const endpoints = {
  // Auth
  auth: {
    register: '/auth/register/',
    login: '/auth/login/',
    logout: '/auth/logout/',
    googleLogin: '/auth/google_login/',
    profile: '/profile/me/',
    updateProfile: '/profile/update_profile/',
    changePassword: '/profile/change_password/',
    addresses: '/addresses/',
    preferences: '/preferences/',
  },

  // Products
  products: {
    list: '/products/',
    detail: (slug) => `/products/${slug}/`,
    categories: '/products/categories/',
    brands: '/products/brands/',
    featured: '/products/featured/',
    reviews: (slug) => `/products/${slug}/reviews/`,
    related: (slug) => `/products/${slug}/related/`,
  },

  // Cart & Wishlist
  cart: {
    view: '/cart/view/',
    add: '/cart/add/',
    remove: '/cart/remove/',
    update: '/cart/update/',
    clear: '/cart/clear/',
  },
  
  wishlist: {
    view: '/cart/wishlist/view/',
    add: '/cart/wishlist/add/',
    remove: '/cart/wishlist/remove/',
    isInWishlist: '/cart/wishlist/is_in_wishlist/',
  },

  // Orders
  orders: {
    list: '/orders/',
    create: '/orders/create_guest_order/',
    detail: (id) => `/orders/${id}/`,
    cancel: (id) => `/orders/${id}/cancel/`,
    tracking: (id) => `/orders/${id}/tracking/`,
    requestReturn: (id) => `/orders/${id}/request_return/`,
  },

  // Reviews
  reviews: {
    list: '/reviews/',
    create: '/reviews/',
    detail: (id) => `/reviews/${id}/`,
    markHelpful: (id) => `/reviews/${id}/mark_helpful/`,
    markUnhelpful: (id) => `/reviews/${id}/mark_unhelpful/`,
  },

  // Payments
  payments: {
    validateCoupon: '/payments/validate_coupon/',
    applyCoupon: '/payments/apply_coupon/',
    coupons: '/payments/coupons/',
    activeCoupons: '/payments/coupons/active/',
  },
};

export default apiClient;
