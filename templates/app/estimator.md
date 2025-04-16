# Project Estimation Web Application

## Overview
This specification defines a web-based project estimation tool designed to streamline project planning and cost estimation for development teams and clients. The application prioritizes an elegant, intuitive user experience (UX), a visually appealing user interface (UI), and minimal dependencies. It supports user authentication, project and story management, developer-driven estimation workflows, and client-facing interactive estimate viewing, all with real-time updates.

## Requirements

### User Management
1. **Login & Registration**
   - **Developer**: Full access to create/edit projects, stories, and estimates.
		- Users register with an email and password.
		- Users log in with credentials.
   - **Client**: Does not require authentication. View-only access to estimates via a shared link.

2. **Role-Based Access Control**
   - Developers perform all actions (create, edit, view).
   - Clients view and toggle estimates interactively.
   - One developer "owns" a project and grants access to other developers
   - Owner can transfer ownership to another developer

### Project Management
1. **Add, Edit, and View Projects**
   - Create projects with name, description, and optional metadata (e.g., client name).
   - Edit project details.
   - View projects individually or in a list.

2. **Phases**
   - Projects support multiple phases (default: one phase).
   - Phases contain stories and can be added/edited.

3. **Stories**
   - Stories are tasks within a phase, with title, description, and estimates.
   - Add, edit, and view stories per project/phase.
   - Each developer provides an independent estimate.
   - Owner select estimate to use our of all provided developer estimates.

### Estimation Features
1. **Fine-Grained Cost Estimates**
   - Story-level estimates with 50% and 90% confidence levels.
   - Aggregated into a project-level cost estimate.

2. **Project Estimate Generation**
   - Automatically calculated in real-time (no manual "generate" button).
   - Includes story estimates, additional factors, and blended hourly rate.

3. **Developer Estimation Interface**
   - Assign developers to project as optional or required to provide estimates.
   - Show the number of developers who provided estimates.
   - Show list of developers who have provided estimates.
   - Developers input hidden estimates in story points (1 point = 1 ideal staff day).
   - Shareable estimate link for clients.

### Bulk Story Import
1. **Import Stories to Phase in a Project**
   - Upload a CSV file.
   - Textarea to paste CSV contents into.

### Client Dashboard
1. **View All Estimates**
   - Private link to their dashboard.
   - List of all estimates by order of completion.

2. **View Estimate Details**
   - Select an Estimate.
   - Toggle on/off stories to see price adjustments.
   - Toggle on/off phases to see price adjustments.

## Estimate Calculation Methodology

### Story-Level Estimates
- All estimates, percentages, and sums should be whole numbers
- Two estimates (50%, 90%) in Fibonacci points (0.25, 0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55).
- Hidden until submitted, then reconciled.

### Project-Level Estimate
1. **Uncertainty**
   - `σ = sqrt((90% - 50%)²) / 2`.
2. **Most Likely**
   - `Sum(50%) + 2 * sqrt(Sum((90% - 50%)²))`.
3. **Total Cost**
   - `Most Likely * Hourly Rate * (1 + Sum(Additional Factors))`.
4. **Calibration**
   - Adjustable factor based on team velocity.

### Reference
- *Agile Estimating and Planning*, Chapter 17, Mike Cohn.