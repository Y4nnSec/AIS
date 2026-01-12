

## TP Réseau HSRP



### 1. Objectif

Le but de cet exercice est d’effectuer une analyse de type « reverse engineering » à partir d’une
infrastructure fonctionnelle, sur le thème de HSRP.


### 2. Prérequis

* Poste de travail avec le logiciel Packet Tracer installé
* Fichier Packet Tracer pré-configuré


### 3. Tâches à réaliser

* Analyser l’infrastructure
* Analyser la configuration
* Proposer un guide des commandes de configuration HSRP


### 4. Topologie

![alt text](Images/Topologie_HSRP.png)


### 5. Tâches à réaliser

**Analyse de l’infrastructure**
* Analyser l'infrastructure et la configuration des équipements

* Qu’est-ce que HSRP ? Proposer une définition simple.
HSRP (Hot Standby Router Protcol) C'est un protocol cisco de redondance qui permet d'assurer la continuité d'accès au réseau au cas ou un routeur tombe en panne.


* Pourquoi utilise-t-on HSRP et quel problème résout-il ? Expliquer l'intérêt de HSRP dans ce
réseau
On utilise HSRP pour assurer la haute disponibilité de la passerelle réseau.
Il résout le risque de coupure réseau, de se fait il ya un 2 ième routeur

**Analyse de la configuration existante**
* Identifier les routeurs primaires et les routeurs de secours HSRP, quels sont leurs rôles
respectifs ?
* Noter les adresses IP virtuelles (VIP) et physiques (R1, R2, R3) utilisées dans les groupes HSRP,
à quoi servent ces différentes adresses ?
* Identifier les interfaces réseau participant à HSRP sur chaque routeur, leurs priorités, les délais
et les autres paramètres HSRP configurés sur les routeurs. Que comprenez-vous ?
Configuration HSRP
* À l'aide des informations que vous avez collectées, proposer un guide de commandes de
configuration HSRP. Expliquer brièvement le rôle de chaque commande utilisée. Identifier les
éléments clés tels que le numéro de groupe HSRP, les adresses IP virtuelles, les priorités, les
délais, ainsi que les commandes permettant d'activer HSRP sur l'interface
