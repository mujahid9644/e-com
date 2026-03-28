# E-Commerce Frontend Setup Guide

## Overview

This is a modern Next.js frontend for a full-featured e-commerce platform with:
- Glassmorphism UI design
- Smooth animations with Framer Motion
- State management with Zustand
- Product catalog with filtering
- Shopping cart & wishlist
- User authentication
- Responsive design for mobile/tablet/desktop

## Prerequisites

- Node.js 16+ & npm/yarn
- Next.js 13+
- Git

## Installation & Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables

```bash
# Create .env.local file
cp .env.example .env.local

# Edit .env.local with your backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Run Development Server

```bash
npm run dev
# or
yarn dev
```

Frontend will be available at: http://localhost:3000

## Project Structure

```
frontend/
├── pages/                  # Next.js pages
│   ├── index.jsx          # Home page
│   ├── products.jsx       # Products listing
│   ├── login.jsx          # Login page
│   ├── cart.jsx           # Shopping cart
│   └── ...
├── components/            # Reusable React components
│   ├── Layout.jsx         # Main layout wrapper
│   ├── Header.jsx         # Navigation header
│   ├── ProductCard.jsx    # Product display card
│   ├── Footer.jsx         # Footer component
│   └── ...
├── store/                 # Zustand state management
│   ├── authStore.js       # Authentication state
│   ├── cartStore.js       # Cart state
│   └── ...
├── utils/                 # Utility functions
│   ├── api.js             # API client configuration
│   └── ...
├── styles/                # CSS & styling
│   ├── globals.css        # Global styles & glassmorphism
│   └── ...
├── public/                # Static assets
├── package.json           # Dependencies
├── next.config.js         # Next.js configuration
└── tailwind.config.js     # Tailwind CSS configuration
```

## Key Technologies

### Frontend Framework
- **Next.js 14**: React framework with SSR and static generation
- **React 18**: UI library

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Glassmorphism**: Frosted glass effect styling

### Animations
- **Framer Motion**: Smooth, production-ready animations

### State Management
- **Zustand**: Lightweight state management

### API Communication
- **Axios**: HTTP client for API requests

### Icons
- **React Icons**: Icon library with multiple icon sets

## Available Pages

### Public Pages
- `/` - Home page with featured products
- `/products` - Products listing with filters
- `/login` - User login
- `/signup` - User registration

### Protected Pages (Requires Authentication)
- `/dashboard` - User dashboard
- `/profile` - User profile management
- `/cart` - Shopping cart
- `/checkout` - Order checkout
- `/orders` - Order history
- `/wishlist` - Wishlist items

## Components

### Layout Component
Main wrapper for all pages with header and footer.

### Header Component
Navigation bar with:
- Logo and branding
- Search functionality
- Cart icon with badge
- User menu
- Mobile hamburger menu

### ProductCard Component
Displays product information with:
- Product image
- Price with discount badge
- Ratings and reviews count
- Add to cart button
- Wishlist button
- Hover animations

### SearchBar Component
Search functionality to find products by keyword.

### Footer Component
Footer with links, company info, and copyright.

## State Management with Zustand

### Auth Store (`authStore.js`)
Manages user authentication state:
```javascript
const { user, isAuthenticated, login, register, logout } = useAuthStore();
```

### Cart Store (`cartStore.js`)
Manages shopping cart:
```javascript
const { items, totalPrice, addToCart, removeFromCart } = useCartStore();
```

## API Integration

### Configuration (`utils/api.js`)
```javascript
import apiClient, { endpoints } from '@/utils/api';

// Add to cart
await apiClient.post(endpoints.cart.add, { product_id: 1, quantity: 1 });

// Logout
await apiClient.post(endpoints.auth.logout);
```

### Axios Interceptors
- Automatically adds JWT token to requests
- Handles authentication headers
- Error handling (can be extended)

## Styling Guide

### Glassmorphism Classes
```html
<!-- Basic glass effect -->
<div class="glass">...</div>

<!-- Dark glass effect -->
<div class="glass-dark">...</div>

<!-- Hover effect -->
<div class="glass-hover">...</div>

<!-- Neon border -->
<div class="neon-border">...</div>
```

### Colors & Gradients
```css
/* Neon colors */
@apply text-neon-blue      /* Cyan blue (#00D9FF) */
@apply text-neon-purple    /* Purple (#FF00FF) */
@apply text-neon-pink      /* Pink (#FF006E) */

/* Gradient text */
<span class="gradient-text">Premium Quality</span>

/* Gradient button */
<button class="gradient-button">Click Me</button>
```

### Animations
```css
/* Fade in */
@apply animate-fade-in

/* Slide up */
@apply animate-slide-up

/* Pulse neon effect */
@apply animate-pulse-neon
```

## Common Tasks

### Add Authentication to a Component
```javascript
'use client';

import { useAuthStore } from '@/store/authStore';

export default function ProfileComponent() {
  const { user, isAuthenticated, logout } = useAuthStore();
  
  if (!isAuthenticated) {
    return <p>Please login</p>;
  }
  
  return <button onClick={logout}>Logout</button>;
}
```

### Fetch Products with Filters
```javascript
import apiClient, { endpoints } from '@/utils/api';

const response = await apiClient.get(endpoints.products.list, {
  params: {
    search: 'laptop',
    category__id: 1,
    price__gte: 100,
    price__lte: 1000,
    ordering: '-price',
    page: 1
  }
});
```

### Add to Cart
```javascript
import { useCartStore } from '@/store/cartStore';

export default function ProductPage() {
  const { addToCart } = useCartStore();
  
  const handleAddToCart = async () => {
    await addToCart(productId, quantity);
  };
}
```

## Building for Production

### Build the Application
```bash
npm run build
# or
yarn build
```

### Test Production Build
```bash
npm run start
# or
yarn start
```

### Export Static Site
```bash
npm run export
# Creates `/out` directory with static files
```

## Performance Optimization

### Image Optimization
- Use Next.js Image component for automatic optimization
- Images are cached and served efficiently

### Code Splitting
- Next.js automatically splits code per page
- Reduces initial bundle size

### Lazy Loading
- Components can be dynamically imported:
```javascript
import dynamic from 'next/dynamic';

const DynamicComponent = dynamic(() => import('@/components/Heavy'));
```

## Troubleshooting

### API Connection Issues
```bash
# Check if backend is running on localhost:8000
curl http://localhost:8000/api/schema/

# Update NEXT_PUBLIC_API_URL in .env.local if needed
```

### Clear Cache & Rebuild
```bash
# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
npm run dev
```

### Port Already in Use
```bash
# Run on different port
npm run dev -- -p 3001
```

## Deployment

### Vercel (Recommended for Next.js)
1. Push code to GitHub
2. Connect repository to Vercel
3. Configure environment variables
4. Deploy automatically

### Other Hosting
1. Build: `npm run build`
2. Start: `npm run start`
3. Configure server to handle client-side routing

## Environment Variables

### Development
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Production
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Resources

- Next.js: https://nextjs.org/docs
- React: https://react.dev
- Tailwind CSS: https://tailwindcss.com/docs
- Framer Motion: https://www.framer.com/motion/
- Zustand: https://github.com/pmndrs/zustand
- Axios: https://axios-http.com/

---

**Happy Coding!** 🚀
