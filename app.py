from flask import Flask
from flask import render_template
from redis import Redis, RedisError
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy, inspect
import os
import socket
import jsonpickle

def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }

def object_as_json(obj):
    json = '{\n'
    for c in inspect(obj).mapper.column_attrs:
        json += '\t\"' + c.key + '\":\"' + getattr(obj, c.key) + "\","
    json -= ','
    json += '\n}'
    return json

# Connect to Redis
redis = Redis(host="redis",db=0,socket_connect_timeout=2,socket_timeout=2)

app = Flask(__name__)
DATABASE = 'flask'
PASSWORD = 'maportofeup2014'
USER = 'root'
HOSTNAME = 'mysqldb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
api = Api(app)
db = SQLAlchemy(app)


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'ee12099'}
    return render_template('index.html', title='Home', user=user)
@app.route('/hello')
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits="<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
       "<b>Hostname:</b> {hostname}<br/>" \
       "<b>Visits:</b> {visits}"

    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
		# initialize columns
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class UserResource(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('username', type=str, help='Username to create user')
            args = parser.parse_args()
            _username = args['username']
            _email = args['email']
            user = User(_username,_email)
            db.session.add(user)
            db.session.commit()
            return {'state': 'success'}
        except Exception as e:
            return {'error': str(e)}
    '''
    def get(self, id):
        try:
            #user = User.query.filter_by(username=request.args['username']).first_or_404()
            user = User.query.filter_by(id=id)
            return json.dumps({user.username:{ 'email': user.email }})
        except Exception as e:
            return {'error': str(e)}
    '''
    def get(self):
        users = []
        try:
            for user in db.session.query(User).all():
                #users.append(str(object_as_dict(user)))
                users.append(object_as_json(user) + ',\n')
            return {'users': [''.join(users)]}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(UserResource, '/users')
#api.add_resource(User, '/users/<int:id>', endpoint='/users')

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8010, debug=True)
