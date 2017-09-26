import sys
import ctypes
from data import inkpixi_products_data as ip_data
from ui.main import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter

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
        
    def btn_test_clicked(self):
        print(self.company_id)
        print(ip_data.get_sku_info('A101', self.company_id))

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
    
