import click
from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Database initialized.')

@app.cli.command('create-admin')
@click.argument('username')
@click.argument('password')
def create_admin(username, password):
    """Create an admin user."""
    admin = User(username=username, email=f"{username}@admin.com", role='admin')
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo(f'Admin user {username} created.')