from datetime import datetime
import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session, jsonify
from flasksystem import app, db, bcrypt, mail
from flasksystem.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flasksystem.models import User, District, Area, Devisionoffice
from flask_login import login_user, login_required, current_user, logout_user
from flask_mail import Message


# Home Route
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


# Contact Route
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


# About Route
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


# Email Confirm Message
def send_confirm_email(user):
    token = user.get_email_confirm_token()
    massage = Message('Email confirmation link', sender='ishanmadhawa440@gmail.com', recipients=[user.email])
    massage.body = f'''To confirm your password and login, please visit fallowing link:
{url_for('confirm_email', token=token, _external=True)} 
If you want to access your Agri info account please use this confirmation link!     
     
     '''
    mail.send(massage)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('loginhome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user_confirm = user.confirmed
        if (user_confirm == 0):
            send_confirm_email(user)
            flash(
                'You need to confirm your email!,Email Confirmation link has been send your Email Please check your Email!! .',
                'info')
            return redirect(url_for('email_confirmation_msg'))
        else:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('loginhome'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Confirm Email Route
@app.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('loginhome'))
    user = User.verify_email_token(token)
    if user is None:
        flash('That is inavalid or expired token', 'warning')
        redirect(url_for('login'))
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.commit()
        flash('Email confirm sucess fully please re enter login credantiels to login', 'success')
        return redirect(url_for('login'))


# Email Confirm Message Route
@app.route('/email_confirmation_msg')
def email_confirmation_msg():
    if current_user.is_authenticated:
        return redirect(url_for('loginhome'))
    return render_template(
        'email_confirmation_msg.html',
        title='Email Confirmation Message',
        year=datetime.now().year,
    )


# Users Login Home Route
@app.route('/loginhome')
@login_required
def loginhome():
    image_file = url_for('static', filename='profilepics/' + current_user.profile)
    return render_template(
        'loginhome.html',
        title='User Home',
        image_file=image_file,
        year=datetime.now().year,

    )


# Farmer Route
@app.route('/farmer')
@login_required
def farmer():
    return render_template(
        'farmer.html',
        title='Farmer Home',
        year=datetime.now().year,

    )


@app.route('/arpa')
@login_required
def arpa():
    return render_template(
        'arpa.html',
        title='Agriculture  Home',
        year=datetime.now().year,

    )


# Agri Development Offficer Route
@app.route('/ado')
@login_required
def ado():
    return render_template(
        'ado.html',
        title='Agriyan Development Officer',
        year=datetime.now().year,

    )


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    district = District.query.all()
    area = Area.query.filter_by(district_id=1).all()
    devisionoffices = Devisionoffice.query.filter_by(area_id=2).all()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
        user = User(fristname=form.fristname.data, lastname=form.lastname.data, email=form.email.data,
                    password=hashed_password, phone=form.phone.data, address=form.address.data,
                    profile='defaultprofile.jpg', usertype='Farmer', active=1,
                    devisionoffice_id=request.form['devisionoffice'], created_timestamp=datetime.now(),
                    modified_timestamp=datetime.now(), confirmed=False)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title='Register',
        district=district,
        area=area,
        devisionoffices=devisionoffices,
        year=datetime.now().year, form=form
    )


# Get Select box Values
@app.route('/district/<district_id>')
def district(district_id):
    areas = Area.query.filter_by(district_id=district_id).all()

    areaListArray = []

    for area in areas:
        areaObj = {}
        areaObj['id'] = area.id
        areaObj['areaName'] = area.areaName
        areaListArray.append(areaObj)

    return jsonify({'areas': areaListArray})


# Get data from JASON format and return to it Register form
@app.route('/area/<area_id>')
def area(area_id):
    # get data from devison oficess using area id
    devisionoffices = Devisionoffice.query.filter_by(area_id=area_id).all()
    # Defining Array
    devisionofficesListArray = []
    # Passing data to Array and redirect it form
    for devisionoffice in devisionoffices:
        devisionofficeObj = {}
        devisionofficeObj['id'] = devisionoffice.id
        devisionofficeObj['officeName'] = devisionoffice.officeName
        devisionofficesListArray.append(devisionofficeObj)
    return jsonify({'devisionoffices': devisionofficesListArray})


# Logout Route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Prifile picture Save Function
def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilepics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# User Profile Route
@app.route('/myaccount', methods=['GET', 'POST'])
@login_required
def myaccount():
    form = UpdateAccountForm()
    ######################################################
    devisionoffices = Devisionoffice.query.all()
    ######################################################
    devisionoffice = Devisionoffice.query.filter_by(id=current_user.devisionoffice_id).first()
    devisionoffice_area_id = devisionoffice.area_id
    print(current_user.devisionoffice_id)
    print(devisionoffice_area_id)
    #####################################################
    area = Area.query.all()
    area_select = Area.query.filter_by(id=devisionoffice_area_id).first()
    area_districts_id = area_select.district_id
    # area = Area.query.filter_by(district_id=area_districts_id).all()

    ########################################################
    select_district = District.query.filter_by(id=area_districts_id).first()
    district = District.query.all()
    ###################################################
    if form.validate_on_submit():
        current_user.fristname = form.fristname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.active = int(request.form['active'])
        current_user.devisionoffice_id = request.form['devisionoffice']
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.profile = picture_file
        db.session.commit()
        flash('your account has been updated', 'success')
    elif request.method == 'GET':
        form.fristname.data = current_user.fristname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address.data = current_user.address

    image_file = url_for('static', filename='profilepics/' + current_user.profile)
    """Renders the about page."""
    return render_template(
        'myaccount.html',
        title='Myaccount',
        year=datetime.now().year,
        image_file=image_file,
        form=form,
        devisionoffices=devisionoffices,
        select_district=select_district,
        district=district,
        area_select=area_select,
        area=area,
        devisionoffice_area_id=devisionoffice_area_id,
        message='Your application description page.'
    )


# Password reset Email Message
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ishanmadhawa440@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your account password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply igrone this email and no changes will be made

    '''
    mail.send(msg)


# password reset form
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', year=datetime.now().year, form=form)


# change password form
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('loginhome'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Reset token invalid or expierd!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been update! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', year=datetime.now().year, form=form)


# farm home
@app.route('/farm_home', methods=['GET', 'POST'])
def farm_home():
    image_file = url_for('static', filename='profilepics/' + current_user.profile)



    return render_template('farm_home.html', title='Reset Password', year=datetime.now().year,image_file=image_file)

#add new farm
@app.route('/addnewfarm', methods=['GET', 'POST'])
def addnewfarm():
    image_file = url_for('static', filename='profilepics/' + current_user.profile)



    return render_template('addnewfarm.html', title='Reset Password', year=datetime.now().year,image_file=image_file)

