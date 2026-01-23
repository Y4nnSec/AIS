<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>


# Procédure d'installation et de configuration de l'Agent GLPI (Debian)


**Objectif :** Installer l'agent GLPI sur un serveur Debian pour scanner le réseau via SNMP.


## Prérequis

* Serveur : Debian 12 ou supérieur
* Accès Root ou Sudo
* Serveur GLPI : Accessible via HTTPS
* Informations nécessaires : URL du GLPI, Communauté SNMP des équipements (ex: `public`).


## Partie 1 : Installation de l'Agent

Nous utilisons les paquets `.deb` officiels pour garantir une installation propre et reconnue par le système.

**Nettoyage (Si une installation précédente a échoué)**

Si des tentatives manuelles ont été faites précédemment :

```bash
sudo apt purge glpi-agent -y
sudo rm -rf /usr/local/bin/glpi-agent
sudo rm -rf /etc/glpi-agent
```

**Téléchargement des paquets**
Il faut télécharger le cœur de l'agent et le module réseau (indispensable pour le SNMP)

**Télécharger l'agent principal**

```bash
wget [https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent_1.15-1_all.deb](https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent_1.15-1_all.deb)
```

**Télécharger le module Network (Obligatoire pour scanner les switchs)**

```bash
wget [https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent-task-network_1.15-1_all.deb](https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent-task-network_1.15-1_all.deb)
```

**vérifier que le module réseau est bien chargé par l'agent**

```bash
sudo glpi-agent --list-tasks
```

* Résultat attendu : On doit voir apparaître ces deux lignes dans la liste :

  * NetDiscovery (v...) 
  * NetInventory (v...)

*Si on ne les voit pas, c'est que le paquet glpi-agent-task-network n'est pas installé*.

**Installation**

On utilise apt pour gérer les dépendances automatiquement (Perl, librairies, etc.)

**Installer l'agent et le module réseau**

```bash
sudo apt install ./glpi-agent_1.15-1_all.deb ./glpi-agent-task-network_1.15-1_all.deb -y
```


## Partie 2 : Configuration de l'Agent

**Configuration du serveur et du SSL**

On modifie le fichier de configuration pour pointer vers le serveur GLPI. (Si le serveur GLPI a un certificat auto-signé, il faut désactiver la vérification SSL)

**Définir l'URL du serveur**

```bash
sudo sed -i 's|# server = http://localhost/glpi|server = https://glpi_test.archeagglo.fr/front/inventory.php|' /etc/glpi-agent/agent.cfg
```

**Désactiver la vérification SSL (pour les environnements de test/auto-signés)**

```bash
echo "no-ssl-check = 1" | sudo tee -a /etc/glpi-agent/agent.cfg
```

**Vérification du Service Systemd**

Il faut s'assurer que le service pointe bien vers le bon exécutable (**/usr/bin/glpi-agent**) et non une ancienne installation.

**Editer le service**

```bash
sudo nano  /etc/systemd/system/glpi-agent.service
```

* Vérifier la ligne **ExecStart**. Elle doit être comme la configuration ci dessous : 

```ini, TOML
ExecStart=/usr/bin/glpi-agent --daemon --no-fork $OPTIONS
```

(*Si elle pointe vers **/usr/local/bin**, corrigez-la vers **/usr/bin***)

**Redémarrage et Validation**

* Recharger la configuration système

```bash
sudo systemctl daemon-reload
```

* Redémarrer l'agent

```bash
sudo systemctl restart glpi-agent
```

* Vérifier que le statut est "Active"

```bash
sudo systemctl status glpi-agent
```


## Partie 3 : Configuration dans GLPI (Interface Web)

**Activation de l'Agent**

* Aller dans **Parc > Agents**
* Cliquer sur l'agent nouvellement remonté
* Aller dans l'onglet **Modules** (ou Configuration).
* Activer (Mettre sur "Oui" ou cocher) :
  * Découverte réseau
  * Inventaire réseau

**Création des identifiants SNMP**

L'agent a besoin du mot de passe pour lire les infos du switch.

* Aller dans **Administration > Inventaire > Authentification SNMP**
* Cliquer sur **Ajouter**
* Nom : **Switchs** (par exemple)
* Communauté : **public** (ou votre mot de passe réel).
* Version : **v2c** (généralement)

**Définition de la cible (Plage IP)**

* Aller dans Administration > **Inventaire > Plages IP**
* Créer une plage nommée "**Switchs Salle Serveur**".
* Renseigner l'IP de début et de fin (ex: **192.168.1.50** à **192.168.1.50**, pour un seul équipement).

**Création de la Tâche de Découverte**

C'est ici qu'on lie tout ensemble

* Aller dans **Administration > Inventaire > Tâches**
* Créer une tâche nommée "**Scan Découverte**" et cocher Actif
* Dans **Configuration du Job** :
  * Méthode du module : Choisir **Découverte réseau**
  * Cibles : Ajouter la **Plage IP** créée plus haut
  * Acteurs : Ajouter l' **Agent**
  * Identifiants SNMP : Ajouter la communauté créée à l'étape 2
* Cliquer sur Mettre à jour.


## Partie 4 : Exécution et Importation

**Lancer le scan**

Sur le serveur Linux, forcer l'agent à récupérer sa tâche immédiatement :

```bash
sudo glpi-agent --force
```

*Le log doit afficher running task NetDiscovery*

**Importer le matériel**
Une fois le scan terminé :

* Aller dans **Administration > Inventaire > Matériel non géré**
* Trouver la ligne correspondant au switch (l'Adresse MAC doit être présente).
* Cocher la ligne.
* Cliquer sur **Actions > Importer**
* Choisir le type : **Matériel réseau**

Le switch est désormais visible et géré dans **Parc > Matériel réseau** avec ses ports et connexions.










# Procédure de déploiement : Agent GLPI et Inventaire Réseau SNMP

**Auteur :** Yann (Administrateur Infrastructure Sécurisée) 

**Contexte :** Mise en place d'une remontée automatique d'inventaire réseau (Switchs) vers GLPI.

**Objectif :**

Installer et configurer l'agent GLPI sur un serveur Debian 13 pour effectuer la découverte et l'inventaire réseau via le protocole SNMP.

### Prérequis :

* Serveur : Debian 12 ou supérieur.
* Privilèges : Accès Root ou utilisateur avec droits sudo.
* Serveur GLPI : Accessible via HTTPS.

Informations nécessaires : URL du serveur GLPI, Communauté SNMP des équipements (ex: public).

### Partie 1 : Installation de l'Agent

Nous utilisons les paquets .deb officiels pour garantir une installation propre, stable et facile à maintenir via apt.

**Nettoyage** (Optionnel)

Cette étape est nécessaire uniquement si une installation manuelle précédente a échoué.

```Bash
sudo apt purge glpi-agent -y
sudo rm -rf /usr/local/bin/glpi-agent
sudo rm -rf /etc/glpi-agent
```

**Téléchargement des paquets**

Il est nécessaire de télécharger le cœur de l'agent et le module réseau (indispensable pour le support SNMP).

**Télécharger l'agent principal (Version 1.15)**

```bash
wget https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent_1.15-1_all.deb
```

**Télécharger le module Network (Obligatoire pour scanner les switchs)**

```bash
wget https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent-task-network_1.15-1_all.deb
```

**Installation**

Nous utilisons **apt** pour gérer automatiquement les dépendances (Perl, librairies système, etc.).

**Installer l'agent et le module réseau simultanément**

```bash
sudo apt install ./glpi-agent_1.15-1_all.deb ./glpi-agent-task-network_1.15-1_all.deb -y
```

**Vérification de l'installation des modules**

Une fois installé, nous vérifions que l'agent a bien chargé les tâches réseaux.

```Bash
glpi-agent --list-tasks
```

**Résultat attendu :**

La liste doit contenir les lignes suivantes :

* NetDiscovery (v...) 
* NetInventory (v...)

Si ces lignes sont absentes, le paquet glpi-agent-task-network est manquant.

### Partie 2 : Configuration de l'Agent

**Configuration du serveur et du SSL**

Nous modifions le fichier de configuration pour pointer vers le serveur GLPI. 

Si le serveur GLPI utilise un certificat auto-signé, la vérification SSL doit être désactivée.

**Définir l'URL du serveur cible**

```bash
sudo sed -i 's|# server = http://localhost/glpi|server = https://glpi_test.archeagglo.fr/front/inventory.php|' /etc/glpi-agent/agent.cfg
```

**Désactiver la vérification SSL (Uniquement pour environnement de test)**

```bash
echo "no-ssl-check = 1" | sudo tee -a /etc/glpi-agent/agent.cfg
```

**Vérification du Service Systemd**

Nous nous assurons que le service pointe vers le bon exécutable installé par APT (/usr/bin).

**Éditer la configuration du service de manière sécurisée**

```bash
sudo systemctl edit --full glpi-agent.service
```

**Vérifier la ligne ExecStart. Elle doit correspondre exactement à ceci :**


```Ini, TOML
ExecStart=/usr/bin/glpi-agent --daemon --no-fork $OPTIONS
```

(Si le chemin indique /usr/local/bin, le corriger vers /usr/bin).

**Redémarrage et Validation**

* Recharger la configuration des démons

```bash
sudo systemctl daemon-reload
```

* Redémarrer l'agent pour appliquer les changements

```bash
sudo systemctl restart glpi-agent
```

**Vérifier que le statut est "Active (running)"**

```bash
sudo systemctl status glpi-agent
```

### Partie 3 : Configuration dans GLPI (Interface Web)

**Activation de l'Agent**

* Aller dans **Parc > Agents**.
* Sélectionner l'agent nouvellement remonté.
* Aller dans l'onglet **Modules** (ou Configuration).
* Activer les options suivantes :
  * Découverte réseau : Oui
  * Inventaire réseau : Oui

**Création des identifiants SNMP**

L'agent a besoin de la communauté ("mot de passe") pour interroger les switchs.

* Aller dans **Administration > Inventaire > Authentification SNMP**.
* Cliquer sur **Ajouter**.
* **Nom** : Switchs (explicite).
* **Communauté** : *public* (ou la communauté configurée sur le matériel).
* **Version** : v2c (Standard actuel).

**Définition de la cible (Plage IP)**

* Aller dans **Administration > Inventaire > Plages IP**.
* Créer une nouvelle plage (ex: "Switchs Salle Serveur").
* Renseigner l'IP de début et de fin (ex: **192.168.1.50** à **192.168.1.50** pour cibler un équipement unique).

**Création de la Tâche de Découverte**

Cette étape lie l'agent, la cible et les identifiants.

* Aller dans **Administration > Inventaire > Tâches**.
* Créer une tâche nommée "Scan Découverte" et cocher la case **Actif**.
* Dans l'onglet **Configuration du Job** :
  * **Méthode du module** : Sélectionner Découverte réseau.
  * **Cibles** : Ajouter la Plage IP créée précédemment.
  * **Acteurs** : Ajouter l' Agent configuré.
  * **Identifiants SNMP** : Ajouter la communauté créée à l'étape 2.
* Cliquer sur **Mettre à jour**.

### Partie 4 : Exécution et Importation

**Lancer le scan (Force Run)**

Sur le serveur Linux, nous forçons l'agent à récupérer sa tâche immédiatement sans attendre le cycle planifié :

```Bash
sudo glpi-agent --force
```

Vérification : Le terminal doit afficher running task NetDiscovery.

**Importer le matériel**

Une fois le scan terminé :

* Retourner dans GLPI : **Administration > Inventaire > Matériel non géré**.
* Repérer la ligne correspondant au switch (Vérifier que l'Adresse MAC est présente).
* Cocher la ligne.
* Cliquer sur **Actions > Importer**.
* Choisir le type : **Matériel réseau**.

**Résultat :**

 Le switch est désormais visible, géré et détaillé (ports, VLANs) dans le menu **Parc > Matériel réseau**.