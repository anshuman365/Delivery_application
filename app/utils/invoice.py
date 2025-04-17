from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime
import os
from flask import current_app

def generate_invoice(order):
    """Generate PDF invoice for an order"""
    # Use current_app instead of importing app directly
    invoice_folder = current_app.config['INVOICE_FOLDER']
    os.makedirs(invoice_folder, exist_ok=True)
    
    filename = f"invoice_{order.id}.pdf"
    filepath = os.path.join(invoice_folder, filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Invoice Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height-1*inch, "Diesel Delivery Invoice")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-1.25*inch, f"Invoice #: {order.id}")
    c.drawString(1*inch, height-1.5*inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(1*inch, height-1.75*inch, f"Status: {order.status}")
    
    # Customer Info
    c.drawString(1*inch, height-2.25*inch, f"Customer: {order.customer.username}")
    c.drawString(1*inch, height-2.5*inch, f"Email: {order.customer.email}")
    c.drawString(1*inch, height-2.75*inch, f"Delivery Address: {order.delivery_address}")
    c.drawString(1*inch, height-3*inch, f"Contact: {order.contact_number}")
    
    # Order Details
    c.drawString(1*inch, height-3.5*inch, "Order Details:")
    c.line(1*inch, height-3.6*inch, 7.5*inch, height-3.6*inch)
    
    # Table Header
    c.drawString(1*inch, height-3.8*inch, "Description")
    c.drawString(4*inch, height-3.8*inch, "Quantity")
    c.drawString(5.5*inch, height-3.8*inch, "Unit Price")
    c.drawString(7*inch, height-3.8*inch, "Amount")
    c.line(1*inch, height-3.9*inch, 7.5*inch, height-3.9*inch)
    
    # Order Line
    c.drawString(1*inch, height-4.1*inch, "Diesel Delivery")
    c.drawString(4*inch, height-4.1*inch, f"{order.litres} L")
    c.drawString(5.5*inch, height-4.1*inch, f"${order.price_per_litre:.2f}")
    c.drawString(7*inch, height-4.1*inch, f"${order.total_amount:.2f}")
    c.line(1*inch, height-4.2*inch, 7.5*inch, height-4.2*inch)
    
    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5.5*inch, height-4.4*inch, "TOTAL:")
    c.drawString(7*inch, height-4.4*inch, f"${order.total_amount:.2f}")
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 0.5*inch, "Thank you for your business!")
    c.drawString(1*inch, 0.35*inch, "For any inquiries, please contact support@diesel-delivery.com")
    
    c.save()
    return filename
