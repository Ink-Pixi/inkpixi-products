import sys
import ctypes
from data import inkpixi_products_data as ip_data
from ui.main import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
class InkPixiProducts(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(InkPixiProducts, self).__init__()
        
        
        self.setupUi(self)
        
        self.get_companies()
        self.cbox_company.currentIndexChanged.connect(self.cbox_company_changed)
        
        
        self.btn_test.clicked.connect(self.btn_test_clicked)
        
    def get_companies(self):
        lst_companies = ip_data.get_companies()
        
        for company in lst_companies:
            self.cbox_company.addItem(company[1], company[0])
    
    def cbox_company_changed(self):
        self.company = Company(self.cbox_company.currentText(), self.cbox_company.itemData(self.cbox_company.currentIndex()))

        try:
            self.sku_completer()
             
            if self.company.company_id == 2:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/retail_logo.png"))
            elif self.company.company_id == 3:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/wholesale_logo.png"))
            else:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/pixi_logo_new.png"))
        except BaseException:
            QMessageBox.information(self, 'Chose Company', 'Please choose a valid company.')
          
    def sku_completer(self):

        root_skus = ip_data.get_sku_names(self.company.company_id)
        
        #set up an auto complete for the sku line edit box
        rsku_completer = QCompleter(root_skus)
        rsku_completer.setCompletionMode(QCompleter.InlineCompletion)
        rsku_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        rsku_completer.setCaseSensitivity(Qt.CaseInsensitive)       
        
        self.le_sku.setCompleter(rsku_completer) 

    def btn_test_clicked(self):
        self.test_combo()
#         try:
#             print(ip_data.get_sku_names(self.company.company_id))
#         except BaseException as e:
#             print(e)
            
    
    def test_combo(self):
        self.cbox_company.addItem('test', 12)

class Company(object):
    #this class sets the company name and ID for the application
    def __init__(self, in_company_name, in_company_id):
        self.company_name = in_company_name
        self.company_id = in_company_id

if __name__ == '__main__':
    myappid = 'InkPixi Products'
    #Windows 7 or x64 only
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) 
        
    app = QApplication(sys.argv)
    ip = InkPixiProducts()
    ip.show()
    
    sys.exit(app.exec_())
    
