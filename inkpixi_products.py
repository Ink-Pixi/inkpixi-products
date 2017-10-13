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

        self.company = Company()
        self.setupUi(self)
        
        self.get_companies()
        self.cbox_company.currentIndexChanged.connect(self.cbox_company_changed)
        
        self.btn_test.clicked.connect(self.btn_test_clicked)
        
    def get_companies(self):
        lst_companies = get_companies()

        for company in lst_companies:
            self.cbox_company.addItem(company[1], company[0])

    def cbox_company_changed(self):
        self.company.set_company(self.cbox_company.currentText(),
                                 self.cbox_company.itemData(self.cbox_company.currentIndex()))
        # clear out current text
        self.le_search_sku.clear()

        try:
            if self.company.company_id == 2:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/retail_logo.png"))
            elif self.company.company_id == 3:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/wholesale_logo.png"))
            elif self.company.company_id == 1:
                self.lblLogo.setPixmap(QtGui.QPixmap(":/images/images/pixi_logo_new.png"))
            else:
                self.lblLogo.setPixmap(QtGui.QPixmap(""))
            
            self.sku_completer()
            
        except BaseException:
            QMessageBox.information(self, 'Chose Company', 'Please choose a valid company.')
          
    def sku_completer(self):
        if self.company.company_id:
            # grab skus information from comapny.
            root_skus = ip_data.get_sku_names(self.company.company_id)
            
            # set up an auto complete for the sku line edit box
            rsku_completer = QCompleter(root_skus)
            rsku_completer.setCompletionMode(QCompleter.InlineCompletion)
            rsku_completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            rsku_completer.setCaseSensitivity(Qt.CaseInsensitive)       
            
            self.le_search_sku.setCompleter(rsku_completer) 
        else:
            QMessageBox.information(self, 'Chose Company', 'Please choose a valid company.')

    def btn_test_clicked(self):
        if not self.company.company_id:
            QMessageBox.information(self, 'Chose Company', 'Please choose a valid company.')
            self.le_search_sku.clear()
        else:
            sku_text = self.le_search_sku.text().split('-')[0].strip()
            
            lst_sku_info = ip_data.get_sku_info(sku_text, self.company.company_id)

            self.le_root_sku.setText(lst_sku_info[0][0])
            self.le_root_sku_name.setText(lst_sku_info[0][1])
            self.le_root_color.setText(lst_sku_info[0][2])
            self.sbox_variables.setValue(lst_sku_info[0][3])
            self.le_variable_syntax.setText(lst_sku_info[0][4])
            self.chk_active.setChecked(lst_sku_info[0][5])
            

class Company(object):
    # this class sets the company name and ID for the application
    def __init__(self):
        self.company_name = None
        self.company_id = None
        
    def set_company(self, in_company_name, in_company_id):
        self.company_id = in_company_id
        self.company_name = in_company_name


def get_companies():
    lst_companies = ip_data.get_companies()
    return lst_companies


if __name__ == '__main__':
    my_app_id = 'Products'
    # Windows 7 or x64 only
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
        
    app = QApplication(sys.argv)
    ip = InkPixiProducts()
    ip.show()
    
    sys.exit(app.exec_())
