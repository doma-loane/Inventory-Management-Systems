from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
