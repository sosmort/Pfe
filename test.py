import sys
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QMessageBox
import sys
from PyQt4.QtGui import *
from PySide import QtCore, QtGui
from PySide import QtUiTools
import os
import sys
import time
from collections import Counter
import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyts.transformation import PAA, SAX, StandardScaler
from pyts.visualization import plot_paa, plot_sax, plot_ts
filtrain = None

#------------------------------------------------------- load_ui ---------------------------------------------------------------#


def load_ui(file_name, where=None):

    loader = QtUiTools.QUiLoader()  # Create a QtLoader

    ui_file = QtCore.QFile(file_name)   # Open the UI file
    ui_file.open(QtCore.QFile.ReadOnly)

    ui = loader.load(ui_file, where)  # Load the contents of the file

    ui_file.close()  # Close the file

    return ui

    #------------------------------------------------------- Main Class ------------------------------------------------------------#
file_array = []
file_array_bis = []
X_standardized = 0
X_paa = 0
X_sax = 0
val = 0
car=0
a=0
b=0
c=0
level1 = []


character_tab = ['a', 'b', 'c', 'd', 'e', 'f',
                 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p']


class MainClass(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUI()

    def setupUI(self):

     # Set up the user interface from Designer.
        ui_file_path = os.path.join(os.path.realpath(
            os.path.dirname(__file__)), 'mainwindow.ui')
        main_widget = load_ui(ui_file_path, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setGeometry(300, 100, 850, 550)
        self.setLayout(layout)
        
        
        self.browse = self.findChild(QtGui.QPushButton, 'browse')
        self.browse.clicked.connect(self.BrowseFunction)

        self.Standaris = self.findChild(QtGui.QPushButton, 'Standaris')
        self.Standaris.clicked.connect(self.stand)

        self.paa = self.findChild(QtGui.QPushButton, 'paa')
        self.paa.clicked.connect(self.PAA)

        self.sax = self.findChild(QtGui.QPushButton, 'sax')
        self.sax.clicked.connect(self.SAX)

        self.vis_stand = self.findChild(QtGui.QPushButton, 'vis_stand')
        self.vis_stand.clicked.connect(self.visstand)

        self.vis_paa = self.findChild(QtGui.QPushButton, 'vis_paa')
        self.vis_paa.clicked.connect(self.visPAA)

        self.vis_sax = self.findChild(QtGui.QPushButton, 'vis_sax')
        self.vis_sax.clicked.connect(self.visSAX)

        self.resultat = self.findChild(QtGui.QPushButton, 'resultat')
        self.resultat.clicked.connect(self.apriori)

        self.browseline = self.findChild(QtGui.QLineEdit, 'browseline')
        self.nbpaa = self.findChild(QtGui.QLineEdit, 'nbpaa')
        self.nbsax = self.findChild(QtGui.QLineEdit, 'nbsax')
        self.nbstandar = self.findChild(QtGui.QLineEdit, 'nbstandar')
        self.paaline = self.findChild(QtGui.QLineEdit, 'paaline')
        self.saxline = self.findChild(QtGui.QLineEdit, 'saxline')
        self.aprioriline = self.findChild(QtGui.QLineEdit, 'aprioriline')

    #------------------------------------------------------ Paths: Train, Test and Save ---------------------------------------------#

    def BrowseFunction(self):

        global file_array
        matrix_array = []
        handle, filter = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                           'E:\Robot data', "files (*.txt)")
        if handle:
            self.browseline.setText(handle)
        filtrain = self.browseline.text()

        if handle == 'E:/Robot data/lp1.data.txt':
            with open(handle, 'r') as UseFile:

                for line in UseFile:

                    # if is a matrix description line
                    if line == 'normal\n'or line == 'collision\n' or line == 'obstruction\n' or line == 'fr_collision\n':
                        # add a array in file array

                        file_array.append(matrix_array)
                        matrix_array = []

                        matrix_array.append(line[0:-1])

                    elif line == "\n":
                        pass

                    # if is a matrix row
                    else:
                        tab = line.split('\t')
                        matrix_array.append(int(tab[3]))

                file_array_bis = []
                global X_standardized
                global X_paa
                global X_sax

                for arr in file_array:
                    file_array_bis.append(arr[1:])

                file_array_bis = file_array_bis[1:]

                X = np.array(file_array_bis)
                standardscaler = StandardScaler(epsilon=1e-2)
                X_standardized = standardscaler.transform(X)

        else:
            print 13

# standarisation
    # def stand(self):
    # 		print X_standardized
    # 		a= self.nbstandar.text()
    def stand(self):
        global val
       
        nbs = self.nbstandar.text()
        try:
            val = int(nbs)
            print X_standardized[val]
        except ValueError:
           QMessageBox.warning(None, 'Warning', 'Please Enter an integer',
            QMessageBox.Ok)
        
            # QMessageBox.Warning(None, 'ERROR', 'Installation complete.')
           

    def visstand(self):
        
       
            plt.show(
                plt.plot(X_standardized[val], color="red", linewidth=1.0, linestyle="-"))
      

# PAA
    def PAA(self):
        global X_paa
        global b
        global a
        a = int(self.paaline.text())
        b = int(self.nbpaa.text())
        paa = PAA(window_size=None, output_size=a, overlapping=True)
        X_paa = paa.transform(X_standardized)
        print X_paa[b]
        print "************************"

    def visPAA(self):
        plt.show(plot_paa(
            X_standardized[b], window_size=None, output_size=a, overlapping=True, marker='o'))
# SAX

    def SAX(self):
        global X_sax
        global car
        global b
        car = int(self.saxline.text())
        c = int(self.nbsax.text())
        sax = SAX(n_bins=car, quantiles='gaussian')
        X_sax = sax.transform(X_paa)
        print X_sax[c]
        print "******************"

    def visSAX(self):
        plt.show(plot_sax(X_paa[c], n_bins=4, quantiles='gaussian'))
    """
	Main code of apriori 
	"""

    def merge_key(self, dico, level1):
        new_dico = dict()
        tab = []
        for key in dico:
            tab.append(key)

        for i in range(len(tab)):
            for j in range(len(level1)):
                new_dico[tab[i] + level1[j]] = 0

        return new_dico

    def car_counting(self, x_sax, dico):
        for line in x_sax:
            for key in dico:
                counter = line.count(key)
                dico[key] += counter

    def minimum_support(self, dico, min_sup):
        for key in dico.keys():
            if dico[key] < min_sup:
                dico.pop(key)
    # apriori

    def apriori(self):
        global car
        car_dic = dict()

        
        for i in range(car):
            car_dic[character_tab[i]] = 0
            level1.append(character_tab[i])
        # car_dic = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}
        # level1 = ['a', 'b', 'c', 'd', 'e']

        min_support = float(self.aprioriline.text())
        a_priory_tab = {}
        ########### GEN ###########
        level_dict = dict()
        while True:
                                # 1 - count
            self.car_counting(X_sax, car_dic)
            # print(car_dic)
            # 2 - occurence dividing
            for key in car_dic:
                level_dict[key] = car_dic[key]/88.0
            print(level_dict)
            # 3 - minimum support deleting
            a_priory_tab = copy.deepcopy(level_dict)
            self.minimum_support(level_dict, min_support)
            print "*****************************************"
            # print(level_dict)

            if len(level_dict) <= 0:
                break
            else:
                # 4 - merge
                car_dic = self.merge_key(level_dict, level1)
                print(level_dict)
                level_dict = {}

        # Printing the last element
        print('The last tab \n')
        print(a_priory_tab)

#-------------------------------------------------------------------------------------------------------------------------------#


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainClass()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
