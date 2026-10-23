# UQOnnect

Site institutionnel et communautaire Django pour le comité étudiant en informatique de l’UQO, campus de Saint-Jérôme.

## Démarrage local

1. Installer Python 3.11 ou plus récent.
2. Créer un environnement virtuel : `python -m venv .venv`, puis l’activer.
3. Installer les dépendances : `pip install -r requirements.txt`.
4. Copier `.env.example` vers `.env` et définir une clé `SECRET_KEY` locale.
5. Initialiser la base : `python manage.py migrate`.
6. Créer un compte de gestion : `python manage.py createsuperuser`.
7. Lancer : `python manage.py runserver`.

Le site est disponible sur `http://127.0.0.1:8000` et l’administration sur `/admin/`. Les événements, actualités, membres et projets se gèrent dans l’administration. Par défaut, les courriels de contact sont consignés dans la console; configurez un backend SMTP avant mise en production.

## Contenus

Les pages ne contiennent pas de données événementielles fictives. Les contenus dynamiques sont publiés depuis Django Admin. Un événement en inscription interne est actuellement orienté vers le courriel du comité; le formulaire d’inscription interne complet et les soumissions de projet attendent une itération dédiée.

## Production

Utiliser PostgreSQL, définir les variables d’environnement, désactiver `DEBUG`, configurer `ALLOWED_HOSTS`, HTTPS, les cookies sécurisés, un backend courriel et le service de fichiers médias. Exécuter `python manage.py collectstatic`. Prévoir des sauvegardes de la base et des médias, et une politique de conservation/suppression des messages et inscriptions avant ouverture publique.
