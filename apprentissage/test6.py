import requests, socket, dns.resolver, psutil, subprocess, platform
from bs4 import BeautifulSoup
from OpenSSL import SSL, crypto

# Réaliser une requête Web GET sur un site Web (Défaut = https://taisen.fr)
r = requests.get("https://taisen.fr")
print("Requête GET effectuée avec succès.")

# Afficher l'IP et le nom du serveur DNS qui résout le nom de domaine
domain = "taisen.fr"
ip_address = socket.gethostbyname(domain)
dns_server = dns.resolver.resolve(domain, 'A')[0].address
print(f"\nIP résolue : {ip_address}")
print(f"Serveur DNS qui résout le domaine : {dns_server}")

# Afficher l'IP et le port Source
print("\nIP et Port Source (associés au domaine Taisen.fr) :")
for conn in psutil.net_connections(kind='tcp'):
    if conn.raddr and conn.raddr.ip == ip_address and conn.raddr.port == 443:
        print(f"IP Source: {conn.laddr.ip}, Port Source: {conn.laddr.port}")

# Afficher l'IP et le port de destination
print("\nIP et Port de Destination :")
for conn in psutil.net_connections(kind='tcp'):
    if conn.raddr and conn.raddr.ip == ip_address and conn.raddr.port == 443:
        print(f"IP Destination: {conn.raddr.ip}, Port Destination: {conn.raddr.port}")

# Afficher les Headers qui ont un lien avec la sécurité
security_headers = ['Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection', 'Content-Security-Policy', 'Permissions-Policy', 'Referrer-Policy', 'Feature-Policy']
r = requests.get('https://taisen.fr')
for header in security_headers:
    if header in r.headers:
        print(f"{header}: {r.headers[header]}")
    else:
        print(f"{header} is not present in the response.")

# Afficher le Content-Type, s'il est générique, afficher son utilité
content_type = r.headers.get('Content-Type', 'Not available')
print(f"Content-Type: {content_type}")
if 'text/plain' in content_type: print("Utilité : C'est du texte brut.")
elif 'application/octet-stream' in content_type: print("Utilité : C'est un flux de données binaire générique.")
elif 'application/json' in content_type: print("Utilité : C'est un format JSON, utilisé pour les API.")
elif 'text/html' in content_type: print("Utilité : C'est du HTML, utilisé pour les pages web.")
else: print("Content-Type spécifique, pas générique.")

# Stocker dans une variable de type tableau, liste ou dictionnaire les différentes balises Web
tags = [tag.name for tag in BeautifulSoup(r.text, 'html.parser').find_all(True)]
print(f"\nBalises HTML extraites: {tags}")

# A partir de la question précédente, afficher le titre de niveau 1 (balise h1)
soup = BeautifulSoup(r.text, 'html.parser')
h1_title = soup.find('h1')
if h1_title:
    print(f"\nTitre de niveau 1 (h1): {h1_title.text}")
else:
    print("\nAucun titre h1 trouvé.")

# Afficher la clé publique du certificat
def get_public_key(host):
    context = SSL.Context(SSL.SSLv23_METHOD)
    conn = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.set_tlsext_host_name(host.encode())
    conn.connect((host, 443))
    conn.do_handshake()
    cert = conn.get_peer_certificate()
    pub_key = cert.get_pubkey()
    pub_key_asn1 = crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key)
    conn.close()
    return pub_key_asn1.decode()
try:
    public_key = get_public_key(domain)
    print(f"\nClé publique du certificat SSL :\n{public_key}")
except Exception as e:
    print(f"\nErreur lors de l'extraction de la clé publique : {e}")
print("\nAudit terminé.")

# Afficher le nom de l'autorité qui a signé le certificat
def get_issuer_name(host):
    context = SSL.Context(SSL.SSLv23_METHOD)
    conn = SSL.Connection(context, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.set_tlsext_host_name(host.encode())
    conn.connect((host, 443))
    conn.do_handshake()
    cert = conn.get_peer_certificate()
    issuer = cert.get_issuer()
    conn.close()
    return issuer
try:
    issuer_name = get_issuer_name(domain)
    print(f"\nAutorité de certification qui a signé le certificat : {issuer_name}")
except Exception as e:
    print(f"\nErreur lors de l'extraction de l'autorité de certification : {e}")

# Afficher la liste des IP des équipements réseau traversés pour atteindre le site Web
def traceroute(host):
    if platform.system().lower() == "windows":
        cmd = ["tracert", host]
    else:
        cmd = ["traceroute", host]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de traceroute : {e}")
        return None
domain = "taisen.fr"
trace_result = traceroute(domain)
if trace_result:
    print(f"\nRésultat du traceroute vers {domain} :\n{trace_result}")