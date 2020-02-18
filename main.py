import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QBrush, QScreen
from PyQt5.QtCore import pyqtSlot, Qt, QDate, QRect
import MySQLdb as mdb
from datetime import date, timedelta, datetime

#MYSQL_HOST = "eu-cdbr-west-02.cleardb.net"
#MYSQL_DB = "heroku_0433427a7e2b4fb"
#MYSQL_USER = "b1682e5f992ac9"
#MYSQL_PASSW = "bfa269a6"

MYSQL_HOST="localhost"
MYSQL_DB="InternshipProject"
MYSQL_USER="intern"
MYSQL_PASSW=""

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Accostage Maritime | Marsa Maroc'
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class DatePopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add logo
        # Here I try to add the logo to the GUI.
        self.label = QLabel(self)
        self.pixmap = QPixmap('MarsaMaroc_logo.png')
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label)

        # Add tabs
        self.tabs.addTab(self.tab1, "Ajouter une navire")
        self.tabs.addTab(self.tab2, "Accoster")
        self.tabs.addTab(self.tab3, "Prévisions")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)

        # Nom_navire field
        self.nom_navire = QLabel(self)
        self.nom_navire.setText('Nom navire: ')
        self.nom_navire_line = QLineEdit(self)
        self.tab1.layout.addWidget(self.nom_navire)
        self.tab1.layout.addWidget(self.nom_navire_line)

        # Agent field
        self.agent = QLabel(self)
        self.agent.setText('Agent: ')
        self.agent_line = QLineEdit(self)
        self.tab1.layout.addWidget(self.agent)
        self.tab1.layout.addWidget(self.agent_line)

        # loa_navire field
        self.loa_navire = QLabel(self)
        self.loa_navire.setText('LOA: (en 10m)')
        self.loa_navire_line = QLineEdit(self)
        self.tab1.layout.addWidget(self.loa_navire)
        self.tab1.layout.addWidget(self.loa_navire_line)

        # tirant field
        self.tirant_eau = QLabel(self)
        self.tirant_eau.setText('Tirant d\'eau: ')
        self.tirant_eau_line = QLineEdit(self)
        self.tab1.layout.addWidget(self.tirant_eau)
        self.tab1.layout.addWidget(self.tirant_eau_line)

        # pays_navire field
        self.pays_navire = QLabel(self)
        self.pays_navire.setText('Pays d\'Origine: ')
        self.pays_navire_line = QLineEdit(self)
        self.tab1.layout.addWidget(self.pays_navire)
        self.tab1.layout.addWidget(self.pays_navire_line)

        # type_navire field
        self.type_navire = QLabel(self)
        self.type_navire.setText('Type Navire: ')
        self.type_navire_menu = QComboBox(self)
        self.type_navire_menu.addItem("")
        self.type_navire_menu.addItem("Porte Conteneurs")
        self.type_navire_menu.addItem("Vraq")
        self.type_navire_menu.activated[str].connect(self.type_navire_menu_)
        self.tab1.layout.addWidget(self.type_navire)
        self.tab1.layout.addWidget(self.type_navire_menu)

        # couleur_navire field
        self.couleur_lbl = QLabel(self)
        self.couleur_lbl.setText('Couleur: ')
        self.couleur_navire = QPushButton("Choisir une couleur")
        self.couleur_navire_line = ""
        self.couleur_navire.clicked.connect(self.openColorDialog)
        self.tab1.layout.addWidget(self.couleur_lbl)
        self.tab1.layout.addWidget(self.couleur_navire)

        # Enregister button
        self.enregister = QPushButton("Enregister")
        self.enregister.setFixedWidth(100)
        self.enregister.setFixedHeight(30)
        self.tab1.layout.addWidget(self.enregister, alignment=Qt.AlignCenter)
        self.enregister.clicked.connect(lambda: self.insertData())

        self.tab1.setLayout(self.tab1.layout)

        self.con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        self.cur = self.con.cursor()
        self.cur.execute("Select * FROM Navire")
        self.list_navires = self.cur.fetchall()
        self.con.close()

        # Create Second tab
        self.tab2.layout = QVBoxLayout(self)

        # select navire field
        self.select_navire = QLabel(self)
        self.select_navire.setText('Selectionner une navire: ')
        self.select_navire_menu = QComboBox(self)
        self.select_navire_menu.addItem("")
        for i in self.list_navires:
            self.select_navire_menu.addItem(" | ".join(list(i[1:-1])))
        self.select_navire_menu.activated[str].connect(
            self.navire_selectionne_)
        self.type_du_navire_selectionne = ""
        self.tab2.layout.addWidget(self.select_navire)
        self.tab2.layout.addWidget(self.select_navire_menu)

        # Nombre de main field
        self.nbr_de_mains = QLabel(self)
        self.nbr_de_mains.setText('Nombre de mains: ')
        self.nbr_de_mains_menu = QComboBox(self)
        self.nbr_de_mains_menu.addItem("1")
        self.nbr_de_mains_menu.addItem("2")
        self.nbr_de_mains_selectionne = "1"
        self.nbr_de_mains_menu.activated[str].connect(self.nbr_de_mains_menu_)
        self.tab2.layout.addWidget(self.nbr_de_mains)
        self.tab2.layout.addWidget(self.nbr_de_mains_menu)

        # tonnage field
        self.tonnage = QLabel(self)
        self.tonnage.setText('Tonnage: ')
        self.tonnage_line = QLineEdit(self)
        self.tonnage_line.setPlaceholderText(
            "Laissez vide pour un porte-conteneurs")
        self.tab2.layout.addWidget(self.tonnage)
        self.tab2.layout.addWidget(self.tonnage_line)

        # import export field
        self.IE_navire = QLabel(self)
        self.IE_navire.setText('Import / Export: (Format: xxx/xxx)')
        self.IE_navire_line = QLineEdit(self)
        self.IE_navire_line.setPlaceholderText("Laissez vide pour un vraquier")
        self.tab2.layout.addWidget(self.IE_navire)
        self.tab2.layout.addWidget(self.IE_navire_line)

        # Point metrique field
        self.point_metrique = QLabel(self)
        self.point_metrique.setText('Point métrique de départ: ')
        self.point_metrique_line = QLineEdit(self)
        self.tab2.layout.addWidget(self.point_metrique)
        self.tab2.layout.addWidget(self.point_metrique_line)

        # Date d'accostage field
        self.cal_lbl = QLabel(self)
        self.cal_lbl.setText('Date d\'accostage: ')
        self.date_accostage = QPushButton("Choisir une date")
        self.date_selectionnee = date.today().strftime('%d/%m/%Y')
        self.date_accostage.clicked.connect(self.showDate)
        self.tab2.layout.addWidget(self.cal_lbl)
        self.tab2.layout.addWidget(self.date_accostage)

        # shift de depart field
        self.shift_de_depart = QLabel(self)
        self.shift_de_depart.setText('Shift de départ: ')
        self.shift_de_departs_menu = QComboBox(self)
        self.shift_de_departs_menu.addItem("1")
        self.shift_de_departs_menu.addItem("2")
        self.shift_de_departs_menu.addItem("3")
        self.shift_de_depart_selectionne = "1"
        self.shift_de_departs_menu.activated[str].connect(
            self.shift_de_departs_menu_)
        self.tab2.layout.addWidget(self.shift_de_depart)
        self.tab2.layout.addWidget(self.shift_de_departs_menu)

        # Accoster button
        self.accoster = QPushButton("Accoster")
        self.accoster.setFixedWidth(100)
        self.accoster.setFixedHeight(30)
        self.tab2.layout.addWidget(self.accoster, alignment=Qt.AlignCenter)
        self.accoster.clicked.connect(lambda: self.insertAccostage())

        self.tab2.setLayout(self.tab2.layout)

        # Create Third tab
        self.tab3.layout = QHBoxLayout()

        # Create the table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(16)
        self.tableWidget.setColumnCount(67 + 2)
        self.tab3.layout.addWidget(self.tableWidget)

        # Hide headers
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.refresh()

        # Effacer tout button
        self.vbox_acc = QVBoxLayout()

        self.effacer_tout = QPushButton("Effacer\nTout")
        self.actualiser = QPushButton("Actualiser")
        self.annuler = QPushButton("Undo")
        self.exporter = QPushButton("Exporter")

        self.vbox_acc.addWidget(self.effacer_tout, 0)
        self.vbox_acc.addWidget(self.actualiser,  0)
        self.vbox_acc.addWidget(self.annuler,  0)
        self.vbox_acc.addWidget(self.exporter,  0)

        self.effacer_tout.clicked.connect(lambda: self.deleteAll())
        self.actualiser.clicked.connect(lambda: self.refresh())
        self.annuler.clicked.connect(lambda: self.deleteLastAccostage())
        self.exporter.clicked.connect(lambda: self._export())

        self.tab3.layout.addLayout(self.vbox_acc)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def type_navire_menu_(self):
        self.type_navire_choice = self.type_navire_menu.currentText()
        print(self.type_navire_choice)

    def dateChanged(self):
        # print(self.cal.selectedDate().toString("dd/MM/yyyy"))
        self.date_selectionnee = self.cal.selectedDate().toString("dd/MM/yyyy")

    def nbr_de_mains_menu_(self):
        # print(self.nbr_de_mains_menu.currentText())
        self.nbr_de_mains_selectionne = self.nbr_de_mains_menu.currentText()

    def shift_de_departs_menu_(self):
        self.shift_de_depart_selectionne = self.shift_de_departs_menu.currentText()

    def navire_selectionne_(self):
        self.navire_selectionne = self.select_navire_menu.currentText()

    @pyqtSlot()
    def openColorDialog(self):
        global color
        color = QColorDialog.getColor()

        if color.isValid():
            self.couleur_navire_line = color.name()
            print(self.couleur_navire_line)

    @pyqtSlot()
    def showDate(self):
        self.popup = DatePopup()
        #self.popup.setGeometry(QRect(100, 100, 400, 200))

        self.popup_layout = QVBoxLayout(self)

        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.show()
        self.cal.selectionChanged.connect(self.dateChanged)
        self.popup_layout.addWidget(self.cal)

        self.popup.setLayout(self.popup_layout)
        self.popup.setWindowTitle("Choisir une date")
        self.popup.show()
        

    def _export(self):
        self.filename = "screenshot.jpg"
        #self.screen = self.tab3
        #self.p = self.screen.grabWindow(0)
        
        #self.pix = QtGui.QPixmap(self.tableWidget.size())
        self.pix = self.tableWidget.grab(QRect(0, 0, self.tableWidget.size().width(), self.tableWidget.size().height()))
        self.pix.save("save.png")        
        #self.p.save(self.filename, 'jpg')
        
        QMessageBox.about(
            self, 'Succès', 'les données ont été exportées avec succès.')
        
       	
		
		
		

    def insertAccostage(self):
        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        cur = con.cursor()
        cur.execute("INSERT INTO Accostage(nom_navire, nbr_de_mains, tonnage_navire, ie_navire, point_metrique, date_accostage, shift_de_depart) VALUES('%s', '%s', '%s', '%s', '%s','%s', '%s')" % (
            self.navire_selectionne,
            self.nbr_de_mains_selectionne,
            self.tonnage_line.text(),
            self.IE_navire_line.text(),
            self.point_metrique_line.text(),
            self.date_selectionnee,
            self.shift_de_depart_selectionne
        )
        )
        con.commit()
        QMessageBox.about(
            self, 'Succès', 'Les données sont bien enregistrées.')
        con.close()

    def deleteAll(self):
        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        cur = con.cursor()
        cur.execute("DELETE FROM Accostage WHERE id_accostage > 0;")
        con.commit()
        QMessageBox.about(
            self, 'Succès', 'Toutes les données ont été supprimées.')
        con.close()

    def deleteLastAccostage(self):
        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        cur = con.cursor()
        cur.execute("DELETE FROM Accostage ORDER BY id_accostage desc limit 1")
        con.commit()
        QMessageBox.about(
            self, 'Succès', 'Le dernier accostage est annulé.\nVeuillez actualiser le tableau.')
        con.close()

    def refresh(self):

        self.tableWidget.clear()
        self.tableWidget.clearSpans()

        # Naming headers
        self.tableWidget.setHorizontalHeaderLabels(
            ['', 'PM en 10m'] + [str(i) for i in range(1, 68)])

        # Setting headers size
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 80)

        for i in range(2, 67 + 3):
            self.tableWidget.setColumnWidth(i, 1)

        # Postes Header
        newItem = QTableWidgetItem("Poste")
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, newItem)

        # Poste 12
        self.tableWidget.setSpan(0, 2, 1, 17)
        newItem = QTableWidgetItem("Poste 12")
        newItem.setTextAlignment(Qt.AlignCenter)
        newItem.setFont(QFont("Times", 15, QFont.Bold))
        newItem.setBackground((QColor(254, 184, 170)))
        self.tableWidget.setItem(0, 2, newItem)

        # Poste 13
        self.tableWidget.setSpan(0, 19, 1, 17)
        newItem = QTableWidgetItem("Poste 13")
        newItem.setTextAlignment(Qt.AlignCenter)
        newItem.setFont(QFont("Times", 15, QFont.Bold))
        newItem.setBackground((QColor(119, 214, 106)))
        self.tableWidget.setItem(0, 19, newItem)

        # Poste 14
        self.tableWidget.setSpan(0, 36, 1, 17)
        newItem = QTableWidgetItem("Poste 14")
        newItem.setTextAlignment(Qt.AlignCenter)
        newItem.setFont(QFont("Times", 15, QFont.Bold))
        newItem.setBackground((QColor(212, 126, 5)))
        self.tableWidget.setItem(0, 36, newItem)

        # RORO
        self.tableWidget.setSpan(0, 53, 1, 17)
        newItem = QTableWidgetItem("RORO")
        newItem.setTextAlignment(Qt.AlignCenter)
        newItem.setFont(QFont("Times", 15, QFont.Bold))
        newItem.setBackground((QColor(222, 199, 241)))
        self.tableWidget.setItem(0, 53, newItem)

        # DATES
        today = date.today()

        #self.tableWidget.setSpan(1, 0, 3, 1)
        newItem = QTableWidgetItem(
            "%s" % ((today - timedelta(days=2)).strftime('%d/%m/%Y')))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(2, 0, newItem)

        #self.tableWidget.setSpan(4, 0, 3, 1)
        newItem = QTableWidgetItem(
            "%s" % ((today - timedelta(days=1)).strftime('%d/%m/%Y')))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(5, 0, newItem)

        #self.tableWidget.setSpan(7, 0, 3, 1)
        newItem = QTableWidgetItem("%s" % (today.strftime('%d/%m/%Y')))
        newItem.setTextAlignment(Qt.AlignCenter)
        newItem.setForeground(QBrush(QColor(255, 0, 0)))
        self.tableWidget.setItem(8, 0, newItem)

        #self.tableWidget.setSpan(10, 0, 3, 1)
        newItem = QTableWidgetItem(
            "%s" % ((today + timedelta(days=1)).strftime('%d/%m/%Y')))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(11, 0, newItem)

        #self.tableWidget.setSpan(13, 0, 3, 1)
        newItem = QTableWidgetItem(
            "%s" % ((today + timedelta(days=2)).strftime('%d/%m/%Y')))
        newItem.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(14, 0, newItem)

        shift = 1
        for i in range(1, 30):
            if shift == 4:
                shift = 1
            newItem = QTableWidgetItem("Shift 0" + str(shift % 4))
            if shift == 3:
                newItem.setForeground(QBrush(QColor(255, 255, 255)))
                newItem.setBackground(QColor(100, 100, 150))
            newItem.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, newItem)
            shift += 1

        # Remplissage du tableau
        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        cur = con.cursor()
        cur.execute(
            "Select nom_navire, point_metrique, date_accostage, shift_de_depart, tonnage_navire, ie_navire, nbr_de_mains FROM Accostage")
        combo_affichage = []
        L = cur.fetchall()
        con.close()

        L = [list(i) for i in L]

        for i in L:
            if "Porte Conteneur" in i[0]:
                i.pop(4)
                try:
                    imp = int(i[4].split("/")[0])
                    exp = int(i[4].split("/")[1])
                    nbr_de_shifts_total = int(
                        (imp + exp) / (120 * int(i[-1]))) + 1
                except ValueError:
                    QMessageBox.about(self, 'erreur de la base de données',
                                      'Il semble que vous ayez entré des données non valides. Afin de résoudre ce problème, le dernier accostage sera supprimé. S\'il vous plaît, réinsérez soigneusement vos données.')
                    self.deleteLastAccostage()
            else:
                i.pop(5)
                try:
                    tonnage = int(i[4])
                    nbr_de_shifts_total = int(
                        tonnage / (1500 * int(i[-1]))) + 1
                except ValueError:
                    QMessageBox.about(self, 'erreur de la base de données',
                                      'Il semble que vous ayez entré des données non valides. Afin de résoudre ce problème, le dernier accostage sera supprimé. S\'il vous plaît, réinsérez soigneusement vos données.')
                    self.deleteLastAccostage()

            shift_de_depart = int(i[3])
            #shift_de_depart = 1
            index_shift = shift_de_depart
            day = i[2]
            for j in range(nbr_de_shifts_total):
                #print("shift 0%d -- day %s" % (index_shift, day))
                combo_affichage.append(
                    [i[0], i[1], index_shift, day, nbr_de_shifts_total])
                index_shift += 1
                if index_shift == 4:
                    index_shift = 1
                    day = (datetime.strptime(day, '%d/%m/%Y') +
                           timedelta(days=1)).strftime('%d/%m/%Y')
        A = []
        for i in range(len(combo_affichage)):
            con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
            cur = con.cursor()
            q = "SELECT loa_navire, couleur_navire FROM Navire WHERE nom_navire LIKE '{}%'".format(
                combo_affichage[i][0][0:5])
            cur.execute(q)
            A = list(cur.fetchall())
            combo_affichage[i] += [A[0][0], A[0][1]]
            con.close()

        today = date.today()
        days_range = [
            (today - timedelta(days=2)).strftime('%d/%m/%Y'),
            (today - timedelta(days=1)).strftime('%d/%m/%Y'),
            today.strftime('%d/%m/%Y'),
            (today + timedelta(days=1)).strftime('%d/%m/%Y'),
            (today + timedelta(days=2)).strftime('%d/%m/%Y')
        ]

        clean_combo_affichage = []
        for i in combo_affichage:
            if i[3] in days_range:
                clean_combo_affichage.append(i)

        for i in clean_combo_affichage:
            i[1] = int(i[1])
            i[-2] = int(i[-2])
            h = i[-1].lstrip('#')
            i[-1] = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            s = 0
            for s in range(5):
                if i[-4] == days_range[s]:
                    cord = {"col": 0, "row": 0}
                    cord["col"] = i[1] + 1
                    cord["row"] = i[2] + s * 3
                    cord["span"] = i[-2] // 10
                    i.append(cord)

        for i in clean_combo_affichage:

            self.tableWidget.setSpan(
                i[-1]["row"], i[-1]["col"], 1, i[-1]["span"])
            newItem = QTableWidgetItem("%s" % (i[0]))
            newItem.setTextAlignment(Qt.AlignCenter)
            newItem.setBackground((QColor(i[-2][0], i[-2][1], i[-2][2])))
            self.tableWidget.setItem(i[-1]["row"], i[-1]["col"], newItem)

        

    def insertData(self):
        con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSW, MYSQL_DB)
        cur = con.cursor()
        cur.execute("INSERT INTO Navire(nom_navire, agent_navire, loa_navire, tirant_eau_navire, pays_navire, type_navire, couleur_navire) VALUES('%s', '%s', '%s', '%s','%s', '%s', '%s')" % (
            self.nom_navire_line.text(),
            self.agent_line.text(),
            self.loa_navire_line.text(),
            self.tirant_eau_line.text(),
            self.pays_navire_line.text(),
            self.type_navire_choice,
            str(self.couleur_navire_line)
        )
        )
        con.commit()
        QMessageBox.about(
            self, 'Succès', 'Les données sont bien enregistrées.')
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
