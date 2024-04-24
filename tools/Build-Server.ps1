$MainDir = (Get-Item $PSScriptRoot).parent.FullName
cd $MainDir
pyinstaller --paths .\src --name 4200-Server --onefile --icon=resources\icon.ico .\src\tcp_server\app.py
$IniSourceFile = ".\src\tcp_server\4200-Server.template.ini"
$IniTargetFile = ".\dist\4200-Server.ini"
$IniText = [IO.File]::ReadAllText($IniSourceFile) -replace '(?<!\r)\n', "`r`n"
[IO.File]::WriteAllText($IniTargetFile, $IniText)
