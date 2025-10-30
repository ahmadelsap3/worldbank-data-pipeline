# Run dbt with password prompt
Write-Host "Please enter your Snowflake password:" -ForegroundColor Yellow
$password = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$env:SNOWFLAKE_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host "`nRunning dbt run...`n" -ForegroundColor Green
& "..\venv\Scripts\dbt.exe" run --profiles-dir .

Write-Host "`nRunning dbt test...`n" -ForegroundColor Green
& "..\venv\Scripts\dbt.exe" test --profiles-dir .

Write-Host "`nDone!" -ForegroundColor Green
