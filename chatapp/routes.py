from chatapp import app, socketio, bcrypt, db
from flask import Flask, render_template, redirect, url_for, flash, request
from chatapp.src.forms import MessageForm, LoginForm, RegisterForm, CreateRoomForm
from chatapp.src.models import User, ChatSchema, ChatRoom
from flask_login import login_user, current_user, logout_user, login_required
import random

@app.route('/')
@app.route('/home')
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
        return redirect(url_for('login'))
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
            return redirect(next_page) if next_page else  redirect(url_for('index')) # change to chatrooms

        flash(f'Incorrect Email or Password! Please try again.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You Logged out!', 'danger')
    return redirect(url_for('index'))


@app.route('/reset_request')
def reset_request():
    pass


# @app.route('/chat/general', methods=["POST", "GET"])
#TODO no need for this code
@app.route('/chat/general', methods=["POST", "GET"])
@login_required
def general_chat():
    room_id = 10000000
    # messages = ChatSchema.query.order_by(ChatSchema.time_sent).filter_by(room_id=1).all()
    room = ChatRoom.query.filter_by(id=room_id).first()
    form = MessageForm()
    if form.validate_on_submit():
        print('message sent!')

    return render_template('chat.html', room=room, form=form, title=room.name)


# TODO
@app.route('/chat/<int:room_id>')
@login_required
def room(room_id):
    room = ChatRoom.query.filter_by(id=room_id).first()
    if not room:
        flash(f'Room of id {room_id} doesn\'t exist!', 'danger')
        return redirect(url_for('index'))

    # messages = ChatSchema.query.order_by(ChatSchema.time_sent).filter_by(room_id=room_id).all()
    form = MessageForm()
    if form.validate_on_submit():
        print('message sent!')

    return render_template('chat.html', room=room, form=form, title=room.name)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/chat/create_room', methods=["POST", "GET"])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        generated = False
        while not generated:
            generatedID = random.randint(10000000, 99999999)
            room = ChatRoom.query.filter_by(id=generatedID).first()
            # check if a room with this id exists
            if not room:
                generated = True
        newRoom = ChatRoom(id=generatedID, name=form.name.data, password=form.password.data)
        db.session.add(newRoom)
        db.session.commit()
        print('---room created---')
        flash(f'Room {form.name.data} with id of {generatedID} is created!', 'success')
        return redirect(url_for('index'))

    return render_template('create_room.html', form=form, title='Create Room')

@app.route('/chat/')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!')


# WebSockets
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    json['user_name'] = current_user.username
    print('received my event: ' + str(json))
    if "message" in json.keys():
        newMessage = ChatSchema(author=current_user, message=json['message'], room_id=json['room_id'])
        db.session.add(newMessage)
        db.session.commit()
        # messages.append(json)
    socketio.emit('chat' + str(json['room_id']), json, callback=messageReceived)
