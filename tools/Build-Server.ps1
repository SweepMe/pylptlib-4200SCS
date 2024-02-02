$MainDir = (Get-Item $PSScriptRoot).parent.FullName
cd $MainDir
pyinstaller --paths .\src --name 4200-Server --onefile --icon=resources\icon.ico .\src\tcp_server\app.py
Copy-Item .\src\tcp_server\4200-Server.template.ini .\dist\4200-Server.ini
