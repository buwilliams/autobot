# Phase 1 – User & Role Management

- **Data model:** Users, Roles (developer), ProjectMembership (owner flag).
- **API:**
  - POST /auth/register, /auth/login, /auth/logout
  - GET /users/me
  - PUT /users/:id/role (owner-only)
- **UI:**
  - Registration & login forms
  - “My Profile” page
  - Simple RBAC guard on protected routes
