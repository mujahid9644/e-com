// ============================================
// Wishlist Store (Zustand)
// ============================================
// State management for user wishlist

import { create } from 'zustand';
import apiClient, { endpoints } from '../utils/api';

export const useWishlistStore = create((set, get) => ({
  // State
  items: [],
  count: 0,
  isLoading: false,

  // Initialize/Fetch wishlist
  fetchWishlist: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get(endpoints.wishlist.view);
      const { items } = response.data;
      set({
        items: items || [],
        count: items?.length || 0,
        isLoading: false,
      });
      return response.data;
    } catch (error) {
      set({ isLoading: false });
      return null;
    }
  },

  // Add to wishlist
  addToWishlist: async (productId) => {
    set({ isLoading: true });
    try {
      await apiClient.post(endpoints.wishlist.add, {
        product_id: productId,
      });
      // Refresh wishlist
      await get().fetchWishlist();
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: error.response?.data?.error || 'Failed to add to wishlist' };
    }
  },

  // Remove from wishlist
  removeFromWishlist: async (productId) => {
    set({ isLoading: true });
    try {
      await apiClient.post(endpoints.wishlist.remove, {
        product_id: productId,
      });
      // Refresh wishlist
      await get().fetchWishlist();
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: 'Failed to remove from wishlist' };
    }
  },

  // Check if product is in wishlist
  isInWishlist: async (productId) => {
    try {
      const response = await apiClient.post(endpoints.wishlist.isInWishlist, {
        product_id: productId,
      });
      return response.data.in_wishlist;
    } catch (error) {
      return false;
    }
  },

  // Toggle wishlist (add if not present, remove if present)
  toggleWishlist: async (productId) => {
    const isIn = await get().isInWishlist(productId);
    if (isIn) {
      return await get().removeFromWishlist(productId);
    } else {
      return await get().addToWishlist(productId);
    }
  },
}));