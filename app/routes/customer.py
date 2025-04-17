from flask import Blueprint, render_template, redirect, url_for, flash, jsonify 
from flask_login import login_required, current_user
from app.models import Order
from app.forms import OrderForm
from app import db

bp = Blueprint('customer', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    orders = current_user.orders.order_by(Order.created_at.desc()).limit(5).all()
    return render_template('customer/dashboard.html', orders=orders)

@bp.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            litres=form.litres.data,
            delivery_address=form.delivery_address.data,
            contact_number=form.contact_number.data,
            delivery_latitude=form.latitude.data,
            delivery_longitude=form.longitude.data,
            price_per_litre=10.50,  # Should come from config
            total_amount=float(form.litres.data) * 10.50
        )
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('customer.dashboard'))
    return render_template('customer/order_form.html', form=form)

@bp.route('/orders')
@login_required
def order_history():
    orders = current_user.orders.order_by(Order.created_at.desc()).all()
    return render_template('customer/order_history.html', orders=orders)

@bp.route('/order/<int:order_id>/track')
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)
    
    # Prepare data for the map
    map_data = {
        'delivery_lat': order.delivery_latitude,
        'delivery_lng': order.delivery_longitude,
        'current_lat': order.current_location_lat,
        'current_lng': order.current_location_lng,
        'delivery_boy': order.delivery_boy.name if order.delivery_boy else None,
        'vehicle_number': order.delivery_boy.vehicle_number if order.delivery_boy else None
    }
    
    return render_template('customer/track_order.html', 
                         order=order,
                         map_data=map_data)

@bp.route('/order/<int:order_id>/details')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)
    
    return jsonify({
        'status': order.status,
        'current_location': {
            'lat': order.current_location_lat,
            'lng': order.current_location_lng
        } if order.current_location_lat else None,
        'delivery_address': order.delivery_address,
        'delivery_boy': {
            'name': order.delivery_boy.name,
            'phone': order.delivery_boy.phone,
            'vehicle': order.delivery_boy.vehicle_number
        } if order.delivery_boy else None
    })