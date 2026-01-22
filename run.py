from app import create_app, db
from app.models import Department, User, Asset, Assignment, HistoryEvent

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Department': Department,
        'User': User,
        'Asset': Asset,
        'Assignment': Assignment,
        'HistoryEvent': HistoryEvent
    }

if __name__ == '__main__':
    app.run(debug=True)