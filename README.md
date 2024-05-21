------------------------------------------------------------------------------------------------------
PROJET CLOE855
------------------------------------------------------------------------------------------------------
Quelles sont les notions qui vont être abordées au cours de cet atelier ?
Cet atelier a pour objectif de vous apprendre à créer des bases de données grace à Python et SQLite. Vous allez ensuite exploter cette base de données via la construction d'API. Vous allez utiliser et mettre en oeuvre au travers de cet atelier, un serveur Python utilisant le Framework Flask. 
Vous allez créer des API, découvrir les Actions et les Secrets GitHUB pour au final mettre en service et exploiter une base de données.
Large programme mais tout à fait accessible et ne nécessitant pas de base technique particulière. Juste de l'observation et de la rigueur dans votre travail.

-------------------------------------------------------------------------------------------------------
Séquence 1 : GitHUB
-------------------------------------------------------------------------------------------------------
Objectif : Création d'un Repository GitHUB pour travailler avec son projet  
Difficulté : Très facile (~10 minutes)
-------------------------------------------------------------------------------------------------------
GitHUB est une plateforme en ligne utilisée pour stocker le code de son programme.
GitHUB est organisé en "Repository", c'est à dire en répertoire (contenant lui même des sous répertoires et des fichiers). Chaque Repository sera indépendant les un des autres. Un Repository doit être vu comme un projet unique (1 Repository = 1 Projet). GitHUB est une plateforme très utilisée par les informaticiens.

**Procedure à suivre :**  
1° - Créez vous un compte sur GitHub : https://github.com/  
Si besoin, une vidéo pour vous aider à créer votre propre compte GitHUB : [Créer un compte GitHUB](https://docs.github.com/fr/get-started/onboarding/getting-started-with-your-github-account)  
A noter que **si vous possédez déjà un compte GitHUB, vous pouvez le conserver pour réaliser cet atelier**. Pas besion d'en créer un nouveau.  
Remarque importante : **Lors de votre inscription, utilisez une adresse mail valide. GitHUB n'accepte pas les adresses mails temporaires**  

2° - Faites un Fork du Repository suivant : [MSPR_CLO855](https://github.com/bstocker/MSPR_CLOE855)  
Voici une vidéo d'accompagnement pour vous aider dans les "Forks" : [Forker ce projet](https://youtu.be/p33-7XQ29zQ)    
  
**Travail demandé :** Créé votre compte GitHUB, faites le fork de ce projet et **copier l'URL de votre Repository GitHUB dans la discussion public**.

Notion acquise lors de cette séquence :  
Vous avez appris lors de cette séquence à créer des Repository pour stocker et travailler avec votre code informatique. Vous pourez par la suite travailler en groupe sur un projet. Vous avez également appris à faire des Forks. C'est à dire, faire des copies de projets déjà existant dans GitHUB que vous pourrez ensuite adapter à vos besoins.
  
---------------------------------------------------
Séquence 2 : Création d'un hébergement en ligne
---------------------------------------------------
Objectif : Créer un hébergement sur Alawaysdata  
Difficulté : Faible (~10 minutes)
---------------------------------------------------

Rendez-vous sur **https://www.alwaysdata.com/fr/**  
  
Remarque : **Attention à bien vous rappeler de vos Login/Password** lors de la création de votre compte site car vous en aurez besoin plus tard pour la création de vos Secrets GitHUB.  
  
Voici une vidéo d'accompagnement pour vous aider dans cette séquence de création d'un site sur Alwaysdata : [Vidéo Alwaysdata](https://youtu.be/6cuHjy8n968)  
  
**Procédure :**  
1° - Créez votre compte Alwaysdata (gratuit jusqu'à 100Mo, aucune carte nécéssaire).  
2° - Depuis la console d'administration (Le panel d'administration de Alwaysdata) :  
 . 2.1 - Cliquez sur "Sites" (Colonne de gauche) puis **supprimer votre site PHP** (via l'icone de la Poubelle).  
 . 2.2 - **Installer ensuite une application Flask** (Bouton **+ Installer une application**).  
 . . 2.2.1 Adresses = utilisez le sous-domaine qui vous appartient que vous trouverez dans l'information " Les sous-domaines suivants vous appartiennent et sont actuellement inutilisés : {Site}.alwaysdata.net  
 . . 2.2.2 Répertoire d'installation = **/www/flask**  
 . 2.2.3 N'oubliez pas d'Accepter les conditions.  
3° - Autoriser les connexions SSH :  
 . 3.1 - Cliquez sur SSH (Accès distant).  
 . 3.2 - Modifier les paramètres de votre utilisateur.  
 . 3.3 - Définissez si besion un nouveau mot de passe.  
 . 3.4 - Cliquez sur **Activer la connexion par mot de passe**.  
  
**Travail demandé :** Mettre en ligne votre application Flask "Hello World !" et **copier l'URL de votre site dans la discussion public**.  
  
Notions acquises lors de cette séquence :  
Vous avez créer un hébergement (gratuit) et découvert également que vous pouvez installer bien d'autres applications (Django, Drupal, Jenkins, Magento, Symphony, etc...). Les perspectives sont nombreuses.

---------------------------------------------------
Séquence 3 : Les actions GitHUB (Industrialisation Continue)
---------------------------------------------------
Objectif : Automatiser la mise à jour de votre hébergement Alwaysdata
Difficulté : Moyen (~45 minutes)
---------------------------------------------------
Depuis le repository que vous venez de créer dans GitHUB vous allez à présent créer une Action afin de déployer votre code automatiquement sur votre serveur Alwaysdata via une connexion SSH. Cette action passe par la création d'un fichier **CICD.yml** dans GitHub dont le contenu sera executé à chaque commit des devellopeurs (c'est à dire à chaque modification de votre code dans GitHUB). Ce fichier est à déposer dans le répertoire **.github/workflows/CICD.yml** de votre repository.

-------------
Etape 1 : Création d'une action dans GitHUB
Créer une Action dans votre repository GitHUB pour y deposer le script suivant :

```
name: Industrialisation continue sur le serveur Alwaysdata
on: push
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Flask app
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST_DNS }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd $HOME/www/
            git clone https://github.com/bstocker/flask_hello_world.git
            rsync -r ./flask_hello_world/ ./flask
            rm -rf ./flask_hello_world
            curl -X POST --basic --user "${{ secrets.ALWAYSDATA_TOKEN }}:" https://api.alwaysdata.com/v1/site/${{ secrets.ALWAYSDATA_SITE_ID }}/restart/
```
-------------
Etape 2 : Vous avez besoin de créer des secrets dans GitHUB afin de ne pas divulguer des informations sensibles aux internautes de passage dans votre repository (vos login, clés, dns, etc..). Ci-dessous une vidéo pour vous expliquer le processus de création d'un secret dans GitHUB. Par exemple le création d'un secret HOST_DNS
https://www.youtube.com/watch?v=7CZde1a7rq0

-----
Les secrets de votre Repository Github que vous devez créer (il y en aura **4 secrets au tota**l) :
**USERNAME** = Le login que vous avez utilisé lors de la création de votre site.
**SSH_KEY** = L'intégralité de la clé privée ci-dessous (depuis ----BEGIN jusqu'à KEY-----)

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACC4LTWO3FUlXJLlxmPXy2enZnARnnqRgZ6+7lzNvwL7OwAAAJBn8JtCZ/Cb
QgAAAAtzc2gtZWQyNTUxOQAAACC4LTWO3FUlXJLlxmPXy2enZnARnnqRgZ6+7lzNvwL7Ow
AAAEC67kacvftsZrOeW19wnOUYHgxqwzb4YYdACf5+MV1tVLgtNY7cVSVckuXGY9fLZ6dm
cBGeepGBnr7uXM2/Avs7AAAABm5vbmFtZQECAwQFBgc=
-----END OPENSSH PRIVATE KEY-----
```

En revanche la clé public est à déposer directement sur votre serveur Alwaysdata. C'est à dire que vous devez vous connecter en SSH depuis une console sur le serveur Alwaysdata. Pour cette connection en SSH, vous pouvez utiliser le logiciel de votre choix (putty, cmd, ...) ou utiliser directement l'interface web proposé par Alwaysdata. Exemple en cliquant sur le lien suivant https://ssh-etudiant11.alwaysdata.net
Attention !! Vous devez activer la connexion par mot de passe pour votre utilisateur SSH dans Alwasdata (Voir paragraphe 3.1 de la séquence 2).

**Procédure pour la clé public :**  
 . 2.1 - Connectez vous à votre serveur Alwaysdatat via une console ssh (ex : https://ssh-etudiant.alwaysdata.net/). Remarque importante : Activer la connexion par mot de passe pour votre utilisateur SSH.  
 . . 2.1.1 : Le login est celui de votre compte site (celui en haut à gauche).  
 . . 2.1.1 : Le mot de passe de compte compte site est à taper en aveugle (le curseur de la console ne bouge pas et c'est normal).  
 . 2.2 - Ensuite, toujours depuis cette console SSH, créer à présent le répertoire .ssh en tapant le commande suivante : **mkdir .ssh**  
 . 2.3 - Récupérer la clé public en tappant la commande suivant dans la console SSH : **git clone https://github.com/bstocker/keyalwaysdata.git**  
 . 2.4 - Déplacer la clé pour la mettre dans le bon répertoire de votre serveur via la commande : **mv keyalwaysdata/authorized_keys .ssh**  
  
Astuce : Pour coller du texte dans votre navigateur, vous pouvez utiliser la combinaison de touche Ctrl+Shift+v pour coller votre texte.
  
Pour vérifier que tout est bon et que votre clé public est bien déclarée sur votre serveur, tapez la commande suivante depuis votre console ssh :
**cat .ssh/authorized_keys** le résultat doit être le suivant :
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILgtNY7cVSVckuXGY9fLZ6dmcBGeepGBnr7uXM2/Avs7 noname
```

3° - Génération d'un token :
Afin de pouvoir utiliser les API de la solution Alwaysdata (ex une demande de relance serveur dans notre cas), il faut créer un token.

**ALWAYSDATA_TOKEN** = Le token est à créer depuis l'interface d'administration Alwaysdata. Cliquez sur votre profil en haut à droite, puis sur 'Profil' puis sur 'Gérer les tokens'. Laissez le champ "Adresses IP autorisées" vide. Dans le cas contraire vous limiteriez les connexions seulement une adresse IP. Pour le champ Application* mettez "flask" par exemple.

**ALWAYSDATA_SITE_ID** = Vous trouverez l'ID de votre site depuis l'interface d'administration Alwaysdata dans les paramètres de votre site (dans le titre #XXXXX) XXXXX étant l'ID de votre site. Ne prenez pas le # mais juste les chiffres.
  
Notions acquises de cette séquence :  
Vous avez vu dans cette séquence comment créer des secrets GiHUB afin de mettre en place de l'industrialisation continue. Nous avons créé des secrets ainsi que des clés public et privée. L'utilité des scripts d'actions (C'est à dire des scripts exécutés lors des Commits) est très importante mais sortes malheureusement du cadre de cet atelier faute de temps. Toutefois, je vous invites à découvrir cet outil via les différentes sources du Web (Google, ChatGPT, etc..).  

---------------------------------------------------
Séquence 4 : Créer la base de données sur votre serveur
---------------------------------------------------
Objectif : Créer la base de données SQLite sur votre serveur  
Difficulté : Faible (~10 minutes)
---------------------------------------------------
1° - Connectez vous en SSH à votre serveur Alwaysdata via l'adresse suivante :**https://ssh-{compte}.alwaysdata.net**. Remarque importante, {compte} est à remplacer par votre compte Alwaysdata. C'est à dire le compte que vous avez utilisé pour renseigner votre secret GitHUB USERNAME.   
2° - Une fois connecté, depuis de la console SSH, executez la commande suivante : **cd www/flask** puis **python3 create_db.py**  
Votre base de données est à présent opérationnelle sur votre serveur (Le fichier database.db à été créé dans votre répertoire sur le serveur)
Vous pouvez, si vous le souhaitez, tappez la commande **ls** dans votre console pour voir la présence de la base de données.

LES ROUTES (API)
-------------------------------------------
Votre solution est à présent opérationnelle. Vous pouvez testez les routes (API) comme suit :  
  
https://{Votre_URL}**/**  
Pointe sur le fichier helloWorld d'accueil  

https://{Votre_URL}**/lecture**  
L'accès est conditionné à un contrôle d'accès  

https://{Votre_URL}**/authentification**  
Page d'authentification (admin, password)  

https://{Votre_URL}**/fiche_client/1**  
Permet de faire un filtre sur un client. Vous pouvez changer la valeur de 1 par le N° du client de votre choix  

https://{Votre_URL}**/consultation/**  
Permet de consutler la base de données  

https://{Votre_URL}**/enregistrer_client**  
API pour enregistrer un nouveau client  

---------------------------------------------------
Séquence 5 : Exercices
---------------------------------------------------
Objectif : Travailler votre code  
Difficulté : Moyenne (~60 minutes)
---------------------------------------------------
**Exercice 1 : Création d'une nouvelle fonctionnalité**    
Créer une nouvelle route dans votre application afin de faire une recherche sur la base du nom d'un client.  
Cette fonctionnalité sera accéssible via la route suivante : **/fiche_nom/**  

**Exercice 2 : Protection**  
Cette nouvelle route "/fiche_nom/" est soumise à un contrôle d'accès User. C'est à dire différent des login et mot de passe administrateur.  
Pour accéder à cette fonctionnalité, l'utilisateur sera authentifié sous les login et mot de passe suivant : **user/12345**
  
---------------------------------------------------
Séquence 6 : Le projet de bibliothèque
---------------------------------------------------
Objectif : Créer une application de biliothèque  
Difficulté : Moyenne (~180 minutes)
---------------------------------------------------
Votre projet consiste à present à concevoir et développer une application de gestion de bibliothèque moderne qui simplifie le processus de prêt et de retour de livres. Les fonctionnalités attendues dans le cadre de ce projet sont les suivantes :  
•	L’enregistrement et la suppression de livres.  
•	La recherche de livres disponibles.  
•	L'emprunt possible d'un livre par un utilisateur.  
•	La gestion des utilisateurs.  
•	La gestion des stocks.  
Votre travail est de modifier votre code afin de répondre aux besoins définis ci-dessus.
L'application exploitera des API pour interagir avec la base de données et un contrôle d'accès Utilisateur/Administrateur doit être mis en place.  
L’application pourra être enrichie avec des fonctionnalités supplémentaires telles que des recommandations de livres, des notifications pour les retours en retard, ou encore des rapports statistiques sur l'utilisation des livres pour améliorer l'expérience utilisateur et la gestion de la bibliothèque.  
