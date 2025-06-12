# Next.js Frontend Specification

## Purpose
Create a modern, client-side React application using the latest Next.js with App Router, TypeScript, and Tailwind CSS for building scalable frontend applications that consume REST APIs.

## Goals
- Build a responsive, client-side application with Next.js App Router
- Implement clean architecture with feature-first organization
- Achieve type safety with comprehensive TypeScript integration
- Provide efficient data fetching and state management
- Support static export for flexible deployment options

## Use Cases
1. **Interactive Web Application**: Users interact with a dynamic React-based interface
2. **API Integration**: Frontend consumes REST APIs from backend services
3. **Responsive Design**: Application works across desktop, tablet, and mobile devices
4. **Static Deployment**: Application can be deployed as static files to any hosting platform

## Usage Rules
- All API calls must target `/api/` endpoints for backend integration
- Use client-side rendering with static export configuration
- Implement atomic design principles for component organization
- All components must be properly typed with TypeScript
- Follow feature-first directory structure for scalability

## Database Schema
```sql
-- Frontend does not directly interact with database
-- All data access through REST API endpoints
-- API calls target backend services at /api/* routes
```

## Services
- **Next.js Application**: Core React framework with App Router
- **HTTP Client Service**: Axios-based API communication layer
- **Data Fetching Service**: SWR for efficient data fetching and caching
- **Styling Service**: Tailwind CSS with CSS Modules for component styling
- **Build Service**: Static export generation for deployment

## Endpoints
### External API Consumption
- `GET /api/*` - All backend API endpoints
- Frontend makes HTTP requests to backend services
- Environment-configurable API base URL

### Internal Routes (Next.js App Router)
- `/` - Home page
- `/about` - About page (example)
- Dynamic routes based on application requirements

## UI Layout
### Application Structure
- **Header**: Navigation bar with primary menu items
- **Main Content**: Dynamic content area for current page/route
- **Sidebar**: Optional secondary navigation or filters
- **Footer**: Additional links and application information

### Component Hierarchy
- **Atoms**: Button, Input, Icon (basic building blocks)
- **Molecules**: FormField, ItemCard (simple combinations)
- **Organisms**: ItemList, Navbar, Footer (complex components)
- **Templates**: Page layouts and structure
- **Pages**: Specific route implementations

## Pages
1. **Home Page** (`/`): Application landing page with overview
2. **Dashboard** (`/dashboard`): Main application interface
3. **About** (`/about`): Application information and details
4. **404 Page**: Error handling for invalid routes

## Technical Requirements

### Project Initialization
```bash
npx create-next-app@latest my-app \
  --typescript \
  --app \
  --eslint \
  --tailwind \
  --import-alias="@/*"
```

### Project Structure
```
src/
├── app/                   # Next.js App Router
│   ├── layout.tsx         # Root HTML layout + providers
│   ├── page.tsx           # Home page
│   └── about/             # Example sub-route
│       └── page.tsx
├── components/            # Reusable UI components
│   ├── Button/            # Each component in own folder
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── ...
├── services/              # HTTP client layer (REST calls)
│   └── api.ts
├── hooks/                 # Custom React hooks
│   └── useItems.ts
├── utils/                 # General helpers and utilities
│   └── formatDate.ts
├── styles/                # Global CSS and Tailwind config
│   └── globals.css
└── types/                 # Shared TypeScript types
    └── item.ts
```

### Configuration Files

#### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  experimental: { outputStandalone: true },
}
module.exports = nextConfig
```

#### package.json Scripts
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

### API Service Layer
```typescript
// src/services/api.ts
import axios from 'axios'

const server = process.env.NEXT_PUBLIC_API_BASE_URL || ''

export const apiClient = axios.create({
  baseURL: `${server}/api`,
  headers: { 'Content-Type': 'application/json' },
})

export async function fetchItems(): Promise<Item[]> {
  const { data } = await apiClient.get<Item[]>('/items')
  return data
}
```

### Data Fetching with SWR
```typescript
// src/hooks/useItems.ts
'use client'
import useSWR from 'swr'
import { fetchItems } from '@/services/api'
import type { Item } from '@/types/item'

export function useItems() {
  const { data, error, isLoading } = useSWR<Item[]>('items', fetchItems)
  return { items: data, error, isLoading }
}
```

### Component Example
```typescript
// src/components/ItemCard/index.tsx
'use client'
import styles from './styles.module.css'

export interface ItemCardProps {
  item: Item
  onClick: (item: Item) => void
}

export default function ItemCard({ item, onClick }: ItemCardProps) {
  return (
    <div className={styles.card} onClick={() => onClick(item)}>
      <h3>{item.title}</h3>
      <p>{item.description}</p>
    </div>
  )
}
```

### Dependencies
- Next.js (latest) with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Axios for HTTP requests
- SWR for data fetching
- ESLint for code quality
- CSS Modules for component styles

### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Build and Deployment
- Development: `npm run dev`
- Production Build: `npm run build` (generates static files in `out/`)
- Deployment: Compatible with Vercel, Netlify, S3 + CloudFront, or any static hosting
- Client-side only with static export configuration