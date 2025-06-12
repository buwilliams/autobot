 # Project Estimation Web Application Roadmap

 Here’s a revised, feature-driven roadmap now that the full tech stack is in place:

 1. Baseline & Discovery
    - Quick code audit: confirm auth middleware, ORM/models, API structure, front-end routing, real-time infra are wired up.
    - Ensure CI, lint/pre-commit, database migrations, and dev environment are green.

 2. Phase 1 – User & Role Management
    - Data model: Users, Roles (developer), ProjectMembership (owner flag).
    - API:
      - POST /auth/register, /auth/login, /auth/logout
      - GET /users/me
      - PUT /users/:id/role (owner-only)
    - UI:
      - Registration & login forms
      - “My Profile” page
      - Simple RBAC guard on protected routes

 3. Phase 2 – Projects & Phases CRUD
    - Models: Project (name, description, metadata, owner_id), Phase (project_id, title, ordinal).
    - API:
      - CRUD /projects
      - Nested CRUD /projects/:projectId/phases
      - POST /projects/:projectId/transfer-ownership
    - UI:
      - Project list & “New Project”
      - Project detail → Phases list + “Add Phase”

 4. Phase 3 – Stories & Estimates Basics
    - Models: Story (phase_id, title, description), Estimate (story_id, user_id, p50, p90, submitted_at).
    - API:
      - CRUD /projects/:projectId/phases/:phaseId/stories
      - POST /stories/:storyId/estimates (hidden until all devs submit)
      - GET /stories/:storyId/estimates
    - UI:
      - Story list under each phase with “Add/Edit”
      - Estimate modal on each story (50%/90% inputs)
      - Show count of estimates submitted

 5. Phase 4 – Calculation Engine & Project-Level Roll-up
    - Calculation logic:
      - σ_story = (p90 – p50) / 2
      - Σ50 = sum of all p50
      - Σσ = sqrt(sum((p90 – p50)²))
      - MostLikely = Σ50 + 2 × Σσ
      - TotalCost = MostLikely × rate × (1 + ΣadditionalFactors) × calibration
    - API: GET /projects/:projectId/estimate (returns detailed breakdown)
    - UI: Project estimate panel with live numbers and confidence intervals

 6. Phase 5 – Team Collaboration & Owner Selection
    - API:
      - PUT /stories/:storyId/choose-estimate (owner selects final estimate)
      - GET /projects/:projectId/team (members + roles)
      - POST /projects/:projectId/invite (email invite)
    - UI:
      - Team settings page (invite devs, transfer ownership)
      - In-story view: list of submitted estimates + “Use this one” toggle

 7. Phase 6 – Client-Facing Dashboard & Share Links
    - Models: ClientLink (project_id, token, expires_at)
    - API:
      - POST /projects/:projectId/client-link → generate sharing token
      - GET /client/:token/estimate
    - UI: Minimal client view with phase/story toggles and live cost recalculation

 8. Phase 7 – Bulk CSV Import
    - API: POST /projects/:projectId/phases/:phaseId/import (file or text payload)
    - Parser: validate Fibonacci story points, dedupe, return errors/warnings
    - UI: Import modal (upload or paste CSV, preview rows, “Confirm Import”)

 9. Phase 8 – Real-Time Updates (WebSockets)
    - Publish events on key actions: new story/phase, estimate submission, project/estimate update
    - Clients subscribe to events for live UI synchronization

 10. Phase 9 – Testing, Monitoring & Polish
     - Unit & integration tests on APIs and calculation logic
     - E2E smoke tests for core flows (login → create project → estimate → client view)
     - Performance profiling, accessibility audit, UI/UX refinements
     - Instrument analytics (event tracking for share link views, estimate submissions)