# Procédure pour installation de GLPI 11 sur Débian 13

**Sommaire :**

I. Présentation

II. Prérequis de GLPI

III. Préparation du serveur pour installer GLPI

```
A. Installer le socle LAMP
B. Préparer une base de donnée pour GLPI
C. Télécharger GLPI
D. Préparer l'installation
E. Configurer Apache2 pour GLPI
F. Utiliser PHP8.4-FPM avec Apache 2
IV. Installation de GLPI
V. Conclusion
```

**I. Présentation**

**GLPI** est un logiciel libre de **gestion de parc informatique** permettant d'avoir une solution de ticketing gratuite pour le support informatique, de gérer l'inventaire des équipements, notamment les ordinateurs et les téléphones, de gérer ses contrats, ses licences, ses consommables, ses baies serveurs, etc.... Créé en 2003, GLPI est une solution populaire utilisée par des milliers d'entreprises et maintenue par un éditeur français nommé Teclib.

**II. Préréquis de GLPI**

Avant d'évoquer l'installation, parlons des prérequis. GLPI a besoin d'**un serveur Web, de PHP et d'une base de données** pour fonctionner. Bien que l'installation de GLPI soit possible sur Windows Server via IIS, l'installation sur Linux est recommandée. D'une façon générale, GLPI supporte **plusieurs serveurs Web** : Apache2, Nginx, lighttpd et IIS.

Pour l'**installation** de GLPI, nous avons besoin de :

*   **Version de PHP** : au minimum **PHP 8.2** pour GLPI 11.
*   Base de données
    *   MySQL 8.0 minimum
    *   MariaDB 10.6 minimum

Il y aura également plusieurs extensions PHP à installer pour que GLPI puisse fonctionner.

III. **Préparer le sereveur pour installer GLPI**

Commençons par l'installation par une **mise à jour des paquets sur la machine Debian 13**. Bien Penser également à lui attribuer une adresse IP, un nom d'hôte (avec un enregistrement DNS pour notre application) et à effectuer la configuration du système.

La suite des opérations s'effectue directement depuis le Terminal :  

`sudo apt update && sudo apt upgrade`

**A. Installer le socle LAMP**

La première grande étape consiste à installer les paquets du socle LAMP : **Linux Apache2 MariaDB PHP**. Sous **Debian 13 Trixie** qui est la dernière version majeure stable de Debian, **PHP 8.4** est distribué par défaut dans les dépôts officiels. Il est à noter que l'intégration de PHP sera effectuée via PHP-FPM plutôt que l'extension PHP pour Apache, pour des raisons de performance.

Commençons par installer les trois paquets principaux :

`sudo apt-get install apache2 php8.4-fpm mariadb-server`

Puis, nous allons installer toutes les extensions nécessaires au bon fonctionnement de GLPI et qui ne sont pas intégrées au paquet `**php8.4-common.**`

 `sudo apt install php8.4-{curl,gd,intl,mysql,zip,bcmath,mbstring,xml,bz2}`

Voici, à titre d'information, le rôle de chaque extension installée :

*   `**curl**` : utilisée pour accéder à des ressources distantes (marketplace, flux RSS, etc.).
*   `**gd**` : permet la manipulation et la génération d’images.
*   `**intl**` : fournit les fonctions d’internationalisation (formats, locale, conversions…).
*   `**mysql**` : gère la connexion et les opérations avec une base de données MySQL/MariaDB.
*   `**zlib**` : nécessaire pour la compression/décompression, notamment pour les paquets gzip du marketplace et la génération de PDF.
*   `**bcmath**` : utilisé pour générer des QR codes (calculs de précision arbitraire).
*   `**mbstring**` : indispensable pour la gestion des chaînes de caractères multioctets (UTF-8, conversions, compatibilité internationale).
*   `**xml**` (inclut `**dom**`, `**simplexml**`, `**xmlreader**`, `**xmlwriter**`) : fournit les outils nécessaires au traitement XML utilisés par diverses fonctions de l’application.
*   `**openssl**` : permet la communication chiffrée (connexion HTTPS, authentification OAuth 2.0, etc.).
*   `**bz2**` : pour le bon fonctionnement de la marketplace.

Ces commandes vont permettre de récupérer les versions de ces extentions pour php 8.4

Pour associer GLPI avec un annuaire LDAP comme active directory, on doit installer l'extention LDAP de PHP, sinon sinon ce n'est pas nécessaire

`sudo apt install php8.4-ldap`

Nous venons d'installer Apache2, MariaDB, PHP et un ensemble d'extensions.

**B. Préparer une base de données pour GLPI**

Nous allons préparer MariaDB afin qu'il puisse héberger la base de données de GLPI, La première action à effectuer, c'est d'exécuter la commande ci-dessous pour **effectuer le minimum syndical en matière de sécurisation de MariaDB**

`sudo mariadb-secure-installation`

`# Si vous utilisez MySQL :`

`sudo mysql_secure_installation`

Ensuite, nous allons changer le mot de passe root, supprimer les utilisateurs anonnymes et désactiver l'accès root à distance.

Ci dessous un exemple de bonne configuration.

Ensuite, nous allons créer **une base de données dédiée pour GLPI** et celle-ci sera accessible par **un utilisateur dédié**. Hors de question d'utiliser le compte root de MariaDB : appliquons le principe de moindre privilège. Donc : une base de données = un utilisateur.

Se connecter à l'instance MariaDB: 

`sudo mysql -u root -p`

Saisir le mot de passe root qu'on vient de définir à l'étape précédente.

`CREATE DATABASE **db25_glpi**;`

`GRANT ALL PRIVILEGES ON **db25_glpi**.* TO **glpi_adm**@localhost IDENTIFIED BY "**MotDePasseRobuste**"; FLUSH PRIVILEGES;`

`EXIT`

**C. Télécharger GLPI**

Maintenant, nous allons télécharger l'archive **".tgz"** qui contient les sources d'installation de GLPI. À partir du **GitHub de GLPI**, récupérez le lien vers la dernière version. Ici, c'est la version **GLPI 11.0.4** qui est installée.

*   [https://github.com/glpi-project/glpi/releases/](https://github.com/glpi-project/glpi/releases/)

l'archive sera téléchargé dans le répertoire `/tmp` :

`cd /tmp wget` [`https://github.com/glpi-project/glpi/releases/download/11.0.4/glpi-11.0.4.tgz`](https://github.com/glpi-project/glpi/releases/download/11.0.4/glpi-11.0.4.tgz)

Ensuite, nous allons exécuter la commande ci-dessous pour **décompresser l'archive .tgz dans le répertoire** `**/var/www/**`, ce qui donnera le chemin d'accès `**/var/www/glpi**` pour GLPI.

`sudo tar -xzvf glpi-11.0.4.tgz -C /var/www/`

**D. Préparer l'installation**

Nous allons préparer l'**installation de GLPI 11** via la création de plusieurs répertoires et la personnalisation des permissions.

Tout d'abord, nous allons définir l'utilisateur `**www-data**` correspondant à **Apache2** (sur Debian/Ubuntu), en tant que **propriétaire** sur les fichiers GLPI.

`sudo chown www-data /var/www/glpi/ -R`