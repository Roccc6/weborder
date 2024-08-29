from flask import Blueprint, jsonify, make_response, render_template, request, redirect, url_for,session

from .import mysql

#创建蓝图
bp = Blueprint('bp', __name__)


@bp.route('/')
def home():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    #从数据库中查询是否有该用户
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM useraccount where username=%s and password=%s", (username, password))
    users = cur.fetchall()
    if users:
        session['username'] = username  # 在 session 中存储用户名
        return redirect(url_for('bp.index'))
    else:
        return render_template('login.html', error_msg='用户名或密码错误')
    
@bp.route('/logout')
def logout():
    session.clear()  # 清除用户的session数据，登出用户
    return redirect(url_for('bp.home'))  # 登出后重定向到首页 


  
@bp.route('/index')
def index():
    cur = mysql.connection.cursor()
    sql = "SELECT Product.ProductID, ProductName, Price, ImagePath FROM ProductDetails JOIN Product ON ProductDetails.ProductID = Product.ProductID"
    cur.execute(sql)
    products = cur.fetchall()
    for product in products:
        product['ImagePath'] = '../static' + product['ImagePath']
        
    cur.close()
    return render_template('index.html',products=products)



@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    cur = mysql.connection.cursor()
    sql = "SELECT Product.ProductID, ProductName,Shippingweight, Price, Description, ImagePath FROM ProductDetails JOIN Product ON ProductDetails.ProductID = Product.ProductID WHERE Product.ProductID = %s"
    cur.execute(sql, (product_id,))
    details = cur.fetchone()
    details['ImagePath'] = '../static' + details['ImagePath']
    cur.close()
    print(details)
    return render_template('details.html', details=details)
    