import sqlite3

cnt=sqlite3.connect ("store.db")

#-----------------------------------------------------------
def getAllProducts():
    sql=''' SELECT * FROM products '''
    result=cnt.execute (sql)
    result2=result.fetchall ()
    return result2


def buyValidate (pid, qnt):
    if pid=="" or qnt=="":
        return False, "please fill the inputs"

    if int(qnt)<=0:
        return False, "please enter a positive number"

    sql=''' SELECT * FROM products WHERE id=?'''
    result=cnt.execute (sql, (pid,))
    result2=result.fetchall ()                              
    if not result2:                                               
        return False, "wrong product id"

    sql=''' SELECT * FROM products WHERE id=? AND qnt>=? '''
    result=cnt.execute (sql, (pid, qnt))
    result2=result.fetchall ()                               
    if not result2:                                               
        return False, "not enough products!"

    return True, " "
    

def savetocart (uid, pid, qnt):
    sql=''' INSERT INTO cart (uid, pid, qnt)
    VALUES (?, ?, ?)'''
    cnt.execute (sql, (uid, pid, qnt))
    cnt.commit ()


def updateqnt (pid, qnt):
    sql=''' UPDATE products SET qnt=(qnt)-? WHERE id=? '''
    cnt.execute (sql, (qnt, pid))
    cnt.commit ()


def showMyCart (uid):
    sql=''' SELECT products.pname, cart.qnt, products.price
    FROM cart INNER JOIN products ON cart.pid=products.id
    WHERE cart.uid=?'''
    result=cnt.execute (sql, (uid,) )
    result2=result.fetchall()
    return result2


def saveValidation (pname, price, qnt):
    if pname=="" or price=="" or qnt=="":
        return False, "please fill all inputs"

    if int(price)<0 or int(qnt)<0:
        return False, "please enter positive values"

    return True, " "


def add2Products (pname, price, qnt):
    sql=''' INSERT INTO products (pname, price, qnt)
    VALUES (?, ?, ?)'''
    cnt.execute (sql, (pname, price, qnt) )
    cnt.commit ()








    
























