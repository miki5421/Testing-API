from flask import Flask, request, jsonify, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KcqoSUtgLzTaIpYGKYNqGVjvcHX6GbtaD1msQpvE5vbWVG6O8zctHEF7__cE8l3hLeUt6ny03y0osodK8FnSIU1rUfbi-lyIm8xIDC72hDF1-QJ82IVEe9MVLDyn5e4wbfyXRw'

def token_requiered(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return jsonify({'message':f'{e}'})

    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently!'


@app.route('/public')
def public():
    return 'For public'

@app.route('/auth')
@token_requiered
def auth():
    return 'JWT is verified, welcome to your dashboard'





@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user' : request.form['username'],
            'experation' : str(datetime.utcnow() + timedelta(seconds=120))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token' : token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed!"'})



if __name__ == "__main__":
    app.run(debug=True)