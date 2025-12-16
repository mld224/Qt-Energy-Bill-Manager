# Qt-Energy-Bill-Manager
Application Python/PyQt5 de gestion énergétique (Graphiques &amp; PDF). Projet réalisé en 1ère année de BUT Informatique.

#  Qt Energy Manager

Application de gestion et de suivi de consommation électrique développée en **Python** avec l'interface **PyQt5**.

Ce projet a été réalisé dans le cadre de la **1ère année de BUT Informatique**. Il démontre la capacité à intégrer une base de données, une interface graphique et de la visualisation de données dans une application complète.

##  Fonctionnalités Clés

* [cite_start]**Authentification Sécurisée** : Système de connexion et d'inscription avec stockage des utilisateurs en base de données SQLite [cite: 341-356].
* **Calculateur de Tarifs Réels** :
    * [cite_start]Prise en charge des tarifs complexes comme **EDF Tempo** (Jours Bleu/Blanc/Rouge) et Heures Pleines/Creuses [cite: 220-234].
* **Tableau de Bord Graphique** :
    * [cite_start]Visualisation dynamique via **Matplotlib** pour comparer la consommation (kWh) et le coût (€) [cite: 178-193].
* **Export Professionnel** :
    * [cite_start]Génération de factures au format PDF incluant logo et tableau récapitulatif via la librairie `ReportLab` [cite: 305-325].
* **Historique** : Sauvegarde et modification des factures passées (CRUD).

##  Stack Technique

* **Langage** : Python 3
* **Interface** : PyQt5 (QStackedWidget, Layouts).
* **Données** : SQLite3 (Gestion relationnelle Utilisateurs/Factures).
* **Vues** : Matplotlib (Intégration native dans Qt).
* **Sortie** : ReportLab (Génération de documents).

##  Installation

1.  Installer les dépendances :
    ```bash
    pip install PyQt5 matplotlib reportlab
    ```
2.  Lancer l'application :
    ```bash
    python main.py
    ```

##  Auteur
**Mamadou Lamine DIALLO** - Étudiant en BUT Informatique (Projet de Semestre 2)
