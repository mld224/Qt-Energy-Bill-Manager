#  Qt Energy Manager

Application de gestion et de suivi de consommation électrique développée en **Python** avec l'interface **PyQt5**.

Ce projet a été réalisé dans le cadre de la **1ère année de BUT Informatique**. Il démontre la capacité à intégrer une base de données, une interface graphique et de la visualisation de données dans une application complète.

##  Fonctionnalités Clés

* **Authentification Sécurisée** : Système de connexion et d'inscription avec stockage des utilisateurs en base de données SQLite.
* **Calculateur de Tarifs Réels** :
    * Prise en charge des tarifs complexes comme **EDF Tempo** (Jours Bleu/Blanc/Rouge) et Heures Pleines/Creuses.
* **Tableau de Bord Graphique** :
    * Visualisation dynamique via **Matplotlib** pour comparer la consommation (kWh) et le coût (€).
* **Export Professionnel** :
    * Génération de factures au format PDF incluant logo et tableau récapitulatif via la librairie `ReportLab`.
* **Historique** : Sauvegarde et modification des factures passées.

##  Stack Technique

* **Langage** : Python 3
* **Interface** : PyQt5 (QStackedWidget, Layouts).
* **Données** : SQLite3 (Gestion relationnelle Utilisateurs/Factures).
* **Vues** : Matplotlib (Intégration native dans Qt).
* **Sortie** : ReportLab (Génération de documents).

##  Installation et Exécution

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
