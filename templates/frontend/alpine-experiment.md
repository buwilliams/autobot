# Frontend

## Architecture

- Frontend should be fully static with no build process
- Use <script> tags to import UI components
- Use Alpine.js for client-side interactivity
- Make REST API calls to `/api/`
- Components stored in `frontend/components/`

## UI Components

### Organization

- Store common components in `frontend/components/`
- Store feature components in `frontend/features/`
- Store global css in `frontend/css/`
- Store global js in `frontend/js/`

### Loading Components

- Create a custom load() function to load components, and use Alpine.js directives to load them.
- Function stored in `frontend/js/load.js`

```javascript
document.addEventListener('alpine:init', () => {
  // Custom x-load directive
  Alpine.directive('load', (el, { expression }, { evaluate, effect, cleanup }) => {
    const load = async (templateUrl) => {
        try {
            const response = await fetch(templateUrl);
            if (!response.ok) {
                throw new Error(`Failed to load template: ${response.status}`);
            }
            return await response.text();
        } catch (error) {
            console.error('Error loading template:', error);
            return '';
        }
    };

    let templateHtml = '';

    // Create a container for the template content
    const container = document.createElement('div');
    el.appendChild(container);

    // Load and render the template
    const updateTemplate = async () => {
        const url = evaluate(expression);
        templateHtml = await load(url);
        if (templateHtml) {
            container.setAttribute('x-html', templateHtml);
            Alpine.bind(container, {
                'x-data': { templateHtml }
            });
        }
    };

    // Initial load
    updateTemplate();

    // Cleanup when the element is removed
    cleanup(() => {
        container.remove();
    });
  });
});
```

### Alpine.js Syntax

All components use Alpine.js syntax from https://alpinejs.dev/

#### Directives

- x-data
- x-init
- x-show
- x-bind
- x-on
- x-text
- x-html
- x-model
- x-modelable
- x-for
- x-transition
- x-effect
- x-ignore
- x-ref
- x-cloak
- x-teleport
- x-if
- x-id

#### Magics

- $el
- $refs
- $store
- $watch
- $dispatch
- $nextTick
- $root
- $data
- $id

#### Globals

- Alpine.data()
- Alpine.store()
- Alpine.bind()