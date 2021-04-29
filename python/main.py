from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['SQL_USER'] + ':' + os.environ['SQL_PASSWORD'] +  '@' + os.environ['SQL_HOST'] +  ':' + os.environ['SQL_PORT'] +  '/' + os.environ['SQL_DB'] +  ''
db = SQLAlchemy(app)

port = 8000


###Models####
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255))
    mail = db.Column(db.VARCHAR(255))
    password = db.Column(db.VARCHAR(255))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, mail, password):
        self.name = name
        self.mail = mail
        self.password = password

    def __repr__(self):
        return '' % self.id


db.create_all()


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    mail = fields.String(required=True)
    password = fields.String(required=True)


@app.route('/api/getAll', methods=['GET'])
def get_all():
    get_users = User.query.all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(get_users)
    return make_response(jsonify({"users": users}))


@app.route('/api/get/<id>', methods=['GET'])
def get_user_by_id(id):
    get_user = User.query.get(id)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/api/post/<id>', methods=['POST'])
def update_user_by_id(id):
    data = request.get_json()
    get_user = User.query.get(id)
    if data.get('name'):
        get_user.name = data['name']
    if data.get('mail'):
        get_user.mail = data['mail']
    if data.get('password'):
        get_user.password = data['password']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema(only=['id', 'name', 'mail', 'password'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}), 204)


@app.route('/api/delete/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    get_user = User.query.get(id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/add', methods=['PUT'])
def create_user():
    data = request.get_json()
    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user": result}), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
