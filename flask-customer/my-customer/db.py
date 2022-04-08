import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# 1. Lấy đối tượng sử dụng để kết nối với csdl: "db"
# Nếu đối tượng "db" đã tồn tại, thì sử dụng lại kết nối đó để truy vấn. Còn không, chúng ta tạo kết nối mới.
# 2. Biến "current_app" là đối tượng đại diện cho app hiện tại của chúng ta.
def get_db():
    if 'db' not in g:
        # kết nối với csdl mang tên config['DATABASE'] đã được chúng ta khai báo trong file __init__.py
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Đóng kết nối sau khi hoàn tất truy vấn
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# mở file schema.sql và chạy các dòng sql.
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# thêm command init-db 
@click.command('init-db') 
@with_appcontext
def init_db_command():
    """xóa data hiện tại nếu có và tạo bảng"""
    init_db()
    click.echo('Database setup successfully.') 

def init_app(app):
    # cho app biết cần gọi hàm close sau khi lấy xong data 
    app.teardown_appcontext(close_db)
    # cho app biết có thể dùng command init-db trên termina/console để khởi tạo csdl. Chúng ta sẽ chạy command này để tạo bảng.
    app.cli.add_command(init_db_command)