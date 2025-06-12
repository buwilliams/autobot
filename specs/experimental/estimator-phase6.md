# Phase 6 – Client-Facing Dashboard & Share Links

- **Models:** ClientLink (project_id, token, expires_at)
- **API:**
  - POST /projects/:projectId/client-link → generate sharing token
  - GET  /client/:token/estimate
- **UI:** Minimal client view with phase/story toggles and live cost recalculation
