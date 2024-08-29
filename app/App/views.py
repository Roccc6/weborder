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
    #首先检查用户是否登录
    if 'username' not in session:
        return redirect(url_for('bp.home'))
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
    sql = "SELECT Product.ProductID, ProductName,ShippingWeight, Price, Description, ImagePath FROM ProductDetails JOIN Product ON ProductDetails.ProductID = Product.ProductID WHERE Product.ProductID = %s"
    cur.execute(sql, (product_id,))
    details = cur.fetchone()
    details['ImagePath'] = '../static' + details['ImagePath']
    cur.close()
    print(details)
    return render_template('details.html', details=details)
    
    
    
@bp.route('/basket')
def basket():
    user = session.get('username')
    cur = mysql.connection.cursor()
    # 查询user购物车中的商品
    sql = '''select product.ProductID,ProductName,ShippingWeight, Price, ImagePath, Quantity
    from useraccount join shoppingbasket on useraccount.UserID = shoppingbasket.UserID 
    join product on shoppingbasket.ProductID = product.ProductID 
    join productdetails on product.ProductID = productdetails.ProductID
    where username = %s
    '''
    cur.execute(sql, (user,))
    products = cur.fetchall()
    for product in products:
        product['ImagePath'] = '../static' + product['ImagePath']
        
    total = sum(item['Price'] * item['Quantity'] for item in products)
    total_weight = sum(item['ShippingWeight'] * item['Quantity'] for item in products)
    return render_template('basket.html',cart=products, total=total,wholeweight=total_weight)



@bp.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    try:
        user = session.get('username')
        #前端通过fetch发送数据到后端，后端通过request.json获取数据
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        if not all([product_id, quantity]):
            return jsonify({'status': 'error', 'message': '参数不完整'}), 400
        cur = mysql.connection.cursor()
        #检查是否存在该产品
        sql = "select * from product where ProductID = %s"
        cur.execute(sql, (product_id,))
        product = cur.fetchone()
        if not product:
            return jsonify({'status': 'error', 'message': '商品不存在'}), 400
        # 查询用户购物车中是否已经有该商品
        sql = '''select * from useraccount join shoppingbasket on useraccount.UserID = shoppingbasket.UserID 
        where username = %s and productID = %s
        '''
        cur.execute(sql, (user, product_id))
        product = cur.fetchone()
        # 如果购物车中已经有该商品，则更新数量
        if product:
            sql = '''update shoppingbasket set quantity = quantity + %s 
            where UserID = (select UserID from useraccount where username = %s) and ProductID = %s
            '''
            cur.execute(sql, (quantity, user, product_id))
            return jsonify({'status': 'success', 'message': '商品数量已更新'}), 200
            
        # 如果购物车中没有该商品，则插入新的记录
        else:
            sql = '''insert into shoppingbasket (UserID, ProductID, Quantity)
            values ((select UserID from useraccount where username = %s), %s, %s)
            '''
            cur.execute(sql, (user, product_id, quantity))
            return jsonify({'status': 'success', 'message': '商品已成功添加到购物车'}), 200
    except:
        return jsonify({'msg': 'error'})
    
    
@bp.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    try:
        user = session.get('username')
        data = request.json
        removearr = data.get('product_id')
        cur = mysql.connection.cursor()
        sql = '''delete from shoppingbasket where UserID = (select UserID from useraccount where username = %s) and ProductID = %s
        '''
        for product_id in removearr:
            cur.execute(sql, (user, product_id))
        
        return jsonify({'status': 'success', 'message': '商品已成功从购物车移除'}), 200
        
    except:
        return jsonify({'msg': 'error'})
    
    
@bp.route('/checkout', methods=['POST'])
def checkout():
    pass

    
