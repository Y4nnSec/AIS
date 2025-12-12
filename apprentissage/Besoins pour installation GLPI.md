# Projet : Besoins et procédure d'installation et de Déploiement GLPI

**Contexte :** Mise en place d'une solution de gestion de parc informatique sur **Debian 13**.


## 1. Analyse des Besoins Clients
Avant tout déploiement technique, il est nécessaire de valider le périmètre avec le client :
* **Volumétrie :** Nombre d'utilisateurs finaux et nombre d'agents techniques.
* **Usage cible :** Gestion de parc (Inventaire), Helpdesk (Tickets), ou les deux.
* **Environnement existant :** Présence d'un Active Directory


## 2. Analyse des Risques
*(Voir la matrice des risques détaillée ci-dessous)*

![alt text](<Images/Matrice des risques.png>)


## 3. Prérequis Infrastructure (Hardware)
Le déploiement s'effectuera sur une **Machine Virtuelle (VM)** hébergée sur un hyperviseur **Proxmox**.

**OS Cible :** Debian 13 .

| Ressource | Recommandation | Justification |
| :--- | :--- | :--- |
| **vCPU** | **2 vCPU** | Suffisant pour le traitement PHP/Web standard. |
| **RAM** | **4 Go** | Minimum recommandé (Passer à 8 Go si >500 utilisateurs). |
| **Stockage** | **50 Go (SSD)** | OS + Base de données + Stockage des pièces jointes/Documents. |
| **Partitionnement** | **LVM Standard** | Séparer `/var` et `/home` si possible pour la sécurité et la gestion des logs. |


## 4. Prérequis Logiciels (LAMP)

Sur la base Debian 13, l'architecture suivante sera déployée :

* **Serveur Web :** `Apache2`
* **Base de données :** `MariaDB 10.11` (minimum) ou `MySQL 8.0`.
* **Langage :** `PHP 8.2` (minimum).


## 5. Prérequis Réseau et Flux

### Configuration IP
* **Adressage :** 1 Adresse IPv4 fixe.
* **DNS :** Enregistrement de type **A** pointant vers l'IP.

### Matrice de Flux (Firewall)

| Sens | Protocole | Port | Service | Description |
| :---: | :---: | :---: | :--- | :--- |
| **IN** | TCP | **80** | HTTP | Redirection automatique vers HTTPS. |
| **IN** | TCP | **443** | HTTPS | Accès sécurisé pour les utilisateurs et agents. |
| **IN** | TCP | **22** | SSH | Administration système (Restreint aux IPs Admins). |
| **OUT** | TCP | **636** | LDAPS | Liaison sécurisée vers l'Active Directory (Authentification). |
| **OUT** | TCP | **587** | SMTP | Relais vers serveur de messagerie (Envoi des notifications). |


## 6. Stratégie de Sécurité

* **Chiffrement (HTTPS) :**
    * Mise en place obligatoire d'un certificat SSL.
    * Utilisation de **Let’s Encrypt** via un Reverse Proxy (type *Nginx Proxy Manager*)

* **Sauvegardes (PRA) :**
    * **Base de données :** Dump SQL quotidien (`mysqldump`).
    * **Fichiers :** Sauvegarde du répertoire `/var/www/glpi` (documents, plugins).
    * **Stockage :** Export automatique vers un stockage externe (NAS/Cloud).


## 7. Planning Prévisionnel de Mise en Œuvre

1.  **Installation OS :** Installation complète de Debian 13 (NetInstall) et durcissement système.
2.  **Préparation LAMP :** Installation des paquets Apache2, MariaDB, PHP et optimisation des fichiers de configuration `php.ini` (memory_limit, upload_max_filesize).
3.  **Déploiement GLPI :** Téléchargement de l'archive, installation et suppression du dossier `/install`.
4.  **Intégration :** Configuration de la liaison **LDAPS** (Active Directory) et du collecteur mail **SMTP**.
5.  **Recette :** Tests fonctionnels (Connexion utilisateur, Création de ticket, Remontée d'inventaire).


*Document technique projet - Infrastructure yann ESCRIVA | Décembre 2025*