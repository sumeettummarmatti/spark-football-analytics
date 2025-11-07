import { create } from 'zustand';
import type { User } from '../types';
import { authAPI } from '../services/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: { username: string; email: string; password: string; full_name?: string }) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: async (username: string, password: string) => {
        const response = await authAPI.login(username, password);
        localStorage.setItem('token', response.access_token);
        
        // Fetch user profile
        const user = await authAPI.getMe();
        
        set({
          token: response.access_token,
          user,
          isAuthenticated: true,
        });
      },
      
      register: async (data) => {
        await authAPI.register(data);
        // Auto-login after registration
        await useAuthStore.getState().login(data.username, data.password);
      },
      
      logout: async () => {
        try {
          await authAPI.logout();
        } catch (error) {
          console.error('Logout error:', error);
        }
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },
      
      loadUser: async () => {
        const token = localStorage.getItem('token');
        if (token) {
          try {
            const user = await authAPI.getMe();
            set({
              user,
              token,
              isAuthenticated: true,
            });
          } catch (error) {
            localStorage.removeItem('token');
            set({
              user: null,
              token: null,
              isAuthenticated: false,
            });
          }
        }
      },
    })
);

