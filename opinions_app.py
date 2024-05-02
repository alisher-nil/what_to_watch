from datetime import datetime
from random import randrange

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "f9a7c58f-8be6-4e69-ac61-4a9ba220610e"

db = SQLAlchemy(app)


class OpinionForm(FlaskForm):
    title = StringField(
        "Введите название фильма",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(1, 128),
        ],
    )
    text = TextAreaField(
        "Напишите мнение",
        validators=[
            DataRequired(message="Обязательное поле"),
        ],
    )
    source = URLField(
        "Добавьте ссылку на подробный обзор фильма",
        validators=[
            Length(1, 256),
            Optional(),
        ],
    )
    submit = SubmitField("Добавить")


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@app.route("/")
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return "В базе данных мнений о фильмах нет."
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template("opinion.html", opinion=opinion)


@app.route("/add")
def add_opinion_view():
    form = OpinionForm()
    return render_template("add_opinion.html", form=form)


@app.route("/opinions/<int:opinion_id>")
def opinion_view(opinion_id):
    opinion = Opinion.query.get_or_404(opinion_id)
    return render_template("opinion.html", opinion=opinion)


if __name__ == "__main__":
    app.run()
