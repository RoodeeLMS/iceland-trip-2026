# Document Structure Guide

This guide defines what topics and sections to include in each document type.

---

## Technical Specification Document

### Purpose
Provide complete technical reference for developers and maintainers to understand, troubleshoot, and extend the application.

### Required Sections

#### Front Matter (Unnumbered)
1. **Cover Page**
   - Document title
   - Project/Application name
   - Version number
   - Date
   - Client logo (top-right)
   - Prepared by section (bottom of page)

2. **Version History**
   - Table: Version | Date | Author | Description
   - Track all document revisions

3. **Table of Contents**
   - All major sections with page numbers
   - Dot leaders between title and page number

#### Main Content (Numbered from Page 1)

##### 1. Executive Summary
- Brief overview (1 paragraph)
- Key functionality delivered
- Target users

##### 2. Introduction
- 2.1 Purpose
- 2.2 Scope (what's included/excluded)
- 2.3 Definitions & Acronyms
- 2.4 References (related documents)

##### 3. System Overview
- 3.1 System Architecture
  - Architecture diagram (Mermaid)
  - Component descriptions
  - Technology stack
- 3.2 Application Screens
  - Table: Screen Name | Purpose | Key Features
- 3.3 Integration Points
  - External systems
  - APIs, email, file systems

##### 4. Functional Specifications
For each major function:
- 4.X Function Name
  - 4.X.1 Purpose
  - 4.X.2 User Interface (screenshots if available)
  - 4.X.3 Business Logic
  - 4.X.4 Flow Diagram (Mermaid)
  - 4.X.5 Error Handling

##### 5. Technical Details
- 5.1 Power Automate Flows
  - Table: Flow Name | Trigger | Purpose | Inputs | Outputs
  - Detailed flow diagrams for each
- 5.2 Data Schema
  - Database/SharePoint list schemas
  - Field definitions with types
  - Relationships
- 5.3 Lookup Tables
  - Reference data descriptions
  - Sample data

##### 6. Configuration
- 6.1 Environment Variables
- 6.2 Connection References
- 6.3 Security Settings
- 6.4 Deployment Notes

##### 7. Appendices
- A. Complete Field Reference
- B. Error Codes
- C. Sample Data

---

## User Manual Document

### Purpose
Provide step-by-step instructions for end users to effectively use the application.

### Required Sections

#### Front Matter (Unnumbered)
1. **Cover Page** (same structure as Tech Spec)
2. **Version History**
3. **Table of Contents**

#### Main Content (Numbered from Page 1)

##### 1. Introduction
- 1.1 Purpose of This Manual
- 1.2 Who Should Read This Manual
- 1.3 How to Use This Manual
- 1.4 Getting Help

##### 2. Getting Started
- 2.1 Accessing the Application
  - URL/Link
  - Login requirements
- 2.2 System Requirements
  - Browser compatibility
  - Network requirements
- 2.3 Navigation Overview
  - Main menu description
  - Common icons/buttons

##### 3. Main Features
For each feature/screen:
- 3.X Feature Name
  - 3.X.1 Overview (what it does)
  - 3.X.2 Step-by-Step Instructions
    - Numbered steps with screenshots
  - 3.X.3 Tips & Best Practices
  - 3.X.4 Common Issues

##### 4. Workflows
- 4.1 Complete Workflow Diagrams
  - Visual flow of common tasks
- 4.2 Workflow Descriptions
  - When to use each workflow
  - Prerequisites

##### 5. Reference
- 5.1 Field Descriptions
  - Table of all user-facing fields
- 5.2 Status Definitions
  - What each status means
- 5.3 Error Messages
  - Common errors and solutions

##### 6. Troubleshooting
- 6.1 Common Problems
  - Problem → Solution format
- 6.2 FAQ
- 6.3 Contact Support

##### 7. Appendices
- A. Keyboard Shortcuts
- B. Glossary
- C. Quick Reference Card

---

## Writing Guidelines

### Tone & Style

**Technical Specification:**
- Formal, precise language
- Use technical terms (define in glossary)
- Focus on "what" and "how" technically
- Include code snippets, schemas, formulas

**User Manual:**
- Friendly, clear language
- Avoid jargon (or explain it)
- Focus on "how to" from user perspective
- Use screenshots and visual aids

### Formatting Rules

1. **Headings**
   - Use hierarchical numbering (1, 1.1, 1.1.1)
   - Keep headings concise
   - Start each major section on new page

2. **Tables**
   - Use for structured data (field lists, comparisons)
   - Include header row with bold text
   - Zebra striping for readability

3. **Lists**
   - Numbered for sequential steps
   - Bulleted for non-sequential items
   - Keep items parallel in structure

4. **Code/Formulas**
   - Use monospace font
   - Light gray background
   - Include comments for complex logic

5. **Diagrams**
   - One diagram per concept
   - Include figure numbers and captions
   - Reference in text: "See Figure 3-1"

### Content Guidelines

1. **Be Complete**
   - Document ALL features, not just new ones
   - Include edge cases and error handling
   - Don't assume prior knowledge

2. **Be Accurate**
   - Verify all field names match actual system
   - Test all procedures before documenting
   - Update screenshots if UI changes

3. **Be Consistent**
   - Use same terminology throughout
   - Follow same format for similar sections
   - Match actual system labels exactly

4. **Be Practical**
   - Include real examples
   - Show actual sample data
   - Provide templates where applicable

---

## Section Templates

### Function Description Template

```markdown
## X.X [Function Name]

### Purpose
[One sentence describing what this function does]

### Prerequisites
- [What must be true before using this function]
- [Required permissions/access]

### User Interface
[Screenshot or description of the screen/button]

### Steps
1. [First step]
2. [Second step]
3. [Continue...]

### Business Logic
[Explain what happens behind the scenes]
- [Rule 1]
- [Rule 2]

### Flow Diagram
[Include Mermaid diagram reference]
*See Figure X-X: [Function Name] Flow*

### Validation Rules
| Field | Rule | Error Message |
|-------|------|---------------|
| [Field] | [Rule] | [Message] |

### Error Handling
| Error | Cause | Resolution |
|-------|-------|------------|
| [Error] | [Cause] | [Fix] |
```

### Data Schema Template

```markdown
## [Table/List Name]

**Purpose:** [What this table stores]

**Record Count:** [Approximate or exact]

### Fields

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| ID | Number | Auto | Primary key |
| [Field] | [Type] | Yes/No | [Description] |

### Relationships
- [Relationship 1]
- [Relationship 2]

### Sample Data
| ID | [Field1] | [Field2] |
|----|----------|----------|
| 1 | [Value] | [Value] |
```

### Troubleshooting Template

```markdown
## [Problem Category]

### Problem: [Description]

**Symptoms:**
- [What user sees]
- [Error message if any]

**Cause:**
[Why this happens]

**Solution:**
1. [Step 1]
2. [Step 2]

**Prevention:**
[How to avoid this in future]
```
