
# TP1 Cryptographie appliquée : TLS/SSL PKI
#### Antoine DEPOISIER & Jules FINCK

## Question 1
- Il faut choisir 2 grands nombres, p et q
- Calculer n = p * x
- Calculer z = (p - 1) * (q - 1)
- Trouver un nombre e tel que e et z soient premiers entre eux
- Trouver d tel que (e * d) mod z = 1
- e et n sont la clé publique
- d et n sont la clé privée

## Question 2
Pour chiffrer le message, on fait C = M<sup>e</sup>mod n
Pour déchiffrer ce message, c'est l'inverse M = C<sup>d</sup>mod n

## Question 3
- Pour qui le certificat a été signé, c'est-à-dire le sujet, dans un certificat TLS, un nom de domaine
- La signature du certificat
- Le CA du certificat, c'est à dire l'entité pouvant créer un certificat valide pour les navigateurs
- La clé publique du nom de domaine

## Question 4
- Le site `alice.com` envoie le certificat au navigateur
- Le navigateur récupère dans le certificat de `root-ca` contenu dans l'OS
- Le navigateur vérifie si le hash de `ca-1` est le même que la signature décryptée du certificat de `root-ca`
- Le navigateur vérifie si le certificat `ca-1` a l'autorité nécessaire pour délivrer des certificats
- Le navigateur vérifie si le hash du dernier certificat est le même que la signature décryptée de `ca-1`
- Le navigateur va vérifier si la date de couverture du certificat est toujours valide
- Le navigateur va vérifier si le nom de domaine délivrant le certificat est bel et bien un sujet alternatif dans le certificat
- Le navigateur récupère la clé publique du site `alice.com` et envoie un message random généré au site, étant encrypté par la clé publique
- Le serveur d'`alice.com` décrypte le message random

## Question 5

Création d'une clé avec une taille 512 bits
```shell
openssl genrsa -out rsa_keys.pem 512
```

La taille des deux nombres premiers choisis est de 33 octets, soit 264 bits.

La longueur du n, c'est celle du modulus est de 65 octets, soit 520 bits.

Le publicExponant est utilisé lors du chiffrement ou du déchiffrement d'un message par l'utilisateur possédant la clé publique. Cette clé peut être connue de tous. Le privateExponant permet d'effectuer les mêmes calculs, mais est utilisé par la personne possédant la clé privée. Elle est seulement connue d'une personne en général.

Le publicExponant est facile à deviner pour un pirate, c'est presque tout le temps le même.

## Question 6

Il n'y a pas d'intérêt à chiffrer une clé publique, étant donné qu'elle est connue de tous, même si elle est chiffrée, on peut la deviner.

Il est néanmoins intéressant de chiffrer une clé privée pour la protéger contre les accès non autorisés.

## Question 7

L'encodage utilisé est en base64. Ça facilite la transmission de données binaires.

## Question 8

Dans la clé publique, on retrouve bien les éléments attendus, tels que le modulo, n, et l'exposant e, étant 65537.

C'est intéressant quand on veut la partager, pour la partager uniquement elle, et non la clé privée en même temps.

## Question 9

Si l'on veut envoyer un message de manière confidentielle, il faut chiffrer ce message avec la clé publique, parce que seulement l'émetteur de la clé publique pourra déchiffrer ce message. Alors que dans le cas inverse, si l'on chiffre une donnée avec la clé privée, tout le monde pourra déchiffrer ce message.

## Question 10

Cette commande permet d'encrypter un message contenu dans un TXT

```shell
openssl pkeyutl -encrypt -in clair.txt -out cipher.bin -pubin -inkey pub.finck.pem
```

- -in clair.txt => fichier input contenant la clé
- -out cipher.bin => fichier output qui va contenir le message chiffré
- -pubin => pour spécifier que l'on utilise une clé publique
- -inkey pub.finck.pem => fichier de la clé utilisée

## Question 11

Ils sont différents, c'est normal parce qu'il y a une part d'aléatoire pour éviter de récupérer des pattern qui permettraient de bypass la sécurité.

```shell
openssl pkeyutl -decrypt -inkey rsa_keys.pem -in cipher.finck.bin -out message.txt
```

si on veut utiliser la passphrase :

```shell
openssl pkeyutl -decrypt -inkey rsa_keys_cyphered.pem -in cipher.finck.bin -out message.txt
```

## Question 12

L'option `-showcerts` permet d'afficher les certificats hébergés par le serveur.

3 Certificats ont été renvoyés par le serveur.

## Question 13

x509 est une norme définie dans les RFC, pour les certificats à clé publique. C'est un algorithme pour la validation du chemin de certification.

Le sujet du certificat est : 
```
Subject: C = FR, ST = Auvergne-Rh\C3\B4ne-Alpes, O = Universit\C3\A9 Grenoble Alpes, CN = *.univ-grenoble-alpes.fr
```

- C => Country, pour le pays
- ST => la région, ou l'état, ou le canton
- O => l'organisation
- CN => configuration name, c'est le nom de domaine pouvant utiliser ce certificat

L'organisme ayant délivré le certificat est Sectigo Limited


## Question 14

Le `s` signifie subject, c'est-à-dire l'entité utilisant le certificat, et `i` signifie l'issuer, c'est-à-dire l'entité délivrant un certificat.

## Question 15

Le certificat possède la clé publique de la clé RSA. L'algorithme utilisé pour signer ce certificat est `sha256WithRSAEncryption`.

Voici le sujet du certificat : 
```
Subject: C = FR, ST = Auvergne-Rh\C3\B4ne-Alpes, O = Universit\C3\A9 Grenoble Alpes, CN = *.univ-grenoble-alpes.fr
```

L'attribut sujet comporte le pays, la région et le nom de l'organisation demandant un certificat. Il comporte également le nom de domaine pouvant utiliser ce certificat.

L'attribut qui comporte les autres noms de machine pouvant utilise ce certificat est `Subject Alternative Name`, et les machines pouvant l'utiliser sont `*.univ-grenoble-alpes.fr` et `univ-grenoble-alpes.fr`, donc le nom de domaine et tous ses sous domaine.

Le certificat est valide du `May  8 00:00:00 2023` au ` May  7 23:59:59 2024`, autrement dit pendant un an.

Le fichier `crl` est la liste des certificats révoquée par l'entité ayant certifié des certificats.

On peut voir son contenu en utilisant la commande 
```shell
openssl crl -in crlfile.crl -inform DER -text -noout
```

## Question 16

Le certificat de l'université a été signé parSectigo Limited.

Pour créer cette signature, `Sectigo Limited` a utilisé la formule suivante : E<sub>KPrivSectigo</sub>(sha256(infoCertifif))

## Question 17

Le sujet de ce certificat est `Sectigo Limited`, ou plus en détail :
```
Subject: C = GB, ST = Greater Manchester, L = Salford, O = Sectigo Limited, CN = Sectigo RSA Organization Validation Secure Server CA
```

La taille de la clé publique du certificat est de 2048 bits.

La CA ayant signé ce certificat est `The USERTRUST Network`, ou plus en détails : 
```
Issuer: C = US, ST = New Jersey, L = Jersey City, O = The USERTRUST Network, CN = USERTrust RSA Certification Authority
```

## Question 18

Pour le certificat de l'université, il n'y a rien à vérifier, il ne certifie aucun certificat.

Pour le certificat `Sectigo Limited`, on voit bien qu'il possède les mêmes informations que la CA ayant certifié l'université. Il possède le même nom que le certificat CA de l'université.

Pour le certificat `The USERTRUST Network`, on voit bien qu'il possède les mêmes informations que la CA ayant certifié `Sectigo Limited`. Il possède le même nom que le certificat CA de `Sectigo Limited`.

Le certificat permettant de valider ce certificat est celui qui est en dernier, c'est le certificat racine, il est généralement stocké dans l'OS, ou bien dans le navigateur.

## Question 19

On voit que le subject et l'issuer sont les mêmes parce que ce certificat a été auto-signé par ` Comodo CA Limited`.

E<sub>KPrivComodo</sub>(sha384(infoCertifif))

Ce sont des `Trusted Root Certificates` ou bien en français des certificats racine de confiance. Ces certificats sont autorisés dans notre OS à certifier des entités.

Quand on vérifie dans le navigateur, on obtient les mêmes informations que celles, dites dans les questions précédentes.

## Question 20

La taille de la clé publique est de 4096 bits.

Le certificat est valide du `Oct 10 15:49:41 2023` au `Oct  5 15:49:41 2043`

On peut voir que c'est un certificat auto-signé parce que le subject et l'issuer sont la même entité.

```
X509v3 Key Usage: Digital Signature, Certificate Sign, CRL Sign
```

Ce certificat peut être utilisé pour effectuer des signatures digitales, des signatures de certificats, et également des signatures de fichier crl, ceux qui permettent de définir une liste de révocations.

La clé privée : `private_key = $dir/private/ca.key.pem`

Pour la lire, on utilise la commande 
```shell
openssl  rsa -in private/ca.key.pem -noout -text
```

## Question 21

Dans le paramètre dir, j'ai mis le paramètre `/home/etudiant/ca`

La clé privée devra être dans le dossier `private` sous le nom de `intermediate.key.pem`

Le certificat devra être dans le dossier `certs` sous le nom de `intermediate.cert.pem`

## Question 22

Voici la commande permettant de créer la clé :

```shell
openssl genrsa -aes128 -out private/intermediate.key.pem 3072
```

```shell
openssl req -config openssl.cnf -new -sha256 -key private/intermediate.key.pem -out csr/intermediate.csr.pem -subj "/C=FR/ST=Savoie/L=Chambery/O=TP Sécurité/CN=RA depoisier"
```

## Question 23

On peut la qualifier de bizarre parce que l'algorithme utilisé n'est pas `aes128` mais `sha256`. La signature du demandeur empêche une entité de demander un faux certificat de la clé publique de quelqu'un d'autre.

```shell
openssl ca -config openssl.cnf -extensions v3_intermediate_ca -days 3650 -notext -md sha256 -in csr/depoisier.csr.pem -out certs/depoisier.cert.pem
```

```shell
openssl x509 -in depoisier.cert.pem -noout -text
```

```shell
sudo openssl req -new -key /etc/pki/tls/private/serveur_http.pem -out serveur_http.csr.pem -subj "/C=FR/ST=Rhone/L=Lyon/O=Canut depoisier inc/CN=www.depoisier.fr"  -addext  "subjectAltName  =  DNS:www.depoisier.fr, DNS:dev.depoisier.fr, DNS:*.depoisier.fr"
```

```shell
openssl ca -config openssl.cnf -extensions server_cert -days 375 -notext -md sha256 -in csr/serveur_http.csr.pem -out certs/serveur_http.cert.pem
```

```conf
events {}
http {
  server {
      listen    443 ssl;
      server_name    www.depoisier.fr;

     ssl_certificate /etc/nginx/ssl/serveur_http.cert.pem;
     ssl_certificate_key /etc/nginx/ssl/serveur_http.pem;

      location / {

          proxy_pass http://web1;
      }

      location /admin/ {

          proxy_pass http://web2/;
      }
  }
}
```

## Question 24

La 3ᵉ solution est la plus pertinente parce que le certificat root expose moins sa clé privée que les certificats intermédiaires. C'est-à-dire, que si un certificat intermédiaire doit changer sa clé privée parce qu'elle a été volée, il faudra modifier les certificats de confiances de notre machine.

Étant donné que le certificat racine expose moins sa clé, on risque de ne jamais avoir besoin de le changer des certificats de confiances.

De plus, les certificats de serveur ont des dates de validités, ce qui demanderait d'update les certificats à chaque fois qu'ils sont expirés.

Petit ajout : après avoir rencontré un problème pour notre certificat mal généré, nous sommes bien contents d'avoir donné confiance au certificat root, et non celui du serveur.


Pour ajouter un CA de confiance, on ajoute le certificat dans le dossier `/etc/pki/ca-trust/source/anchors/` et on effectue la commande `update-ca-trust`

## Question 25

Nous avons ajouté cette information :
```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 www.depoisier.fr
```

## Question 26

[Voici le lien du repo Github](https://github.com/copsfuraxx/info001Secu)
```
https://github.com/copsfuraxx/info001Secu
```

Pour tester l'application, il faut ajouter dans les host de son serveur, les différents host différent comme alias de `127.0.0.1` :
- `www.depoisier.fr`
- `dev.depoisier.fr`
- `test.depoisier.fr`

Il faut ensuite ajouter dans son ca-bundle, le fichier `certificates/rout-ca-lorne.pem` contenu dans le projet.

Pour ajouter un CA de confiance, on ajoute le certificat dans le dossier `/etc/pki/ca-trust/source/anchors/` et on effectue la commande `update-ca-trust`

Maintenant, vous pouvez lancer le serveur en effectuant la commande 
```
python3 server.py
```

Et le client avec la commande 
```
python3 client.py
```

Le client demande un serveur, vous pouvez utiliser les 3 serveurs ajoutés en alias de localhost.

Quand le client a envoyé son message au serveur, le serveur se ferme.

## Question 27

Le navigateur nous affiche deux erreur, la première `ERR_CERT_AUTHORITY_INVALID` nous indique que l'authorité ayant délivré le certificat n'est pas de confiance.

La seconde erreur `SSL_ERROR_BAD_CERT_DOMAIN`, nous indique que le nom du serveur n'est pas celui indiqué dans le certificat.

La première erreur a pu être corrigé en ajoutant dans le magasin de certificat de Firefox le certificat root-ca-lorne.

## Question 28

C'est pour avoir une sécurité renforcé, étant donné que la CA expose moins sa clé privée.

Il y a plus de détails à la réponse de cette question dans la question 24.