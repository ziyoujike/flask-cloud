from flask import Flask
import settings

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置文件
app.config.from_object(settings)

from sqlalchemy import create_engine

# 数据库的配置变量
HOSTNAME = 'rm-uf6w8th6if60vb548uo.mysql.rds.aliyuncs.com'
PORT = '3306'
DATABASE = 'cloud-pro'
USERNAME = 'pxtk'
PASSWORD = 'eer#$89000rtynp'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

# 创建数据库引擎
# engine = create_engine(DB_URI)
db = SQLAlchemy(app)


# 创建ORM模型

class User(db.Model):
    __tablename__ = 'db_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
db.create_all()

@app.route('/')
def hello_world():  # put application's code here

    engine = db.get_engine()
    with engine.connect() as conn:
        rest = conn.execute("select 1")
        print(rest.fetchone())
        return {"message": "成功"}


if __name__ == '__main__':
    app.run()
