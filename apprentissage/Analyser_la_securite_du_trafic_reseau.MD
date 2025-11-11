<p align="center">
  <img src="https://raw.githubusercontent.com/Y4nnSec/AIS/main/apprentissage/Images/yannsec_banner.png" alt="YannSec Banner" width="600">
</p>

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



2. **qu’est ce que le `DHCP Starvation` / `snooping` ? `Rogue DHCP` ?**

* **DHCP Starvation** : attaquant envoie un grand nombre de requêtes pour épuiser la table des baux du serveur .

* **Rogue DHCP** : machine malveillante/ mauvaise config qui propose de fausses adresses/DNS/gateway → MITM, interception, redirection.

* **DHCP Snooping** : fonctionnalité L2 qui marque des ports  *trusted/untrusted* , bloque les offres DHCP venant de ports non-trustés
et maintient une table binding (MAC↔IP↔port) pour prévenir rogue DHCP et attaques.

3. **Que ce passe-t-il lors de l'execution de la commande `ipconfig /release` (windows) ? D’un point de vue sécurité quel peut etre l'enjeu ?**

**Technique :** ipconfig /release = la machine **libère** son adresse IP actuelle (elle la supprime localement et envoie si possible un `DHCPRELEASE` au serveur pour informer que le bail est rendu).

Pour demander une nouvelle adresse, on utilise ensuite  ipconfig /renew , qui déclenche la séquence DHCP.

**Enjeux sécurité** : un attaquant peut forcer ou automatiser des releases/renewals sur clients (social engineering, script) afin de provoquer des renouvellements, faciliter le DHCP starvation, ou forcer clients à utiliser un rogue DHCP s’il est présent. Aussi utile à l’attaquant pour provoquer un renouvellement et capter/diriger trafic.

4. **Quelle fonctionnalité propose CISCO pour se prémunir des `attaques DHCP` ?**
Cisco propose le DHCP Snooping : il distingue les ports fiables et non fiables pour bloquer les faux serveurs DHCP, garde une table des IP attribuées, et s’associe souvent à Dynamic ARP Inspection et IP Source Guard pour empêcher qu’un appareil usurpe une IP ou une adresse MAC.

5. **Capturer une `requête DNS` et sa réponse**



6. **Qu’est-ce que le `DNS Spoofing` ? Comment s’en protéger ?**

* **DNS spoofing** : injection de fausses réponses DNS dans un résolveur pour rediriger des victimes vers IP malveillantes (phishing, MITM).

* **Protections** :
  * déployer **DNSSEC** (signatures RRSIG + chain of trust) ;
  * utiliser **DoT/DoH** pour chiffrer la transport (empêche l’écoute/modification on-path) ;
  * config sécurisée des serveurs (pas d’open resolvers), monitoring, et validation des réponses.

7. **Qu’est-ce que `DNSSec` ? `DNS over TLS` ou `DNS over HTTPS` ?**

* **DNSSEC** : extensions de sécurité DNS qui ajoutent des signatures numériques aux enregistrements DNS pour garantir intégrité/authenticité (ne chiffre pas, mais signe). DNS chiffré via TLS.

* **DNS over HTTPS (DoH)** : DNS chiffré via HTTPS, mélange avec trafic HTTPS (protection de la vie privée et évasion). Les deux protègent contre l’espionnage on‑path; DoH se confond dans HTTPS.

8. **Dans quels cas trouve-t-on du DNS sur TCP ?**
Par défaut DNS = UDP, mais **TCP** est utilisé quand :

* la réponse dépasse la taille UDP (EDNS0) ;
* pour les transferts de zone (AXFR/IXFR) ;
* certaines résolutions recourent au TCP par fallback ou politiques RFC (RFC 7766).

9. **Capturer un flux `HTTP`**





10. **Qu’est-ce que le `HTTP Smuggling` ? Donner un exemple de `CVE`**
C’est une astuce qui consiste à cacher une requête HTTP dans une autre en profitant du fait que deux éléments qui traitent les requêtes (par ex. un reverse-proxy devant un serveur web)  ne calculent pas la fin de la requête de la même façon .

Résultat : le proxy pense « tout est normal », mais le serveur reçoit 
une requête supplémentaire (la « smuggled ») et l’exécute.

**CVE-2022-22720** — Apache HTTP Server (<= 2.4.52) avait un comportement permettant du request smuggling ; correctif publié en mars 2022. [httpd.apache.org](https://httpd.apache.org/security/vulnerabilities_24.html?utm_source=chatgpt.com).

11. **Comment mettre en place la confidentialité et l'authenticité pour HTTP ?**

**Confidentialité** : chiffrer le flux HTTP avec **TLS** pour que personne sur puisse lire les flux en clair

**Authenticité** : prouver que le serveur est bien celui qu’il prétend être — via un **certificat X.509** signé par une Autorité de Certification de confiance.

**Renforcement** : configurer TLS correctement, activer HSTS, cookies sécurisés, et en complément des headers de sécurité.

12.  **Qu’est-ce qu’une `PKI` ?**
Une PKI est un système qui permet de créer, distribuer, vérifier et révoquer des certificats numériques pour assurer :

* **Confidentialité** (on peut chiffrer)
* **Authenticité** (on sait qui parle)
* **Intégrité** (le message n’a pas été modifié)
* **Non-répudiation**

C’est le moteur derrière  **HTTPS** ,  **TLS** ,  **certificats serveurs** ,  **VPN d’entreprise** , etc...

13. **Capturer un `mot de passe` HTTP via le projet VulnerableLightApp.**



14. **Comment mettre en place la `confidentialité` pour ce service ?**

Mettre un reverse proxy TLS et un certificat  avec nginx proxy manager par exemple et d’y déployer un certificat localement approuvé ou un certificat auto-signé (moins pratique).

15. **Capturer un `handshake TLS`**



16. **Qu’est-ce qu’une autorité de certification (`AC`) racine ? Qu'est qu'une `AC intermediaire` ?**

* Une autorité de certification racine est une source de confiance, son certificat est auto signé et elle signe les AC intermédiaires mais rarement les certificats serveurs directement.

* Une autorité de certification intermédiaire est signé par la root CA, elle sert à déléguer des certificats serveurs. elle protège la root CA. Si l'intermédiaire est compromis, la racine reste sûre.

17. **Connectez-vous sur `taisen.fr` et affichez la `chaine de confiance` du certificat**



18. **Capturer une authentification `Kerberos` (mettre en place le service si nécessaire), identifier l'`AS_REQ`, `AS_REP` et les messages suivants.**



19. **Capturer une `authentification RDP` (mettre en place le service si nécessaire), quel est le protocole d'authentification capturé ?**



Protocol utilisé : 3389

21. **Quelles sont les attaques connues sur `NetLM` ?**

Attaques connues contre NetLM :

* **LM hash facile à casser** — mot de passe divisé et affaibli.

* **Crackage hors-ligne** — l’attaquant récupère le hash et le casse sans connexion réseau.

* **Pass-the-Hash (PtH)** — l’attaquant réutilise le hash pour se connecter ailleurs sans connaître le mot de passe.

* **Relay NTLM** — l’attaquant redirige une authentification volée vers un autre service pour se faire passer pour la victime.

* **Poisoning LLMNR/NBT-NS** — l’attaquant force un client à s’authentifier contre lui et récupère le hash.

21. **Capturer une `authentification WinRM` (Vous pouvez utiliser EvilWinRM si nécessaire côté client.), quel est le protocole d'authentification capturé ?**



22. **Capturer une `authentification SSH` ou SFTP (mettre en place le service si nécessaire)**



23. **Intercepter un `fichier au travers du protocole SMB`**



24. **Comment proteger l'`authenticité` et la `confidentialité` d'un partage SMB ?**

Pour protéger l'authenticité d'un partage SMB, il faut :

* **Kerberos (Active Directory)** : le protocole utilise des tickets chiffrés, impossibles à falsifier facilement. Il permet d’authentifier de façon centralisée et fiable tous les utilisateurs d’un domaine.

* **NTLMv2** : si Kerberos n’est pas disponible, NTLMv2 est beaucoup plus sécurisé que NTLMv1 et LM, car il utilise des challenges cryptographiques et protège le mot de passe.

* **Contrôle d’accès basé sur les utilisateurs et groupes** : limiter les droits de lecture/écriture aux personnes qui en ont vraiment besoin. Cela réduit l’impact d’un compte compromis.

Pour protéger la confidentialité d'un partage SMB, il faut :

* **SMB 3.0 avec chiffrement activé** : le trafic est chiffré de bout en bout entre le client et le serveur. Même si quelqu’un capture les paquets, il ne peut pas lire le contenu.

* **Limiter les ports SMB** aux réseaux de confiance via le pare-feu.

* **VPN ou tunnel sécurisé** si les partages sont accessibles depuis l’extérieur.





**Auteur : ESCRIVA Yann**

**Projet : Octobre 2025**




![alt text](Images/kerberos.png)
