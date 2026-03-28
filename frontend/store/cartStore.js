// ============================================
// Cart Store (Zustand)
// ============================================
// State management for shopping cart

import { create } from 'zustand';
import apiClient, { endpoints } from '../utils/api';

export const useCartStore = create((set, get) => ({
  // State
  items: [],
  totalPrice: 0,
  totalItems: 0,
  isLoading: false,

  // Initialize/Fetch cart
  fetchCart: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get(endpoints.cart.view);
      const { items, total_price, total_items } = response.data;
      set({
        items: items || [],
        totalPrice: total_price,
        totalItems: total_items,
        isLoading: false,
      });
      return response.data;
    } catch (error) {
      set({ isLoading: false });
      return null;
    }
  },

  // Add to cart
  addToCart: async (productId, quantity = 1) => {
    set({ isLoading: true });
    try {
      await apiClient.post(endpoints.cart.add, {
        product_id: productId,
        quantity,
      });
      // Refresh cart
      await get().fetchCart();
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: error.response?.data?.error || 'Failed to add item' };
    }
  },

  // Remove from cart
  removeFromCart: async (productId) => {
    set({ isLoading: true });
    try {
      await apiClient.post(endpoints.cart.remove, { product_id: productId });
      await get().fetchCart();
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: 'Failed to remove item' };
    }
  },

  // Update quantity
  updateQuantity: async (productId, quantity) => {
    try {
      await apiClient.post(endpoints.cart.update, {
        product_id: productId,
        quantity,
      });
      await get().fetchCart();
      return { success: true };
    } catch (error) {
      return { success: false, error: 'Failed to update quantity' };
    }
  },

  // Clear cart
  clearCart: async () => {
    set({ isLoading: true });
    try {
      await apiClient.post(endpoints.cart.clear);
      set({ items: [], totalPrice: 0, totalItems: 0, isLoading: false });
      return { success: true };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: 'Failed to clear cart' };
    }
  },
}));
