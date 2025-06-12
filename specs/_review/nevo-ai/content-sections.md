# Section-Based Content Management for Nevo.ai

## Overview

The Nevo.ai site uses a section-based content management system that allows you to target specific areas of a template with different content blocks. This provides more flexibility than a single content stream and helps maintain the design structure of the site while allowing content updates.

## How It Works

Sections are defined in markdown files using HTML comments with a specific format:

```markdown
<!-- section: section-name -->
Your content here (can be markdown or HTML)
<!-- /section -->
```

The static site generator extracts these sections and makes them available to the templates. If a section is not defined in the content file, the template will use default content if available.

## Available Section Names

### Home Page Sections

| Section Name | Description |
|--------------|-------------|
| `power-title` | Title for the Power of AI section |
| `power-intro` | Introductory text for the Power of AI section |
| `power-grid` | Grid items for the Power of AI section |
| `power-conclusion` | Conclusion text for the Power of AI section |
| `journey-intro` | Introduction text for the Journey section |
| `journey-steps` | Step items for the Journey section |
| `process-intro` | Introduction text for the Process section |
| `process-timeline` | Timeline items for the Process section |
| `services-tabs` | Content for the Services tabs |
| `testimonials` | Testimonial items |
| `final-cta` | Call to action section at the bottom |

### Regular Page Sections

| Section Name | Description |
|--------------|-------------|
| `page-intro` | Introductory panel at the top of the page |
| `main` | Main content section |
| `benefits` | Benefits/features section |
| `timeline` | Process timeline section |
| `features` | Features/outcomes section |
| `testimonials` | Testimonials section |
| `cta` | Call to action section at the bottom |

## Example Usage

Here's an example of how to structure content for a regular page:

```markdown
---
title: Educate
url: /educate.html
description: AI education services
subtitle: Empower Your Team with AI Knowledge
pageClass: educate-page
order: 2
ctaTitle: Ready to implement AI?
ctaText: Let's make AI your competitive edge
ctaButton: Explore Embracing AI
ctaLink: embrace.html
---

<!-- section: page-intro -->
<div class="intro-panel">
  <div class="intro-content">
    <p class="tagline"><strong>Unlock AI's Potential</strong></p>
    <p>The journey to an AI-first organization begins with education.</p>
  </div>
</div>
<!-- /section -->

<!-- section: main -->
## Main Content Heading

This is the main content section. You can use Markdown here.
<!-- /section -->

<!-- section: benefits -->
<div class="benefits-grid">
  <div class="benefit-card">
    <h4>Benefit 1</h4>
    <p>Description here.</p>
  </div>
  <div class="benefit-card">
    <h4>Benefit 2</h4>
    <p>Description here.</p>
  </div>
</div>
<!-- /section -->

<!-- section: cta -->
<h2>Custom CTA Heading</h2>
<p>This will override the frontmatter CTA settings.</p>
<a href="contact.html" class="btn btn-primary">Contact Us</a>
<!-- /section -->
```

## Homepage Sections Example

For the homepage, you would use the home-specific sections:

```markdown
---
title: Home
url: /
description: Nevo.ai helps forward-thinking organizations harness AI
keywords: AI, artificial intelligence, business strategy
isHomepage: true
heroTitle: Pioneering the AI Revolution
heroSubtitle: Transform your business through strategic AI
heroCTAText: Discover Your AI Potential
heroCTALink: educate.html
order: 1
---

<!-- section: power-intro -->
AI isn't just another technology trend—it's fundamentally reshaping business across all industries.
<!-- /section -->

<!-- section: power-grid -->
<div class="grid-item feature-card">
  <div class="card-icon">
    <div class="icon-data"></div>
  </div>
  <h3>Data Analysis</h3>
  <p>Analyze complex data sets with unprecedented speed and accuracy.</p>
</div>

<div class="grid-item feature-card">
  <div class="card-icon">
    <div class="icon-process"></div>
  </div>
  <h3>Process Automation</h3>
  <p>Automate routine tasks and workflows to increase efficiency.</p>
</div>
<!-- /section -->
```

## Fallbacks and Defaults

If a section is not defined in the content file, the template will use default content if available. For example, if you don't define a `cta` section, the template will use the CTA information from the frontmatter (ctaTitle, ctaText, etc.).

## Technical Details

The section extraction process happens in the `extractContentSections` function in the `generator.js` file. Sections are extracted using a regular expression that matches the HTML comments format.

Each section's content is then processed (converting markdown to HTML if needed) and passed to the template as a property of the `sections` object. The template can then use the sections as needed, with fallbacks for missing sections.

## Best Practices

1. **Be consistent with section names** - Use the standard section names listed above to ensure templates work correctly.

2. **Use HTML for complex layouts** - When you need precise control over layout, use HTML within the section. Markdown is fine for simple content.

3. **Include all required sections** - Make sure to include all sections that are needed for the page type you're working with.

4. **Test your changes** - Always run the build after making changes to see how they appear in the browser.

5. **Maintain HTML structure** - When editing HTML sections, be careful to maintain the correct structure and class names to preserve styling.