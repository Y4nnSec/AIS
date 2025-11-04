
# Analyser la sécurité du trafic réseau


**Rappels :** 

* **Quelle est votre adresse IP ? Quelle est sa classe (IPv4) ?**

192.168.79.139 qui est en class C

* **Quel est votre masque de sous-réseau ?**

Mon masque de sous réseau est : 255.255.255.0 ou en cidr /24

* **Quelle est l'adresse de votre passerelle ?**

L'adresse de la passerelle est : 192.168.79.2


**Questions :**


0. **Quels sont les `flags TCP` ?**

* flag *SYN* pour demander l'établissement d'une session;
* flag *SYN/ACK* pour confirmer la demande;
* flag *ACK* pour acquitter la bonne réception de la confirmation;
* flag *FIN* pour mettre fin à la session.


1. **Capturer le processus `DORA` du protocole DHCP**
5. **qu’est ce que le `DHCP Starvation` / `snooping` ? `Rogue DHCP` ?**

* **DHCP Starvation** : attaquant envoie un grand nombre de requêtes pour épuiser la table des baux du serveur .
* **Rogue DHCP** : machine malveillante/ mauvaise config qui propose de fausses adresses/DNS/gateway → MITM, interception, redirection.

* **DHCP Snooping** : fonctionnalité L2 qui marque des ports  *trusted/untrusted* , bloque les offres DHCP venant de ports non-trustés

et maintient une table binding (MAC↔IP↔port) pour prévenir rogue DHCP et attaques. 


4. **Que ce passe-t-il lors de l'execution de la commande `ipconfig /release` (windows) ? D’un point de vue sécurité quel peut etre l'enjeu ?**

**Technique :** ipconfig /release = la machine **libère** son adresse IP actuelle (elle la supprime localement et envoie si possible un `DHCPRELEASE` au serveur pour informer que le bail est rendu).

Pour demander une nouvelle adresse, on utilise ensuite  ipconfig /renew , qui déclenche la séquence DHCP.

**Enjeux sécurité** : un attaquant peut forcer ou automatiser des releases/renewals sur clients (social engineering, script) afin de provoquer des renouvellements, 

faciliter le DHCP starvation, ou forcer clients à utiliser un rogue DHCP s’il est présent. Aussi utile à l’attaquant pour provoquer un renouvellement et capter/diriger trafic.


4. **Quelle fonctionnalité propose CISCO pour se prémunir des `attaques DHCP` ?**

Cisco propose le DHCP Snooping : il distingue les ports fiables et non fiables pour bloquer les faux serveurs DHCP, garde une table des IP attribuées, et s’associe souvent à Dynamic ARP Inspection et IP Source Guard pour empêcher qu’un appareil usurpe une IP ou une adresse MAC.


5. **Capturer une `requête DNS` et sa réponse**


6. **Qu’est-ce que le `DNS Spoofing` ? Comment s’en protéger ?**

* **DNS spoofing** : injection de fausses réponses DNS dans un résolveur pour rediriger des victimes vers IP malveillantes (phishing, MITM).
* **Protections** :

  * déployer **DNSSEC** (signatures RRSIG + chain of trust) ;
  * utiliser **DoT/DoH** pour chiffrer la transport (empêche l’écoute/modification on-path) ;
  * config sécurisée des serveurs (pas d’open resolvers), monitoring, et validation des réponses.










**Qu’est-ce que `DNSSec` ? `DNS over TLS` ou `DNS over HTTPS` ?**

**Dans quels cas trouve-t-on du DNS sur TCP ?**

**Capturer un flux `HTTP`**

**Qu’est-ce que le `HTTP Smuggling` ? Donner un exemple de `CVE`**

**Comment mettre en place la confidentialité et l'authenticité pour HTTP ?**

**Qu’est-ce qu’une `PKI` ?**

**Capturer un `mot de passe` HTTP via le projet VulnerableLightApp.**

**Comment mettre en place la `confidentialité` pour ce service ?**

**Capturer un `handshake TLS`**

**Qu’est-ce qu’une autorité de certification (`AC`) racine ? Qu'est qu'une `AC intermediaire` ?**

**Connectez-vous sur `taisen.fr` et affichez la `chaine de confiance` du certificat**

**Capturer une authentification `Kerberos` (mettre en place le service si nécessaire), identifier l'`AS_REQ`, `AS_REP` et les messages suivants.**

**Capturer une `authentification RDP` (mettre en place le service si nécessaire), quel est le protocole d'authentification capturé ?**

**Quelles sont les attaques connues sur `NetLM` ?**

**Capturer une `authentification WinRM` (Vous pouvez utiliser EvilWinRM si nécessaire côté client.), quel est le protocole d'authentification capturé ?**

**Capturer une `authentification SSH` ou SFTP (mettre en place le service si nécessaire)**

**Intercepter un `fichier au travers du protocole SMB`**

**Comment proteger l'`authenticité` et la `confidentialité` d'un partage SMB ?**
