# PDF Generation Guide

This guide covers using wkhtmltopdf to generate professional PDF documents from HTML.

---

## Installation

### Windows
```powershell
# Using winget
winget install wkhtmltopdf

# Or download from: https://wkhtmltopdf.org/downloads.html
# Install to default location: C:\Program Files\wkhtmltopdf\
```

### Verify Installation
```powershell
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --version
```

---

## Basic Command

```powershell
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" `
    --enable-local-file-access `
    --print-media-type `
    --javascript-delay 2000 `
    --page-size A4 `
    --margin-top 25 `
    --margin-bottom 25 `
    --margin-left 25 `
    --margin-right 25 `
    --footer-html "footer.html" `
    --footer-spacing 5 `
    "Document.html" `
    "Document.pdf"
```

---

## Command Options Explained

### Essential Options

| Option | Value | Purpose |
|--------|-------|---------|
| `--enable-local-file-access` | - | Allow loading local images/files |
| `--print-media-type` | - | Use CSS `@media print` styles |
| `--javascript-delay` | 2000 | Wait 2s for JS to execute |
| `--page-size` | A4 | Standard paper size |

### Margins (in millimeters)

| Option | Recommended | Purpose |
|--------|-------------|---------|
| `--margin-top` | 25 | Top margin |
| `--margin-bottom` | 25 | Bottom margin (+ footer space) |
| `--margin-left` | 25 | Left margin |
| `--margin-right` | 25 | Right margin |

### Footer Options

| Option | Value | Purpose |
|--------|-------|---------|
| `--footer-html` | footer.html | Custom footer template |
| `--footer-spacing` | 5 | Space between content and footer |
| `--footer-right` | "[page]" | Simple page number (alternative) |

### Other Useful Options

| Option | Value | Purpose |
|--------|-------|---------|
| `--dpi` | 300 | Print quality DPI |
| `--image-quality` | 100 | Image compression (0-100) |
| `--no-outline` | - | Disable PDF outline/bookmarks |
| `--title` | "Doc Title" | PDF metadata title |

---

## Footer Template

Create `footer.html` for custom page numbering:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Open Sans', Arial, sans-serif;
            font-size: 10pt;
            color: #666;
            margin: 0;
            padding: 0;
        }
        .page-number {
            text-align: right;
            width: 100%;
        }
    </style>
    <script>
        function subst() {
            var vars = {};
            var query_strings_from_url = document.location.search.substring(1).split('&');
            for (var query_string in query_strings_from_url) {
                if (query_strings_from_url.hasOwnProperty(query_string)) {
                    var temp_var = query_strings_from_url[query_string].split('=', 2);
                    vars[temp_var[0]] = decodeURI(temp_var[1]);
                }
            }
            var page = parseInt(vars['page']);

            // Hide page number on Cover (1), Version History (2), ToC (3)
            // Content starts on page 4, show as page 1
            if (page <= 3) {
                document.getElementById('pageNum').style.display = 'none';
            } else {
                document.getElementById('pageNum').textContent = (page - 3);
            }
        }
    </script>
</head>
<body onload="subst()">
    <div class="page-number">
        <span id="pageNum"></span>
    </div>
</body>
</html>
```

### Footer Variables Available

wkhtmltopdf passes these via query string:
- `page` - Current page number
- `topage` - Total page count
- `section` - Current section name
- `subsection` - Current subsection name
- `title` - Document title

### Customizing Page Number Offset

Adjust the offset based on your front matter:

```javascript
// For 3 front matter pages (Cover, Version, ToC)
if (page <= 3) {
    // Hide
} else {
    document.getElementById('pageNum').textContent = (page - 3);
}

// For 2 front matter pages (Cover, ToC)
if (page <= 2) {
    // Hide
} else {
    document.getElementById('pageNum').textContent = (page - 2);
}
```

---

## Common Issues & Solutions

### Issue: Images Not Loading

**Symptom:** Blank spaces where images should be

**Solution:**
1. Ensure `--enable-local-file-access` is set
2. Use relative paths from HTML file location
3. Verify image files exist at specified paths

```html
<!-- Good -->
<img src="diagrams/fig-1-1.png">
<img src="assets/logo.png">

<!-- Bad -->
<img src="C:\full\path\image.png">
<img src="file:///path/image.png">
```

### Issue: CSS Not Applied Correctly

**Symptom:** Styles look different in PDF vs browser

**Solution:**
1. Enable `--print-media-type`
2. Use `@media print` for print-specific styles
3. Avoid CSS features unsupported by WebKit

```css
@media print {
    .no-print {
        display: none;
    }
}
```

### Issue: JavaScript Not Executing

**Symptom:** Dynamic content not appearing

**Solution:**
1. Increase `--javascript-delay` (try 3000 or 5000)
2. Ensure JS doesn't have errors
3. Use `--debug-javascript` to see errors

### Issue: Page Breaks Not Working

**Symptom:** Content breaks in unexpected places

**Solution:**
1. Use `page-break-before: always` (more reliable)
2. Avoid `page-break-after: avoid` (less reliable in wkhtmltopdf)
3. Group content with `page-break-inside: avoid`

```css
/* Reliable */
.new-page {
    page-break-before: always;
}

/* Less reliable */
h2 {
    page-break-after: avoid; /* May not work */
}

/* Group content */
.keep-together {
    page-break-inside: avoid;
}
```

### Issue: Flexbox Not Working

**Symptom:** Layout broken when using flexbox

**Solution:**
wkhtmltopdf uses older WebKit. Avoid:
- `margin-top: auto` (doesn't work)
- Complex flexbox layouts

Use instead:
- `position: absolute` for precise positioning
- `display: table` for layouts
- Traditional floats

### Issue: "Unable to Write to Destination"

**Symptom:** PDF generation fails with write error

**Solution:**
1. Close PDF if open in viewer
2. Check write permissions
3. Try different output path

### Issue: Fonts Not Rendering

**Symptom:** Wrong font in PDF

**Solution:**
1. Use web-safe fonts (Arial, Times, Courier)
2. Or embed fonts with @font-face
3. Specify font stack with fallbacks

```css
body {
    font-family: 'Open Sans', Arial, Helvetica, sans-serif;
}
```

### Issue: Table Rows Breaking Across Pages

**Symptom:** Table row content split between pages

**Solution:**
```css
tr {
    page-break-inside: avoid;
}

/* For entire table */
table {
    page-break-inside: avoid;
}
```

---

## PowerShell Generation Script

Create `generate-pdf.ps1`:

```powershell
param(
    [string]$InputFile,
    [string]$OutputFile
)

$wkhtmltopdf = "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
$footerFile = Join-Path $PSScriptRoot "footer.html"

if (-not $OutputFile) {
    $OutputFile = $InputFile -replace '\.html$', '.pdf'
}

Write-Host "Generating PDF..."
Write-Host "Input: $InputFile"
Write-Host "Output: $OutputFile"

& $wkhtmltopdf `
    --enable-local-file-access `
    --print-media-type `
    --javascript-delay 2000 `
    --page-size A4 `
    --margin-top 25 `
    --margin-bottom 25 `
    --margin-left 25 `
    --margin-right 25 `
    --footer-html $footerFile `
    --footer-spacing 5 `
    $InputFile `
    $OutputFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "PDF generated successfully: $OutputFile" -ForegroundColor Green
} else {
    Write-Host "PDF generation failed!" -ForegroundColor Red
}
```

**Usage:**
```powershell
.\generate-pdf.ps1 -InputFile "Document.html"
.\generate-pdf.ps1 -InputFile "Document.html" -OutputFile "Output.pdf"
```

---

## Batch Generation Script

Create `generate-all-pdfs.ps1`:

```powershell
$documents = @(
    "Technical Specification",
    "User Manual"
)

$wkhtmltopdf = "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
$footerFile = Join-Path $PSScriptRoot "footer.html"

foreach ($doc in $documents) {
    $input = "$doc.html"
    $output = "$doc.pdf"

    if (Test-Path $input) {
        Write-Host "Generating: $output"

        & $wkhtmltopdf `
            --enable-local-file-access `
            --print-media-type `
            --javascript-delay 2000 `
            --page-size A4 `
            --margin-top 25 `
            --margin-bottom 25 `
            --margin-left 25 `
            --margin-right 25 `
            --footer-html $footerFile `
            --footer-spacing 5 `
            $input `
            $output

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Success!" -ForegroundColor Green
        } else {
            Write-Host "  Failed!" -ForegroundColor Red
        }
    } else {
        Write-Host "Skipping (not found): $input" -ForegroundColor Yellow
    }
}

Write-Host "Done!"
```

---

## Cover Page Styling Notes

### Logo Positioning
Place logo in top-left corner (not top-right):
```css
.title-page .logo {
    position: absolute;
    top: 0;
    left: 0;
    height: 2in;  /* Adjust size as needed */
}
```

### Title Positioning
Use adequate padding to center the title vertically:
```css
.title-page {
    page-break-after: always;
    text-align: center;
    padding-top: 3.5in;  /* Pushes title to middle of page */
    height: 10in;
    position: relative;
}
```

### Version/Date on Cover
**Best Practice:** Do NOT include version number and date on the cover page. This information belongs in the Version History page, which is the authoritative source for document versioning.

---

## Quality Checklist

Before finalizing PDF:

### Layout
- [ ] Cover page looks correct (logo top-left, title centered)
- [ ] Version history on separate page
- [ ] ToC page numbers align with dots
- [ ] Major sections start on new pages
- [ ] No orphaned headings (title alone at bottom)

### Content
- [ ] All images load correctly
- [ ] Diagrams are readable size
- [ ] Tables don't break awkwardly
- [ ] Code blocks are formatted
- [ ] No text cut off at margins

### Page Numbers
- [ ] Cover page has no number
- [ ] Version history has no number
- [ ] ToC has no number
- [ ] Content starts at page 1
- [ ] Numbers are right-aligned

### Final
- [ ] Print a test copy
- [ ] Check on different PDF viewer
- [ ] Verify file size is reasonable
- [ ] Document metadata is correct

---

## Reference: Full Command with All Options

```powershell
"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" `
    --enable-local-file-access `
    --print-media-type `
    --javascript-delay 3000 `
    --no-stop-slow-scripts `
    --page-size A4 `
    --orientation Portrait `
    --dpi 300 `
    --image-quality 100 `
    --margin-top 25 `
    --margin-bottom 25 `
    --margin-left 25 `
    --margin-right 25 `
    --footer-html "footer.html" `
    --footer-spacing 5 `
    --title "Document Title" `
    --encoding UTF-8 `
    "input.html" `
    "output.pdf"
```
