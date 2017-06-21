from flask import render_template
from app import app

@app.route('/')
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

@app.route('/index')
def index():
    user = {'nickname': 'ee12099'}
    return render_template('index.html', title='Home', user=user)
