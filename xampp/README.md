# Lancer UQOnnect avec XAMPP

Le site utilise Django. Apache (XAMPP) écoute sur le port `8080`, transmet les pages dynamiques au serveur Django local sur `8000`, et sert directement `/static/` et `/media/`. Les images du site sont dans `static/img/`.

Dans PowerShell, à la racine du projet :

```powershell
powershell -ExecutionPolicy Bypass -File .\xampp\start-local.ps1
```

Ouvrir ensuite [http://localhost:8080/](http://localhost:8080/). XAMPP est supposé installé dans `C:\xampp`. Le script active `mod_proxy_http`, ajoute une configuration Apache locale et en sauvegarde une copie avant sa première modification. Les photos du site sont servies depuis `static/img/`; les futures images téléversées dans l’administration sont accessibles sous `/media/`.

Pour arrêter les serveurs, utiliser Apache > Stop dans le panneau XAMPP, puis arrêter Django avec `Stop-Process -Id (Get-Content .\xampp\django.pid)`.
