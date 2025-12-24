<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>

# Procédure pour installation de GLPI 11 sur Débian 13

### Sommaire

1. Présentation
2. Les Prérequis d'installation
3. Préparation du serveur
  * Installation du socle LAMP (Linux, Apache, MariaDB, PHP)
  * Préparation de la base de donnée MariaDB
  * Télécharger GLPI 11.04
  * Préparation de GLPI
  * Configurer Apache 2 pour GLPI
  * Utiliser PHP8.4-FPM qui est la dernière version recommandé pour Apache2
4. Installation de GLPI 
5. Conclusion

### 1. Présentation

Afin de faire cette procédure d'installation de GLPI 11.04 qui est la dernière version en date, je vais l'installer sur une machine Debian 13. GLPI est un logiciel libre de gestion de parc informatique. Il permet la gestion du support informatique grace à un système de tickets, ainsi que l'inventaire des équipements informatiques (postes de travail, téléphones, imprimantes, licences etc). Créé en 2003 et maintenu par l'éditeur français Teclib, GLPI est une solution open source gratuite pouvant ètre installée sur un serveur interne ou utilisée pour la gestion du support de clients.

Une offre optionnelle, **GLPI Network**, est également proposé par l'éditeur. Elle peut ètre déployée sur site ou en mode cloud et permet de bénéficier de fonctionnalités supplémentaires et d'un support avancé.

### 2. Les prérequis d'installation

Avant de passer à l’installation, il est nécessaire de vérifier les prérequis. GLPI fonctionne avec un serveur web, PHP et une base de données. Même s’il peut être installé sur Windows Server avec IIS, une installation sous Linux est recommandée. GLPI est compatible avec plusieurs serveurs web comme Apache2, Nginx ou IIS.

Pour GLPI 11, la version minimale requise est PHP 8.2, ainsi qu’une base de données MySQL (8.0 minimum) ou MariaDB (10.6 minimum). Certaines extensions PHP sont également nécessaires au bon fonctionnement de l’application.

Dans cette procédure, l’installation sera réalisée sur une machine Debian 13 avec Apache2, PHP 8.4 et MariaDB, versions disponibles dans les dépôts Debian.

Pour plus d’informations, la documentation officielle de GLPI peut être consultée. https://github.com/glpi-project/glpi

### 3. Préparation du serveur

L’installation débute par la mise à jour des paquets du système sur la machine Debian 13. Il est également nécessaire de configurer l’adresse IP, le nom d’hôte et, si besoin, l’enregistrement DNS associé à l’application.

Etape suivante en pratique: 

```bash
sudo apt update && sudo apt upgrade -y
```

### Installation du socle LAMP

La première étape consiste à installer les composants du socle LAMP nécessaires au fonctionnement de GLPI : Linux, Apache2, MariaDB et PHP.

Sous Debian 13, PHP 8.4 est disponible par défaut dans les dépôts officiels. Dans cette procédure, PHP sera utilisé via PHP-FPM, afin d’améliorer les performances par rapport au module PHP intégré à Apache.

L’installation débute par la mise en place des paquets principaux :

```bash
sudo apt install apache2 php8.4-fpm mariadb-server
```

Ensuite, les extensions PHP nécessaires au bon fonctionnement de GLPI seront installées, celles-ci n’étant pas incluses dans le paquet php8.4-common.

```bash
sudo apt install php8.4-{curl,gd,intl,mysql,zip,bcmath,mbstring,xml,bz2}
```

   * **curl** : permet à GLPI de communiquer avec des services externes, comme le téléchargement de plugins depuis la marketplace ou la récupération de flux distants.

   * **gd** : sert au traitement des images, notamment pour l’affichage ou la génération d’éléments graphiques dans l’interface.

   * **intl** : gère les paramètres régionaux, tels que les formats de date, de nombre et les langues, afin d’assurer une bonne internationalisation de l’application.

   * **mysql** : assure la connexion entre GLPI et la base de données MySQL ou MariaDB pour le stockage et l’accès aux données.

   * **zlib** : utilisée pour la compression et la décompression des fichiers, notamment lors de l’utilisation de la marketplace et pour la génération de documents.

   * **bcmath** : fournit des fonctions de calcul précis, nécessaires entre autres à la génération des QR codes.

   * **mbstring** : permet la gestion correcte des caractères multioctets, indispensable pour le support de l’UTF-8 et la compatibilité avec plusieurs langues.

   * **xml** (dom, simplexml, xmlreader, xmlwriter) : fournit les outils nécessaires à la lecture et au traitement des fichiers XML utilisés par certaines fonctionnalités de GLPI.

   * **openssl** : permet l’utilisation de connexions sécurisées, comme le HTTPS ou l’authentification via des services externes.

   * **bz2** : utilisée pour la gestion des fichiers compressés nécessaires au bon fonctionnement de la marketplace GLPI.

Ces commandes permettent d’installer les extensions PHP requises pour PHP 8.4.

L’extension LDAP est uniquement nécessaire si GLPI doit être connecté à un annuaire, comme Active Directory. Dans le cas contraire, son installation peut être réalisée ultérieurement si le besoin se présente.

```bash
sudo apt install php8.4-ldap
```

L’installation de Apache2, MariaDB, PHP et de toutes les extensions nécessaires est maintenant terminée.

### Préparation de la base de donnée

Nous allons préparer MariaDB pour héberger la base de données de GLPI.
La première étape consiste à exécuter la commande suivante afin de réaliser les réglages de sécurité de base de MariaDB.

```bash
sudo mariadb-secure-installation
```

Ensuite, nous allons créer une base de données dédiée pour GLPI, accessible via un utilisateur spécifique.
Il est important de ne pas utiliser le compte root de MariaDB et d’appliquer le principe du moindre privilège : une base = un utilisateur.

Connectez-vous à votre instance MariaDB avec la commande suivante :

```bash
sudo mysql -u root -p
```

Saisissez le mot de passe root de MariaDB défini précédemment.

Ensuite, exécutez les requêtes SQL suivantes pour créer la base de données dbyann_glpi et l’utilisateur glpi_admin avec son mot de passe (à personnaliser).
Cet utilisateur disposera de tous les droits sur cette base, et uniquement sur celle-ci.

```bash
CREATE DATABASE dbyann_glpi;
GRANT ALL PRIVILEGES ON dbyann_glpi.* TO glpi_admin@localhost IDENTIFIED BY "*Militaire26100@";
FLUSH PRIVILEGES;
EXIT
```

### Télécharger GLPI 11.04

L’étape suivante consiste à télécharger l’archive .tgz contenant les fichiers d’installation de GLPI.
Depuis le dépôt GitHub officiel de, récupérez le lien correspondant à la dernière version disponible.

* https://github.com/glpi-project/glpi/releases/

```bash
cd /tmp
wget https://github.com/glpi-project/glpi/releases/download/11.0.4/glpi-11.0.4.tgz
```

Si le wget n'est pas installé, faire un : 

```bash
sudo apt install wget
```
Ensuite, exécutez la commande suivante afin de décompresser l’archive .tgz dans le répertoire /var/www/.
Les fichiers de GLPI seront alors accessibles via le chemin /var/www/glpi.

```bash
sudo tar -xzvf glpi-11.0.4.tgz -C /var/www/
```

### Préparation de GLPI

Nous allons maintenant préparer l’installation de GLPI 11 en créant les répertoires nécessaires et en configurant les permissions.

Dans un premier temps, l’utilisateur www-data (utilisé par Apache2 sous Debian/Ubuntu) sera défini comme propriétaire des fichiers GLPI.

```bash
sudo chown www-data /var/www/glpi/ -R
```

Ensuite, plusieurs répertoires doivent être créés afin de déplacer certaines données en dehors de la racine web /var/www/glpi. Cette organisation permet de renforcer la sécurité de l’installation, conformément aux recommandations de l’éditeur.

Répertoire /etc/glpi
Ce répertoire est destiné à accueillir les fichiers de configuration de GLPI. Des droits d’accès sont accordés à l’utilisateur www-data afin de permettre à l’application d’y accéder correctement.

```bash
sudo mkdir /etc/glpi
sudo chown www-data /etc/glpi/
```

Ensuite, le répertoire sensible config de GLPI est déplacé vers /etc/glpi afin de le sortir de la racine web :

```bash
sudo mv /var/www/glpi/config /etc/glpi
```

* Le répertoire /var/lib/glpi

Répétons la même opération avec la création du répertoire /var/lib/glpi :

```bash
sudo mkdir /var/lib/glpi
sudo chown www-data /var/lib/glpi/
```

Dans lequel nous déplaçons également le dossier files qui contient la majorité des fichiers de GLPI : CSS, plugins, etc.

```bash
sudo mv /var/www/glpi/files /var/lib/glpi
```

* Répertoire /var/log/glpi

Cette dernière étape consiste à créer le répertoire /var/log/glpi, destiné au stockage des journaux (logs) de GLPI.
Comme précédemment, les droits nécessaires sont attribués à l’utilisateur www-data afin de permettre le bon fonctionnement de l’application.

```bash
sudo mkdir /var/log/glpi
sudo chown www-data /var/log/glpi
```

Aucun déplacement de fichiers n’est nécessaire dans ce répertoire.

* Création des fichiers de configuration

Il faut maintenant configurer GLPI pour lui indiquer l’emplacement des nouveaux répertoires créés.
Le premier fichier de configuration sera créé à cette étape.

```bash
sudo nano /var/www/glpi/inc/downstream.php
```

Nous allons maintenant renseigner le fichier de configuration afin d’indiquer à GLPI l’emplacement du répertoire /etc/glpi.
Insérez le contenu suivant dans le fichier :

```bash
<?php
define('GLPI_CONFIG_DIR', '/etc/glpi/');
if (file_exists(GLPI_CONFIG_DIR . '/local_define.php')) {
    require_once GLPI_CONFIG_DIR . '/local_define.php';
}
```

Une fois ce fichier configuré, créez un second fichier de configuration avec la commande suivante :

```bash
sudo nano /etc/glpi/local_define.php
```

```bash
<?php
define('GLPI_VAR_DIR', '/var/lib/glpi/files');
define('GLPI_LOG_DIR', '/var/log/glpi');
```

GLPI permet de définir d’autres variables pour personnaliser l’emplacement de différents répertoires. À titre d’exemple, la variable **GLPI_CACHE_DIR** peut être utilisée pour spécifier un répertoire dédié au cache.

Cette étape de configuration est maintenant terminée.

### Configurer Apache 2 pour GLPI

La configuration du serveur web Apache2 passe par la création d’un VirtualHost spécifique à GLPI.

Pour cet environnement de test, le fichier de configuration utilisé est glpi.test.archeagglo.fr.conf, correspondant au nom de domaine glpi.test.archeagglo.fr, choisi pour accéder à l’application.

L’utilisation d’un nom de domaine dédié, même en interne, permet de structurer les environnements et facilite par la suite la mise en place d’une connexion sécurisée via HTTPS.

```bash
sudo nano /etc/apache2/sites-available/glpi.test.archeagglo.conf
```

```bash
<VirtualHost *:80>
    ServerName glpi.test.archeagglo.fr

    DocumentRoot /var/www/glpi/public

    # If you want to place GLPI in a subfolder of your site (e.g. your virtual host is serving multiple applications),
    # you can use an Alias directive. If you do this, the DocumentRoot directive MUST NOT target the GLPI directory itself.
    # Alias "/glpi" "/var/www/glpi/public"

    <Directory /var/www/glpi/public
        Require all granted

        RewriteEngine On

        # Ensure authorization headers are passed to PHP.
        # Some Apache configurations may filter them and break usage of API, CalDAV, ...
        RewriteCond %{HTTP:Authorization} ^(.+)$
        RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

        # Redirect all requests to GLPI router, unless file exists.
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^(.*)$ index.php [QSA,L]

    </Directory>
</VirtualHost>
```

Une fois la configuration terminée, enregistrez le fichier.

Il est ensuite nécessaire d’activer ce nouveau VirtualHost au sein d’Apache2 à l’aide de la commande suivante :

```bash
sudo a2ensite glpi.test.archeagglo.fr.conf
```

Par la même occasion, le site configuré par défaut dans Apache2 est désactivé, celui-ci n’étant pas nécessaire.

```bash
sudo a2dissite 000-default.conf
```

Le module rewrite d’Apache doit également être activé. Il est indispensable au fonctionnement des règles de réécriture définies dans le fichier de configuration du VirtualHost, notamment via les directives RewriteCond et RewriteRule.

```bash
sudo a2enmod rewrite
```

Il ne reste plus qu'à redémarrer le service Apache2

```bash
sudo systemctl restart apache2
```

### Utiliser PHP8.4-FPM qui est la dernière version recommandé pour Apache2

Pour permettre l’exécution des scripts PHP avec Apache2, deux modes sont possibles : l’utilisation du module PHP intégré à Apache ou le recours à PHP-FPM.

Dans cette procédure, PHP-FPM a été retenu car il offre de meilleures performances et fonctionne comme un service séparé d’Apache, contrairement au module PHP intégré où chaque processus Apache charge son propre moteur PHP.

Le paquet php8.4-fpm ayant déjà été installé précédemment, il reste à finaliser son intégration avec Apache2.
Cette étape consiste à activer les modules nécessaires ainsi que la configuration associée à PHP-FPM, puis à recharger le service Apache2 afin d’appliquer les changements.

```bash
sudo a2enmod proxy_fcgi setenvif
sudo a2enconf php8.4-fpm
sudo systemctl reload apache2
```

```bash
sudo nano /etc/php/8.4/fpm/php.ini
```

Dans ce fichier, repérez le paramètre **session.cookie_httponly** (via CTRL + W avec nano) et définissez sa valeur sur **ON**, afin de renforcer la sécurité des cookies utilisés par GLPI

```bash
; Whether or not to add the httpOnly flag to the cookie, which makes it
; inaccessible to browser scripting languages such as JavaScript.
; https://php.net/session.cookie-httponly
session.cookie_httponly = on
```

Afin d’améliorer la sécurité, configurez également la directive session.cookie_samesite avec la valeur Lax, conformément aux recommandations de la documentation GLPI.
Cette option permet de contrôler l’envoi du cookie de session par le navigateur et contribue à limiter certaines attaques de type CSRF (Cross-Site Request Forgery)

```bash
; Add SameSite attribute to cookie to help mitigate Cross-Site Request Forgery (CSRF/XSRF)
; Current valid values are "Strict", "Lax" or "None". When using "None",
; make sure to include the quotes, as `none` is interpreted like `false` in ini files.
; https://tools.ietf.org/html/draft-west-first-party-cookies-07
session.cookie_samesite = Lax
```

Une fois les modifications effectuées, enregistrez le fichier.
D’autres ajustements pourront être réalisés par la suite, notamment pour augmenter la taille maximale des fichiers envoyés dans GLPI (upload_max_filesize, fixée à 2 Mo par défaut) ou pour activer la directive session.cookie_secure lorsque l’application sera accessible en HTTPS.

Afin de prendre en compte ces changements, il est nécessaire de redémarrer le service PHP-FPM

```bash
sudo systemctl restart php8.4-fpm.service
```

Pour terminer, il est nécessaire d’adapter le VirtualHost Apache afin d’indiquer que le traitement des fichiers PHP doit être assuré par PHP-FPM.

Cette configuration permet à Apache2 de transmettre l’exécution des fichiers .php au socket PHP-FPM dédié.

Éditez le fichier glpi.test.archeagglo.fr.conf et ajoutez la configuration suivante

```bash
<FilesMatch \.php$>
    SetHandler "proxy:unix:/run/php/php8.4-fpm.sock|fcgi://localhost/"
</FilesMatch>
```

Voici un exemple: 



Quand c'est fait, relancer Apache2

```bash
sudo systemctl restart apache2
```

La configuration est maintenant terminée. Il ne reste plus qu’à lancer l’installation de GLPI via l’interface web

### 4. Installation de GLPI

La configuration est maintenant terminée. Il ne reste plus qu’à lancer l’installation de GLPI via l’interface web.

* Vérification des prérequis
GLPI analyse la configuration du serveur pour vérifier que tous les prérequis sont remplis.

Si toutes les vérifications sont vertes dans la colonne des résultats, vous pouvez continuer.

* Configuration de la base de données

  * Serveur SQL : localhost (MariaDB est installé sur le même       serveur).
  
  * Utilisateur : glpi_admin et le mot de passe correspondant.
  
  * Base de données : sélectionnez dbyann_glpi (créée précédemment).
  Cliquez ensuite sur Continuer et patientez pendant l’initialisation.

* Résultat attendu
Si tout s’est bien passé, l’initialisation se termine correctement et vous obtenez l’écran indiquant que la base est prête.

* Création du compte administrateur
  * Le compte administrateur par défaut est glpi / glpi.
  * Connectez-vous avec ces identifiants pour accéder à votre interface GLPI.

* Désactivation des données de démonstration
Dans l’interface, cliquez sur Désactiver les données de démonstration pour obtenir un environnement vierge



* Actions de sécurité finales
  * Changez le mot de passe de tous les comptes par défaut (liens dans l’encadré orange).
  * Supprimez le fichier install.php pour éviter tout risque de réinstallation

```bash
sudo rm /var/www/glpi/install/install.php
```

L’installation est désormais terminée. GLPI est prêt à être utilisé et configuré selon les besoins (création des utilisateurs, gestion des catégories, mise en place des tickets, etc.).

### 5. Conclusion

Ce tutoriel a permis de détailler, étape par étape, l’installation de GLPI sur un serveur Debian 13.
À quelques ajustements près, cette procédure peut également être adaptée à d’autres distributions Linux ou versions du système.



# Procédure d’installation et de préparation de GLPI 11

![alt text](<../Images/Tableau de bord glpi.png>)

## Sommaire

- [Procédure pour installation de GLPI 11 sur Débian 13](#procédure-pour-installation-de-glpi-11-sur-débian-13)
    - [Sommaire](#sommaire)
    - [1. Présentation](#1-présentation)
    - [2. Les prérequis d'installation](#2-les-prérequis-dinstallation)
    - [3. Préparation du serveur](#3-préparation-du-serveur)
    - [Installation du socle LAMP](#installation-du-socle-lamp)
    - [Préparation de la base de donnée](#préparation-de-la-base-de-donnée)
    - [Télécharger GLPI 11.04](#télécharger-glpi-1104)
    - [Préparation de GLPI](#préparation-de-glpi)
    - [Configurer Apache 2 pour GLPI](#configurer-apache-2-pour-glpi)
    - [Utiliser PHP8.4-FPM qui est la dernière version recommandé pour Apache2](#utiliser-php84-fpm-qui-est-la-dernière-version-recommandé-pour-apache2)
    - [4. Installation de GLPI](#4-installation-de-glpi)
    - [5. Conclusion](#5-conclusion)
- [Procédure d’installation et de préparation de GLPI 11](#procédure-dinstallation-et-de-préparation-de-glpi-11)
  - [Sommaire](#sommaire-1)
  - [1. Présentation](#1-présentation-1)
    - [1.1 Objectifs](#11-objectifs)
  - [2. Prérequis](#2-prérequis)
    - [2.1 Matériel](#21-matériel)
    - [2.2 Logiciel](#22-logiciel)
    - [2.3 Réseau et flux](#23-réseau-et-flux)
  - [3. Préparation du serveur Debian 13](#3-préparation-du-serveur-debian-13)
    - [3.1 Mise à jour](#31-mise-à-jour)
    - [3.2 Durcissement de base](#32-durcissement-de-base)
  - [4. Installation de la stack LAMP](#4-installation-de-la-stack-lamp)
    - [4.1 Installation Apache, PHP-FPM et MariaDB](#41-installation-apache-php-fpm-et-mariadb)
    - [4.2 Installation des extensions PHP](#42-installation-des-extensions-php)
  - [5. Préparation de MariaDB](#5-préparation-de-mariadb)
    - [5.1 Sécurisation](#51-sécurisation)
    - [5.2 Création de la base GLPI](#52-création-de-la-base-glpi)
  - [6. Téléchargement et préparation de GLPI](#6-téléchargement-et-préparation-de-glpi)
    - [6.1 Téléchargement](#61-téléchargement)
    - [6.2 Préparation des répertoires et permissions](#62-préparation-des-répertoires-et-permissions)
  - [7. Configuration Apache pour GLPI](#7-configuration-apache-pour-glpi)
    - [7.1 VirtualHost complet](#71-virtualhost-complet)
    - [7.2 Activation et redémarrage](#72-activation-et-redémarrage)
  - [8. Configuration PHP-FPM](#8-configuration-php-fpm)
  - [9. Installation via l’interface web](#9-installation-via-linterface-web)
  - [10. Sécurisation post-installation](#10-sécurisation-post-installation)
  - [11. Sauvegardes et PRA](#11-sauvegardes-et-pra)
  - [12. Tests et validation](#12-tests-et-validation)
  - [13. Table de correspondance DAT ↔ Procédure](#13-table-de-correspondance-dat--procédure)
  - [14. Conclusion](#14-conclusion)



## 1. Présentation

### 1.1 Objectifs

Installer GLPI 11.04 sur Debian 13 en environnement de test, en respectant les besoins du DAT : gestion de parc, helpdesk, intégration LDAP, sécurité, supervision et stratégie de sauvegarde.

## 2. Prérequis

### 2.1 Matériel

* VM Proxmox
* 2 vCPU, 4 Go RAM, 50 Go SSD
* Partitionnement recommandé : `/` 15 Go, `/var` 10 Go, `/var/log` 5 Go, `/var/lib/mysql` 15 Go, `/home` 5 Go

### 2.2 Logiciel

* Debian 13
* Apache2
* MariaDB 10.11+
* PHP 8.4
* Extensions : php-mysqli, php-curl, php-gd, php-intl, php-ldap, php-zip, php-mbstring, php-xml

### 2.3 Réseau et flux

* IP fixe, DNS configuré
* Ports : 22 (SSH), 443 (HTTPS), 636 (LDAPS), 587 (SMTP), 161 (SNMP)

## 3. Préparation du serveur Debian 13

### 3.1 Mise à jour

```bash
sudo apt update && sudo apt upgrade -y
```

![alt text](../Images/Mise_à_jour_debian13.png)

### 3.2 Durcissement de base

* Désactiver SSH root
* Authentification par clé
* Pare-feu UFW activé

## 4. Installation de la stack LAMP

### 4.1 Installation Apache, PHP-FPM et MariaDB

```bash
sudo apt install apache2 php8.4-fpm mariadb-server
```

### 4.2 Installation des extensions PHP

```bash
sudo apt install php8.4-{curl,gd,intl,mysql,zip,bcmath,mbstring,xml,bz2,ldap}
```

## 5. Préparation de MariaDB

### 5.1 Sécurisation

```bash
sudo mariadb-secure-installation
```

![alt text](../Images/Securisation_MariaDB.png)

### 5.2 Création de la base GLPI

```sql
CREATE DATABASE dbyann_glpi;
GRANT ALL PRIVILEGES ON dbyann_glpi.* TO glpi_admin@localhost IDENTIFIED BY 'Monmotdepasse';
FLUSH PRIVILEGES;
EXIT;
```

![alt text](../Images/Création_de_la_base_de_donnée.png)

## 6. Téléchargement et préparation de GLPI

### 6.1 Téléchargement

```bash
cd /tmp
wget https://github.com/glpi-project/glpi/releases/download/11.0.4/glpi-11.0.4.tgz
sudo tar -xzvf glpi-11.0.4.tgz -C /var/www/
```

### 6.2 Préparation des répertoires et permissions

```bash
sudo chown www-data:www-data /var/www/glpi -R
sudo mkdir /etc/glpi /var/lib/glpi /var/log/glpi
sudo chown www-data:www-data /etc/glpi /var/lib/glpi /var/log/glpi
sudo mv /var/www/glpi/config /etc/glpi
sudo mv /var/www/glpi/files /var/lib/glpi
```

Créer fichiers de configuration :

```bash
sudo nano /var/www/glpi/inc/downstream.php
```

```php
<?php
define('GLPI_CONFIG_DIR', '/etc/glpi/');
if (file_exists(GLPI_CONFIG_DIR . '/local_define.php')) {
    require_once GLPI_CONFIG_DIR . '/local_define.php';
}
```

```bash
sudo nano /etc/glpi/local_define.php
```

```php
<?php
define('GLPI_VAR_DIR', '/var/lib/glpi/files');
define('GLPI_LOG_DIR', '/var/log/glpi');
```

## 7. Configuration Apache pour GLPI

### 7.1 VirtualHost complet

```bash
sudo nano /etc/apache2/sites-available/glpi_test.archeagglo.fr.conf
```

```apache
<VirtualHost *:80>
    ServerName glpi_test.archeagglo.fr

    DocumentRoot /var/www/glpi/public

    # Alias optionnel
    # Alias "/glpi" "/var/www/glpi/public"

    <Directory /var/www/glpi/public>
        Require all granted

        RewriteEngine On
        RewriteCond %{HTTP:Authorization} ^(.+)$
        RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteRule ^(.*)$ index.php [QSA,L]
    </Directory>
</VirtualHost>
```

![alt text](../Images/Config_apache2.png)

### 7.2 Activation et redémarrage

```bash
sudo a2ensite glpi.test.archeagglo.fr.conf
sudo a2dissite 000-default.conf
sudo a2enmod rewrite proxy_fcgi setenvif
sudo systemctl restart apache2
```

## 8. Configuration PHP-FPM

```bash
sudo nano /etc/php/8.4/fpm/php.ini
```

```ini
session.cookie_httponly = on
session.cookie_samesite = Lax
```

![alt text](../Images/Config_php.ini.png)

Redémarrage PHP-FPM :

```bash
sudo systemctl restart php8.4-fpm
```

Pour terminer, il est nécessaire d’adapter le VirtualHost Apache afin d’indiquer que le traitement des fichiers PHP doit être assuré par PHP-FPM.

Cette configuration permet à Apache2 de transmettre l’exécution des fichiers .php au socket PHP-FPM dédié.

Éditez le fichier glpi_test.archeagglo.fr.conf et ajoutez la configuration suivante

```bash
<FilesMatch \.php$>
    SetHandler "proxy:unix:/run/php/php8.4-fpm.sock|fcgi://localhost/"
</FilesMatch>
```

![alt text](../Images/Config_php-fpm_pour_apache2.png)

Quand c'est fait, relancer Apache2

```bash
sudo systemctl restart apache2
```

La configuration est maintenant terminée. Il ne reste plus qu’à lancer l’installation de GLPI via l’interface web.

## 9. Installation via l’interface web

* Vérifier prérequis
* Configurer BDD `dbyann_glpi` / utilisateur `glpi_admin`
* Créer compte administrateur
* Supprimer `/install`

```bash
sudo rm /var/www/glpi/install/install.php
```

![alt text](../Images/Conf_glpi_test.png)
![alt text](../Images/conf_glpi_test2.png)
![alt text](../Images/conf_glpi_test3.png)
![alt text](../Images/conf_glpi_test4.png)
![alt text](../Images/conf_glpi_test5.png)
![alt text](../Images/conf_glpi_test6.p,g.png)
![alt text](../Images/conf_glpi_test7.png)
![alt text](../Images/conf_glpi_test8.png)
![alt text](../Images/conf_glpi_test9.png)
![alt text](../Images/conf_glpi_test10.png)
![alt text](../Images/conf_glpi_test11.png)
![alt text](../Images/conf_glpi_test12.png)
![alt text](../Images/conf_glpi_test13.png)

## 10. Sécurisation post-installation

* HTTPS (Let's Encrypt en production)
* SSH restreint / clé
* Fail2ban
* Mises à jour régulières

## 11. Sauvegardes et PRA

* Dump quotidien MariaDB
* Backup répertoires `/etc/glpi` et `/var/lib/glpi`
* Snapshots VM Proxmox
* Rétention 30 jours
* Stratégie 3-2-1

## 12. Tests et validation

* Vérifier accès HTTPS
* Authentification LDAP
* Envoi notifications SMTP
* Création et gestion tickets
* Ajout équipements
* Sauvegardes restaurables

## 13. Table de correspondance DAT ↔ Procédure

| Exigence DAT        | Section Procédure |
| ------------------- | ----------------- |
| Gestion de parc     | Sections 6, 12    |
| Helpdesk            | Sections 9, 12    |
| Authentification AD | Section 13.2      |
| Sécurité HTTPS      | Section 10        |
| Sauvegardes         | Section 11        |
| PRA                 | Section 11        |
| Supervision         | Section 12        |
| Sécurité système    | Sections 3.2, 8   |

## 14. Conclusion

Procédure complète, conforme aux besoins du DAT, sécurisée et prête pour mise en production.

**Auteur :** ESCRIVA Yann

**Projet :** Décembre 2025