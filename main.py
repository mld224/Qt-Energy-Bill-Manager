import sys
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QStackedWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QInputDialog, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4
import database

MOIS = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

STYLESHEET = """
QMainWindow { background-color: #f5f9ff; }
QWidget { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #343a40; }
QLabel { color: #343a40; }
QLabel#TitleLabel {
    font-size: 22pt;
    font-weight: bold;
    color: #007bff;
    text-align: center;
    padding-bottom: 8px;
    border-bottom: 2px solid #007bff;
}
QLineEdit, QComboBox {
    padding: 8px;
    border: 1px solid #ced4da;
    border-radius: 6px;
    background-color: #ffffff;
    min-height: 30px;
}
QPushButton {
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    text-transform: uppercase;
    min-width: 140px;
}
QPushButton#btn_login, QPushButton#btn_graph {
    background-color: #007bff; color: white;
}
QPushButton#btn_calc, QPushButton#btn_inscrire {
    background-color: #28a745; color: white;
}
QPushButton#btn_annuler, QPushButton#btn_quitter {
    background-color: #dc3545; color: white;
}
QPushButton#btn_revenir {
    background-color: #ffc107; color: #212529;
}
QPushButton:hover { opacity: 0.9; }
"""

class PlaceholderLineEdit(QLineEdit):
    def __init__(self, text):
        super().__init__(text)
        self.clicked = False
        self.setStyleSheet("color: grey;")
        self.setPlaceholderText(text)
    def focusInEvent(self, ev):
        if not self.clicked:
            self.clear()
            self.setStyleSheet("color: black;")
            self.clicked = True
            if "mot de passe" in self.placeholderText().lower():
                self.setEchoMode(QLineEdit.Password)
        super().focusInEvent(ev)

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(20, 10, 20, 20)
        v.setSpacing(12)

        logo = QLabel(self)
        pixmap = QPixmap("Logo.png")
        logo.setPixmap(pixmap.scaledToWidth(150, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        v.addWidget(logo)

        title = QLabel("CONNEXION", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.email = PlaceholderLineEdit("abcd@gmail.com")
        self.passw = PlaceholderLineEdit("Mot de passe...")
        v.addWidget(self.email)
        v.addWidget(self.passw)

        self.btn_login    = QPushButton("Connexion"); self.btn_login.setObjectName("btn_login")
        self.btn_register = QPushButton("S'inscrire");  self.btn_register.setObjectName("btn_inscrire")
        v.addWidget(self.btn_login)
        v.addWidget(self.btn_register)

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)

        title = QLabel("INSCRIPTION", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.nom    = PlaceholderLineEdit("Nom")
        self.prenom = PlaceholderLineEdit("Prénom")
        self.email  = PlaceholderLineEdit("abcd@gmail.com")
        self.pwd    = PlaceholderLineEdit("Mot de passe...")
        self.conf   = PlaceholderLineEdit("Mot de passe...")
        for w in (self.nom, self.prenom, self.email, self.pwd, self.conf):
            v.addWidget(w)

        self.btn_inscrire = QPushButton("S'inscrire"); self.btn_inscrire.setObjectName("btn_inscrire")
        self.btn_annuler  = QPushButton("Annuler");     self.btn_annuler.setObjectName("btn_annuler")
        v.addWidget(self.btn_inscrire)
        v.addWidget(self.btn_annuler)

class CalculPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)

        title = QLabel("Calcul de la facture", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.i0 = PlaceholderLineEdit("Index initiale (ex: 120)")
        self.i1 = PlaceholderLineEdit("Index  final (ex: 750)")
        v.addWidget(self.i0)
        v.addWidget(self.i1)

        v.addWidget(QLabel("Type d'abonnement:"))
        self.combo = QComboBox()
        self.combo.addItems(["Base", "Heures pleines/Heures creuses", "Tempo"])
        v.addWidget(self.combo)

        v.addWidget(QLabel("Fournisseur d'électricité:"))
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItems(["EDF", "Engie", "TotalEnergies"])
        v.addWidget(self.supplier_combo)

        self.tempo_day_label = QLabel("Jour Tempo:")
        self.tempo_day_combo = QComboBox()
        self.tempo_day_combo.addItems(["Bleu", "Blanc", "Rouge"])
        self.tempo_day_label.hide()
        self.tempo_day_combo.hide()
        v.addWidget(self.tempo_day_label)
        v.addWidget(self.tempo_day_combo)

        self.combo.currentTextChanged.connect(self._on_abonnement_changed)

        self.btn_calc = QPushButton("Calculer"); self.btn_calc.setObjectName("btn_calc")
        v.addWidget(self.btn_calc)

    def _on_abonnement_changed(self, text):
        is_tempo = (text == "Tempo")
        self.tempo_day_label.setVisible(is_tempo)
        self.tempo_day_combo.setVisible(is_tempo)

class InvoicePage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)

        title = QLabel("Facture générée", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.labels = {}
        for key in ("Nom", "Prénom", "Indice initial", "Indice final", "Consommation", "Montant"):
            h = QHBoxLayout()
            h.addWidget(QLabel(f"{key} :"))
            lbl = QLabel("")
            h.addWidget(lbl)
            v.addLayout(h)
            self.labels[key] = lbl

        self.month_combo = QComboBox()
        self.month_combo.addItems(MOIS)
        v.addWidget(QLabel("Choisir le mois"))
        v.addWidget(self.month_combo)


        self.btn_add     = QPushButton("Ajouter la facture au mois"); self.btn_add.setObjectName("btn_calc")
        self.btn_pdf     = QPushButton("Télécharger PDF");            self.btn_pdf.setObjectName("btn_calc")
        self.btn_view    = QPushButton("Historique des factures");     self.btn_view.setObjectName("btn_revenir")
        self.btn_logout  = QPushButton("Déconnexion");                self.btn_logout.setObjectName("btn_annuler")
        self.btn_quitter = QPushButton("Quitter");                    self.btn_quitter.setObjectName("btn_quitter")
        for b in (self.btn_add, self.btn_pdf, self.btn_view, self.btn_logout, self.btn_quitter):
            v.addWidget(b)

class GestionPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)

        title = QLabel("Factures enregistrées", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.list = QListWidget()
        v.addWidget(self.list)

        h = QHBoxLayout()
        self.btn_modifier  = QPushButton("Modifier");  self.btn_modifier.setObjectName("btn_calc")
        self.btn_supprimer = QPushButton("Supprimer"); self.btn_supprimer.setObjectName("btn_annuler")
        self.btn_compare   = QPushButton("Comparer"); self.btn_compare.setObjectName("btn_graph")
        self.btn_revenir   = QPushButton("Retour");    self.btn_revenir.setObjectName("btn_revenir")
        self.btn_quitter   = QPushButton("Quitter");   self.btn_quitter.setObjectName("btn_quitter")
        self.btn_retour    = QPushButton("Revenir à la page de calcul"); self.btn_retour.setObjectName("btn_retour")
        for b in (self.btn_modifier, self.btn_supprimer, self.btn_compare,
                  self.btn_revenir, self.btn_quitter):
            h.addWidget(b)
        v.addLayout(h)

class GraphiquePage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)

        title = QLabel("Graphique comparatif", self)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        v.addWidget(self.canvas)

        self.btn_revenir = QPushButton("Retour"); self.btn_revenir.setObjectName("btn_revenir")
        v.addWidget(self.btn_revenir)

    def plot(self, data):
        if not data:
            QMessageBox.information(self, "Aucune donnée", "Pas de factures à comparer.")
            return
        mois    = [row[0] for row in data]
        conso   = [row[2] for row in data]
        montant = [row[3] for row in data]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(range(len(mois)), montant, label="Montant (€)")
        ax.plot(range(len(mois)), conso, marker='o', label="Conso (kWh)")
        ax.set_xticks(range(len(mois)))
        ax.set_xticklabels(mois, rotation=45)
        ax.legend()
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        database.init_db()
        self.setWindowTitle("Énergie Manager")
        self.setMinimumSize(QSize(800,700))
        self.setStyleSheet(STYLESHEET)

        self.stack    = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.login    = LoginPage()
        self.register = RegisterPage()
        self.calcul   = CalculPage()
        self.invoice  = InvoicePage()
        self.gestion  = GestionPage()
        self.graph    = GraphiquePage()
        for page in (self.login, self.register, self.calcul, self.invoice, self.gestion, self.graph):
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(self.login)

        self.user_id     = None
        self.user_nom    = ""
        self.user_prenom = ""
        self.current_data= {}

        self.login.btn_login.clicked.connect(self.connexion)
        self.login.btn_register.clicked.connect(lambda: self.stack.setCurrentWidget(self.register))
        self.register.btn_inscrire.clicked.connect(self.inscription)
        self.register.btn_annuler.clicked.connect(lambda: self.stack.setCurrentWidget(self.login))
        self.calcul.btn_calc.clicked.connect(self.generate_invoice)
        self.invoice.btn_add.clicked.connect(self.add_to_month)
        self.invoice.btn_pdf.clicked.connect(self.download_pdf)
        self.invoice.btn_view.clicked.connect(self.show_gestion)
        self.invoice.btn_logout.clicked.connect(self.logout)
        self.invoice.btn_quitter.clicked.connect(QApplication.instance().quit)
        self.gestion.btn_revenir.clicked.connect(self.generate_invoice)
        self.gestion.btn_modifier.clicked.connect(self.modify_invoice)
        self.gestion.btn_supprimer.clicked.connect(self.delete_invoice)
        self.gestion.btn_compare.clicked.connect(self.show_graph)
        self.gestion.btn_quitter.clicked.connect(QApplication.instance().quit)
        self.graph.btn_revenir.clicked.connect(lambda: self.stack.setCurrentWidget(self.gestion))
        

    def connexion(self):
        email = self.login.email.text().strip()
        pwd   = self.login.passw.text().strip()
        uid = database.verifier_utilisateur(email, pwd)
        if uid:
            self.user_id = uid
            info = database.get_user_info(uid)
            self.user_nom    = info.get("nom", "")
            self.user_prenom = info.get("prenom", "")
            self.stack.setCurrentWidget(self.calcul)
        else:
            QMessageBox.warning(self, "Erreur", "Identifiants incorrects")

    def inscription(self):
        nom, prenom = self.register.nom.text().strip(), self.register.prenom.text().strip()
        email       = self.register.email.text().strip()
        pwd, conf   = self.register.pwd.text().strip(), self.register.conf.text().strip()
        if pwd != conf:
            QMessageBox.warning(self, "Erreur", "Mots de passe différents")
            return
        if database.ajouter_utilisateur(nom, prenom, email, pwd):
            QMessageBox.information(self, "Succès", "Inscription réussie")
            self.login.email.setText(email)
            self.stack.setCurrentWidget(self.login)
        else:
            QMessageBox.warning(self, "Erreur", "Email déjà utilisé")

    def generate_invoice(self):
        try:
            i0 = float(self.calcul.i0.text())
            i1 = float(self.calcul.i1.text())
            if i1 <= i0:
                raise ValueError
        except:
            QMessageBox.warning(self, "Erreur", "Valeurs invalides")
            return

        conso    = i1 - i0
        supplier = self.calcul.supplier_combo.currentText()
        abo      = self.calcul.combo.currentText()

        tarifs = {
            "EDF": {
                "Base": 0.2016, "HP": 0.2146, "HC": 0.1696,
                "Tempo": {
                    "Bleu":  (0.1552, 0.1288),
                    "Blanc": (0.1792, 0.1447),
                    "Rouge": (0.6586, 0.1518)
                }
            },
            "Engie": {
                "Base": 0.2150, "HP": 0.2243, "HC": 0.1847
            },
            "TotalEnergies": {
                "Base": 0.1823, "HP": 0.1937, "HC": 0.1541
            }
        }

        if abo == "Base":
            montant = conso * tarifs[supplier]["Base"]
        elif abo == "Heures pleines/Heures creuses":
            montant = conso * 0.7 * tarifs[supplier]["HP"] + conso * 0.3 * tarifs[supplier]["HC"]
        else:
            if supplier != "EDF":
                QMessageBox.warning(self, "Erreur", "Tempo uniquement chez EDF")
                return
            day = self.calcul.tempo_day_combo.currentText()
            hp_t, hc_t = tarifs["EDF"]["Tempo"][day]
            montant    = conso * 0.7 * hp_t + conso * 0.3 * hc_t

        self.current_data = {
            "Nom":             self.user_nom.capitalize(),
            "Prénom":          self.user_prenom.capitalize(),
            "Indice initial":  f"{i0:.2f}",
            "Indice final":    f"{i1:.2f}",
            "Consommation":    f"{conso:.2f} kWh",
            "Montant":         f"{montant:.2f} €",
            "abo":             abo,
            "fournisseur":     supplier,
            "i0":              i0,
            "i1":              i1,
            "conso":           conso,
            "montant":         montant
        }
        for key, lbl in self.invoice.labels.items():
            lbl.setText(self.current_data[key])

        self.invoice.month_combo.setCurrentIndex(0)
        self.stack.setCurrentWidget(self.invoice)

    def add_to_month(self):
        mois      = self.invoice.month_combo.currentText()
        d         = self.current_data
        today_iso = date.today().isoformat()
        database.ajouter_facture(
            self.user_id, mois,
            d["i0"], d["i1"], d["conso"],
            d["abo"], d["montant"], today_iso
        )
        QMessageBox.information(self, "Succès", f"Facture de {mois} du {today_iso} ajoutée")
        self.show_gestion()

    def show_gestion(self):
        self.gestion.list.clear()
        self.factures = database.get_factures(self.user_id)
        for m, date_iso, c, p in self.factures:
            self.gestion.list.addItem(f"{date_iso} — {m} — {c:.1f} kWh — {p:.2f} €")
        self.stack.setCurrentWidget(self.gestion)

    def delete_invoice(self):
        row = self.gestion.list.currentRow()
        if row >= 0:
            mois = self.factures[row][0]
            database.supprimer_facture(self.user_id, mois)
            self.show_gestion()

    def modify_invoice(self):
        row = self.gestion.list.currentRow()
        if row < 0:
            return
        mois = self.factures[row][0]
        i0, ok1 = QInputDialog.getDouble(self, "Modifier", "Indice initial:", 0)
        i1, ok2 = QInputDialog.getDouble(self, "Modifier", "Indice final:",   0)
        if ok1 and ok2 and i1 > i0:
            conso   = i1 - i0
            montant = conso * 0.18
            database.modifier_facture(self.user_id, mois, i0, i1, conso, "Base", montant)
            self.show_gestion()

    def show_graph(self):
        data = database.get_factures(self.user_id)
        if not data:
            QMessageBox.information(self, "Vide", "Aucune facture à afficher")
            return
        self.graph.plot(data)
        self.stack.setCurrentWidget(self.graph)

    def download_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer la facture", "", "PDF Files (*.pdf)")
        if not path:
            return
        c = pdfcanvas.Canvas(path, pagesize=A4)
        w, h = A4
        logo_path = "Logo.png"
        c.drawImage(logo_path, (w-150)/2, h-140, width=150, height=150, mask='auto')
        y = h - 180
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Nom             : {self.current_data['Nom']}")
        c.drawString(300, y, f"Prénom          : {self.current_data['Prénom']}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Fournisseur     : {self.current_data['fournisseur']}")
        c.drawString(300, y, f"Abonnement      : {self.current_data['abo']}")
        y -= 20
        c.drawString(50, y, f"Indice initial  : {self.current_data['i0']:.2f} kWh")
        c.drawString(300, y, f"Indice final    : {self.current_data['i1']:.2f} kWh")
        y -= 20
        c.drawString(50, y, f"Consommation    : {self.current_data['conso']:.2f} kWh")
        c.drawString(300, y, f"Montant         : {self.current_data['montant']:.2f} €")
        y -= 30
        c.drawString(50, y, f"Date d'émission : {date.today().isoformat()}")
        c.showPage()
        c.save()
        QMessageBox.information(self, "PDF généré", f"Facture enregistrée dans :\n{path}")

    def logout(self):
        self.user_id = None
        self.stack.setCurrentWidget(self.login)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
