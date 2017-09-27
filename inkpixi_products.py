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
        
        self.cbox_company.addItems(self.get_companies())
        self.cbox_company.currentIndexChanged.connect(self.cbox_company_changed)
        
        
        self.btn_test.clicked.connect(self.btn_test_clicked)
        
    def get_companies(self):
        lst_companies = ip_data.get_companies()

        lst_company_name = []
        for company in lst_companies:
            lst_company_name.append(company[1])
        
        return lst_company_name
    
    def cbox_company_changed(self):
        try:
            company = Company(self.cbox_company.currentText())
    
            self.sku_completer(company.company_id)
            
            if company.company_id == 2:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/retail_logo.png"))
            elif company.company_id == 3:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/wholesale_logo.png"))
            else:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/pixi_logo_new.png"))
        except BaseException:
            QMessageBox.information(self, 'Chose Company', 'Please choose a valid company.')
        
    def sku_completer(self, company_id):
        
        root_skus = ip_data.get_sku_names(company_id)
        
        #set up an auto complete for the sku line edit box
        rsku_completer = QCompleter(root_skus)
        rsku_completer.setCompletionMode(QCompleter.InlineCompletion)
        rsku_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        rsku_completer.setCaseSensitivity(Qt.CaseInsensitive)       
        
        self.le_sku.setCompleter(rsku_completer) 

    def btn_test_clicked(self):
        try:
            print(ip_data.get_sku_names(self.company_id))
        except BaseException as e:
            print(e)

class Company(object):
    #this class sets the company name and ID for the application
    def __init__(self, company_name):
        self.company_name = company_name
        self.company_id = self.get_company_id(company_name) 

    def get_company_id(self, company_name):
        #get a list of the companies from the database for reference
        self.lst_companies = ip_data.get_companies()
        #based on the text of the company name sent loop through the list to determine id and Name
        for company in self.lst_companies:
            if company_name == company[1]:
                company_id = company[0]
        return company_id
    

if __name__ == '__main__':
    myappid = 'InkPixi Products'
    #Windows 7 or x64 only
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) 
        
    app = QApplication(sys.argv)
    ip = InkPixiProducts()
    ip.show()
    
    sys.exit(app.exec_())
    
