rem reg add HKCR\Microsoft.PowerShellScript.1\Shell\0\Command /ve /t reg_sz /f /d "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoExit -ExecutionPolicy RemoteSigned -Command %%1"

powershell -ExecutionPolicy RemoteSigned -Command "Install-PackageProvider ChocolateyGet; Install-Package GoogleChrome,eac,paint.net,steam,vscode,hyper,AndroidStudio -Force -ProviderName ChocolateyGet"
pause