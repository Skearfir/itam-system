"""
ITAM - IT Asset Management System
Main Flask Application

Built by: Merry
Started: December 2025
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# Simple HTML template for now (we'll move to separate files later)
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ITAM - IT Asset Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 60px;
            max-width: 800px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }

        h1 {
            font-size: 3rem;
            color: #2c3e50;
            margin-bottom: 20px;
        }

        .emoji {
            font-size: 4rem;
            margin-bottom: 30px;
        }

        .tagline {
            font-size: 1.5rem;
            color: #7f8c8d;
            margin-bottom: 40px;
            font-style: italic;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin: 40px 0;
        }

        .stat {
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            transition: transform 0.2s;
        }

        .stat:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .stat-value {
            font-size: 3rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }

        .stat-label {
            color: #6c757d;
            font-size: 1rem;
        }

        .button {
            display: inline-block;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: 600;
            margin: 10px;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6);
        }

        .status {
            margin-top: 40px;
            padding: 20px;
            background: #d4edda;
            border-left: 4px solid #28a745;
            border-radius: 8px;
            color: #155724;
        }

        .footer {
            margin-top: 40px;
            color: #95a5a6;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🖥️</div>
        <h1>ITAM System</h1>
        <p class="tagline">"Money shouldn't stop you from having good tools."</p>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">0</div>
                <div class="stat-label">Machines</div>
            </div>
            <div class="stat">
                <div class="stat-value">0</div>
                <div class="stat-label">Users</div>
            </div>
            <div class="stat">
                <div class="stat-value">0</div>
                <div class="stat-label">Assignments</div>
            </div>
        </div>

        <div class="status">
            <strong>🎉 Flask is working!</strong><br>
            Your ITAM system is up and running.<br>
            Database setup coming next.
        </div>

        <div style="margin-top: 40px;">
            <a href="/machines" class="button">View Machines</a>
            <a href="/users" class="button">View Users</a>
        </div>

        <div class="footer">
            <p><strong>ITAM v0.1-alpha</strong></p>
            <p>Built with ❤️ by someone who got tired of Excel</p>
            <p>Open Source • MIT License • Free Forever</p>
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page / Dashboard"""
    return render_template_string(HOME_TEMPLATE)


@app.route('/machines')
def machines():
    """Machines page (placeholder)"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Machines - ITAM</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f7fa;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💻 Machines</h1>
            <p>Inventory Management</p>
        </div>

        <div class="card">
            <h2>Machine Inventory</h2>
            <p>No machines in database yet.</p>
            <p>Database setup coming next!</p>
            <br>
            <a href="/">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """)


@app.route('/users')
def users():
    """Users page (placeholder)"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Users - ITAM</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f7fa;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>👥 Users</h1>
            <p>Employee Management</p>
        </div>

        <div class="card">
            <h2>User Directory</h2>
            <p>No users in database yet.</p>
            <p>Database setup coming next!</p>
            <br>
            <a href="/">← Back to Dashboard</a>
        </div>
    </body>
    </html>
    """)


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 ITAM System Starting...")
    print("=" * 50)
    print("📍 Open your browser and go to:")
    print("   http://localhost:5000")
    print("=" * 50)
    print("Press CTRL+C to stop the server")
    print("=" * 50)

    app.run(debug=True, port=5000)