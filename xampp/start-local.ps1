$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$XamppRoot = 'C:\xampp'
$ApacheExe = Join-Path $XamppRoot 'apache\bin\httpd.exe'
$ApacheConf = Join-Path $XamppRoot 'apache\conf\httpd.conf'
$LocalConf = Join-Path $PSScriptRoot 'uqonnect-vhost.conf'
$DjangoPort = 8000
$ApachePort = 8080
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectRoot 'media') | Out-Null

if (-not (Test-Path $ApacheExe)) { throw "Apache XAMPP introuvable : $ApacheExe" }
if (-not (Test-Path $ApacheConf)) { throw "Configuration Apache introuvable : $ApacheConf" }

# Apache sert directement les images et fichiers statiques du projet.
$safeRoot = $ProjectRoot.Replace('\','/')
$conf = @"
Listen $ApachePort
<VirtualHost *:$ApachePort>
    ServerName localhost
    ProxyPreserveHost On
    ProxyPass /static/ !
    ProxyPass /media/ !
    Alias /static/ "$safeRoot/static/"
    Alias /media/ "$safeRoot/media/"
    <Directory "$safeRoot/static/">
        Require all granted
        Options FollowSymLinks
    </Directory>
    <Directory "$safeRoot/media/">
        Require all granted
        Options FollowSymLinks
    </Directory>
    ProxyPass / http://127.0.0.1:$DjangoPort/ retry=0 timeout=60
    ProxyPassReverse / http://127.0.0.1:$DjangoPort/
</VirtualHost>
"@
[IO.File]::WriteAllText($LocalConf,$conf,[Text.UTF8Encoding]::new($false))

# Keep a one-time backup before enabling Apache proxying and the site include.
$apacheText = [IO.File]::ReadAllText($ApacheConf)
$backup = "$ApacheConf.uqonnect.bak"
if (-not (Test-Path $backup)) { Copy-Item -LiteralPath $ApacheConf -Destination $backup }
if ($apacheText -notmatch '(?m)^\s*LoadModule\s+proxy_http_module\s+') {
    $apacheText = [regex]::Replace($apacheText,'(?m)^\s*#\s*LoadModule\s+proxy_http_module\s+modules/mod_proxy_http\.so\s*$','LoadModule proxy_http_module modules/mod_proxy_http.so',1)
}
if ($apacheText -notmatch [regex]::Escape($LocalConf.Replace('\','/'))) {
    $apacheText += "`r`nInclude `"$($LocalConf.Replace('\','/'))`"`r`n"
}
[IO.File]::WriteAllText($ApacheConf,$apacheText,[Text.UTF8Encoding]::new($false))

& $ApacheExe -t -f $ApacheConf
if ($LASTEXITCODE -ne 0) { throw 'La configuration Apache est invalide. Consultez le message ci-dessus.' }

$djangoListening = Get-NetTCPConnection -State Listen -LocalPort $DjangoPort -ErrorAction SilentlyContinue | Where-Object LocalAddress -eq '127.0.0.1'
if (-not $djangoListening) {
    $python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path $python)) { throw 'Python environment missing. Install requirements.txt in .venv first.' }
    $oldRedirectSetting = $env:SECURE_SSL_REDIRECT
    $env:SECURE_SSL_REDIRECT = 'False'
    $djangoProcess = Start-Process -FilePath $python -ArgumentList @('manage.py','runserver',"127.0.0.1:$DjangoPort",'--noreload') -WorkingDirectory $ProjectRoot -WindowStyle Hidden -PassThru
    $env:SECURE_SSL_REDIRECT = $oldRedirectSetting
    Set-Content -LiteralPath (Join-Path $PSScriptRoot 'django.pid') -Value $djangoProcess.Id -NoNewline
    Start-Sleep -Seconds 2
}

$apacheListening = Test-NetConnection -ComputerName 127.0.0.1 -Port $ApachePort -InformationLevel Quiet -WarningAction SilentlyContinue
if (-not $apacheListening) {
    Start-Process -FilePath $ApacheExe -ArgumentList @('-f',$ApacheConf) -WindowStyle Hidden | Out-Null
    Start-Sleep -Seconds 2
}
Write-Host "UQOnnect est disponible via XAMPP : http://localhost:$ApachePort/"
Write-Host "Les images et fichiers statiques sont servis par Apache depuis $ProjectRoot\static."
