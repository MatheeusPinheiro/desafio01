$exclude = @("venv", "LME.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "LME.zip" -Force