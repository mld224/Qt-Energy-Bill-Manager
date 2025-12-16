import sqlite3
from datetime import date

DB_PATH = "factures.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Table des utilisateurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        nom     TEXT    NOT NULL,
        prenom  TEXT    NOT NULL,
        email   TEXT    UNIQUE NOT NULL,
        pwd     TEXT    NOT NULL
    )
    """)
    # Table des factures, avec champ date
    c.execute("""
    CREATE TABLE IF NOT EXISTS factures (
        user_id INTEGER,
        mois    TEXT,
        date    TEXT,
        i0      REAL,
        i1      REAL,
        conso   REAL,
        abo     TEXT,
        montant REAL,
        PRIMARY KEY(user_id, mois),
        FOREIGN KEY(user_id) REFERENCES utilisateurs(id)
    )
    """)
    conn.commit()
    conn.close()

def ajouter_utilisateur(nom, prenom, email, pwd):
    """Retourne True si l'utilisateur a bien été créé, False si l'email existe déjà."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO utilisateurs(nom, prenom, email, pwd) VALUES (?, ?, ?, ?)",
            (nom, prenom, email, pwd)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verifier_utilisateur(email, pwd):
    """Retourne l'id de l'utilisateur si email+pwd corrects, sinon None."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM utilisateurs WHERE email = ? AND pwd = ?", (email, pwd))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_info(user_id):
    """Retourne un dict {'nom':…, 'prenom':…} pour l'utilisateur donné."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nom, prenom FROM utilisateurs WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"nom": row[0], "prenom": row[1]}
    return {}

def ajouter_facture(user_id, mois, i0, i1, conso, abo, montant, date_iso=None):
    """Insère ou remplace une facture, en ajoutant la date (aujourd'hui si non fournie)."""
    if date_iso is None:
        date_iso = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT OR REPLACE INTO factures
           (user_id, mois, date, i0, i1, conso, abo, montant)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, mois, date_iso, i0, i1, conso, abo, montant)
    )
    conn.commit()
    conn.close()
    return True

def get_factures(user_id):
    """
    Retourne la liste des factures de l'utilisateur sous forme de tuples :
    (mois, date, conso, montant), triés par date.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT mois, date, conso, montant FROM factures WHERE user_id = ? ORDER BY date",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def supprimer_facture(user_id, mois):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM factures WHERE user_id = ? AND mois = ?", (user_id, mois))
    conn.commit()
    conn.close()

def modifier_facture(user_id, mois, i0, i1, conso, abo, montant):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """UPDATE factures
           SET i0 = ?, i1 = ?, conso = ?, abo = ?, montant = ?
           WHERE user_id = ? AND mois = ?""",
        (i0, i1, conso, abo, montant, user_id, mois)
    )
    conn.commit()
    conn.close()
