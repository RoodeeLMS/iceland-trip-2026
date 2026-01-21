# CSS Troubleshooting Guide for PDF Generation

This guide documents common CSS issues encountered when generating PDFs with wkhtmltopdf and their solutions.

---

## Quick Reference

| Issue | Solution | CSS |
|-------|----------|-----|
| Orphaned headers | Wrap with `.keep-together` | `page-break-inside: avoid` |
| Force new page | Add `.new-page` class | `page-break-before: always` |
| Tables splitting | Add to `tr` | `page-break-inside: avoid` |
| Content splitting | Wrap in `<div class="keep-together">` | `page-break-inside: avoid` |

---

## Issue 1: Orphaned Headers (Header at Bottom of Page)

### Problem
Headers (h1, h2, h3) appear at the bottom of a page with their content on the next page, creating an "orphaned" header.

### Example of the Problem
```
Page 3:
... previous content ...

3.2 Approving Submissions    <-- Header alone at bottom
---end of page---

Page 4:
Content for section 3.2...   <-- Content starts on new page
```

### Solution: Use `.keep-together` Class

Wrap the header and its first content element in a `<div class="keep-together">`:

```html
<!-- BEFORE (orphaned header) -->
<h2>3.2 Approving Submissions</h2>
<h3>Overview</h3>
<p>RFOE and TradeOps users review submissions...</p>

<!-- AFTER (header stays with content) -->
<div class="keep-together">
    <h2>3.2 Approving Submissions</h2>
    <h3>Overview</h3>
    <p>RFOE and TradeOps users review submissions...</p>
</div>
```

### CSS Definition
```css
.keep-together {
    page-break-inside: avoid;
}
```

### When to Apply

1. **h2 + First Paragraph/Table** - Most common case
   ```html
   <div class="keep-together">
       <h2>1.1 Purpose</h2>
       <p>This document defines test cases for...</p>
   </div>
   ```

2. **h3 + Content Block** - Subsections
   ```html
   <div class="keep-together">
       <h3>Overview</h3>
       <p>Sales representatives submit photos of product displays...</p>
   </div>
   ```

3. **h3 + Figure** - When screenshot follows header
   ```html
   <div class="keep-together">
       <h3>4.2.2 Chiller List View</h3>
       <figure>
           <img src="assets/chiller-list.png" alt="Chiller List" class="screenshot">
           <figcaption>Figure 4-4: Chiller List</figcaption>
       </figure>
   </div>
   ```

4. **Section Header Only** - When first element is self-contained (like test cases)
   ```html
   <div class="keep-together">
       <h2>4.1 Submission Tests</h2>
   </div>
   <!-- Test cases follow with their own page-break-inside: avoid -->
   ```

### Systematic Approach

When fixing orphaned headers, work through the document systematically:

1. Search for all `<h2>` tags in the document
2. For each h2, wrap it with its first content element
3. Search for all `<h3>` tags
4. For each h3, wrap it with its first content element
5. Regenerate PDF and verify

---

## Issue 2: Tables Breaking Across Pages

### Problem
Table rows split across pages, making data hard to read.

### Solution: Apply to Table Rows

```css
tr {
    page-break-inside: avoid;
}

/* For entire table (use sparingly - only for small tables) */
table {
    page-break-inside: avoid;
}
```

### When Table is Too Large
For large tables that won't fit on one page:
- Let it span pages (don't add `page-break-inside: avoid` to the table)
- Ensure each row stays together with `tr { page-break-inside: avoid; }`
- Consider repeating headers with `<thead>` (limited support in wkhtmltopdf)

---

## Issue 3: Test Cases Breaking

### Problem
Test case cards split across pages.

### Solution: Test Case Container

```css
.test-case {
    border: 1px solid #ddd;
    margin: 15px 0;
    page-break-inside: avoid;  /* Keep entire test case together */
}
```

---

## Issue 4: Figures Breaking

### Problem
Images and their captions split across pages.

### Solution: Figure Element

```css
figure {
    margin: 20px 0;
    text-align: center;
    page-break-inside: avoid;
}
```

---

## Issue 5: Forcing New Pages

### Problem
Need a section to start on a new page.

### Solution: Use `.new-page` Class

```html
<h1 id="section4" class="new-page">4. Functional Specifications</h1>
```

```css
.new-page {
    page-break-before: always;
}
```

### When to Use
- Major sections (h1 level)
- Appendices
- Sign-off pages

---

## Issue 6: Code Blocks Breaking

### Problem
Code blocks split across pages.

### Solution

```css
pre {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    page-break-inside: avoid;  /* Keep code block together */
}
```

---

## Complete CSS Template

Here's the complete set of page-break CSS rules to include in your document:

```css
/* ===== PAGE BREAK CONTROLS ===== */

/* Force new page before element */
.new-page {
    page-break-before: always;
}

/* Prevent page break inside element */
.keep-together {
    page-break-inside: avoid;
}

/* Table rows should not split */
tr {
    page-break-inside: avoid;
}

/* Figures should not split */
figure {
    page-break-inside: avoid;
}

/* Code blocks should not split */
pre {
    page-break-inside: avoid;
}

/* Test cases should not split */
.test-case {
    page-break-inside: avoid;
}

/* Cover and special pages force page break after */
.title-page,
.version-page,
.toc {
    page-break-after: always;
}
```

---

## Debugging Tips

### 1. Check PDF Page by Page
After generating PDF, scroll through each page looking for:
- Headers alone at bottom of page
- Split tables
- Split figures
- Awkward content breaks

### 2. Browser Preview Limitations
**Warning:** Browser print preview may not match wkhtmltopdf output!

Always test with actual PDF generation:
```powershell
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" `
    --enable-local-file-access `
    --print-media-type `
    document.html document.pdf
```

### 3. Identify Problem Areas
Use background colors temporarily to see element boundaries:
```css
.keep-together {
    page-break-inside: avoid;
    background-color: rgba(255, 0, 0, 0.1); /* Debug: red tint */
}
```

### 4. wkhtmltopdf Page Break Quirks

| Property | Reliability | Notes |
|----------|-------------|-------|
| `page-break-before: always` | High | Most reliable |
| `page-break-inside: avoid` | Medium | Works on most elements |
| `page-break-after: always` | Medium | Sometimes ignored |
| `page-break-after: avoid` | Low | Often ignored - don't rely on this |

**Best Practice:** Use `page-break-before: always` instead of `page-break-after: always` when possible.

---

## Real-World Example: TH Trade Display Contest

### Test Document Fix

We encountered orphaned headers throughout the Test Document. Here's how we fixed them:

**Section 1 - Introduction:**
```html
<div class="keep-together">
    <h2>1.1 Purpose</h2>
    <p>This document defines test cases for the TH Trade Display Contest...</p>
</div>

<div class="keep-together">
    <h2>1.2 Scope</h2>
    <table>
        <tr><th>In Scope</th><th>Out of Scope</th></tr>
        ...
    </table>
</div>
```

**Section 4 - Test Cases:**
```html
<div class="keep-together">
    <h2>4.1 Submission Tests</h2>
</div>

<div class="test-case">
    <!-- Test case already has page-break-inside: avoid -->
    <div class="test-case-header">TC-DC-001: Submit Contest Photos</div>
    ...
</div>
```

**Section 9 - UAT Sign-Off:**
```html
<div class="keep-together">
    <h2>9.1 Test Execution Summary</h2>
    <table>
        <tr><th>Category</th><th>Total</th><th>Passed</th>...</tr>
        ...
    </table>
</div>

<div class="keep-together">
    <h2>9.4 Sign-Off Approval</h2>
    <table>
        <tr><th>Role</th><th>Name</th><th>Signature</th><th>Date</th></tr>
        ...
    </table>
</div>
```

### User Manual Fix

For user manuals with step-by-step instructions:

```html
<h2 id="section3-1">3.1 Submitting Photos</h2>

<div class="keep-together">
    <h3>Overview</h3>
    <p>Sales representatives submit photos of product displays...</p>
</div>

<div class="keep-together">
    <h3>Step-by-Step Instructions</h3>
    <ol class="steps">
        <li><strong>Navigate to Display Contest</strong><br>Click on the menu...</li>
        <li><strong>Select your shop</strong><br>Choose from the list...</li>
        ...
    </ol>
</div>
```

---

## Checklist Before PDF Generation

- [ ] All h2 headers wrapped with first content element
- [ ] All h3 headers wrapped with first content element
- [ ] Major sections have `.new-page` class
- [ ] Test cases have `page-break-inside: avoid`
- [ ] Tables have `tr { page-break-inside: avoid }`
- [ ] Figures have `page-break-inside: avoid`
- [ ] Code blocks have `page-break-inside: avoid`

---

## Summary

| Element | CSS Class/Property | Purpose |
|---------|-------------------|---------|
| Headers + Content | `.keep-together` | Prevent orphaned headers |
| Major Sections | `.new-page` | Start on new page |
| Table Rows | `tr { page-break-inside: avoid }` | Keep rows together |
| Test Cases | `page-break-inside: avoid` | Keep cards together |
| Figures | `page-break-inside: avoid` | Keep image + caption together |
| Code Blocks | `page-break-inside: avoid` | Keep code together |

**Key Principle:** When in doubt, wrap problematic content in `<div class="keep-together">` and test.

---

## Cover Page Styling Reference

### Recommended Cover Page CSS

```css
.title-page {
    page-break-after: always;
    text-align: center;
    padding-top: 3.5in;    /* Centers title vertically */
    height: 10in;
    position: relative;
}

.title-page .logo {
    position: absolute;
    top: 0;                 /* Flush with page margin */
    left: 0;                /* Top-left corner */
    height: 2in;            /* Logo height */
}

.title-page h1 {
    font-size: 28pt;
    color: #0066b3;
    margin-bottom: 0.3in;
    font-weight: 700;
}

.title-page .subtitle {
    font-size: 18pt;
    color: #333;
    margin: 10px 0;
}

.prepared-section {
    position: absolute;
    bottom: 0;
    left: 0;
    text-align: left;
    font-size: 11pt;
    line-height: 1.8;
}
```

### Cover Page Best Practices

| Element | Recommendation |
|---------|---------------|
| Logo | Top-left corner, 2 inches height |
| Title | Centered, approximately 3.5 inches from top |
| Subtitle | Below title, slightly smaller font |
| Version/Date | Do NOT include on cover (use Version History page) |
| Prepared for/by | Bottom-left, aligned left |
