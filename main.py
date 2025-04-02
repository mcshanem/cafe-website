from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Load variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

# Connect Bootstrap to Flask app
Bootstrap5(app)


# Connect to database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafes.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define Cafe class/table
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    map_url: Mapped[str] = mapped_column(String(500))
    img_url: Mapped[str] = mapped_column(String(500))
    location: Mapped[str] = mapped_column(String(250))
    has_sockets: Mapped[bool]
    has_toilet: Mapped[bool]
    has_wifi: Mapped[bool]
    can_take_calls: Mapped[bool]
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))


# # Create tables
# with app.app_context():
#     db.create_all()

def bool_to_yes_no(b_value):
    if b_value:
        return 'Yes'
    else:
        return 'No'


@app.route('/')
def home():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()
    return render_template('index.html', cafes=cafes, bool_to_yes_no=bool_to_yes_no)


if __name__ == '__main__':
    app.run(debug=True)
