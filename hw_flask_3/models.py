from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
"""
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True,   nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'User({self.first_name} {self.last_name} : {self.email})'
