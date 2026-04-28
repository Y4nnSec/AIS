## TP1 CyberChef – Cryptographie appliquée


#### 1 Objectifs 

* Utiliser CyberChef pour appliquer différentes techniques de chiffrement, hachage, et encodage 
* Visualiser le fonctionnement de la cryptographie symétrique et asymétrique 
* Comprendre les différences entre encodage, hachage et chiffrement 


### 2 Consignes 

* Travail en binôme 
* Utilisation de l’application web « CyberChef » : https://gchq.github.io/CyberChef/  
* Pour chaque section 
  * Réaliser les opérations demandées dans CyberChef 
  * Appliquer les méthodes sur un message de votre choix puis transmettre ce message à votre binôme afin qu’il le décode/déchiffre 
  * Répondre aux questions 


### 3 Contenu de ce TP 

1. Chiffrement de César 
2. Encodage de Vigenère 
3. Chiffrement symétrique AES 
4. Chiffrement asymétrique RSA 
5. Hachage 
6. Encodage 


### 4 Tâches à réaliser 

**I. Partie 1 : Chiffrement de César**


Dans « CyberChef » utilisez la recette « ROT13 » 

1. Avec une « Box Height » de 13, chiffrer la phrase suivante : RENDEZ-VOUS À MIDI 
 * . Quel est le texte chiffré ? 
 * Déchiffrez ce texte pour vérifier le résultat 
  
2. Chiffrer le nom de votre film préféré avec une « Box Height » de votre choix 
   * Transmettre le texte chiffré à votre binôme sans lui communiquer la clé 
   * Au sein de votre binôme, essayer de retrouver le message en sens inverse


**II. Partie 2 : Vigenère**

Dans « CyberChef » utilisez la recette « Vigenère Encode » 
* Encodez le nom de votre plat préféré avec la clé 'KEY' 
  * Quel est le texte chiffré ? 

* Transmettre le texte chiffré à votre binôme 
* Transmettre la clé à votre binôme par un autre canal 
  * Au sein de votre binôme, déchiffrez le message pour découvrir vos plats préférés respectifs


**III. Partie 3 : Chiffrement symétrique AES**

Dans « CyberChef » utilisez les recettes « AES Encrypt » et « AES Decrypt » 
**Découverte** 

* Chiffrez la chaîne 'TESTSECRET1234567' avec les paramètres suivants  
  * Key : c34fa73d7c5f8901a23e4cd98e7f650d9a17d4e8f902fa0d3286d0beaad219b6
  * IV :  
  * Mode : ECB 
  * Input : mode Raw 
  * Output : Hex 
* Que constatez-vous si vous modifiez 1 caractère du texte initial ? 
* Déchiffrez le texte AES chiffré précédemment en adaptant les paramètres 
  * Vous devez retrouver le texte d'origine 


**Transmission d’un message chiffré à votre binôme**

* Générer une clé adéquate 
* Chiffrez le nom de votre équipe de sport préférée avec les paramètres suivants 
  * Key : « la clé que vous avez généré » 
  * IV :  
  * Mode : ECB 
  * Input : mode Raw 
  * Output : Hex 
 * Transmettre le texte chiffré à votre binôme 
* Transmettre la clé à votre binôme par un autre canal 
  * Au sein de votre binôme, déchiffrez le message pour découvrir vos équipes de sport préférées respectives 

