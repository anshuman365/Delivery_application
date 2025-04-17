from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'customer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    litres = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Assigned, Delivered, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    delivery_latitude = db.Column(db.Float)
    delivery_longitude = db.Column(db.Float)
    price_per_litre = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    delivery_boy_id = db.Column(db.Integer, db.ForeignKey('delivery_boy.id'))
    current_location_lat = db.Column(db.Float)
    current_location_lng = db.Column(db.Float)

    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'

    def get_delivery_progress(self):
        if not self.current_location_lat or not self.delivery_latitude:
            return 0
            
        # Simple distance calculation (for demonstration)
        lat_diff = abs(float(self.delivery_latitude) - float(self.current_location_lat))
        lng_diff = abs(float(self.delivery_longitude) - float(self.current_location_lng))
        return min(100, int(100 - ((lat_diff + lng_diff) * 1000)))

class DeliveryBoy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    current_location_lat = db.Column(db.Float)
    current_location_lng = db.Column(db.Float)
    orders = db.relationship('Order', backref='delivery_boy', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_assigned_orders(self):
        return Order.query.filter(
            Order.delivery_boy_id == self.id,
            or_(Order.status == 'Assigned', Order.status == 'Out for Delivery')
        ).all()
    
    def update_location(self, lat, lng):
        self.current_location_lat = lat
        self.current_location_lng = lng
        db.session.commit()
    
    def get_active_deliveries(self):
        return self.orders.filter(Order.status.in_(['Assigned', 'Out for Delivery'])).all()
    
    def get_delivery_locations(self):
        return [(order.delivery_latitude, order.delivery_longitude, order.delivery_address) 
                for order in self.get_active_deliveries()]

