# Start Dagster with password prompt
Write-Host "🚀 Starting Dagster for World Bank Pipeline" -ForegroundColor Cyan
Write-Host ""

# Check if password is already in environment
if (-not $env:SNOWFLAKE_PASSWORD -or $env:SNOWFLAKE_PASSWORD -eq 'your_password_here') {
    Write-Host "🔒 Please enter your Snowflake password:" -ForegroundColor Yellow
    $password = Read-Host -AsSecureString "Password"
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
    $env:SNOWFLAKE_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    Write-Host "✅ Password captured securely" -ForegroundColor Green
    Write-Host ""
}

Write-Host "🌐 Starting Dagster UI at http://localhost:3000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start Dagster
$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
& "$projectRoot\venv\Scripts\dagster.exe" dev -f "$PSScriptRoot\worldbank_pipeline.py"
