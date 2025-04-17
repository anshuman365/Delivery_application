import os
from app.config import Config

def create_upload_folders():
    """Create necessary upload folders if they don't exist"""
    os.makedirs(Config.INVOICE_FOLDER, exist_ok=True)