import mysql.connector
import json
from contextlib import closing
from PyQt5.QtWidgets import QMessageBox


def connect_mysql():
    # dev = 0
    # live = 1
    stage = 1
    
    with open('data/config.json', 'r') as f:
        config = json.load(f)

    conn = mysql.connector.connect(user=config['user'], password=config['password'], host=config['host'],
                                   database=config['database'][stage], raise_on_warnings=True)
    
    return conn 


def get_companies():
    con = connect_mysql()
    cur = con.cursor()
    
    with closing(cur) as db:
        db.callproc('get_companies')
        for result in db.stored_results():
            results = result.fetchall()
    
    lst_companies = []
    for company in results:
        lst_companies.append(company)
    
    return lst_companies


def get_sku_names(company_id):
    con = connect_mysql()
    cur = con.cursor()
    lst_results = []
    
    with closing(cur) as db:
        db.callproc('get_skus_names', [company_id])
        for result in db.stored_results():
            results = result.fetchall()
        
    for result in results:
        lst_results.append(result[0]) 
    return lst_results 


def get_sku_info(sku, company_id):
    con = connect_mysql()
    cur = con.cursor()
    
    with closing(cur) as db:
        db.callproc('get_sku_info', [sku, company_id])
        for result in db.stored_results():
            return result.fetchall()


def get_available_sizes_per_garm_color(garm_color):
    con = connect_mysql()
    cur = con.cursor()
    lst_results = []
    
    with closing(cur) as db:
        db.callproc('get_available_sizes_per_garm_color', [garm_color])
        for result in db.stored_results():
            results = result.fetchall()
            
    for result in results:
        lst_results.append(result[0])
        
    return lst_results

        
def throw_db_error(error):
    ErrorMessage(error)
    
    
class ErrorMessage(QMessageBox):
    def __init__(self, error):
        super(ErrorMessage, self).__init__()
        QMessageBox.critical(self, 'A database error has occured.', str(error))

