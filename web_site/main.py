from flask import Flask, url_for, request, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.user import User
from forms.login_form import LoginForm
from forms.autification_tg_form import TgForm
from forms.register_form import RegisterForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'universe_site_Akim_and_Val_secret_key'


@app.route('/')
def main():
    return render_template('main_window.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_repeat.data:
            user = User()
            db_sess = db_session.create_session()
            user.email = form.login_email.data
            user.set_password(form.password.data)
            user.name = form.name.data
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.login_email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/menu_login')
def menu_login():
    return render_template('menu_login.html')


@app.route('/autification_tg', methods=['GET', 'POST'])
def autification_tg():
    form = TgForm()
    if form.validate_on_submit():
        # Запрос в тг
        # form.tg_id.data - здесь хранится id пользователя
        return render_template('menu_login.html')  # если все хорошо
        return render_template('autification_tg.html', form=form, message='Нету такого пользователя проверте данные которые вы вводите')  # если нету пользователя
    return render_template('autification_tg.html', form=form)



if __name__ == '__main__':
    db_session.global_init(f"db/universe_site.sqlite")
    app.run(port=8080, host='127.0.0.1')
