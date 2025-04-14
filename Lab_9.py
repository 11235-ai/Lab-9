from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.String(20), nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

# Главная страница
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form["city"]
        visit_date = request.form["visit_date"]
        
        if city_name and visit_date:
            new_city = City(name=city_name, visit_date=visit_date)
            db.session.add(new_city)
            db.session.commit()
        
        return redirect("/")
    
    cities = City.query.all()
    return render_template("Findex.html", cities=cities)

# Очистка списка городов
@app.route("/clear", methods=["POST"])
def clear():
    db.session.query(City).delete()
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

