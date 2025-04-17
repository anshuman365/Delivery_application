from flask import Blueprint, render_template, redirect, url_for, flash, request 
from flask_login import login_user, logout_user, current_user
from app.models import User, DeliveryBoy
from app.forms import LoginForm, RegistrationForm, DeliveryRegistrationForm
from app import db, login_manager

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user is not None:
        return user
    return DeliveryBoy.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    role = request.args.get('role')
    if role == 'delivery_boy':
        form = DeliveryLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data, role='delivery_boy').first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login', role='delivery_boy'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('delivery.dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if user.role == 'delivery_boy':
                return redirect(url_for('delivery.dashboard'))
            return redirect(next_page or url_for('customer.dashboard' if user.role == 'customer' else 'admin.dashboard'))
    return render_template('auth/login.html', form=form, role=role)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='customer'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register/delivery', methods=['GET', 'POST'])
def register_delivery():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = DeliveryRegistrationForm()
    if form.validate_on_submit():
        delivery_boy = DeliveryBoy(
            username=form.username.data,
            name=form.name.data,
            phone=form.phone.data,
            vehicle_number=form.vehicle_number.data
        )
        delivery_boy.set_password(form.password.data)
        db.session.add(delivery_boy)
        db.session.commit()

        # Create a User instance with role 'delivery_boy'
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='delivery_boy'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_delivery.html', form=form)