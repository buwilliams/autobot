# Phase 2 – Projects & Phases CRUD

- **Models:** Project (name, description, metadata, owner_id), Phase (project_id, title, ordinal).
- **API:**
  - CRUD /projects
  - Nested CRUD /projects/:projectId/phases
  - POST /projects/:projectId/transfer-ownership
- **UI:**
  - Project list & “New Project”
  - Project detail → Phases list + “Add Phase”
