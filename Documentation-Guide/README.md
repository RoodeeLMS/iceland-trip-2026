# Professional Documentation Guide for Power Apps Projects

## Purpose

This guide enables Claude (or any AI assistant) to create professional, consistent PDF documentation for Nestle Power Apps projects. It includes templates, workflows, and lessons learned from the MT FOC project.

## Quick Start for AI Agents

**READ THIS FIRST** - Follow these steps in order:

1. **Understand the document types** - Read `01-document-structure-guide.md`
2. **Set up diagrams** - Read `02-mermaid-diagram-guide.md`
3. **Create HTML from content** - Read `03-markdown-to-html-workflow.md`
4. **Generate PDF** - Read `04-pdf-generation-guide.md`
5. **Fix layout issues** - Read `05-css-troubleshooting-guide.md` (orphaned headers, page breaks)

## Folder Structure

```
Documentation-Guide/
├── README.md                          # This file (start here)
├── 01-document-structure-guide.md     # What topics/sections to include
├── 02-mermaid-diagram-guide.md        # How to create flowcharts
├── 03-markdown-to-html-workflow.md    # Converting content to HTML
├── 04-pdf-generation-guide.md         # wkhtmltopdf commands & tips
├── 05-css-troubleshooting-guide.md    # CSS fixes (orphaned headers, page breaks)
├── templates/
│   ├── technical-spec-template.html   # Full HTML template for tech specs
│   ├── user-manual-template.html      # Full HTML template for user manuals
│   ├── test-document-template.html    # Full HTML template for SIT/UAT test docs
│   ├── footer.html                    # Page number footer template
│   └── mermaid-config.json            # Mermaid diagram configuration
├── diagrams/
│   ├── example-workflow.mmd           # Example Mermaid diagram
│   └── regenerate.ps1                 # Script to regenerate all diagrams
├── assets/
│   └── nestle-logo.png                # Nestle logo for documents
└── examples/
    ├── MT FOC Technical Specification.pdf
    └── MT FOC User Manual.pdf
```

## Document Types

### 1. Technical Specification
- **Audience**: Developers, maintainers, IT support
- **Purpose**: Complete technical reference for system maintenance
- **Sections**: Architecture, data flows, schemas, business logic, integrations

### 2. User Manual
- **Audience**: End users, business users
- **Purpose**: Step-by-step usage instructions
- **Sections**: Screen guides, workflows, troubleshooting

### 3. Test Document (SIT/UAT)
- **Audience**: QA team, business testers, project stakeholders
- **Purpose**: Define test cases and track testing progress
- **Sections**: Test environment, test cases by category, UAT sign-off
- **Key Features**: Priority badges, status badges, checklist styling, sign-off tables

## Key Tools Required

| Tool | Purpose | Installation |
|------|---------|--------------|
| wkhtmltopdf | HTML to PDF conversion | `winget install wkhtmltopdf` |
| Mermaid CLI (mmdc) | Generate flowchart PNGs | `npm install -g @mermaid-js/mermaid-cli` |
| Node.js | Required for Mermaid | `winget install OpenJS.NodeJS` |

## Workflow Overview

```
1. Gather Requirements
   └── Understand the application, screens, data flows

2. Create Mermaid Diagrams (.mmd files)
   └── System architecture, workflows, flow charts
   └── Generate PNGs using mmdc command

3. Write Content (can use .md for drafting)
   └── Follow document-structure-guide.md

4. Create HTML Document
   └── Use templates/technical-spec-template.html
   └── Add content with proper CSS classes
   └── Reference diagram PNGs

5. Generate PDF
   └── Use wkhtmltopdf with footer.html
   └── Apply lessons learned (page breaks, etc.)

6. Review & Iterate
   └── Check page breaks, diagram sizing
   └── Fix orphaned headings
```

## Critical Lessons Learned

### Orphaned Headers (Most Common Issue!)
- **Problem**: Headers appear at bottom of page, content on next page
- **Solution**: Wrap header + first content in `<div class="keep-together">`
- **CSS**: `page-break-inside: avoid`
- **See**: `05-css-troubleshooting-guide.md` for detailed examples

```html
<div class="keep-together">
    <h2>1.1 Purpose</h2>
    <p>First paragraph of content...</p>
</div>
```

### Page Breaks
- Use `page-break-before: always` (more reliable than `page-break-after: avoid`)
- Add `.new-page` class to sections that must start on new pages
- Test with actual PDF generation, not browser preview

### Diagram Sizing
- Use two CSS classes: `.flow-diagram-long` and `.flow-diagram-short`
- Long diagrams (5+ steps): `max-height: 7.5in`
- Short diagrams (3-4 steps): `max-height: 4in`
- Always set `width: 100%` for consistency

### Cover Page Layout
- Use `position: absolute` for "Prepared by" section at bottom
- wkhtmltopdf doesn't support flexbox `margin-top: auto`
- Set container to `position: relative; height: 10in`

### Table of Contents
- Use `display: table` for dot leaders (not flexbox)
- Three cells: title, dots (border-bottom: dotted), page number

### Page Numbering
- Use separate footer.html with JavaScript
- Hide page numbers on Cover, Version History, ToC
- Start content numbering from 1 (not actual page number)

### wkhtmltopdf Quirks
- Enable `--print-media-type` for proper CSS rendering
- Use `--javascript-delay 2000` for complex pages
- Enable `--enable-local-file-access` for local images

## File Naming Convention

```
[Project Name] Technical Specification.html  → .pdf
[Project Name] User Manual.html              → .pdf
fig-X-Y-description.mmd                      → .png
```

## Brand Guidelines (Nestle)

- **Primary Blue**: #0066b3
- **Secondary Blue**: #004d99
- **Font**: Open Sans (fallback: Arial, sans-serif)
- **Logo**: Nestle logo in top-right of cover page
- **Margins**: 25mm all sides

## Quick Commands Reference

### Generate single diagram
```powershell
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json -s 3 -b white
```

### Generate PDF
```powershell
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" `
  --enable-local-file-access `
  --print-media-type `
  --javascript-delay 2000 `
  --page-size A4 `
  --margin-top 25 --margin-bottom 25 `
  --margin-left 25 --margin-right 25 `
  --footer-html "footer.html" `
  --footer-spacing 5 `
  "Document.html" "Document.pdf"
```

### Regenerate all diagrams
```powershell
powershell -ExecutionPolicy Bypass -File "diagrams/regenerate.ps1"
```

## Checklist Before Delivery

### Layout & Page Breaks
- [ ] No orphaned headings (title alone at page bottom)
- [ ] All h2 headers wrapped with `.keep-together` + first content
- [ ] All h3 headers wrapped with `.keep-together` + first content
- [ ] Tables don't break awkwardly across pages
- [ ] Test cases stay together on same page
- [ ] Major sections start on new pages (`.new-page` class)

### Front Matter
- [ ] Cover page "Prepared by" is at bottom
- [ ] Version History page is between Cover and ToC
- [ ] ToC page numbers align right with dot leaders
- [ ] Page numbers start at 1 after front matter

### Content
- [ ] All diagrams render correctly in PDF
- [ ] All images load (check paths)
- [ ] Code blocks formatted properly
- [ ] No text cut off at margins

### Final Review
- [ ] Generate PDF and scroll through every page
- [ ] Print test copy if possible
- [ ] Check on different PDF viewer

## Support

For questions about this guide, refer to:
- `examples/` folder for working examples
- Original MT FOC project documentation
- wkhtmltopdf documentation: https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
- Mermaid documentation: https://mermaid.js.org/
