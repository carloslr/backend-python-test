from alayatodo import app, message
from flask import (
    redirect,
    flash,
    render_template,
    request,
    session
)

from alayatodo.utils import verify_password
import alayatodo.service.user as user_service


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    (blocked, userdata) = user_service.login(username, password)
    if userdata:
        if blocked:
            flash(message.LOGIN_BLOCKED)
            return redirect('/login')
        else:
            user = {
                'id': userdata['id'],
                'username': userdata['username'],
                'ip': request.remote_addr
            }
            session['user'] = user
            return redirect('/todo')

    flash(message.LOGIN_FAIL)
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')