from chatapp import app, socketio, bcrypt
from flask import Flask, render_template, redirect, url_for
from chatapp.src.forms import MessageForm, LoginForm, RegisterForm
from chatapp.src.models import User, ChatSchema
from flask_login import login_user, current_user, logout_user, login_required

messages = []

@app.route('/')
def index():
    return render_template('index.html', title='home')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    listForms = form.get_form()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newUser = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(newUser)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', listForms=listForms, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username_email.data).first() or User.query.filter_by(username=form.username_email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as {form.username_email.data}!', 'success')
            return redirect(next_page) if next_page else  redirect(url_for('index'))

        flash(f'Incorrect Email or Password! Please try again.', 'danger')


    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/chat/general')
# @login_required TODO
def chat():
    # add login form
    form = MessageForm()
    if form.validate_on_submit():
        print('message sent!')
    return render_template('chat.html', messages=messages, form=form, title='general')

# TODO
# @app.route('/chat/<room_id>')
# def index():
#     # add login form
#     form = MessageForm()
#     if form.validate_on_submit():
#         print('message sent!')
#     return render_template('index.html', messages=messages, form=form)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    if "message" in json.keys():
        messages.append(json)
    socketio.emit('my response', json, callback=messageReceived)






