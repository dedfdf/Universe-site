from flask import Flask, request, render_template, redirect, jsonify
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from data import db_session
from data.user import User
import os
from data.satellites import Satellite
from data.planet import Planet
from data.star_system import Star_System
from data.galaxies import Galaxies
from forms.create_satellites_form import Create_Satellites_Form
from forms.create_star_systems_form import Create_Star_System_Form
from forms.create_planet_form import Create_Planet_Form
from forms.create_galaxy_form import Create_Galaxy_Form
from forms.login_form import LoginForm
from forms.catalog_form import CatalogForm
from forms.menu_login import MenuForm
from forms.autification_tg_form import TgForm
from forms.register_form import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'universe_site_Akim_and_Val_secret_key'
app.config['MAIL_SERVER'] = 'http://127.0.0.1:8080'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'my_bot_kira@mail.ru'
app.config['MAIL_PASSWORD'] = ''
app.config['UPLOAD_PATH'] = 'static/uploads'
mail = Mail(app)
blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')

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


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


@app.route('/create_satellites', methods=['GET', 'POST'])
def create_satellites():
    form = Create_Satellites_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/catalog')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            satellite = Satellite()
            planet = db_sess.query(Planet).filter(Planet.name == form.planet.data)
            if not [x for x in planet]:
                return render_template('create_satellite.html', form=form, message='Нет такой планеты')
            planet = planet[0]
            if db_sess.query(Satellite).filter(Satellite.name != form.name.data) and planet:
                satellite.name = form.name.data
                if uploaded_file.filename != '':
                    satellite.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + satellite.name + '.txt', 'w', encoding='utf-8') as file:
                    file.write(form.text.data)
                satellite.text = 'static/uploads_txt/' + satellite.name + '.txt'
                satellite.planet = planet.id
                db_sess.add(satellite)
                db_sess.commit()
                db_sess.close()
                return redirect('/')
            db_sess.close()
            return render_template('create_satellite.html', form=form, message='Такой спутник уже есть')
    return render_template('create_satellite.html', form=form)


@app.route('/create_galaxy', methods=['GET', 'POST'])
def create_galaxy():
    form = Create_Galaxy_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/catalog')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            galaxy = Galaxies()
            if db_sess.query(Galaxies).filter(Galaxies.name != form.name.data):
                galaxy.name = form.name.data
                if uploaded_file.filename != '':
                    galaxy.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + galaxy.name + '.txt', 'w', encoding='utf-8') as file:
                    file.write(form.text.data)
                galaxy.text = 'static/uploads_txt/' + galaxy.name + '.txt'
                db_sess.add(galaxy)
                db_sess.commit()
                db_sess.close()
                return redirect('/')
            db_sess.close()
            return render_template('create_galaxy.html', form=form, message='Такая галактика уже есть')
    return render_template('create_galaxy.html', form=form)


@app.route('/create_planet', methods=['GET', 'POST'])
def create_planet():
    form = Create_Planet_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/catalog')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            planet = Planet()
            star_system = db_sess.query(Star_System).filter(Star_System.name == form.star_system.data)
            if not [x for x in star_system]:
                return render_template('create_planet.html', form=form, message='Такой системы нет')

            if db_sess.query(Planet).filter(Planet.name != form.name.data) and star_system:
                planet.name = form.name.data
                if uploaded_file.filename != '':
                    planet.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + planet.name + '.txt', 'w', encoding='utf-8') as file:
                    file.write(form.text.data)
                planet.text = 'static/uploads_txt/' + planet.name + '.txt'
                planet.star_system = star_system.id
                db_sess.add(planet)
                db_sess.commit()
                db_sess.close()
                return redirect('/')
            db_sess.close()
            return render_template('create_planet.html', form=form, message='Такая планета уже есть')
    return render_template('create_planet.html', form=form)


@app.route('/create_star_systems', methods=['GET', 'POST'])
def create_star_systems():
    form = Create_Star_System_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/catalog')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            star_system = Star_System()
            galaxy = db_sess.query(Galaxies).filter(Galaxies.name == form.galaxy.data)
            if [x for x in galaxy]:
                return render_template('create_star_systems.html', form=form, message='Такой галактики нет')
            if db_sess.query(Star_System).filter(star_system.name != form.name.data) and galaxy:
                star_system.name = form.name.data
                if uploaded_file.filename != '':
                    star_system.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + star_system.name + '.txt', 'w', encoding='utf-8') as file:
                    file.write(form.text.data)
                star_system.text = 'static/uploads_txt/' + star_system.name + '.txt'
                star_system.galaxy = galaxy[0].id
                db_sess.add(star_system)
                db_sess.commit()
                db_sess.close()
                return redirect('/')
            db_sess.close()
            return render_template('create_star_systems.html', form=form, message='Такая звездная система уже есть')
    return render_template('create_star_systems.html', form=form)


@app.route('/galaxy', methods=['GET', 'POST'])
def galaxies():
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Galaxies)
    arr = arr[:9]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/')
    if form.submit_planets.data:
        return redirect('/planet')
    if form.submit_star_systems.data:
        return redirect('/star_systems')
    if form.submit_satellites.data:
        return redirect('/satellites')
    return render_template('galaxy.html', form=form, arr=arr, len_arr=len(arr))


@app.route('/star_systems', methods=['GET', 'POST'])
def star_systems():
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Star_System)
    arr = arr[:9]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy')
    if form.submit_planets.data:
        return redirect('/planet')
    if form.submit_satellites.data:
        return redirect('/satellites')
    return render_template('star_systems.html', form=form, arr=arr, len_arr=len(arr))


@app.route('/planet', methods=['GET', 'POST'])
def planets():
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Planet)
    arr = arr[:9]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy')
    if form.submit_star_systems.data:
        return redirect('/star_systems')
    if form.submit_satellites.data:
        return redirect('/satellites')
    return render_template('planet.html', form=form, arr=arr, len_arr=len(arr))


@app.route('/satellites', methods=['GET', 'POST'])
def satellites():
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Satellite)
    arr = arr[:9]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy')
    if form.submit_planets.data:
        return redirect('/planet')
    if form.submit_star_systems.data:
        return redirect('/star_systems')
    return render_template('satellites.html', form=form, arr=arr, len_arr=len(arr))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.submit_return.data:
        return redirect('/')
    if form.validate_on_submit():
        if form.password.data == form.password_repeat.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.login_email.data).first()
            if not user:
                user = User()
                db_sess = db_session.create_session()
                user.email = form.login_email.data
                user.set_password(form.password.data)
                user.name = form.name.data
                user.user_level = 0
                db_sess.add(user)
                db_sess.commit()
                login_user(user)
                db_sess.close()
                return redirect('/')
            return render_template('register.html', form=form, message='С такой почтой пользователь уже есть')
        return render_template('register.html', form=form, message='Пароли не совпадают')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.submit_return.data:
        return redirect('/')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.login_email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            db_sess.close()
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    form = CatalogForm()
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy')
    if form.submit_planets.data:
        return redirect('/planet')
    if form.submit_star_systems.data:
        return redirect('/star_systems')
    if form.submit_satellites.data:
        return redirect('/satellites')
    return render_template('catalog.html', form=form)


@app.route('/check_galaxy/<int:id>')
def check_galaxy(id):
    pass


@app.route('/menu_login', methods=['GET', 'POST'])
def menu_login():
    form = MenuForm()
    if form.submit_return.data:
        return redirect('/')
    if form.submit.data:
        return redirect('/catalog')
    if form.submit_leave.data:
        return redirect('/logout')
    return render_template('menu_login.html', form=form)

@app.route('api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict(only=('name', 'email'))
                for item in users]

        }
    )


@app.route('/autification_tg', methods=['GET', 'POST'])
def autification_tg():
    form = TgForm()
    if form.submit_return.data:
        return render_template('menu_login.html')
    if form.validate_on_submit():
        # Запрос в тг
        # form.tg_id.data - здесь хранится id пользователя
        return render_template('menu_login.html')  # если все хорошо
        return render_template('autification_tg.html', form=form,
                               message='Нету такого пользователя проверте данные которые вы вводите')
        # если нету пользователя
    return render_template('autification_tg.html', form=form)


if __name__ == '__main__':
    db_session.global_init(f"db/universe_site.sqlite")
    app.run(port=8080, host='127.0.0.1')
