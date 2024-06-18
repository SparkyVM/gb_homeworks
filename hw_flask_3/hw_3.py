from flask import Flask, render_template, request, flash
from flask_wtf import CSRFProtect
from models import db, User
from forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

"""
Создать форму для регистрации пользователей на сайте. 
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
"""

app = Flask(__name__)

app.config['SECRET_KEY'] = '32b2c9982dab56275242e90ba6b200a7fa8e7a3dca17dc77e394985f17df1bba'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def main():
    return 'Добро пожаловать!'

@app.route('/reg/', methods=['GET','POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate:
        f_first_name = form.first_name.data
        f_last_name = form.last_name.data
        f_email = form.email.data
        f_password = generate_password_hash(form.password.data)
        #f_password = form.password.data
        new_user = User(first_name = f_first_name, last_name = f_last_name, email = f_email, password = f_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрированы", "success")
        print(f'Зарегистрировался {f_last_name}')
    return render_template('reg.html', form=form)


if __name__ =='__main__':
    app.run(debug=True)