from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from app.models import Order, DeliveryBoy
from app.utils.decorators import delivery_boy_required
from app import db
import datetime

bp = Blueprint('delivery', __name__, url_prefix='/delivery')

@bp.route('/dashboard')
@login_required
@delivery_boy_required
def dashboard():
    delivery_boy = DeliveryBoy.query.filter_by(username=current_user.username).first()
    if delivery_boy:
        deliveries = delivery_boy.get_active_deliveries()
        delivery_locations = delivery_boy.get_delivery_locations()
        return render_template('delivery/dashboard.html', deliveries=deliveries, delivery_locations=delivery_locations)
    else:
        abort(404)

@bp.route('/update_location', methods=['POST'])
@login_required
@delivery_boy_required
def update_location():
    data = request.get_json()
    current_user.current_location_lat = data['lat']
    current_user.current_location_lng = data['lng']
    current_user.last_location_update = datetime.datetime.utcnow()
    
    # Update all assigned orders
    for order in current_user.get_active_deliveries():
        order.current_location_lat = data['lat']
        order.current_location_lng = data['lng']
        db.session.add(order)
    
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/order/<int:order_id>/start', methods=['POST'])
@login_required
@delivery_boy_required
def start_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    if order.delivery_boy_id != current_user.id:
        abort(403)
    
    order.status = 'Out for Delivery'
    order.delivery_start_time = datetime.datetime.utcnow()
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/order/<int:order_id>/complete', methods=['POST'])
@login_required
@delivery_boy_required
def complete_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    if order.delivery_boy_id != current_user.id:
        abort(403)
    
    order.status = 'Delivered'
    order.delivery_end_time = datetime.datetime.utcnow()
    db.session.commit()
    
    return jsonify({'status': 'success'})