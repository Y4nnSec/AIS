**DAT_Lab: Environnement de tes**t

1. **Résumé :**

Ce DAT décrit le déploiement d'un laboratoire reproduisant un service d'entreprise avec un contrôleur de domaine Windows server 2022, un pc client Windows 10 et un serveur Linux hébergeant l'application VulnerableLightApp. L'objectif est de fournir un environnement réaliste et vulnérable pour des exercices d'audit.

2. **Contexte et objectifs**

* Objectifs pédagogiques du Lab (déploiementet installation des machines comme demandé.
* Contraintes (vérifier intégrités des iso(Hashs ou Signatures).
* Rappels sécurité (isolement réseau, gestion des mots de passeet snapshot).

3. **Architecture réseau**

![alt text](../Apprentissage/Images/Diagramme Lab secu.png)

4. **Caractéristiques des machines**

| 🖥️**Nom VM** | 🧩**Rôle**      | 💿**OS (ISO)**      | ⚙️**CPU** | 🧠**RAM** | 💾**Stockage** | 🌐**IP** | 📝**Notes**                        |
| -------------------- | ---------------------- | ------------------------- | ----------------- | --------------- | -------------------- | -------------- | ---------------------------------------- |
| SRV-AIS              | Contrôleur de domaine | Windows Server 2022 (ISO) | 4                 | 4 GB            | 60 GB                | 192.168.79.143 | AD, DNS, DHCP, WINRM, SMB, RDP, BADBLOOD |
| PC-yann              | PC client              | Windows 10 (ISO)          | 4                 | 4 GB            | 60 GB                | 192.168.79.144 | Joins AD                                 |
| SRV-Linux            | Serveur Web            | Debian 12 (ISO)           | 2                 | 2 GB            | 20 GB                | 192.168.79.139 | WEB-VLA, SSH                             |

5. Inventaire des comptes à privilèges

| 👤**Compte** | 🧩**Rôle** | 💻**Machine** | 🔐**Emplacement du mot de passe** |
| ------------------ | ----------------- | ------------------- | --------------------------------------- |
| Administrateur     | Admin du domaine  | SRV-AIS             | Bitwarden                               |
| Local_admin        | Admin local       | PC-yann             | Bitwarden                               |
| Local_user         | Client            | PC-yann             | Bitwarden                               |
| Root               | Admin SRV Linux   | SRV_WEB             | Bitwarden                               |
| SRV_WEB User       | SRV Linux         | SRV_WEB             | Bitwarden                               |

![alt text](../Apprentissage/Images/Bitwarden.png)

6. **Diagramme Projet**

![alt text](<../Apprentissage/Images/Capture Diagramme projet.png>)


7. Vérification des images (hashs/ signatures)

Hash debian 13

![alt text](<../Apprentissage/Images/Capture hash debian officiel 2025-10-18 074053.png>)

Hash Windows server 2022

![alt text](<../Apprentissage/Images/Capture vérification hash debian.png>)

![alt text](<../Apprentissage/Images/Capture hash iso winserver.png>)





