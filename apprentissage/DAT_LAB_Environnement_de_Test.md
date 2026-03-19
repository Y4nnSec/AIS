<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>

**DAT_Lab: Environnement de test**


**Auteur** : Yann (Administrateur Infrastructure Sécurisée)

**Projet** : Octobre 2025


1. **Résumé :**

Ce DAT décrit le déploiement d'un laboratoire reproduisant un service d'entreprise avec un contrôleur de domaine Windows server 2022, un pc client Windows 10 et un serveur Linux hébergeant l'application VulnerableLightApp. L'objectif est de fournir un environnement réaliste et vulnérable pour des exercices d'audit.

2. **Contexte et objectifs**

* Objectifs pédagogiques du Lab (déploiementet installation des machines comme demandé.
* Contraintes (vérifier intégrités des iso(Hashs ou Signatures).
* Rappels sécurité (isolement réseau, gestion des mots de passeet snapshot).

3. **Architecture réseau**

![alt text](Images/Diagramme_Lab_secu.png)

4. **Caractéristiques des machines**

| 🖥️**Nom VM** | 🧩**Rôle**      | 💿**OS (ISO)**      | ⚙️**CPU** | 🧠**RAM** | 💾**Stockage** | 🌐**IP** | 📝**Notes**                        |
| -------------------- | ---------------------- | ------------------------- | ----------------- | --------------- | -------------------- | -------------- | ---------------------------------------- |
| SRV-AIS              | Contrôleur de domaine | Windows Server 2022 (ISO) | 4                 | 4 GB            | 60 GB                | 192.168.79.143 | AD, DNS, DHCP, WINRM, SMB, RDP, BADBLOOD |
| PC-yann              | PC client              | Windows 10 (ISO)          | 4                 | 4 GB            | 60 GB                | 192.168.79.144 | Joins AD                                 |
| SRV-Linux            | Serveur Web            | Debian 12 (ISO)           | 2                 | 2 GB            | 20 GB                | 192.168.79.139 | WEB-VLA, SSH                             |

5. **Inventaire des comptes à privilèges**

| 👤**Compte** | 🧩**Rôle** | 💻**Machine** | 🔐**Emplacement du mot de passe** |
| ------------------ | ----------------- | ------------------- | --------------------------------------- |
| Administrateur     | Admin du domaine  | SRV-AIS             | Bitwarden                               |
| Local_admin        | Admin local       | PC-yann             | Bitwarden                               |
| Local_user         | Client            | PC-yann             | Bitwarden                               |
| Root               | Admin SRV Linux   | SRV_WEB             | Bitwarden                               |
| SRV_WEB User       | SRV Linux         | SRV_WEB             | Bitwarden                               |

![alt text](Images/Bitwarden.png)

6. **Diagramme Projet**

![alt text](Images/Diagramme_projet.png)

7. **Vérification des images (hashs/ signatures)**

Hash debian 13

![alt text](Images/Hash_debian_officiel.png)

![alt text](Images/Vérification_hash_debian.png)

Hash Windows server 2022

![alt text](Images/Hash_iso_winserver.png)

8. **Installation et configuration**

J’ai installé et configuré mes 3 machines virtuelles sur un hyperviseur de type 2 (VMWare Workstation pro) à savoir Windows server, Windows 10 ainsi que Debian13. Concernant les 3 machines, j’ai fait les mises à jour de sécurité ainsi qu'installé les VMWare Tools afin d’avoir de meilleurs performances et d’intégrations des VM avec mon hôte.Sur Windows server, j’ai installé mes rôles AD DS, DHCP, DNS et j’ai créé mon domaine (AIS.LAN).J’ai aussi fait mon partage SMB et activé le RDP Jai également lancé le script powershell (Badblood) qui permet de rajouter des milliers de comptes dans l’AD.Sur Windows10, je l’ai joint au domaine et Debian13, j’ai configuré et activé le SSH.J’ai aussi lancé Vulnerablelightapp qui est une application web volontairement vulnérable, conçue pour l’apprentissage et la pratique de la cybersécurité (tests d’intrusion, analyse de vulnérabilités, sécurisation d’applications, etc.). Elle héberge un serveur web (Kestrel)

Mise à jour de sécurité Windows server 2022 :

![alt text](Images/Mise_a_jour_windows_server.png)

![alt text](Images/Visuel_windows_server.png)

![alt text](Images/Gestionnaire_DHCP.png)

![alt text](Images/Nom_de_domaine_et_nom_de_serveur.png)

**Fichier partage SMB :**

![alt text](Images/Partage_SMB.png)

Droits NTFS Readonly:

![alt text](Images/Droits_NTFS_readonly.png)

Droits NTFS Writeaccess:

![alt text](Images/Droits_NTF_Writeaccess.png)

Partage sans authentification:

![alt text](Images/Partage_sans_authentification.png)

Statut RDP Windows server:

![alt text](Images/RDP_activé.png)

Lancement du script BadBlood :

![alt text](Images/Telechargement_badblood.png)

![alt text](Images/Lancement_du_script_badblood.png)

Mise à jour de sécurité Windows 10 :

![alt text](<Images/Mise_a jour_windows_10.png>)

Windows 10 au domaine :

![alt text](Images/Windows10_au_domaine.png)

Connection winrm et ssh réussi du pc client à l’AD :

![alt text](Images/Connection_winrm.png)

![alt text](Images/Connection_SSH.png)

Mise à jour de sécurité Debian 13 :

![alt text](Images/Mise_a_jour_de_securite_debian13.png)

Statut SSH :

![alt text](Images/SSH_Debian13.png)

Serveur-Web Linux VulnerableLightApp:

![alt text](Images/Vulnerablelightapp.png)

![alt text](Images/Erreur_401_vulnerabllightapp.png)

Nombre d'utilisateurs contenus dans l'AD :

![alt text](Images/Compteur_Users_AD.png)

Liste des comptes critiques de l’AD :

![alt text](Images/Users_critiques_AD_1.png)
![alt text](Images/Users_critiques_AD_2.png)

9. **Conclusionet retour d’expérience**

La mise en place de cet environnement de test m’a permis de reconstituer une architecture réseau complète et réaliste, intégrant les principaux services utilisés en entreprise : Active Directory, DNS, SMB, WinRM, SSH et un service Web.

L’infrastructure, composée d’un contrôleur de domaine Windows Server, d’un poste Client Windows et d’un serveur Linux hébergeant VulnerableLightApp, offre une base fonctionnelle pour la formation et l’analyse de vulnérabilités.

L’exécution du script BadBlood a enrichi le domaine Active Directory avec des comptes et relations typiques d’un réseau d’entreprise, ce qui permet de simuler des scénarios d’attaque et d’audit réalistes.

L’ensemble des services a été vérifié : connexions SSH et WinRM réussies, partages SMB opérationnels avec droits NTFS.Sur le plan technique, ce projet m’a permis de renforcer mes compétences en administration système Windows et Linux, en gestion des droits NTFS et des comptes AD.

 En conclusion, ce laboratoire constitue une base solide pour les futurs audits de sécurité, tests d’exploitation et exercices de pentest.