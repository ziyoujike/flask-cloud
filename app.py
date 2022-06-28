from flask import Flask, session, g
import settings
from extend import mail, db, swagger
from flask_migrate import Migrate
from models.db_common import UserModel

from apps import *

app = Flask(__name__)
# 配置文件
app.config.from_object(settings)
# 把app绑定在db上
db.init_app(app)
# 把app绑定在mial上
mail.init_app(app)
# 绑定swagger
swagger.init_app(app)

app.register_blueprint(common)
app.register_blueprint(resources)
app.register_blueprint(message_board)

migrate = Migrate(app, db)


@app.before_request
def before_request():

    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            # 绑定全局变量
            g.user = user
    else:
        pass


if __name__ == '__main__':
    app.run()
