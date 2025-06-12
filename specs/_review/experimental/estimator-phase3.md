# Phase 3 – Stories & Estimates Basics

- **Models:** Story (phase_id, title, description), Estimate (story_id, user_id, p50, p90, submitted_at).
- **API:**
  - CRUD /projects/:projectId/phases/:phaseId/stories
  - POST /stories/:storyId/estimates (hidden until all devs submit)
  - GET /stories/:storyId/estimates
- **UI:**
  - Story list under each phase with “Add/Edit”
  - Estimate modal on each story (50%/90% inputs)
  - Show count of estimates submitted
