# MEDICODent-ETL
Portail de Gestion des Données d'une Clinique Dentaire
## Aperçu

Ce projet fait partie de notre programme de Master en Informatique à l'Université Lyon 2 pour le module SI SI Décisionnels. 
L'objectif de ce projet est de développer un portail web offrant des fonctionnalités ETL (Extraction, Transformation, Chargement) pour traiter les données à partir d'un fichier XLS, générer des fichiers CSV, puis charger les données dans un datamart. 
Cette étude de cas concerne les données financières et patientelles d'un cabinet dentaire sur une période de sept ans, avec une attention particulière à l'activité de radiographie panoramique.

## Structure du Projet

1. **Processus ETL**
    - **Extraction :** Extraction des données à partir des fichiers XLS.
    - **Transformation :** Nettoyage et transformation des données selon les besoins.
    - **Chargement :** Chargement des données transformées dans une base de données MySQL.

2. **Portail Web**
    - Fournir une interface permettant aux utilisateurs de téléverser des fichiers XLS.
    - Afficher les données traitées et permettre le téléchargement des fichiers CSV.
    - Charger les données dans le datamart (base de données MySQL).

## Stack Technique

- **Backend :** Python
    - Bibliothèques : pandas, openpyxl, SQLAlchemy, Flask
- **Frontend :** HTML, CSS, JavaScript (Flask pour servir les templates)
- **Base de données :** MySQL

## Fonctionnalités

- **Téléversement de fichiers XLS :** Les utilisateurs peuvent téléverser des fichiers XLS contenant les données.
- **Traitement des données :** Extraire et transformer les données téléversées.
- **Génération de CSV :** Générer et télécharger des fichiers CSV à partir des données traitées.
- **Chargement des données :** Charger les données traitées dans le datamart MySQL.
- **Validation des données :** Vérifier la cohérence et l'exactitude des données par rapport aux données de terrain fournies.

## Directives de Contribution

Nous accueillons les contributions ! Veuillez suivre ces étapes :
1. Forkez le répertoire.
2. Créez une nouvelle branche (`git checkout -b feature/votre-fonctionnalite`).
3. Commitez vos modifications (`git commit -am 'Ajout d'une fonctionnalité'`).
4. Pushez vers la branche (`git push origin feature/votre-fonctionnalite`).
5. Créez une nouvelle Pull Request.

## Commande pour lancer l'application

`python app.py`
