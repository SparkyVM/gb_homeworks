from flask import Flask, render_template, make_response, request, redirect,url_for

"""
Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан cookie-файл с данными пользователя, 
а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.

На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными пользователя и произведено 
перенаправление на страницу ввода имени и электронной почты.
"""

app = Flask(__name__)


@app.route('/')
def main():
    return 'Добро пожаловать!'

@app.route('/auth/', methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('auth_name')
        email = request.form.get('email')

        # устанавливаем cookie
        response = make_response(redirect(url_for('login')))
        response.set_cookie('username', username)
        return response
    return render_template('auth.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    name = request.cookies.get('username')
    if request.method == 'POST':
        name = request.cookies.get('username')
        if name is None:
            print('nobody')
        response = make_response(redirect(url_for('auth')))
        response.set_cookie('username', '', expires=0)
        return response
    context = {
        'username' : name
    }
    return render_template('login.html', **context)


if __name__ =='__main__':
    app.run(debug=True)