<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>

INITIALISATION A LA CLASSIFICATION DES VULNERABILITEES

**Eternal Blue :**

1. **Donnez la référence CVE** :CVE-2017-0144
2. **Description en une phrase :**

EternalBlue est une vulnérabilité dans le protocole SMBv1 de Windows qui permet une exécution de code à distance sans authentification via des paquets, il est utilisé par des vers comme Wannacry et NotPetya.

3. **Citez des éléments d'infrastructure pouvant être concernés :**

* Serveurs et postes Windows non patché.
* Controleur de domaine
* Ordinateurs connectés en réseau local avec SMBv1 activé
* Partages réseau utilisant SMBv1

4. **Trouvez, mettez à jour ou calculez le score base CVSS (dernière version)**

Le score CVSS v3.1 pour la vulnérabilité EternalBlue est évalué à 8.8 sur 10, ce qui correspond à un niveau de sévérité élevé.

5. **Déterminer si un exploit est disponible publiquement, si oui en prendre connaissance et le citer en référence.**

Oui, un exploit est disponible publiquement pour EternalBlue. Il a été divulgué par le groupe Shadow Brokers en avril 2017, et il est diffusé depuis.

Références d’exploits publics :
Metasploit Framework
Module officiel : exploit/windows/smb/ms17_010_eternalblue

Documentation :

https://www.rapid7.com/db/modules/exploit/windows/smb/ms17_010_eternalblue

GitHub (Python)

Repo de Worawit Wang :
https://github.com/worawit/MS17-010

Ce repo contient plusieurs scripts de détection et d’exploitation de la faille.

EternalBlue Scanner :

Nmap a aussi des scripts de détection (ex : smb-vuln-ms17-010).

6. **Trouver si un score EPSS existe pour cette vuln :**

Score EPSS (au 10 avril 2025) : 0.97587 (97.59%)
Ce qui signifie une très forte probabilité.

**Krack :**

1. **Donnez la référence CVE :**

CVE-2017-13077

2. **Décrire la vulnérabilité en une phrase**

KRACK est une attaque contre le protocole WPA2 qui permet à un attaquant de réinitialiser des clés cryptographiques en interceptant et en rejouant desmessages entre 2 parties, compromettant ainsi la confidentialité du trafic Wi-Fi.

3. **Citez des éléments d'infrastructure pouvant être concernés :**

* Points d'accès Wi-Fi (routeurs, bornes)
* Clients Wi-Fi (ordinateurs portables, smartphones, objets connectés)
* Systèmes d’exploitation : Linux, Android (particulièrement vulnérables), Windows, macOS

4. **Trouvez, mettez à jour ou calculez le score base CVSS (dernière version) :**

Le score CVSS v3.1 pour la vulnérabilité Crack est évalué à 6.8 sur 10, ce qui correspond à un niveau de sévérité medium.

Le vecteur d'attaque associé est le suivant : CVSS:3.1 AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N

5. **décrit une vulnérabilité dans laquelle un attaquant, situé sur le même réseau local, peut exploiter une faille facilement,**

sans privilèges ni interaction de l'utilisateur, pour espionner partiellement le trafic sans affecter l'intégrité ou la disponibilité des données.

Déterminer si un exploit est disponible publiquement, si oui en prendre connaissance et le citer en référence.

Un exploit public a été développé par Mathy Vanhoef, le chercheur ayant découvert la vulnérabilité KRACK. Il a publié un proof-of-concept

qui permet de reproduire l'attaque sur des réseaux Wi-Fi vulnérables, notamment sur des systèmes Linux et Android.

Source https://github.com/vanhoefm/krackattacks-scripts

6. **Trouver si un score EPSS existe pour cette vuln :**

Environ 0,48%, indiquant une faible probabilité d'exploitation dans les 30 jours suivant la publication.

**log4shell :**

1. **Donnez la référence CVE :**

CVE-2021-44228

2. **Décrire la vulnérabilité en une phrase:**

Log4Shell est une vulnérabilité dans la bibliothèque de journalisation Log4j 2 qui permet à un attaquant d’exécuter du code à distance en envoyant une requête spécialement malveillante, ce qui expose les systèmes à des attaques de prise de contrôle à distance.

3. **Citez des éléments d'infrastructure pouvant être concernés :**

* Serveurs Web, notamment ceux utilisant des frameworks comme Apache Struts, Spring, ou Solr.
* Applications Java qui intègrent Log4j 2.
* Cloud services et plateformes utilisant Log4j 2 pour la gestion des logs.
* Serveurs de base de données, API, et applications qui reposent sur cette bibliothèque de logging pour leurs services.

4. **Trouvez, mettez à jour ou calculez le score base CVSS (dernière version) :**

Le score CVSS v3.1 pour la vulnérabilité Log4j est évalué à 10 sur 10, ce qui correspond à un niveau de sévérité critique.

Le vecteur d'attaque associé est le suivant : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H

Log4Shell est une vulnérabilité dans la bibliothèque de journalisation Log4j 2 qui permet à un attaquant d'exécuter du code arbitraire à distance

en exploitant la fonctionnalité de recherche de chaîne dans les journaux, exposant ainsi les systèmes vulnérables à des attaques de prise de contrôle.

5. **Déterminer si un exploit est disponible publiquement, si oui en prendre connaissance et le citer en référence :**

Oui, un exploit public est disponible pour Log4Shell.

Des scripts ont été publiés dès la découverte de la vulnérabilité, permettant à un attaquant d'exploiter la faille pour exécuter du code à distance.

6. **Trouver si un score EPSS existe pour cette vuln :**

Score EPSS : ~0.94 (94%) (valeur élevée, exploitabilité très probable dans un court délai)

Classement : Très élevé, ce qui indique une exploitation quasi immédiate après la découverte de la vulnérabilité.

Ce score montre que Log4Shell était une vulnérabilité à très haut risque d'exploitation rapide.

**Looney-tunables :**

1. **Donnez la référence CVE :**

CVE -2023-4911

2. **Décrire la vulnérabilité en une phrase**

Cette vulnérabilité permet à un attaquant local de manipuler une variable d'environnement d'éxécuter du code arbitraire avec des privilèges élevés.

3. **Citez des éléments d'infrastructure pouvant être concernés**

* Serveurs Linux exécutant des services critiques (web, bases de données, mail) avec des binaires SUID root.
* Stations de travail Linux utilisées par les administrateurs ou développeurs.
* Systèmes embarqués ou appliances utilisant glibc (routeurs, firewalls, IoT).
* Conteneurs Docker ou autres environnements virtualisés basés sur des images Linux vulnérables.
* Applications internes utilisant des scripts ou binaires dépendant de glibc pour le traitement de tâches automatisées avec élévation de privilèges.

4. **Trouvez, mettez à jour ou calculez le score base CVSS (dernière version)**

La vulnérabilité suivante dispose d'un score CVSS v3.1 de  **7.8** , classée comme  **élevée** .

5. **Déterminer si un exploit est disponible publiquement, si oui en prendre connaissance et le citer en référence.**

Un module Metasploit est disponible, (`linux/local/glibc_tunables_priv_esc` (vérifie la version vulnérable et tente l'élévation de privilèges.)

6. **Trouver si un score EPSS existe pour cette vuln**

Score EPSS : ~0.78 (78,3%) (valeur élevée, exploitabilité très probable dans un court délai).

la probabilité estimée d’exploitation dans les 30 jours est d’environ 78% .

**CITRIX**

1. **Donnez la référence CVE :**

CVE-2025-7775

2. **Décrire la vulnérabilité en une phrase**

C'est une vulnérabilité qui permet à un attaquant non authentifié d'envoyer des données spécialement conçu à un serveur NetScaler vulnérable.

3. **Citez des éléments d'infrastructure pouvant être concernés**

* Appliances NetScaler ADC / NetScaler Gateway (physiques & virtuels) — prise de contrôle RCE ou plantage complet du service.
* Interfaces d’administration (GUI/CLI) exposées — compromission des identifiants d’administration et modification de la config.
* Passerelles VPN / accès distant — compromission des sessions VPN, accès non autorisé au réseau interne.
* Équilibreur de charge (load-balancer) en front-office — interruption de service pour toutes les applis derrière lui (DoS).

4. **Trouvez, mettez à jour ou calculez le score base CVSS (dernière version)**

CVSS v4.0 (base) :  9.2 — Critical .

Vecteur (CVSS 4.0) : CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L

5. **Déterminer si un exploit est disponible publiquement, si oui en prendre connaissance et le citer en référence.**

Pas d'exploit public pour le moment.

### Auteur : ESCRIVA Yann

### Projet : Octobre 2025
