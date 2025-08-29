import streamlit as st
import time
import mysql.connector
import datetime
from streamlit_option_menu import option_menu

con=mysql.connector.connect(host="localhost",user="root",password="Karthi1104",database="ecommerce_online")
res = con.cursor()

st.set_page_config(page_title="NextGen System", page_icon="💻", layout="wide")

with st.sidebar:
    st.sidebar.image("logo1.png") 
    rad= option_menu(
        menu_title= "NextGen System",
        options=["Home","Register","Login","Store","My Orders","About us"],
        icons=["house", "person-plus", "box-arrow-in-right", "bag", "cart", "info-circle"],
        menu_icon="cast",  
        default_index=0,)
     


if rad=="Home":
    st.title("Welcome to NextGen System⭐")
    st.subheader("Your One-Stop Destination for Computer Hardware")
    
    col1,col2= st.columns(2)
    with col1:
        st.subheader("Latest Arrivals") 
        st.markdown("Cutting-edge processors, high-speed RAM, and next-gen SSDs. Stay ahead with the newest tech for gamers, developers, and creators.")
        st.subheader("Best Sellers") 
        st.markdown("Trusted hardware chosen by thousands of customers. From NVIDIA & AMD graphics cards to Intel & AMD CPUs.")
        st.subheader("Build Your Dream PC")
        st.markdown("Pick your CPU, GPU, motherboard, storage, and more. Get expert recommendations for compatibility.")
        st.write("👉 Start browsing our products today and take your computing experience to the next level!")
    with col2:
        st.image("hardware.png",caption='Image caption')
        
    st.header("Customer Reviews")
    st.subheader("What our customers are saying")
    st.write("⭐⭐⭐⭐⭐ - 'I love this store! Great products and fast shipping.'")
    st.write("⭐⭐⭐⭐ - 'Good quality products at affordable prices.'")
    st.write("⭐⭐⭐⭐⭐ - 'Excellent customer service and a wide selection of items.'")
    
    st.markdown("---")
    st.markdown("2025 My Online Store. All rights reserved.")
        
        
if rad == "Register":
    st.title("💻 NextGen System")
    st.subheader("Create Account")
    first,last=st.columns(2)
    first_name=first.text_input("Name")
    last_name = last.text_input("last")

    mail,no = st.columns([3,1])
    mail_id = mail.text_input("Mail Id")
    number = no.text_input("Number")

    us,pw,pw1 = st.columns(3)
    user_name=us.text_input("User name")
    password = pw.text_input("Password",type="password")
    password_re = pw1.text_input("Re-Enter Password",type="password")
    if password!=password_re:
        st.warning("password mismatch")
    
    if  st.checkbox("I agree"):
        if st.button("Submit"):
                qry = "insert into customer values (%s,%s,%s,%s,%s,%s)"
                val=(first_name,last_name,mail_id,number,user_name,password_re)
                res.execute(qry,val)
                con.commit()
                p=st.progress(20)
                for i in range(1,100):
                    time.sleep(0.1)
                    p.progress(i+1)
                st.balloons()
                st.info("Register succesfully")
                
if rad == "Login":
    st.title("💻 NextGen System")
    user = st.text_input("Enter your username")
    pass_key = st.text_input("Enter the password",type="password")
    bt = st.button("Login")
    if bt==True:
        user_name_list =[]
        qry = "select user_name from customer"
        res.execute(qry)
        data=res.fetchall()
        for i in data:
            user_name_list.append(i[0])
    
        if user in user_name_list:
        
            qry = "select password from customer where user_name = %s"
            val = (user,)
            res.execute(qry,val)
            key = res.fetchall()[0][0]
            if key == pass_key:
                st.session_state["user"] = user
                st.info("login succesfully")
            else:
                st.error("incorrect password")
        else:
            st.error("Invalid username")


if rad=='Store':
    st.title("💻 NextGen System")
    if 'user' not in st.session_state:
        st.warning('please login first')
    else:
        st.subheader('Our Products')
        res.execute("select id,name,price,stock from products")
        products = res.fetchall()
        
        cols= st.columns(2)
        for idx,prod in enumerate(products):
            col=cols[idx%2]
            with col:
                st.markdown(f"**{prod[1]}**")
                st.write(f"₹{prod[2]}| stock:{prod[3]}")
                qty = st.number_input(f"Qty_{prod[0]}",1,5,1,key=f"qty{prod[0]}")
                if st.button("Order" ,key=f"order{prod[0]} "):
                    if prod[3] >= qty:
                        res.execute("INSERT INTO orders(user_name,product_id,quantity,order_date,status)values(%s,%s,%s,%s,%s)",
                                    (st.session_state['user'],prod[3],qty,datetime.datetime.now(),"Placed"))
                        res.execute("update products set stock=stock-%s where id=%s",(qty,prod[3]))
                        con.commit()
                        st.success(f"order{qty} x{prod[1]}")
                    else:
                        st.error("Not enough stock")

if rad=="My Orders":
    st.title("My Orders")
    if "user" not in st.session_state:
        st.warning("Please login")
    
    else:
        st.subheader("My orders")
        qry = """SELECT o.id,p.name,o.quantity,o.status,o.order_date
                 FROM orders o JOIN products p ON o.product_id=p.id
                 WHERE o.user_name=%s"""
        res.execute(qry,(st.session_state['user'],))
        orders = res.fetchall()
        if not orders:
            st.info("No order yet")
        
        else:
            for oid,pname,qty,status,odate in orders:
                status_color = {"Placed": "🟢","Cancelled": "🔴","Shipped": "📦","Delivered": "✅"}
                st.markdown(f"**{pname}** | Qty: {qty} | Status: {status} | Date: {odate}")
                if status=="Placed":
                    if st.button(f"Cancel {oid}", key=f"cancel{oid}"):
                        res.execute("UPDATE orders SET status='Cancelled' WHERE id=%s",(oid,))
                        con.commit()
                        st.warning("Order Cancelled")

if rad=="About us":
    st.title("💻 About NextGen System")
    # st.image("team.jpg", use_column_width=True)
    st.write("""
        Welcome to **NextGen System** – your trusted partner for premium system hardware.  
        🖥️ From CPUs to GPUs, RAM, and SSDs, we bring you the latest components.  
        🚀 Fast shipping | 🔒 Secure Payments | 📞 24/7 Support
    """)
