from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Order
from app import db
from app.utils.decorators import admin_required

bp = Blueprint('orders', __name__)

@bp.route('/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.json.get('status')
    
    if new_status not in ['Pending', 'Assigned', 'Delivered', 'Cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Status updated successfully'})

@bp.route('/<int:order_id>')
@login_required
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    if current_user.role != 'admin' and order.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(order.to_dict())