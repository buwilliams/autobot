# Codebase Analysis and Specification Generation

## Purpose
Analyze an existing codebase in a tech-stack agnostic way and generate a comprehensive application specification following the standardized Autobot spec format. The goal is to create a specification that captures the essence, functionality, and requirements of the application without being tied to specific technologies, enabling regeneration with different tech stacks.

## Goals
- Analyze codebase structure, configuration, and patterns to understand application purpose
- Extract business logic and functionality independent of implementation details
- Generate a technology-agnostic specification following the 9-section Autobot format
- Identify core services, data models, and user interactions
- Document current technical stack while focusing on functional requirements
- Create a spec that enables regenerating the application with different technologies

## Use Cases
1. **Legacy Modernization**: Analyze old codebases to create specs for modern rebuilds
2. **Technology Migration**: Document existing apps before migrating to new tech stacks
3. **Documentation Generation**: Create comprehensive specs from underdocumented codebases
4. **Architecture Analysis**: Understand complex applications through systematic analysis

## Usage Rules
- Focus on WHAT the application does, not HOW it's implemented
- Abstract away technology-specific details while preserving functional requirements
- Identify core business rules and data relationships
- Capture user workflows and interaction patterns
- Document external integrations and dependencies conceptually
- Preserve security and performance requirements at a functional level

## Analysis Process

### Step 1: Codebase Discovery
Examine the provided codebase directory structure and identify:
- Project structure and organization patterns
- Configuration files (package.json, requirements.txt, etc.)
- README files and documentation
- Database schema files or model definitions
- API route definitions and endpoints
- Frontend components and page structures
- Test files and examples

### Step 2: Technology Stack Detection
Identify technologies used but focus on their PURPOSE:
- Backend frameworks → API/service layer functionality
- Frontend frameworks → user interface capabilities  
- Databases → data persistence and relationship patterns
- Build tools → deployment and development workflow needs
- Testing frameworks → quality assurance approaches

### Step 3: Functional Analysis
Extract business logic and functionality:
- Core features and capabilities
- User roles and permissions
- Data models and relationships (conceptual, not implementation-specific)
- Business rules and validation logic
- External service integrations (APIs, third-party services)
- Authentication and authorization patterns

### Step 4: User Experience Analysis
Understand user interactions:
- Main user journeys and workflows
- UI patterns and layout structures
- Navigation and information architecture
- Input/output patterns
- Error handling and feedback mechanisms

## Output Specification Format

Generate a complete specification following this exact structure:

```markdown
# [Application Name] Specification

## Purpose
[Clear description of what the application does and why it exists, inferred from README, code comments, and functionality]

## Goals  
- [Primary business objectives derived from analysis]
- [Key functional requirements identified]
- [Performance and scalability considerations]
- [User experience objectives]

## Use Cases
1. **[Primary Use Case]**: [Main user workflow and interaction]
2. **[Secondary Use Case]**: [Supporting functionality]
3. **[Administrative Use Case]**: [Management and configuration tasks]

## Usage Rules
- [Business rules and constraints identified in code]
- [Data validation and integrity requirements]
- [Security and access control requirements]
- [Performance and reliability expectations]

## Database Schema
```sql
-- [Conceptual data model derived from analysis]
-- [Key entities and relationships]
-- [Important constraints and indexes]
```

## Services
- **[Service Name]**: [Core functionality description]
- **[Service Name]**: [Supporting service description]
[Continue for all identified services/modules]

## Endpoints
### API Endpoints
- `[METHOD] [ROUTE]` - [Functional description]
[List all identified endpoints with their purpose]

### Frontend Routes  
- `[ROUTE]` - [Page/component purpose]
[List main application routes and their function]

## UI Layout
### Application Structure
- **[Component]**: [Purpose and functionality]
- **[Component]**: [Purpose and functionality]

### Key Components
[Describe main UI patterns and component types identified]

## Pages
1. **[Page Name]** (`[route]`): [Purpose and functionality]
2. **[Page Name]** (`[route]`): [Purpose and functionality]
[Continue for all main pages/views]

## Technical Requirements

### Functional Requirements
[Technology-agnostic requirements derived from current implementation]

### Integration Requirements  
[External services and APIs that must be supported]

### Performance Requirements
[Performance characteristics observed or configured]

### Security Requirements
[Authentication, authorization, and security patterns identified]

### Migration Notes
- Current technology stack: [detected technologies]
- Key architectural patterns: [identified patterns]
- Critical dependencies: [essential integrations]
- Data migration considerations: [data formats and structures]
```

## Analysis Instructions

When analyzing a codebase:

1. **Start with documentation**: Read README files, comments, and any existing documentation
2. **Examine project structure**: Understand how the application is organized
3. **Identify entry points**: Find main application files, routes, and controllers
4. **Map data flow**: Trace how data moves through the application
5. **Extract business logic**: Focus on WHAT the code does for users
6. **Abstract implementation details**: Describe functionality without tech-specific terms
7. **Identify patterns**: Look for common architectural and design patterns
8. **Consider user perspective**: Think about how users interact with the application

## Output Guidelines

- Use clear, non-technical language for business functionality
- Focus on capabilities rather than implementation details
- Provide enough detail for regenerating core functionality
- Include migration notes for preserving current behavior
- Mark uncertain areas for review and clarification
- Ensure the spec could enable building the same application with completely different technologies

## Quality Checklist

Ensure the generated specification:
- [ ] Follows the exact 9-section Autobot format
- [ ] Describes WHAT the application does, not HOW
- [ ] Is technology-agnostic while preserving functional requirements
- [ ] Includes all major features and capabilities identified
- [ ] Captures user workflows and interaction patterns
- [ ] Documents data relationships conceptually
- [ ] Provides sufficient detail for regeneration
- [ ] Includes notes about current implementation for reference