import sys
import ctypes
from data import inkpixi_products_data as ip_data
from ui.main import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter
from PyQt5.QtCore import Qt

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
        company = Company()
        company.set_company(self.cbox_company.currentText())
        
        self.company_id = company.company_id
        
        self.sku_completer(self.company_id)
        
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
    def __init__(self):
        self.company_name = None
        self.company_id = None
        #get a list of the companies from the database for reference
        self.lst_companies = ip_data.get_companies()
    
    def company_name(self):
        return self.company_name
        
    def company_id(self):
        return self.company_id
            
    def set_company(self, in_company):
        #based on the text of the company name sent loop through the list to determine id and Name
        for company in self.lst_companies:
            if in_company == company[1]:
                self.company_name = company[1]
                self.company_id = company[0]
    

if __name__ == '__main__':
    myappid = 'InkPixi Products'
    #Windows 7 or x64 only
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) 
        
    app = QApplication(sys.argv)
    ip = InkPixiProducts()
    ip.show()
    
    sys.exit(app.exec_())
    
