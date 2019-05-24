from Get_Quote_Data import *
from Generate_Graphs import *
from nsetools import Nse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton
from PyQt5.QtGui import QIcon


class App(QWidget):


    def __init__(self):
        super().__init__()
        self.title = 'Select a Stock'
        self.left = 200
        self.top = 200
        self.width = 200
        self.height = 200
        #self.move(-500,500)
        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.combo = QComboBox(self)
        nse = Nse()
        quoteCodeList = nse.get_index_list()
        #list_1 = ['Avengers']
        self.combo.move(0,60)
        self.combo.addItem("Select")
        self.combo.addItems(quoteCodeList)
        self.button = QPushButton("Ok", self)
        self.button.clicked.connect(self.save)
        self.button.move(0,100)
        self.show()

    def save(self):
        code = self.combo.currentText()
        #code = get_base_url(curr_val)
        print(code)
        new_table = get_page_content(Stock_Code)
        #print(type(new_table))
        get_graphs(Stock_Code)
        plt.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())