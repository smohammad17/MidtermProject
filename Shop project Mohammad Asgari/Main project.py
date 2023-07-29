import tkinter
import sqlite3
import productAction                   


#==============  Functions   ===============

# --------------------   login function   --------------------
def login():
    global session, login_user, login_cnt
    user =txt_user.get ()
    pas=txt_pas.get ()
    
    sql=''' SELECT * FROM users WHERE username=? AND pass=?'''

    result=cnt.execute (sql, (user,pas) )
    result2=result.fetchall ()

    if len (result2)<1:
        lbl_msg.configure (text="wrong username or password ", fg="red")
        login_cnt+=1
        if login_cnt==3:
            btn_login.configure (state="disabled")
            lbl_msg.configure (text="3 failed login attempts, please restart the program", fg="red")
    else:
        lbl_msg.configure (text="welcome to your account "+user, fg="green")
        txt_user.delete (0, "end")
        txt_pas.delete (0, "end")
        btn_login.configure (state="disabled")
        btn_shop.configure (state="active")
        btn_mycart.configure (state="active")
        btn_logout.configure (state="active")        
        session=result2 [0][0]
        login_user=user
        login_cnt=0
        if login_user=="admin":
            btn_admin.configure (state="active")

# --------------------   submit panel   --------------------
def submit ():
    def register():
        user=txt_user.get ()
        pas=txt_pas.get ()
        cpas=txt_cpas.get ()
        addr=txt_addr.get ()

        result, errorMSG=validation (user, pas, cpas, addr)
        
        if result==True:                        
            sql='''INSERT INTO users (username, pass, addr, grade)
                    VALUES (?, ?, ?, ?)'''
            cnt.execute (sql, (user, pas, addr, 5))
            cnt.commit ()
            
            lbl_msg.configure (text="account created successfully", fg="green")
            txt_user.delete (0, "end")
            txt_pas.delete (0, "end")
            txt_cpas.delete (0, "end")
            txt_addr.delete (0, "end")
            
        else:
            lbl_msg.configure (text=errorMSG, fg="red")
    
            
    win_submit=tkinter.Toplevel()  
    win_submit.title("Submit Panel")
    win_submit.geometry("400x500")
    
    lbl_user=tkinter.Label(win_submit,text="Username: ")
    lbl_user.pack()
    txt_user=tkinter.Entry(win_submit)
    txt_user.pack()

    lbl_pas=tkinter.Label(win_submit,text="Password: ")
    lbl_pas.pack()
    txt_pas=tkinter.Entry(win_submit)
    txt_pas.pack()

    lbl_cpas=tkinter.Label(win_submit,text="Password confirmation: ")
    lbl_cpas.pack()
    txt_cpas=tkinter.Entry(win_submit)
    txt_cpas.pack()
    
    lbl_addr=tkinter.Label(win_submit,text="Address: ")
    lbl_addr.pack()
    txt_addr=tkinter.Entry(win_submit)
    txt_addr.pack()
    
    lbl_msg=tkinter.Label(win_submit,text="")
    lbl_msg.pack()
    
    btn_register=tkinter.Button(win_submit,text="Register", command=register)
    btn_register.pack()
    
# --------------------   validation function (for submit)   --------------------
def validation (user, pas, cpas, addr):
    
    if user=="" or pas=="" or addr=="":
        return False, "please fill all fields"
    
    if len(pas)<8:
        return False, "password is too short"

    if pas != cpas:
        return False, "password and confirmation don't match"
    
    sql=''' SELECT * FROM users WHERE username=? '''

    result=cnt.execute (sql, (user,) )
    result2=result.fetchall ()
    if len (result2) != 0:
        return False, "username already exists"
    
    return True, " "


# --------------------   logout function   --------------------
def logout():                                   
    global session, login_user
    
    session=False
    login_user=False
    btn_login.configure (state="active")
    btn_shop.configure (state="disabled")
    btn_mycart.configure (state="disabled")
    btn_admin.configure (state="disabled")
    btn_logout.configure (state="disabled")
    lbl_msg.configure (text="You have logged out successfully", fg="blue")
        

# --------------------   shop panel   --------------------
def shop():
    def buy():
        global session
        pid=txt_id.get()
        qnt=txt_qnt.get()
        
        result, msg=productAction.buyValidate(pid, qnt)
        
        if not result:
            lbl_msg.configure (text=msg, fg="red")
            return

        productAction.savetocart (session, pid, qnt)
        lbl_msg.configure (text="saved to cart", fg="green")
        txt_id.delete (0, "end")
        txt_qnt.delete (0, "end")
        
        productAction.updateqnt (pid, qnt)
        
        lstbx.delete (0, "end")
        products=productAction.getAllProducts ()
        for product in products:
            text="id:{},    Name:{},    Price:{},    Quantity:{}".format (product[0], product[1], product[2], product[3])
            lstbx.insert ("end", text)
        
   
    win_shop=tkinter.Toplevel (win)
    win_shop.geometry ("500x500")
    win_shop.title ("Shop Panel")

    lstbx=tkinter.Listbox (win_shop, width=65, bg="black", fg="yellow")                 
    lstbx.pack()

    products=productAction.getAllProducts()
    for product in products:
        text="id:{},   Name:{},    Price:{},    Quantity:{}   ".format (product [0], product [1], product [2], product [3])
        lstbx.insert ("end", text)

    lbl_id=tkinter.Label (win_shop, text="product id: ")
    lbl_id.pack()
    txt_id=tkinter.Entry (win_shop)
    txt_id.pack()

    lbl_qnt=tkinter.Label (win_shop, text="quantity: ")
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry (win_shop)
    txt_qnt.pack()

    lbl_msg=tkinter.Label (win_shop, text="")
    lbl_msg.pack()

    btn_buy=tkinter.Button(win_shop, text="Buy", command=buy)
    btn_buy.pack()


    win_shop.mainloop ()

# --------------------   cart panel   --------------------
def mycart():
    global session

    win_cart=tkinter.Toplevel (win)
    win_cart.geometry ("500x500")
    win_cart.title ("cart panel")

    lbl_user=tkinter.Label (win_cart, text="{}'s cart: ".format(login_user), width=65 )
    lbl_user.pack()

    lstbx=tkinter.Listbox (win_cart, width=75, fg="blue")
    lstbx.pack()

    result=productAction.showMyCart (session)

    for product in result:
        Tprice= product [1] * product [2]
        text="Product:{},   Quantity:{},   Price per item:{},   Total Price:{}".format (product[0], product[1], product[2], Tprice)
        lstbx.insert ("end", text)
    
    win_cart.mainloop ()

# --------------------   admin panel    --------------------
def adminPanel():
    def save ():
        pname=txt_name.get ()
        price=txt_price.get ()
        qnt=txt_qnt.get ()

        result, errorMSG=productAction.saveValidation (pname, price, qnt)

        if not result:
            lbl_msg.configure (text=errorMSG, fg="red")
            return

        productAction.add2Products (pname, price, qnt)
        txt_name.delete (0, "end")
        txt_price.delete (0, "end")
        txt_qnt.delete (0,"end")
        lbl_msg.configure (text="product has been added successfully", fg="green")
        
    
    win_admin=tkinter.Toplevel (win)
    win_admin.geometry ("300x400")
    win_admin.title ("Admin Panel")

    lbl_name=tkinter.Label (win_admin, text="Product Name: ")
    lbl_name.pack ()
    txt_name=tkinter.Entry (win_admin)
    txt_name.pack ()

    lbl_price=tkinter.Label (win_admin, text="Price: ")
    lbl_price.pack ()
    txt_price=tkinter.Entry (win_admin)
    txt_price.pack ()

    lbl_qnt=tkinter.Label (win_admin, text="Quantity: ")
    lbl_qnt.pack ()
    txt_qnt=tkinter.Entry (win_admin)
    txt_qnt.pack ()

    lbl_msg=tkinter.Label (win_admin, text="")
    lbl_msg.pack ()

    btn_save=tkinter.Button (win_admin, text="Save", command=save)
    btn_save.pack()


    win_admin.mainloop ()



#===============   MAIN   ===============
session=False
login_user=False
login_cnt=0

cnt=sqlite3.connect ("store.db")

win=tkinter.Tk()
win.title("SHOP PROJECT")
win.geometry("500x600")

lbl_user=tkinter.Label(win,text="Username: ")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pas=tkinter.Label(win,text="Password: ")
lbl_pas.pack()
txt_pas=tkinter.Entry(win)
txt_pas.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

btn_login=tkinter.Button(win,text="Login",command=login)
btn_login.pack()

btn_submit= tkinter.Button (win, text="Submit", command=submit)
btn_submit.pack ()

btn_shop=tkinter.Button (win, text="SHOP", state="disabled", command=shop)
btn_shop.pack()

btn_mycart=tkinter.Button (win, text="My cart", state="disabled", command=mycart)
btn_mycart.pack()

btn_admin=tkinter.Button (win, text="Admin panel", state="disabled", command=adminPanel)
btn_admin.pack()

btn_logout=tkinter.Button (win, text="Log out", state="disabled", command=logout)
btn_logout.pack()


win.mainloop()





















