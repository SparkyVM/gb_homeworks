from flask import Flask, render_template

app = Flask(__name__)

# Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных товаров. 
# Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.
@app.route('/')
def main():
    return 'Добро пожаловать в магазин отдежды'

@app.route('/clothes/')
def clothes():
    return render_template('clothes.html')

@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')

@app.route('/shirts/')
def shirts():
    return render_template('shirts.html')

@app.route('/pants/')
def pants():
    return render_template('pants.html')

@app.route('/sneakers/')
def sneakers():
    return render_template('sneakers.html')

@app.route('/timber/')
def timber():
    return render_template('timber.html')

if __name__ =='__main__':
    app.run(debug=True)