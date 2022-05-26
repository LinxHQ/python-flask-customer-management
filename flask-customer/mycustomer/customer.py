from werkzeug.exceptions import abort

# import các mod cần thiết cho 1 blueprint cơ bản:
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# import hàm get_db từ module db mà chúng ta đã viết ở bài trước. Hàm này phục vụ cho việc truy vấn CSDL.
from mycustomer.db import get_db

# tạo blueprint cho module customer
bp = Blueprint('customer', __name__, url_prefix='/customer')

# trước hết khai báo route để truy nhập chức năng này là "customer/create". Nhưng vì chúng ta đã khai báo prefix cho blueprint customer là "/customer" trong __init__.py, nên tại đây chỉ cần dùng "/create".
# method cho phép user submit để gọi route là cả GET và POST. Thực tế trong ví dụ đơn giản này, dùng POST thôi cũng là đủ 
@bp.route('/create', methods=('GET', 'POST'))
def create():
    # nếu form đã submit qua POST, kiểm tra các trường bắt buộc và insert vào cơ sở dữ liệu nếu hợp lệ.
    if request.method == 'POST':
        customer_name = request.form['name']
        customer_email = request.form['email']
        error = None

        if not customer_name:
            error = 'Customer Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.execute(
                'INSERT INTO customer (name, email)'
                ' VALUES (?, ?)',
                (customer_name, customer_email)
            )
            db.commit()
            return redirect(url_for('customer.view', id=cur.lastrowid))

    return render_template('customer/create.html')

@bp.route('/<int:id>', methods=('GET',))
def view(id):
    customer = get_db().execute(
        'SELECT * FROM customer'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if customer is None:
        abort(404, f"customer id {id} doesn't exist.")

    return render_template('customer/view.html', customer=customer)

# route index, duoc truy cap qua path "customer/"
@bp.route('/', methods=('GET', 'POST'))
def index():
    customer_list = get_db().execute(
        'SELECT * FROM customer'
    ).fetchall()

    return render_template('customer/index.html', customer_list=customer_list)