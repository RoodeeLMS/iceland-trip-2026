# Markdown to HTML Workflow

This guide explains how to convert documentation content into professional HTML suitable for PDF generation.

---

## Overview

While you can draft content in Markdown for easier editing, the final deliverable must be HTML with proper CSS styling for professional PDF output. wkhtmltopdf converts HTML to PDF, not Markdown.

## Workflow Options

### Option A: Direct HTML (Recommended)
1. Start with HTML template
2. Write content directly in HTML
3. Use CSS classes for formatting
4. Generate PDF

**Best for:** Final documents, complex layouts, precise control

### Option B: Markdown Draft → HTML
1. Draft content in Markdown
2. Convert structure to HTML
3. Apply CSS classes
4. Generate PDF

**Best for:** Initial content drafting, collaborative editing

---

## HTML Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document Title</title>
    <style>
        /* All CSS goes here - see CSS Reference section */
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="title-page">...</div>

    <!-- Version History -->
    <div class="version-page">...</div>

    <!-- Table of Contents -->
    <div class="toc">...</div>

    <!-- Main Content -->
    <div class="content">
        <h1>1. First Section</h1>
        ...
    </div>
</body>
</html>
```

---

## CSS Classes Reference

### Page Layout Classes

```css
/* Force new page before element */
.new-page {
    page-break-before: always;
}

/* Keep element with next (avoid orphan headings) */
.keep-together {
    page-break-inside: avoid;
}

/* Avoid page break after (less reliable) */
.no-break-after {
    page-break-after: avoid;
}
```

### Cover Page

```css
.title-page {
    page-break-after: always;
    text-align: center;
    padding-top: 2in;
    height: 10in;
    position: relative;
}

.title-page h1 {
    font-size: 28pt;
    color: #0066b3;
    margin-bottom: 0.5in;
}

.title-page .subtitle {
    font-size: 18pt;
    color: #333;
}

.title-page .logo {
    position: absolute;
    top: 0.5in;
    right: 0.5in;
    height: 1in;
}

.prepared-section {
    position: absolute;
    bottom: 0;
    left: 0;
    text-align: left;
    font-size: 11pt;
}
```

### Version History Page

```css
.version-page {
    page-break-after: always;
}

.version-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1em;
}

.version-table th {
    background-color: #0066b3;
    color: white;
    padding: 10px;
    text-align: left;
}

.version-table td {
    border: 1px solid #ddd;
    padding: 10px;
}

.version-table tr:nth-child(even) {
    background-color: #f9f9f9;
}
```

### Table of Contents

```css
.toc {
    page-break-after: always;
}

.toc h2 {
    color: #0066b3;
    border-bottom: 2px solid #0066b3;
    padding-bottom: 10px;
}

.toc-item {
    display: table;
    width: 100%;
    margin: 8px 0;
}

.toc-item a {
    display: table-cell;
    text-decoration: none;
    color: #333;
}

.toc-item .toc-dots {
    display: table-cell;
    width: 100%;
    border-bottom: 1px dotted #999;
    height: 1em;
    margin: 0 5px;
}

.toc-item .toc-page {
    display: table-cell;
    text-align: right;
    white-space: nowrap;
    padding-left: 10px;
}

.toc-section {
    font-weight: bold;
    margin-top: 15px;
}
```

### Content Sections

```css
h1 {
    color: #0066b3;
    font-size: 18pt;
    border-bottom: 2px solid #0066b3;
    padding-bottom: 5px;
    margin-top: 20px;
}

h2 {
    color: #004d99;
    font-size: 14pt;
    margin-top: 15px;
}

h3 {
    color: #333;
    font-size: 12pt;
    margin-top: 12px;
}

p {
    line-height: 1.6;
    margin: 10px 0;
}
```

### Tables

```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 10pt;
}

th {
    background-color: #0066b3;
    color: white;
    padding: 10px;
    text-align: left;
    font-weight: 600;
}

td {
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Prevent table rows from breaking across pages */
tr {
    page-break-inside: avoid;
}
```

### Code Blocks

```css
code {
    font-family: 'Consolas', 'Monaco', monospace;
    background-color: #f5f5f5;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 9pt;
}

pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.4;
}

pre code {
    background: none;
    padding: 0;
}
```

### Figures and Diagrams

```css
figure {
    margin: 20px 0;
    text-align: center;
    page-break-inside: avoid;
}

figcaption {
    font-style: italic;
    color: #666;
    margin-top: 10px;
    font-size: 10pt;
}

/* Long flowcharts (5+ steps) */
.flow-diagram-long {
    width: 100%;
    max-height: 7.5in;
    object-fit: contain;
    display: block;
    margin: 0 auto;
}

/* Short flowcharts (3-4 steps) */
.flow-diagram-short {
    width: 100%;
    max-height: 4in;
    object-fit: contain;
    display: block;
    margin: 0 auto;
}
```

### Lists

```css
ul, ol {
    margin: 10px 0;
    padding-left: 25px;
}

li {
    margin: 5px 0;
    line-height: 1.5;
}

/* Nested lists */
ul ul, ol ol, ul ol, ol ul {
    margin: 5px 0;
}
```

### Callout Boxes

```css
.note {
    background-color: #e7f3ff;
    border-left: 4px solid #0066b3;
    padding: 15px;
    margin: 15px 0;
}

.warning {
    background-color: #fff3e0;
    border-left: 4px solid #ff9800;
    padding: 15px;
    margin: 15px 0;
}

.tip {
    background-color: #d4edda;
    border-left: 4px solid #28a745;
    padding: 15px;
    margin: 15px 0;
}
```

---

## HTML Element Examples

### Cover Page

```html
<div class="title-page">
    <img src="assets/nestle-logo.png" alt="Nestle" class="logo">

    <h1>Project Name</h1>
    <p class="subtitle">Technical Specification</p>
    <p class="subtitle">Version 1.0</p>
    <p class="subtitle">December 2025</p>

    <div class="prepared-section">
        <p><strong>Prepared for:</strong><br>
        Client Name<br>
        Department</p>

        <p><strong>Prepared by:</strong><br>
        Your Company<br>
        Author Name</p>
    </div>
</div>
```

### Version History

```html
<div class="version-page">
    <h2>Version History</h2>
    <table class="version-table">
        <tr>
            <th>Version</th>
            <th>Date</th>
            <th>Author</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>1.0</td>
            <td>December 2, 2025</td>
            <td>Author Name</td>
            <td>Initial release</td>
        </tr>
    </table>
</div>
```

### Table of Contents

```html
<div class="toc">
    <h2>Table of Contents</h2>

    <div class="toc-item toc-section">
        <a href="#section1">1. Introduction</a>
        <span class="toc-dots"></span>
        <span class="toc-page">1</span>
    </div>

    <div class="toc-item">
        <a href="#section1-1">&nbsp;&nbsp;&nbsp;1.1 Purpose</a>
        <span class="toc-dots"></span>
        <span class="toc-page">1</span>
    </div>

    <div class="toc-item">
        <a href="#section1-2">&nbsp;&nbsp;&nbsp;1.2 Scope</a>
        <span class="toc-dots"></span>
        <span class="toc-page">2</span>
    </div>
</div>
```

### Content Section with Force New Page

```html
<h1 id="section3" class="new-page">3. Functional Specifications</h1>

<h2 id="section3-1">3.1 Export Function</h2>
<p>Description of the export function...</p>

<figure>
    <img src="diagrams/fig-3-1-export-flow.png"
         alt="Export Flow"
         class="flow-diagram-long">
    <figcaption>Figure 3-1: Export Function Flow</figcaption>
</figure>
```

### Data Table

```html
<h3>Field Definitions</h3>
<table>
    <tr>
        <th>Field Name</th>
        <th>Type</th>
        <th>Required</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>RequestNo</td>
        <td>Text</td>
        <td>Yes</td>
        <td>Unique request identifier (format: GR#####-MM/DD/YYYY)</td>
    </tr>
    <tr>
        <td>RequestDate</td>
        <td>DateTime</td>
        <td>Yes</td>
        <td>Date when request was created</td>
    </tr>
</table>
```

### Code Block

```html
<h4>XML Structure</h4>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;E2OFile Date="yyyymmdd" Time="hhmmss"&gt;
    &lt;FileName&gt;NE2O_V06_XXXX.XML&lt;/FileName&gt;
    &lt;Order OrderSequencial="1"&gt;
        &lt;hdrCustomer&gt;12345678&lt;/hdrCustomer&gt;
    &lt;/Order&gt;
&lt;/E2OFile&gt;</code></pre>
```

### Callout Boxes

```html
<div class="note">
    <strong>Note:</strong> This feature requires admin permissions.
</div>

<div class="warning">
    <strong>Warning:</strong> This action cannot be undone.
</div>

<div class="tip">
    <strong>Tip:</strong> Use keyboard shortcut Ctrl+S to save quickly.
</div>
```

---

## Markdown to HTML Conversion Reference

| Markdown | HTML |
|----------|------|
| `# Heading 1` | `<h1>Heading 1</h1>` |
| `## Heading 2` | `<h2>Heading 2</h2>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `- item` | `<ul><li>item</li></ul>` |
| `1. item` | `<ol><li>item</li></ol>` |
| `` `code` `` | `<code>code</code>` |
| `[link](url)` | `<a href="url">link</a>` |
| `![alt](img)` | `<img src="img" alt="alt">` |

---

## Tips & Best Practices

### 1. Page Break Strategy
- Add `class="new-page"` to major section headings (h1)
- Test in actual PDF, not browser
- `page-break-before: always` is more reliable than `page-break-after: avoid`

### 2. Avoid Orphaned Headings
If a heading appears alone at the bottom of a page:
- Add `class="new-page"` to force it to next page
- Or group heading with following content in a div with `page-break-inside: avoid`

### 3. Table Handling
- Keep tables simple (avoid very wide tables)
- Use `page-break-inside: avoid` on `<tr>`
- Consider splitting large tables across sections

### 4. Image Paths
- Use relative paths: `src="diagrams/fig-1-1.png"`
- Verify paths work from HTML file location
- Enable `--enable-local-file-access` in wkhtmltopdf

### 5. Font Consistency
- Define font-family in body CSS
- Use web-safe fonts or embed fonts
- Test special characters (Thai, symbols)

### 6. Print Media
- Use `@media print` for print-specific styles
- Enable `--print-media-type` in wkhtmltopdf
- Test both screen and print rendering

---

## Complete Workflow Example

```
1. Create folder structure
   project/
   ├── Document.html
   ├── diagrams/
   │   └── *.png
   ├── assets/
   │   └── logo.png
   └── footer.html

2. Copy HTML template from templates/

3. Update cover page content
   - Title, version, date
   - Logo path
   - Prepared by information

4. Add version history entry

5. Write content sections
   - Use proper CSS classes
   - Reference diagrams with correct paths
   - Add new-page class where needed

6. Update Table of Contents
   - Add all sections
   - Update page numbers after first PDF generation

7. Generate PDF
   wkhtmltopdf --enable-local-file-access ...

8. Review and iterate
   - Check page breaks
   - Verify diagram sizing
   - Update ToC page numbers
   - Regenerate PDF
```
