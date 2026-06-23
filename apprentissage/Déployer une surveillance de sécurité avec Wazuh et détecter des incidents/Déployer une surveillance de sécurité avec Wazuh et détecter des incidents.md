<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>


**Auteur** : Yann (Administrateur Infrastructure Sécurisée)

**Projet** : Juin 2026


# Déployer une surveillance de sécurité avec Wazuh et détecter des incidents

**Mission 1** : Installation et Configuration de Wazuh - Installer Wazuh dans un environnement simulé et configurer la collecte de logs.

## Déploiement de la plateforme Wazuh (Quickstart)

Wazuh est une solution de sécurité open-source combinant des fonctionnalités XDR (protection des terminaux) et SIEM (gestion des événements). La solution repose sur un agent universel et trois composants centraux : le serveur (Manager), l'Indexer et le Dashboard. 

Pour ce projet, nous utilisons la méthode d'installation *Quickstart*, qui permet de déployer ces trois composants centraux sur un seul et même hôte.

### 1. Prérequis

**Prérequis système**
L'installation nécessite un processeur 64-bit. Pour ce déploiement, nous utilisons un environnement **Ubuntu 24.04**

**Prérequis matériels**
Les ressources nécessaires dépendent du nombre de machines supervisées. Pour un déploiement *All-in-one* avec 90 jours de rétention des logs, voici les recommandations :

| Nombre d'agents | CPU | RAM | Stockage (90 jours) |
| :--- | :--- | :--- | :--- |
| **1 à 25** | 4 vCPU | 8 Go | 50 Go |
| **25 à 50** | 8 vCPU | 8 Go | 100 Go |
| **50 à 100** | 8 vCPU | 8 Go | 200 Go |

📸 **[Capture d'écran : Affiche le terminal de ton serveur Ubuntu avec la commande `htop` (ou `free -m` et `lscpu`) et `df -h` pour prouver que ta machine virtuelle respecte bien ces prérequis matériels]**

### 2. Installation de Wazuh

Sur le serveur Ubuntu, télécharger et exécuter l'assistant d'installation avec l'option `-a` (pour tout installer sur la même machine) :

```bash
curl -sO [https://packages.wazuh.com/4.14/wazuh-install.sh](https://packages.wazuh.com/4.14/wazuh-install.sh) && sudo bash ./wazuh-install.sh -a
```

Une fois le script terminé, le terminal affichera un message de succès ainsi que les identifiants de connexion :

INFO: --- Summary ---
INFO: You can access the web interface https://<IP_DE_DU_SERVEUR>
    User: admin
    Password: <MOT_DE_PASSE_GENERE>
INFO: Installation finished.

📸 [Capture d'écran : Le terminal affichant ce fameux message "Summary" avec l'IP et le mot de passe. Pense à flouter une partie du mot de passe pour montrer que tu appliques les bonnes pratiques de sécurité]

**Note :** Tu peux trouver les mots de passe de tous les utilisateurs de l'indexeur Wazuh et de l'API Wazuh dans le fichier wazuh-passwords.txt à l'intérieur de l'archive wazuh-install-files.tar. Pour les imprimer, exécute la commande suivante :

```bash
sudo tar -O -xvf wazuh-install-files.tar wazuh-install-files/wazuh-passwords.txt
```

**Désinstallation :** Si tu souhaites désinstaller les composants centraux de Wazuh ultérieurement, il suffit d'exécuter l'assistant d'installation de Wazuh en utilisant l'option -u ou --uninstall.

### 3. Accès au Dashboard

* Ouvre le navigateur et se rendre sur https://<IP_DU_SERVEUR>.
* Lors du premier accès, le navigateur affiche un message d'avertissement indiquant que le certificat n'a pas été émis par une autorité de confiance. Ceci est attendu et l'utilisateur a la possibilité d'accepter le certificat comme exception ou, alternativement, de configurer le système pour utiliser un certificat provenant d'une autorité de confiance.

📸 [Capture d'écran : L'avertissement de sécurité du navigateur (type "Votre connexion n'est pas privée").]

Connecte-toi avec l'utilisateur admin et le mot de passe fourni à l'étape précédente.

📸 [Capture d'écran : La page d'accueil globale de Wazuh (le Dashboard) montrant que l'interface est fonctionnelle.]

### 4. Post-installation : Désactiver les mises à jour

**Action recommandée : désactiver les mises à jour de Wazuh**

Il est recommandé de désactiver les référentiels de packages Wazuh après l'installation pour éviter les mises à niveau accidentelles qui pourraient briser l'environnement.

Exécute la commande suivante pour désactiver le référentiel Wazuh (version APT pour Ubuntu :

```bash
sudo sed -i "s/^deb/#deb/" /etc/apt/sources.list.d/wazuh.list
```

📸 [Capture d'écran : Un petit cat /etc/apt/sources.list.d/wazuh.list montrant que la ligne est bien commentée avec un # devant]

