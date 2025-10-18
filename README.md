# 🐍 Script-Python – Automatisation pour l’AIS & 🧾 DAT – Environnement de test (Dojo-101)

Ce dépôt contient deux volets complémentaires :

1. **Script-Python AIS** : automatisation de tâches liées à l'administration sécurisée.  
2. **DAT – Dojo-101** : Document d’Architecture Technique décrivant un lab (AD, Windows, Linux).

---

## 📝 1️⃣ Script-Python – Automatisation AIS

### Description
Ce projet a pour but de faciliter la gestion de la sécurité sur un réseau ou une infrastructure via des scripts Python.  
Il permet notamment :
- l’automatisation de vérifications de sécurité,
- l'exécution de tests sur des serveurs,
- la gestion de configurations critiques (pare-feu, conformité, etc.).

### Arborescence (extrait)
Script-AIS/
├── apprentissage/
│ ├── test.py
│ └── test6.py
└── README.md

bash
Copier le code

### Installation rapide
```bash
git clone https://github.com/Y4nnSec/Script-AIS.git
cd Script-AIS
Auteur
Y4nnSec – Développeur principal – Formation AIS (Administrateur d’Infrastructure Sécurisée)

🏗️ 2️⃣ DAT – Document d’Architecture Technique (Dojo-101)
Présentation
Environnement de test vulnérable pour pratiquer l’administration Windows et Linux.
Inclut :

Active Directory (AIS.LAN)

Client Windows

Serveur Linux (Debian)

Contenu du dépôt
Fichier / Dossier	Description
DAT_Lab_DoJo101_Yann_2025.pdf	Document complet DAT (à la racine)
schema_reseau.png	Schéma réseau du lab (à la racine)
screens/	Captures d’écran des services et configurations
scripts/	Scripts PowerShell utilisés pour le lab

Accès au DAT
📄 Ouvrir le DAT en PDF

Schéma réseau


📸 Captures d’écran (mini-aperçus)
Remplace les noms d’image ci‑dessous si nécessaire pour correspondre à ton dossier screens/.

Active Directory


SMB / Partages

VulnerableLightApp

SSH / Linux

💡 Si certaines images n’existent pas encore, supprime ou commente la ligne correspondante pour éviter les images cassées.

⚙️ Services et commandes clés
Active Directory
powershell
Copier le code
# Export des utilisateurs AD (exemple)
Get-ADUser -Filter * | Select Name,SamAccountName,UserPrincipalName,WhenCreated
# Activer WinRM
Enable-PSRemoting -Force
DNS
bash
Copier le code
nslookup ais.lan
ping 10.0.0.10
WinRM / SSH
WinRM pour administration distante Windows, SSH pour Linux.

SMB
Partages Readonly / WriteAccess — tests de transferts de fichiers.

VulnerableLightApp
App Web sur Debian — tests et démonstrations de vulnérabilité.

📂 Où mettre les fichiers
Place DAT_Lab_DoJo101_Yann_2025.pdf et schema_reseau.png à la racine du repo.

Place tes captures dans screens/ avec les noms utilisés ci‑dessus (ou adapte les noms dans le README).

Place les scripts PowerShell pour le lab dans scripts/.

✔️ Notes finales
Ce README est pensé pour être lisible directement sur GitHub (aperçu PDF cliquable + mini‑aperçus d’images).

Pour alléger l’affichage, tu peux ajouter des miniatures (redimensionner les images) ou héberger le PDF sur GitHub Pages si nécessaire.

Auteur DAT : Yann – Alternance Administrateur Infrastructures Sécurisées
Projet réalisé en octobre 2025
