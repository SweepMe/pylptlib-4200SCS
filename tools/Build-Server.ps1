$MainDir = (Get-Item $PSScriptRoot).parent.FullName
cd $MainDir
pyinstaller --paths .\src --onefile .\src\tcp_server\app.py
