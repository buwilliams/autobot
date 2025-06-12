# Specification Update from Codebase Changes

## Purpose
Intelligently update an existing application specification by analyzing current codebase changes and merging them with the existing spec. This combines codebase analysis, spec refinement, and preservation of human-crafted content to keep specifications synchronized with evolving codebases while maintaining the value of manual refinements.

## Goals
- Synchronize specifications with current codebase state
- Preserve valuable human refinements and customizations in existing specs
- Identify and incorporate new features, endpoints, and functionality
- Update outdated sections while maintaining spec quality and consistency
- Provide clear indication of what changed during the update process
- Maintain technology-agnostic language and Autobot format standards

## Use Cases
1. **Codebase Evolution**: Update specs after significant development phases
2. **Feature Addition**: Incorporate new features and functionality into existing specs
3. **Architecture Changes**: Reflect structural changes in application design
4. **Synchronization**: Bring specs up-to-date after periods of development without spec updates
5. **Team Handoffs**: Update specs when new team members need current documentation

## Usage Rules
- **Use with extreme caution**: This command can overwrite carefully crafted spec content
- **Always backup existing specs** before running updates
- **Review all changes thoroughly** after update completion
- **Preserve human intent**: Maintain the purpose and goals established in original specs
- **Flag breaking changes**: Clearly indicate when updates contradict existing spec content
- **Maintain quality**: Ensure updated specs meet Autobot standards for AI code generation

## Update Process

### Step 1: Pre-Update Analysis
Before making any changes, analyze:
- Current specification content and structure
- Human-added customizations and refinements
- Critical business logic and requirements documented in spec
- Sections that should be preserved vs. updated
- Codebase changes since last spec update

### Step 2: Codebase Analysis
Perform comprehensive analysis of current codebase:
- New features and functionality not in current spec
- Changed API endpoints or user interfaces
- Modified data models and relationships
- Updated business logic and workflows
- New external integrations or dependencies
- Removed or deprecated functionality

### Step 3: Intelligent Merging
Merge codebase analysis with existing specification:
- **Preserve human intent**: Keep manually crafted Purpose, Goals, and business context
- **Update factual sections**: Refresh endpoints, database schema, and technical details
- **Add new functionality**: Incorporate new features while maintaining spec structure
- **Flag conflicts**: Identify where codebase changes contradict existing spec content
- **Maintain consistency**: Ensure all sections work together cohesively

### Step 4: Quality Enhancement
Apply refinement principles during update:
- Improve clarity and technology-agnostic language
- Ensure consistency across all sections
- Maintain Autobot format standards
- Optimize for AI code generation readiness

## Update Strategy by Section

### Always Preserve (Human Intent)
- **Purpose**: Core application purpose should remain stable
- **Goals**: Business objectives typically don't change with code updates
- **Custom sections**: Specialized sections added for specific requirements

### Update with Caution (Merge Intelligently)
- **Use Cases**: May need new use cases, but preserve existing user workflows
- **Usage Rules**: Update business rules that changed, preserve policy decisions

### Update Actively (Technical Reality)
- **Database Schema**: Reflect current data model and relationships
- **Services**: Update to match current service architecture
- **Endpoints**: Synchronize with current API and route definitions
- **UI Layout**: Update to reflect current interface structure
- **Pages**: Update to match current application navigation

### Context-Dependent Updates
- **Technical Requirements**: Update based on new dependencies or constraints

## Conflict Resolution

When codebase analysis conflicts with existing spec content:

1. **Breaking Changes**: If code contradicts fundamental spec assumptions
   - Flag the conflict clearly in the updated spec
   - Provide both the spec expectation and current code reality
   - Suggest review and manual resolution

2. **Feature Additions**: New functionality not covered in existing spec
   - Integrate seamlessly into appropriate sections
   - Maintain consistency with existing spec style and structure

3. **Feature Removals**: Functionality in spec but not in current code
   - Mark as deprecated or removed
   - Note when the functionality was removed if detectable

4. **Architectural Changes**: Fundamental structural changes
   - Update affected sections to reflect new architecture
   - Preserve business intent while updating technical approach

## Update Instructions

When updating a specification:

1. **Load existing spec**: Parse and understand current specification structure and content
2. **Identify preservation areas**: Mark sections with clear human intent and customization
3. **Perform codebase analysis**: Use codebase-analyzer principles to understand current state
4. **Map changes**: Identify what's new, changed, or removed since spec creation
5. **Intelligent merge**: Combine findings while preserving valuable human content
6. **Apply refinement**: Use spec-refiner principles to enhance the merged result
7. **Flag issues**: Clearly mark any conflicts or areas needing human review
8. **Generate summary**: Provide clear overview of what was changed

## Output Format

The updated specification should include:

```markdown
# [Application Name] Specification

<!-- UPDATE SUMMARY: Generated on [DATE] -->
<!-- CHANGES: [Brief summary of major changes made] -->
<!-- CONFLICTS: [Any conflicts that need human review] -->
<!-- PRESERVED: [Key sections that were intentionally preserved] -->

[Standard Autobot specification sections with updates applied]

## Update Notes
### Changes Made
- [List of significant changes during this update]
- [New features or functionality added]
- [Updated sections and why]

### Conflicts Detected
- [Any areas where code contradicts existing spec]
- [Items requiring manual review and resolution]

### Preserved Content
- [Human-crafted content that was intentionally preserved]
- [Custom sections or business logic maintained]
```

## Safety Guidelines

### Pre-Update Precautions
- Always create a backup of the existing specification
- Verify the target codebase path is correct
- Ensure you have the latest version of the specification
- Consider the impact on team members who rely on the current spec

### Update Execution
- Run in a controlled environment where changes can be reviewed
- Use the most reliable AI tool available for analysis
- Provide clear path to the target codebase for analysis
- Capture all output and change summaries

### Post-Update Review
- Thoroughly review all changes made to the specification
- Verify that business intent and goals are preserved
- Check that new functionality is accurately represented
- Ensure technical details match current codebase reality
- Test that the updated spec can generate working code

## Quality Checklist

Ensure the updated specification:
- [ ] Preserves the original purpose and business intent
- [ ] Accurately reflects current codebase functionality
- [ ] Maintains technology-agnostic language throughout
- [ ] Follows Autobot format standards appropriately
- [ ] Includes clear documentation of what changed
- [ ] Flags any conflicts between spec and code
- [ ] Provides sufficient detail for AI code generation
- [ ] Maintains internal consistency across all sections
- [ ] Preserves valuable human refinements and customizations
- [ ] Is ready for team review and approval

## Warning Messages

The update command should display prominent warnings:

```
⚠️  CAUTION: WHOLESALE SPEC UPDATE ⚠️

This command will perform a comprehensive update of your specification
based on current codebase analysis. This may overwrite manual refinements
and carefully crafted content.

BEFORE PROCEEDING:
- Backup your current specification
- Ensure team awareness of the update
- Plan time for thorough review of changes
- Consider using 'refine' command for smaller adjustments

This update will:
✓ Analyze current codebase state
✓ Merge findings with existing specification  
✓ Preserve business intent where possible
⚠️ May overwrite technical sections completely
⚠️ May modify carefully crafted content

Continue? (y/N):
```