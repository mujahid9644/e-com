// ============================================
// Authentication Store (Zustand)
// ============================================
// State management for authentication

import { create } from 'zustand';
import apiClient, { endpoints } from '../utils/api';

export const useAuthStore = create((set) => ({
  user: null,
  tokens: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  // Initialize from localStorage
  initAuth: () => {
    if (typeof window !== 'undefined') {
      const savedUser = localStorage.getItem('user');
      const savedTokens = localStorage.getItem('tokens');
      
      if (savedUser && savedTokens) {
        set({
          user: JSON.parse(savedUser),
          tokens: JSON.parse(savedTokens),
          isAuthenticated: true,
        });
      }
    }
  },

  // Register
  register: async (email, username, password, first_name = '') => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(endpoints.auth.register, {
        email,
        username,
        first_name,
        password,
        password_confirm: password,
      });
      
      const { user, tokens } = response.data;
      
      // Save to localStorage
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('tokens', JSON.stringify(tokens));
      localStorage.setItem('access_token', tokens.access);
      
      set({
        user,
        tokens,
        isAuthenticated: true,
        isLoading: false,
      });
      
      return { success: true, data: user };
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed';
      set({ error: message, isLoading: false });
      return { success: false, error: message };
    }
  },

  // Login
  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(endpoints.auth.login, {
        email,
        password,
      });
      
      const { user, tokens } = response.data;
      
      // Save to localStorage
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('tokens', JSON.stringify(tokens));
      localStorage.setItem('access_token', tokens.access);
      
      set({
        user,
        tokens,
        isAuthenticated: true,
        isLoading: false,
      });
      
      return { success: true, data: user };
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed';
      set({ error: message, isLoading: false });
      return { success: false, error: message };
    }
  },

  // Google OAuth Login
  googleLogin: async (idToken) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(endpoints.auth.googleLogin, {
        id_token: idToken,
      });
      
      const { user, tokens } = response.data;
      
      // Save to localStorage
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('tokens', JSON.stringify(tokens));
      localStorage.setItem('access_token', tokens.access);
      
      set({
        user,
        tokens,
        isAuthenticated: true,
        isLoading: false,
      });
      
      return { success: true, data: user };
    } catch (error) {
      const message = error.response?.data?.detail || 'Google login failed';
      set({ error: message, isLoading: false });
      return { success: false, error: message };
    }
  },

  // Logout
  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('tokens');
    localStorage.removeItem('access_token');
    
    set({
      user: null,
      tokens: null,
      isAuthenticated: false,
    });
  },

  // Get current user profile
  getProfile: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get(endpoints.auth.profile);
      set({ user: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      return null;
    }
  },

  // Update profile
  updateProfile: async (data) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.patch(endpoints.auth.updateProfile, data);
      set({ user: response.data, isLoading: false });
      localStorage.setItem('user', JSON.stringify(response.data));
      return { success: true, data: response.data };
    } catch (error) {
      set({ isLoading: false });
      return { success: false, error: error.message };
    }
  },

  // Clear error
  clearError: () => set({ error: null }),
}));

export default useAuthStore;
