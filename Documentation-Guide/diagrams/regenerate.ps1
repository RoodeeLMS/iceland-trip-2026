# Diagram Regeneration Script
# Run this script to regenerate all diagram PNGs from Mermaid source files

$configPath = Join-Path $PSScriptRoot "mermaid-config.json"

# If no config in diagrams folder, use templates folder
if (-not (Test-Path $configPath)) {
    $configPath = Join-Path $PSScriptRoot "..\templates\mermaid-config.json"
}

# List all diagram source files (without extension)
$diagrams = @(
    "example-workflow"
    # Add more diagram names here as you create them
    # "fig-1-1-system-architecture",
    # "fig-3-1-main-workflow"
)

Set-Location $PSScriptRoot

Write-Host "Using config: $configPath"
Write-Host ""

foreach ($name in $diagrams) {
    $inputFile = "$name.mmd"
    $outputFile = "$name.png"

    if (Test-Path $inputFile) {
        Write-Host "Generating $outputFile..."
        & mmdc -i $inputFile -o $outputFile -c $configPath -s 3 -b white

        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Success!" -ForegroundColor Green
        } else {
            Write-Host "  Failed!" -ForegroundColor Red
        }
    } else {
        Write-Host "Skipping (not found): $inputFile" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Cyan
