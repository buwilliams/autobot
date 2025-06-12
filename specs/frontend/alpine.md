# Frontend using the latest Alpine.js

## 1. Project Initialization

1. **Bootstrap with Vite + Vanilla**  
   ```bash
   npm init vite@latest my‑alpine‑app -- --template vanilla
   cd my‑alpine‑app
   npm install
   ```
2. **Install Dependencies**  
   ```bash
   npm install alpinejs
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```
3. **Configure Tailwind** (`frontend/tailwind.config.js`)  
   ```js
   module.exports = {
     content: [
       './index.html',
       './src/**/*.{js,ts,html}',
     ],
     theme: { extend: {} },
     plugins: [],
   }
   ```
4. **Add Tailwind Directives** (`frontend/src/styles.css`)  
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. **Import Styles & Alpine** (`frontend/src/main.js`)  
   ```js
   import 'tailwindcss/tailwind.css'
   import Alpine from 'alpinejs'

   window.Alpine = Alpine
   Alpine.start()
   ```

---

## 2. Folder & File Layout

Use a feature‑first structure under `frontend/src/`:

```
frontend/src/
├── components/         ← reusable UI bits (each with markup + optional JS)
│   ├── ItemCard.html
│   └── Navbar.html
├── services/           ← thin REST client wrappers
│   └── api.js
├── utils/              ← helpers (formatters, constants)
│   └── formatDate.js
├── styles.css          ← Tailwind entrypoint
└── main.js             ← app bootstrap (imports Alpine + styles)
index.html              ← root HTML (loads main.js)
```

---

## 3. Root HTML & Alpine Components

**`index.html`**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>My Alpine App</title>
  <link rel="stylesheet" href="/src/styles.css" />
  <script type="module" src="/src/main.js"></script>
</head>
<body>
  <!-- Example usage of a component -->
  <div x-data="itemsComponent()" class="p-4">
    <template x-for="item in items" :key="item.id">
      <div x-html="renderItemCard(item)"></div>
    </template>
  </div>

  <!-- Include component templates -->
  <template id="item-card">
    <div class="border rounded p-4 mb-2">
      <h2 class="font-bold" x-text="item.title"></h2>
      <p x-text="item.description"></p>
    </div>
  </template>
</body>
</html>
```

- Alpine components live in JS factories (see next).

---

## 4. REST Service Layer

**`frontend/src/services/api.js`**  
```js
const SERVER = import.meta.env.VITE_API_BASE_URL || ''

export async function fetchItems() {
  const res = await fetch(`${SERVER}/api/items`)
  if (!res.ok) throw new Error('Failed to fetch items')
  return res.json()
}

// add more endpoints as needed
```

- **Env var**: add `VITE_API_BASE_URL=https://your-domain.com` to `.env`

---

## 5. Alpine Data Components

Define your interactive widgets in JS.

**`frontend/src/components/itemsComponent.js`**  
```js
import { fetchItems } from '@/services/api.js'
import { renderTemplate } from '@/utils/template.js'

export function itemsComponent() {
  return {
    items: [],
    async init() {
      try {
        this.items = await fetchItems()
      } catch (e) {
        console.error(e)
      }
    },
    renderItemCard(item) {
      // grabs the <template id="item-card"> and fills in `item`
      return renderTemplate('item-card', { item })
    }
  }
}
```

- In `index.html`, you’d import this and attach it:
  ```html
  <script type="module">
    import { itemsComponent } from '/src/components/itemsComponent.js'
    window.itemsComponent = itemsComponent
  </script>
  ```

---

## 6. Template Utility

A small helper to stamp out HTML snippets:

**`frontend/src/utils/template.js`**  
```js
export function renderTemplate(templateId, context = {}) {
  const tpl = document.getElementById(templateId)
  if (!tpl) return ''
  let html = tpl.innerHTML
  // simple context replacement: {{ item.title }}, etc.
  Object.entries(context).forEach(([key, val]) => {
    html = html.replaceAll(new RegExp(`\\b${key}\\b`, 'g'), JSON.stringify(val))
  })
  return html
}
```

*(Or swap in a lightweight templating lib if you prefer.)*

---

## 7. Styling & CSS

- **Tailwind** for utility‑first styling  
- **Component‑scoped CSS** by adding `<style>` blocks inside `<template>` or via separate class files if needed  
- **Global overrides** in `frontend/src/styles.css`

---

## 8. Build & Development

- **Local dev**:  
  ```bash
  npm run dev
  # Vite serves at http://localhost:5173
  ```
- **Production build**:  
  ```bash
  npm run build
  ```
  > outputs to `dist/` by default—just serve that directory as a static site.

---

## 9. Linting & Formatting

- **ESLint** for JS (`npm install -D eslint`)  
- **Prettier** for consistent formatting  
- **Husky + lint‑staged** for pre‑commit checks

---

## 10. Testing (Optional)

- **Jest + Testing Library** for unit tests of your template functions  
- **Playwright/Cypress** for end‑to‑end tests against the running build

---

## 11. CI/CD & Deployment

A simple GitHub Actions workflow:

```yaml
name: Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          publish_dir: ./dist
```

---

## 12. Additional Best Practices

- **Feature‑first modules**: keep related HTML/JS together under `components/`  
- **Semantic HTML** and **ARIA** attributes for accessibility  
- **Error handling** in each Alpine component (`try/catch` around fetch)  
- **Environment flags** via `import.meta.env` for feature toggles  
- **Optimize images** and lazy‑load resources  
- **Document** your component API (attributes, events) in a `README.md`