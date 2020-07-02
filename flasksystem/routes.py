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


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


'''This is Login Route '''
'''
@app.route('/login',methods=['GET', 'POST'])
def login():
    """Renders the Login page."""
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            utype = user.usertype
            session['usertype'] = utype
            print(utype)
            return  redirect(url_for('loginhome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('loginhome'))
    return render_template(
        'login.html',
        title='Login Page',
        year=datetime.now().year,form=form

    )
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('loginhome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/loginhome')
@login_required
def loginhome():
    return render_template(
        'loginhome.html',
        title='User Home',
        year=datetime.now().year,

    )


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


@app.route('/ado')
@login_required
def ado():
    return render_template(
        'ado.html',
        title='Agriyan Development Officer',
        year=datetime.now().year,

    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.district.choices = [(d.id, d.districtName) for d in District.query.all()]
    form.area.choices = [(area.id, area.areaName) for area in Area.query.filter_by(district_id='1').all()]
    form.devisionoffice.choices = [(devisionoffice.id, devisionoffice.officeName) for devisionoffice in
                                   Devisionoffice.query.filter_by(area_id='1').all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
        user = User(fristname=form.fristname.data, lastname=form.lastname.data, email=form.email.data,
                    password=hashed_password, phone=form.phone.data, address=form.address.data,
                    profile='defaultprofile.jpg', usertype='Farmer', active=1,
                    devisionoffice_id=form.devisionoffice.data, created_timestamp=datetime.now(),
                    modified_timestamp=datetime.now())
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title='Register',
        year=datetime.now().year, form=form
    )


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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route('/myaccount', methods=['GET', 'POST'])
@login_required
def myaccount():
    form = UpdateAccountForm()
    ######################################################
    user = User.query.filter_by(id=current_user.id).first()
    cid = user.devisionoffice_id

    ####################################################
    # form.devisionoffice.choices = [(devisionoffice.id, devisionoffice.officeName) for devisionoffice in  Devisionoffice.query.all()]
    devisionoffices = Devisionoffice.query.filter_by(id=cid).first()
    devisionoffice_id = devisionoffices.id
    devisionoffice_name = devisionoffices.officeName
    devisionoffice_area_id = devisionoffices.area_id
    form.devisionoffice.choices = [(devisionoffice_id, devisionoffice_name)]
    #######################################################
    # form.area.choices = [(area.id, area.areaName) for area in Area.query.all()]
    area = Area.query.filter_by(id=devisionoffice_area_id).first()
    area_default_id = area.id
    area_default_name = area.areaName
    area_districts_id = area.district_id
    form.area.choices = [(area_default_id, area_default_name)]
    ##########################################################
    # form.district.choices = [(d.id, d.districtName) for d in District.query.all()]
    # district = District.query.filter_by(id=area_districts_id).first()
    # district_default_id = district.id
    # district_default_name = district.districtName
    # form.district.default = [(district_default_id)]
    select_district = District.query.filter_by(id=area_districts_id).first()
    district = District.query.all()

    if form.validate_on_submit():

        current_user.fristname = form.fristname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.isactive = form.isactive.data
        current_user.devisionoffice_id = form.devisionoffice.data
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
        form.isactive.data = current_user.active
        form.devisionoffice.data = current_user.devisionoffice

    image_file = url_for('static', filename='profilepics/' + current_user.profile)
    """Renders the about page."""
    return render_template(
        'myaccount.html',
        title='Myaccount',
        year=datetime.now().year,
        image_file=image_file,
        form=form,
        district=district,
        select_district=select_district,
        message='Your application description page.'
    )


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ishanmadhawa440@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your account password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply igrone this email and no changes will be made

    '''
    mail.send(msg)


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


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
