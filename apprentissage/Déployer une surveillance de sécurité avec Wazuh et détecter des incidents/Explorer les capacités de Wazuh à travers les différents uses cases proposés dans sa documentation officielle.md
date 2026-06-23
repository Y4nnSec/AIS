<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>


**Auteur** : Yann (Administrateur Infrastructure Sécurisée)

**Projet** : Juin 2026


* Intégration de l'IDS Suricata : https://documentation.wazuh.com/current/proof-of-concept-guide/integrate-network-ids-suricata.html

# Intégration d'un NIDS (Suricata) avec Wazuh

L'intégration d'un système de détection d'intrusions réseau (NIDS) permet d'améliorer la détection des menaces en surveillant et en analysant le trafic réseau. 

Ce cas d'usage démontre comment intégrer Suricata avec Wazuh. Suricata fournit une visibilité supplémentaire sur la sécurité du réseau grâce à ses capacités d'inspection du trafic en temps réel.

## 1. Infrastructure requise

* **Machine cible (Endpoint) :** Un serveur sous **Ubuntu 24.04** avec l'agent Wazuh préalablement installé. 
* **Rôle :** C'est sur cette machine qu'est installé Suricata. Wazuh surveillera et analysera le trafic réseau généré et intercepté sur ce point de terminaison.

## 2. Installation et configuration de Suricata

Les étapes suivantes permettent de configurer Suricata sur la machine cible et d'envoyer les journaux générés vers le serveur Wazuh.

### 2.1 Installation des paquets

Ajouter le dépôt officiel, mettre à jour la liste des paquets et installer Suricata :

```bash
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt-get update
sudo apt-get install suricata -y
```

📸 [Capture d'écran : Le terminal affichant la fin de l'installation de Suricata avec succès, ou le résultat de la commande *suricata -V* montrant la version installée]

### 2.2 Téléchargement des règles de détection

**Télécharger et extraire le jeu de règles Emerging Threats pour Suricata :**

```bash  
cd /tmp/ && curl -LO [https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz](https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz)
sudo tar -xvzf emerging.rules.tar.gz && sudo mkdir -p /etc/suricata/rules && sudo mv rules/*.rules /etc/suricata/rules/
sudo find /etc/suricata/rules -name "*.rules" -exec chmod 777 {} \;
```  
  
### 2.3 Configuration de Suricata

Il est nécessaire de modifier les paramètres de Suricata dans le fichier */etc/suricata/suricata.yaml* afin de définir le réseau à surveiller et l'interface réseau.

**Définir les variables de réseau :**
  
```YAML
HOME_NET: "<IP_DE_LA_MACHINE_UBUNTU_24.04>"
EXTERNAL_NET: "any"

default-rule-path: /etc/suricata/rules
rule-files:
  - "*.rules"

# Configuration globale des statistiques
stats:
  enabled: yes
```  
  
Définir l'interface réseau à écouter (remplacer *enp0s3* par le nom réel de l'interface de la machine, qui peut être obtenu via la commande *ip a* :
  
```YAML  
# Prise en charge de la capture haute vitesse Linux
af-packet:
  - interface: enp0s3 
```  
  
📸 [Capture d'écran : Le terminal affichant le résultat de la commande *ip a* prouvant le nom de l'interface réseau, à côté du fichier *suricata.yaml* modifié montrant le bon nom d'interface renseigné]

Redémarrer le service Suricata pour appliquer les modifications :
  
```BASH  
sudo systemctl restart suricata  
```  
  
📸 [Capture d'écran : Le résultat de la commande *systemctl status suricata* montrant le service en statut "active (running)"]

## 3. Configuration de l'agent Wazuh

Afin que l'agent Wazuh puisse lire et transmettre les alertes générées par Suricata, il faut modifier la configuration locale de l'agent.

Ajouter le bloc de configuration suivant dans le fichier */var/ossec/etc/ossec.conf* de la machine cible (Ubuntu) :  
  
```XML  
 <ossec_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</ossec_config> 
```  
  
Redémarrer l'agent Wazuh pour appliquer les changements :
  
```BASH  
sudo systemctl restart wazuh-agent  
```  
  
## 4. Simulation d'attaque et vérification

Wazuh analyse désormais automatiquement les données du fichier */var/log/suricata/eve.json* et génère les alertes correspondantes sur le tableau de bord.

### 4.1 Émulation
Pour vérifier le bon fonctionnement, générer un trafic ICMP (Ping) depuis le serveur Wazuh (ou une autre machine) vers la machine cible Ubuntu surveillée par Suricata :

```Bash  
 ping -c 20 "<IP_DE_LA_MACHINE_UBUNTU>" 
```  
  
 📸 [Capture d'écran : Le terminal d'une machine distante en train d'exécuter la commande ping vers la machine Ubuntu surveillée]
  
### 4.2 Visualisation des alertes

Il est possible de visualiser les données d'alerte directement dans le tableau de bord Wazuh.

Pour ce faire :

* Accéder au module Threat Hunting.

* Ajouter le filtre suivant dans la barre de recherche pour isoler les événements du NIDS : rule.groups:suricata.

📸 [Capture d'écran : Le dashboard Wazuh (Threat Hunting) filtré avec rule.groups:suricata, montrant clairement les événements de trafic réseau interceptés (ex: ICMP request)]

## 5. Dépannage (Troubleshooting)

En cas d'erreur de démarrage de Suricata, il est fréquent de rencontrer l'erreur suivante dans les journaux (*/var/log/suricata/suricata.log*) :

```plaintext  
16/9/2022 -- 12:32:16 - <Error> - [ERRCODE: SC_ERR_AFP_CREATE(190)] - Unable to find iface eth0: No such device
16/9/2022 -- 12:32:16 - <Error> - [ERRCODE: SC_ERR_AFP_CREATE(190)] - Couldn't init AF_PACKET socket, fatal error
``` 
  
**Résolution :** Ce problème survient lorsque le nom de l'interface réseau renseigné dans la configuration est incorrect. Il convient de vérifier le nom exact de l'interface réseau disponible sur le système (*ip a*) et de corriger la directive interface dans le fichier */etc/suricata/suricata.yaml*.

* Surveillance de l'intégrité de répertoires/fichiers sensibles : https://documentation.wazuh.com/current/proof-of-concept-guide/poc-file-integrity-monitoring.html

# Surveillance de l'intégrité des fichiers (FIM)

Le contrôle d'intégrité des fichiers (File Integrity Monitoring - FIM) permet d'auditer les fichiers sensibles et de répondre aux exigences de conformité réglementaire. Wazuh dispose d'un module FIM intégré qui surveille les modifications du système de fichiers afin de détecter la création, la modification et la suppression de fichiers.

Ce cas d'usage exploite le module FIM de Wazuh pour détecter les modifications dans des répertoires surveillés sur des points de terminaison Linux et Windows. Le module enrichit les données d'alerte en récupérant des informations sur l'utilisateur et le processus à l'origine des modifications.

## 1. Infrastructure requise

* **Serveur Linux (Ubuntu 24.04) :** Le module FIM surveillera un répertoire spécifique sur cette machine cible pour détecter les changements de fichiers.
* **Poste Client (Windows 11) :** Le module FIM surveillera un répertoire spécifique sur ce point de terminaison pour détecter les mêmes types d'événements.

## 2. Configuration

### 2.1 Configuration de la machine cible Ubuntu

Les étapes suivantes permettent de configurer l'agent Wazuh pour surveiller les modifications du système de fichiers dans le répertoire `/root` (ou tout autre répertoire de test).

1. Éditer le fichier de configuration de l'agent Wazuh `/var/ossec/etc/ossec.conf`. 
2. Ajouter le répertoire à surveiller dans le bloc `<syscheck>`. Pour obtenir des informations supplémentaires (audit complet en temps réel et reporting des changements), la configuration suivante doit être utilisée :

```xml
<directories check_all="yes" report_changes="yes" realtime="yes">/root</directories>
```

(*Note : Il est possible de configurer n'importe quel chemin dans le bloc <directories> en fonction des besoins de sécurité*).

📸 [Capture d'écran : Le fichier ossec.conf ouvert dans un éditeur de texte (comme nano ou vim) sur la machine Ubuntu, mettant en évidence la ligne <directories...> ajoutée dans le bloc <syscheck>]

* Redémarrer l'agent Wazuh pour appliquer les modifications de configuration :

```bash
sudo systemctl restart wazuh-agent
```

### 2.2 Configuration de la machine cible Windows

Les étapes suivantes permettent de configurer l'agent Wazuh pour surveiller les modifications dans le répertoire du bureau de l'utilisateur.

* Ouvrir le fichier de configuration *C:\Program Files (x86)\ossec-agent\ossec.conf* sur la machine Windows surveillée (avec des droits d'administrateur).

* Ajouter le répertoire à surveiller dans le bloc <*syscheck*>. Il faut remplacer <*USER_NAME*> par le nom de l'utilisateur de la session Windows 11 :

```XML
<directories check_all="yes" report_changes="yes" realtime="yes">C:\Users\<USER_NAME>\Desktop</directories>
```

📸 [Capture d'écran : Le fichier ossec.conf ouvert dans le Bloc-notes (Notepad) ou Notepad++ sur la machine Windows 11, avec la ligne bien renseignée avec le bon nom d'utilisateur]

Redémarrer le service de l'agent Wazuh à l'aide de PowerShell (lancé en tant qu'administrateur) pour appliquer les changements :

```PowerShell
Restart-Service -Name wazuh
```

(*Note : En environnement de production, plutôt que de configurer localement chaque agent, il est possible de configurer de manière centralisée des groupes d'agents depuis le serveur Wazuh*).

## 3. Test et simulation

Afin de vérifier que le module FIM remonte correctement les informations, il faut simuler une activité suspecte sur les deux machines (Ubuntu et Windows) dans les répertoires surveillés :

* Créer un fichier texte dans le répertoire surveillé.

* Attendre 5 secondes.

* Ajouter du contenu au fichier texte, puis l'enregistrer.

* Attendre 5 secondes.

* Supprimer le fichier texte du répertoire surveillé.

📸 [Capture d'écran : Deux terminaux (ou fenêtres) côte à côte. L'un montrant la création/modification du fichier sur Ubuntu (via des commandes comme touch, echo, rm), l'autre montrant l'action équivalente sur le bureau Windows 11]

## 4. Visualisation des alertes

Il est possible de visualiser les données d'alerte générées par ces actions directement dans le tableau de bord Wazuh.

Pour ce faire :

* Se rendre dans le module File Integrity Monitoring (ou Threat Hunting) de l'interface web.

* Ajouter le filtre suivant dans la barre de recherche pour interroger spécifiquement les alertes de création, modification et suppression de fichiers :

  * rule.id: is one of 550,553,554

📸 [Capture d'écran : Le tableau de bord Wazuh filtré par ces rule.id, montrant clairement les trois phases de l'attaque simulée (Création = 554, Modification = 550, Suppression = 553) pour les deux agents (Ubuntu et Windows)]

📸 [Capture d'écran supplémentaire (Optionnelle mais recommandée) : Le détail d'une des alertes (en cliquant sur la petite flèche pour l'étendre), montrant le contenu exact qui a été modifié ou ajouté dans le fichier texte, prouvant que l'attribut report_changes="yes" fonctionne correctement]





























































Détection d'attaques bruteforce : https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html
* Détection de processus non autorisés : https://documentation.wazuh.com/current/proof-of-concept-guide/detect-unauthorized-processes-netcat.html
* Détection de tentatives d'injection SQL : https://documentation.wazuh.com/current/proof-of-concept-guide/detect-web-attack-sql-injection.html
* Détection de cheval de troie : https://documentation.wazuh.com/current/proof-of-concept-guide/poc-detect-trojan.html
* Traitement de malware à travers l'intégration de VirusTotal : https://documentation.wazuh.com/current/proof-of-concept-guide/detect-remove-malware-virustotal.html
* Détection de vulnérabilités : https://documentation.wazuh.com/current/proof-of-concept-guide/poc-vulnerability-detection.html
* Détection de processus cachés par rootkit : https://documentation.wazuh.com/current/proof-of-concept-guide/poc-detect-hidden-process.html
* Détection de commandes malveillantes : https://documentation.wazuh.com/current/proof-of-concept-guide/audit-commands-run-by-user.html
* Détection d'attaques shellshock : https://documentation.wazuh.com/current/proof-of-concept-guide/detect-web-attack-shellshock.html