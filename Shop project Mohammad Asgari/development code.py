import sqlite3

cnt=sqlite3.connect("store.db")

# ---------------create products table-----------
# sql=''' CREATE TABLE products(
#         id INTEGER PRIMARY KEY,
#         pname CHAR(30) NOT NULL,
#         price INTEGER NOT NULL,
#         qnt INTEGER NOT NULL
#         )'''
# cnt.execute(sql)

# ------------------ insert data into products------------

##sql=''' INSERT INTO products(pname,price,qnt)
##        VALUES ("BMW X5",9500,5)'''
##
##cnt.execute(sql)
##cnt.commit()


#------------------create cart table-----------------------

##sql=''' CREATE TABLE cart (
##id INTEGER PRIMARY KEY,
##uid INTEGER NOT NULL,
##pid INTEGER NOT NULL,
##qnt INTEGER NOT NULL
##)'''
##cnt.execute (sql)






