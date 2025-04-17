# Frontend using the latest Next.js

## Architecture

- Use the latest version of Next.js for frontend development
- Make REST API calls to `/api/`

## 1. Project Initialization

1. **Bootstrapping**  
   ```bash
   npx create-next-app@latest my‑app \
     --typescript \
     --app \
     --eslint \
     --tailwind \
     --import-alias="@/*"
   cd my‑app
   ```
   - `--app` => use the App Router  
   - `--import-alias="@/*"` => sets up `@/` → `frontend/`

2. **Make it Client‑Only**  
   In `next.config.js`, force static export and disable SSR:
   ```js
   /** @type {import('next').NextConfig} */
   const nextConfig = {
     output: 'export',
     experimental: { outputStandalone: true },
     // optional: disable built‑in SSR routes
     // experimental: { appDir: true, serverActions: false },
   }
   module.exports = nextConfig
   ```

3. **Scripts** (in `package.json`)  
   ```jsonc
   {
     "scripts": {
       "dev": "next dev",
       "build": "next build && next export",
       "start": "next start",
       "lint": "next lint"
     }
   }
   ```

---

## 2. Folder & File Layout

Use a **feature‑first** organization under `src/`:

```
src/
├── app/                   ← Next.js App Router
│   ├── layout.tsx         ← root HTML + providers
│   ├── page.tsx           ← home page
│   └── about/             ← example sub‑route
│       └── page.tsx
├── components/            ← reusable UI (atoms → molecules → organisms)
│   ├── Button/            ← each component in its own folder
│   │   ├── index.tsx
│   │   └── styles.module.css
│   └── ...
├── services/              ← thin HTTP‑client layer (REST calls)
│   └── api.ts
├── hooks/                 ← custom React hooks (data fetching, etc.)
│   └── useItems.ts
├── utils/                 ← general helpers (formatters, constants)
│   └── formatDate.ts
├── styles/                ← global CSS/Tailwind config overrides
│   └── globals.css
└── types/                 ← shared TypeScript types & interfaces
    └── item.ts
```

---

## 3. TypeScript & Path Aliases

1. **frontend/tsconfig.json** already includes:
   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"]
       }
     }
   }
   ```
2. Now you can import via:
   ```ts
   import { Item } from '@/types/item'
   import api from '@/services/api'
   import Button from '@/components/Button'
   ```

---

## 4. API Service Layer

Create `frontend/src/services/api.ts`:

```ts
// frontend/src/services/api.ts
import axios from 'axios'

const server = process.env.NEXT_PUBLIC_API_BASE_URL || ''

export const apiClient = axios.create({
  baseURL: `${server}/api`,
  headers: { 'Content-Type': 'application/json' },
})

// example endpoint
export async function fetchItems(): Promise<Item[]> {
  const { data } = await apiClient.get<Item[]>('/items')
  return data
}
```

- **Env var**: put `NEXT_PUBLIC_API_BASE_URL=https://your-domain.com` in `.env.local`

---

## 5. Data Fetching & State

Use a React‑friendly data‑fetching lib (e.g. SWR):

```bash
npm install swr
```

```ts
// frontend/src/hooks/useItems.ts
'use client'
import useSWR from 'swr'
import { fetchItems } from '@/services/api'
import type { Item } from '@/types/item'

export function useItems() {
  const { data, error, isLoading } = useSWR<Item[]>('items', fetchItems)
  return { items: data, error, isLoading }
}
```

---

## 6. Component Organization

Follow **atomic design**:

- **Atoms**: Buttons, Inputs, Icons  
- **Molecules**: FormField (Label + Input), ItemCard  
- **Organisms**: ItemList, Navbar, Footer  

Each in its own folder:

```
components/
└── ItemCard/
    ├── index.tsx
    └── styles.module.css
```

Inside each `index.tsx`:

```tsx
'use client'
import styles from './styles.module.css'

export interface ItemCardProps { /* ... */ }

export default function ItemCard({ /* props */ }: ItemCardProps) {
  return (
    <div className={styles.card}>
      {/* render item */}
    </div>
  )
}
```

---

## 7. Styling

- **Tailwind CSS** (already set up by `create-next-app`)  
- **Component CSS Modules** for scoped overrides  
- **Global resets** in `styles/globals.css`

---

## 8. Layout & Routing

In `frontend/src/app/layout.tsx`:

```tsx
'use client'
import '@/styles/globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {/* <Navbar /> */}
        <main>{children}</main>
        {/* <Footer /> */}
      </body>
    </html>
  )
}
```

Each `page.tsx` is client‑only by default when you include `use client` in components that need hooks.

---

## 9. Build & Deployment

- **Local dev**: `npm run dev`  
- **Production build**: `npm run build` (→ static export under `out/`)  
- Serve with any static host (Vercel, Netlify, S3 + CloudFront).

---

## 10. Linting & Formatting

- **ESLint**: built‑in, with Next.js plugin  
- **Prettier**: add `.prettierrc` for consistent code style  
- **Husky + lint‑staged** for pre‑commit checks

---

## 11. CI/CD (optional)

Example **GitHub Actions** workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with: { node-version: '18' }
      - run: npm ci
      - run: npm run build
      - run: npm run export
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          publish_dir: ./out
```

---

## 12. Additional Best Practices

- **Type everything** (interfaces for API data)  
- **Error boundaries** for components  
- **Feature flags** / config via `next.config.js` or env vars  
- **Accessibility**: use semantic HTML + aria‑labels  
- **Testing**: add Jest + React Testing Library  