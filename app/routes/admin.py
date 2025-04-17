from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Order, User, DeliveryBoy
from app.utils.decorators import admin_required
from app.utils.invoice import generate_invoice
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    pending_orders = Order.query.filter_by(status='Pending').count()
    total_orders = Order.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         pending_orders=pending_orders,
                         total_orders=total_orders,
                         total_customers=total_customers,
                         recent_orders=recent_orders)

@bp.route('/orders')
@login_required
@admin_required
def all_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/all_orders.html', orders=orders)

@bp.route('/order/<int:order_id>')
@login_required
@admin_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    available_delivery_boys = DeliveryBoy.query.filter_by(is_available=True).all()
    return render_template('admin/order_details.html', order=order,available_delivery_boys=available_delivery_boys)

@bp.route('/order/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status not in ['Pending', 'Assigned', 'Delivered', 'Cancelled']:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin.order_details', order_id=order.id))
    
    order.status = new_status
    db.session.commit()
    
    flash(f'Order status updated to {new_status}', 'success')
    return redirect(url_for('admin.order_details', order_id=order.id))

@bp.route('/order/<int:order_id>/generate_invoice')
@login_required
@admin_required
def generate_order_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'Delivered':
        flash('Invoice can only be generated for delivered orders', 'warning')
        return redirect(url_for('admin.order_details', order_id=order.id))
    
    try:
        invoice_filename = generate_invoice(order)
        flash('Invoice generated successfully', 'success')
        return redirect(url_for('static', filename=f'invoices/{invoice_filename}'))
    except Exception as e:
        flash(f'Error generating invoice: {str(e)}', 'danger')
        return redirect(url_for('admin.order_details', order_id=order.id))

@bp.route('/order/<int:order_id>/track')
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)
    
    return render_template('customer/track_order.html', order=order)

@bp.route('/order/<int:order_id>/assign', methods=['POST'])
@admin_required
def assign_delivery_boy(order_id):
    order = Order.query.get_or_404(order_id)
    delivery_boy_id = request.form.get('delivery_boy_id')
    
    if not delivery_boy_id:
        flash('Please select a delivery boy', 'danger')
        return redirect(url_for('admin.order_details', order_id=order.id))
    
    delivery_boy = DeliveryBoy.query.get(delivery_boy_id)
    if not delivery_boy:
        flash('Invalid delivery boy', 'danger')
        return redirect(url_for('admin.order_details', order_id=order.id))
    
    order.delivery_boy_id = delivery_boy.id
    order.status = 'Assigned'
    db.session.commit()
    
    # Here you would typically send a notification to the delivery boy
    flash(f'Order assigned to {delivery_boy.name}', 'success')
    return redirect(url_for('admin.order_details', order_id=order.id))

@bp.route('/delivery-boys')
@admin_required
def delivery_boys():
    boys = DeliveryBoy.query.all()
    return render_template('admin/delivery_boys.html', delivery_boys=boys)
