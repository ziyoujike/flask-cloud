from flask import Flask
import settings
from extend import mail, db
from flask_migrate import Migrate

from apps import *

app = Flask(__name__)
# 配置文件
app.config.from_object(settings)
# 把app绑定在db上
db.init_app(app)
# 把app绑定在mial上
mail.init_app(app)

app.register_blueprint(common)
app.register_blueprint(resources)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
