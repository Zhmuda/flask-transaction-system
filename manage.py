from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command("create-admin")
def create_admin():
    username = input("Enter admin username: ")
    admin = User(balance=0, commission_rate=0, webhook_url="", role="admin")
    db.session.add(admin)
    db.session.commit()
    print(f"Admin created successfully.")
