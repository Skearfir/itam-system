from app import create_app, db

app = create_app()
app.app_context().push()
db.create_all()
print('Database reset completed!')
