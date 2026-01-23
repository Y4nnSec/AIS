<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>


# Procédure d'installation et de configuration de l'Agent GLPI (Debian)



**Objectif :** Installer l'agent GLPI sur un serveur Debian pour scanner le réseau via SNMP.


## Prérequis

* Serveur : Debian 12 ou supérieur
* Accès Root ou Sudo.
* Serveur GLPI : Accessible via HTTPS.
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
Il faut télécharger le cœur de l'agent et le module réseau (indispensable pour le SNMP).

**Télécharger l'agent principal**

```bash
wget [https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent_1.15-1_all.deb](https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent_1.15-1_all.deb)
```

**Télécharger le module Network (Obligatoire pour scanner les switchs)**

```bash
wget [https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent-task-network_1.15-1_all.deb](https://github.com/glpi-project/glpi-agent/releases/download/1.15/glpi-agent-task-network_1.15-1_all.deb)
```

**Installation**

On utilise apt pour gérer les dépendances automatiquement (Perl, librairies, etc.)

* Installer l'agent et le module réseau

```bash
sudo apt install ./glpi-agent_1.15-1_all.deb ./glpi-agent-task-network_1.15-1_all.deb -y
```


## Partie 2 : Configuration de l'Agent

**Configuration du serveur et du SSL**

On modifie le fichier de configuration pour pointer vers le serveur GLPI. (Si le serveur GLPI a un certificat auto-signé, il faut désactiver la vérification SSL).

* Définir l'URL du serveur

```bash
sudo sed -i 's|# server = http://localhost/glpi|server = https://glpi_test.archeagglo.fr/front/inventory.php|' /etc/glpi-agent/agent.cfg
```

* Désactiver la vérification SSL (pour les environnements de test/auto-signés)

```bash
echo "no-ssl-check = 1" | sudo tee -a /etc/glpi-agent/agent.cfg
```

**Vérification du Service Systemd**

Il faut s'assurer que le service pointe bien vers le bon exécutable (/usr/bin/glpi-agent) et non une ancienne installation.

* Editer le service

```bash
sudo nano  /etc/systemd/system/glpi-agent.service
```

Vérifier la ligne **ExecStart**. Elle doit être comme la configuration ci dessous : 

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

* Activation de l'Agent
  * Aller dans Parc > Agents.

  * Cliquer sur l'agent nouvellement remonté.

  * Aller dans l'onglet Modules (ou Configuration).

  * Activer (Mettre sur "Oui" ou cocher) :

    * Découverte réseau
    * Inventaire réseau$

**Création des identifiants SNMP**

L'agent a besoin du mot de passe pour lire les infos du switch.

Aller dans Administration > Inventaire > Authentification SNMP.

Cliquer sur Ajouter.

Nom : Communauté Switchs (par exemple).

Communauté : public (ou votre mot de passe réel).

Version : v2c (généralement).

3. Définition de la cible (Plage IP)
Aller dans Administration > Inventaire > Plages IP.

Créer une plage nommée "Switchs Salle Serveur".

Renseigner l'IP de début et de fin (ex: 192.168.1.50 à 192.168.1.50 pour un seul équipement).

4. Création de la Tâche de Découverte
C'est ici qu'on lie tout ensemble.

Aller dans Administration > Inventaire > Tâches.

Créer une tâche nommée "Scan Découverte" et cocher Actif.

Dans Configuration du Job :

Méthode du module : Choisir Découverte réseau (Network Discovery).

Cibles : Ajouter la Plage IP créée plus haut.

Acteurs : Ajouter l' Agent (glpi-test).

Identifiants SNMP : Ajouter la communauté créée à l'étape 2.

Cliquer sur Mettre à jour.