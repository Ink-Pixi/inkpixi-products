import mysql.connector
from contextlib import closing

def connect_mysql():
    conn = mysql.connector.connect(user = 'root', password = 'rowsby01', host = 'APPSERVER1', database = 'inkpixi_art', raise_on_warnings = True) 
   
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
            
    