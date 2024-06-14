<a name="readme-top"></a>

<div align="center">
  <img src="static/img/roomquestic.png" alt="Logo CReSTIC" width="140"  height="auto" />
  <br/>
  <h3><b>Site de réservation - CReSTIC</b></h3>
</div>

# 📗 Sommaire
- [📝 Description](#description)
- [👥 Auteur(s)](#auteur)
- [🛠️ Versions](#versions)
- [🧰️ Installation](#installation)
- [📧 Configuration du service de mail](#configmail)
- [🔧️ Lancement du projet](#launchproject)
- [🧾 Licence](#licence)
- [🔍 Projet original](#origproject)

## 📝 Description <a name="description"></a>
<div style="text-align: justify;">
Ce site web a été réalisé, pour le CReSTIC (un laboratoire de recherche) dans le cadre d'un stage de 2ème année de BUT Informatique de l'Université de Reims Champagne Ardenne.
Il permet de réserver des salles et équipements, mais aussi de les gérer, c'est-à-dire, en créer, en modifier et en supprimer. 
</div>

## 👥 Auteur(s) <a name="auteur"></a>
- 👤 Nino SAUVAGEOT - [sauv0037](https://github.com/sauv0037)
- 👤 Léo BERNARD - [bern0181](https://github.com/bern0181)
- 👤 Tom SIKORA - [tom512000](https://github.com/tom512000)

## 🛠️ Versions <a name="versions"></a>
- Python 3.9.x
- Django 3.2.12
- FullCalendar 5.5.1
- icalendar 5.0.12

## 🧰️ Installation <a name="installation"></a>
1. **Dans la racine du projet, créez un environnement virtuel :**
    ```shell
    $ python -m venv venv
    ```
2. **Pour gérer le JavaScript, installez npm :**
   ````shell
   npm install
   ````
2. **Activez cet environnement :**
    - Si vous êtes sur Linux :
        ```shell
        source venv/bin/activate
        ```
    - Si vous êtes sur Windows :
        ```shell
        venv\Scripts\activate
        ```
3. **Installez les dépendances :**
    ```shell
    pip install -r requirements.txt
    ```
4. **Migrez les modèles :**
    ```shell
    python manage.py migrate
    ```
5. **Créez votre compte administrateur :**
    ```shell
    python manage.py createsuperuser
    ```

## 🔧️ Lancement du projet <a name="launchproject"></a>
1. Lancez le serveur avec la commande :
    ```shell
    python manage.py runserver
    ```
Accéder maintenant au projet à l'adresse http://localhost:8000.

## 📧 Configuration du service de mail <a name="configmail"></a>
### Setup Mail Service
1. **Créez un fichier _.env_ à la racine du projet**.
2. **Dans ce fichier, ajoutez les lignes de code suivantes :**
   ```shell
   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_HOST = "adresse de l'hôte"
   EMAIL_USE_SSL = True
   EMAIL_PORT = port-du-serveur
   EMAIL_HOST_USER = nom-d-utilisateur
   EMAIL_HOST_PASSWORD = mot-de-passe
   ```
3. **Importez les fonctions suivantes dans le fichier _settings.py_ :**
   ```py
   import os
   from pathlib import Path
   from dotenv import load_dotenv
   ```
4. **Ajoutez les paramètres suivants pour récupérer les données du fichier _.env_ :**
   ```py
   env_path = Path('.') / '.env'
   load_dotenv(dotenv_path=env_path)
   
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = os.getenv('EMAIL_HOST')
   EMAIL_PORT = int(os.getenv('EMAIL_PORT', numero-du-port))
   EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
   EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
   DEFAULT_FROM_EMAIL = 'à compléter par votre adresse mail'
   ```
5. **Dans un fichier nommé _utils.py_ à la racine du projet, ajoutez les emails des destinataires et des expéditeurs.**

## 🧾 Licence <a name="licence"></a>
Ce projet est licencié sous la Licence Publique Générale Limitée GNU (LGPL) version 3 ou ultérieure. Voir le fichier [LICENSE](./LICENSE.txt) pour plus de détails.

---
## 🔍 Projet original <a name="origproject"></a>
Le projet a été initialement créé à partir de https://github.com/c3n7/hotel-reservation.
