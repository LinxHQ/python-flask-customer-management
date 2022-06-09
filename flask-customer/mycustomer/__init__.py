import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

def create_app(test_config=None):
    # tạo app 
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    datepicker(app)
    
    app.config.from_mapping(
        SECRET_KEY='my-secret-key',
        DATABASE=os.path.join(app.instance_path, 'mycustomer.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Mội đường url cở bản để test app mới của chúng ta. Nội dung trả về là "Xin chào!"
    @app.route('/hi')
    def hello():
        return 'Xin chào!'

    from . import db
    db.init_app(app)

    from . import customer
    app.register_blueprint(customer.bp)

    from . import invoice 
    app.register_blueprint(invoice.bp)

    return app
