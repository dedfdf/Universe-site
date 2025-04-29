import flask
from flask import Flask, request, render_template, redirect, jsonify, make_response
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from data import db_session
import os
from data.satellites import Satellite
from data.planet import Planet
from data.star_system import Star_System
from data.galaxies import Galaxies
from data.user import User
from forms.chooise_create import Choise_Create_Form
from forms.check_galaxy_form import Check_Galaxy_Form
from forms.check_star_system import Check_Star_System_Form
from forms.check_planet_form import Check_Planet_Form
from forms.check_satellites_form import Check_satellites_Form
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
    db_sess.close()
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
            return redirect('/choise_create')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            satellite = Satellite()
            planet = db_sess.query(Planet).filter(Planet.name == form.planet.data)
            if not [x for x in planet]:
                return render_template('create_satellite.html', form=form,
                                       message='Нет такой планеты')
            planet = planet[0]
            g = [x for x in db_sess.query(Satellite).filter(Satellite.name == form.name.data)]
            if not g:
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
                return redirect('/satellites/1')
            db_sess.close()
            return render_template('create_satellite.html', form=form, message='Такой спутник уже есть')
    return render_template('create_satellite.html', form=form)


@app.route('/create_galaxy', methods=['GET', 'POST'])
def create_galaxy():
    form = Create_Galaxy_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/choise_create')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            galaxy = Galaxies()
            g = [x for x in db_sess.query(Galaxies).filter(Galaxies.name == form.name.data)]
            if not g:
                galaxy.name = form.name.data
                if uploaded_file.filename != '':
                    galaxy.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + galaxy.name + '.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(form.text.data)
                galaxy.text = 'static/uploads_txt/' + galaxy.name + '.txt'
                db_sess.add(galaxy)
                db_sess.commit()
                db_sess.close()
                return redirect('/galaxy/1')
            db_sess.close()
            return render_template('create_galaxy.html', form=form,
                                   message='Такая галактика уже есть')
    return render_template('create_galaxy.html', form=form)


@app.route('/create_planet', methods=['GET', 'POST'])
def create_planet():
    form = Create_Planet_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/choise_create')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            planet = Planet()
            star_system = db_sess.query(Star_System).filter(
                Star_System.name == form.star_system.data)
            if not [x for x in star_system]:
                db_sess.close()
                return render_template('create_planet.html', form=form, message='Такой системы нет')
            g = [x for x in db_sess.query(Planet).filter(Planet.name == form.name.data)]
            if not g:
                planet.name = form.name.data
                if uploaded_file.filename != '':
                    planet.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + planet.name + '.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(form.text.data)
                star_system = star_system[0]
                planet.text = 'static/uploads_txt/' + planet.name + '.txt'
                planet.star_system = star_system.id
                db_sess.add(planet)
                db_sess.commit()
                db_sess.close()
                return redirect('/planet/1')
            db_sess.close()
            return render_template('create_planet.html', form=form,
                                   message='Такая планета уже есть')
    return render_template('create_planet.html', form=form)


@app.route('/create_star_systems', methods=['GET', 'POST'])
def create_star_systems():
    form = Create_Star_System_Form()
    if request.method == 'POST':
        if form.submit_return.data:
            return redirect('/choise_create')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            star_system = Star_System()
            galaxy = db_sess.query(Galaxies).filter(Galaxies.name == form.galaxy.data)
            if not [x for x in galaxy]:
                db_sess.close()
                return render_template('create_star_systems.html', form=form, message='Такой галактики нет')
            g = [x for x in db_sess.query(Star_System).filter(Star_System.name == form.name.data)]
            if not g:
                star_system.name = form.name.data
                if uploaded_file.filename != '':
                    star_system.photo = 'static/uploads/' + filename
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                with open('static/uploads_txt/' + star_system.name + '.txt', 'w',
                          encoding='utf-8') as file:
                    file.write(form.text.data)
                star_system.text = 'static/uploads_txt/' + star_system.name + '.txt'
                star_system.galaxy = galaxy[0].id
                db_sess.add(star_system)
                db_sess.commit()
                db_sess.close()
                return redirect('/star_systems/1')
            db_sess.close()
            return render_template('create_star_systems.html', form=form,
                                   message='Такая звездная система уже есть')
    return render_template('create_star_systems.html', form=form)


@app.route('/edit_galaxy/<int:id_galaxy>', methods=['GET', 'POST'])
def edit_galaxy(id_galaxy):
    form = Create_Galaxy_Form()
    db_sess = db_session.create_session()
    galaxy = db_sess.query(Galaxies).filter(Galaxies.id == id_galaxy)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/galaxy/1')
    galaxy = galaxy[0]
    if not form.submit.data:
        form.name.data = galaxy.name
        with open(galaxy.text, 'r', encoding='utf-8') as file:
            arr = file.readlines()
        arr = '\n\n'.join([x.strip() for x in arr if x != '\n'])
        form.text.data = arr
    if form.validate_on_submit():
        if galaxy.text:
            if os.path.isfile(galaxy.text):
                os.remove(galaxy.text)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if uploaded_file.filename != '':
            if galaxy.photo:
                if os.path.isfile(galaxy.photo):
                    os.remove(galaxy.photo)
            galaxy.photo = 'static/uploads/' + filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        with open('static/uploads_txt/' + galaxy.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        galaxy.text = 'static/uploads_txt/' + galaxy.name + '.txt'
        galaxy.name = form.name.data
        db_sess.add(galaxy)
        db_sess.commit()
        db_sess.close()
        return redirect('/galaxy/1')
    db_sess.close()
    return render_template('create_galaxy.html', form=form)


@app.route('/edit_star_system/<int:id_star_system>', methods=['GET', 'POST'])
def edit_star_system(id_star_system):
    form = Create_Star_System_Form()
    db_sess = db_session.create_session()
    star_system = db_sess.query(Star_System).filter(Star_System.id == id_star_system)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/star_systems/1')
    star_system = star_system[0]
    if not form.submit.data:
        form.name.data = star_system.name
        if star_system.text:
            if os.path.isfile(star_system.text):
                with open(star_system.text, 'r', encoding='utf-8') as file:
                    arr = file.readlines()
                arr = '\n\n'.join([x.strip() for x in arr if x != '\n'])
                form.text.data = arr
        galaxy = db_sess.query(Galaxies).filter(Galaxies.id == star_system.galaxy)
        galaxy = galaxy[0]
        form.galaxy.data = galaxy.name
    if form.validate_on_submit():
        if star_system.text:
            if os.path.isfile(star_system.text):
                os.remove(star_system.text)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        galaxy = db_sess.query(Galaxies).filter(Galaxies.name == form.galaxy.data)
        if not [x for x in galaxy]:
            db_sess.close()
            return render_template('create_star_systems.html', form=form, message='Такой галактики нет')
        else:
            star_system.galaxy = galaxy[0].id
        if uploaded_file.filename:
            if star_system.photo:
                if os.path.isfile(star_system.photo):
                    os.remove(star_system.photo)
            star_system.photo = 'static/uploads/' + filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        with open('static/uploads_txt/' + star_system.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        star_system.text = 'static/uploads_txt/' + star_system.name + '.txt'
        star_system.name = form.name.data
        db_sess.add(star_system)
        db_sess.commit()
        db_sess.close()
        return redirect('/star_systems/1')
    db_sess.close()
    return render_template('create_star_systems.html', form=form)


@app.route('/edit_planet/<int:id_planet>', methods=['GET', 'POST'])
def edit_planet(id_planet):
    form = Create_Planet_Form()
    db_sess = db_session.create_session()
    planet = db_sess.query(Planet).filter(Planet.id == id_planet)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/planet/1')
    planet = planet[0]
    if not form.submit.data:
        form.name.data = planet.name
        if planet.text:
            if os.path.isfile(planet.text):
                with open(planet.text, 'r', encoding='utf-8') as file:
                    arr = file.readlines()
                arr = '\n\n'.join([x.strip() for x in arr if x != '\n'])
                form.text.data = arr
        star_system = db_sess.query(Star_System).filter(Star_System.id == planet.star_system)
        star_system = star_system[0]
        form.star_system.data = star_system.name
    if form.validate_on_submit():
        if planet.text:
            if os.path.isfile(planet.text):
                os.remove(planet.text)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        star_system = db_sess.query(Star_System).filter(Star_System.name == form.star_system.data)
        if not [x for x in star_system]:
            db_sess.close()
            return render_template('create_planet.html', form=form, message='Такой звездной системы нет')
        else:
            planet.star_system = star_system[0].id
        if uploaded_file.filename:
            if planet.photo:
                if os.path.isfile(planet.photo):
                    os.remove(planet.photo)
            planet.photo = 'static/uploads/' + filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        with open('static/uploads_txt/' + planet.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        planet.text = 'static/uploads_txt/' + planet.name + '.txt'
        planet.name = form.name.data
        db_sess.add(planet)
        db_sess.commit()
        db_sess.close()
        return redirect('/planet/1')
    db_sess.close()
    return render_template('create_planet.html', form=form)


@app.route('/edit_satellite/<int:id_satellite>', methods=['GET', 'POST'])
def edit_satellite(id_satellite):
    form = Create_Satellites_Form()
    db_sess = db_session.create_session()
    satellite = db_sess.query(Satellite).filter(Satellite.id == id_satellite)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/satellites/1')
    satellite = satellite[0]
    if not form.submit.data:
        form.name.data = satellite.name
        if satellite.text:
            if os.path.isfile(satellite.text):
                with open(satellite.text, 'r', encoding='utf-8') as file:
                    arr = file.readlines()
                arr = '\n\n'.join([x.strip() for x in arr if x != '\n'])
                form.text.data = arr
        planet = db_sess.query(Planet).filter(Planet.id == satellite.planet)
        planet = planet[0]
        form.planet.data = planet.name
    if form.validate_on_submit():
        if satellite.text:
            if os.path.isfile(satellite.text):
                os.remove(satellite.text)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        planet = db_sess.query(Planet).filter(Planet.name == form.planet.data)
        if not [x for x in planet]:
            db_sess.close()
            return render_template('create_satellite.html', form=form, message='Такой планеты нет')
        else:
            satellite.planet = planet[0].id
        if uploaded_file.filename != '':
            if satellite.photo:
                if os.path.isfile(satellite.photo):
                    os.remove(satellite.photo)
            satellite.photo = 'static/uploads/' + filename
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        with open('static/uploads_txt/' + satellite.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        satellite.text = 'static/uploads_txt/' + satellite.name + '.txt'
        satellite.name = form.name.data
        db_sess.add(satellite)
        db_sess.commit()
        db_sess.close()
        return redirect('/satellites/1')
    db_sess.close()
    return render_template('create_satellite.html', form=form)


@app.route('/delete_galaxy/<int:id_galaxy>', methods=['GET', 'POST'])
def delete_galaxy(id_galaxy):
    db_sess = db_session.create_session()
    galaxy = db_sess.query(Galaxies).filter(Galaxies.id == id_galaxy)
    galaxy = galaxy[0]
    star_system = db_sess.query(Star_System).filter(Star_System.galaxy == galaxy.id)
    for x in star_system:
        x.galaxy = 1
        db_sess.add(x)
    if galaxy.text:
        if os.path.isfile(galaxy.text):
            os.remove(galaxy.text)
    if galaxy.photo:
        if os.path.isfile(galaxy.photo):
            os.remove(galaxy.photo)
    db_sess.delete(galaxy)
    db_sess.commit()
    db_sess.close()
    return redirect('/galaxy/1')


@app.route('/delete_star_system/<int:id_star_system>', methods=['GET', 'POST'])
def delete_star_system(id_star_system):
    db_sess = db_session.create_session()
    star_system = db_sess.query(Star_System).filter(Star_System.id == id_star_system)
    star_system = star_system[0]
    planet = db_sess.query(Planet).filter(Planet.star_system == star_system.id)
    for x in planet:
        x.star_system = 1
        db_sess.add(x)
    if star_system.text:
        if os.path.isfile(star_system.text):
            os.remove(star_system.text)
    if star_system.photo:
        if os.path.isfile(star_system.photo):
            os.remove(star_system.photo)
    db_sess.delete(star_system)
    db_sess.commit()
    db_sess.close()
    return redirect('/star_systems/1')


@app.route('/delete_planet/<int:id_planet>', methods=['GET', 'POST'])
def delete_planet(id_planet):
    db_sess = db_session.create_session()
    planet = db_sess.query(Planet).filter(Planet.id == id_planet)
    planet = planet[0]
    satellite = db_sess.query(Satellite).filter(Satellite.planet == planet.id)
    for x in satellite:
        x.planet = 1
        db_sess.add(x)
    if planet.text:
        if os.path.isfile(planet.text):
            os.remove(planet.text)
    if planet.photo:
        if os.path.isfile(planet.photo):
            os.remove(planet.photo)
    db_sess.delete(planet)
    db_sess.commit()
    db_sess.close()
    return redirect('/planet/1')


@app.route('/delete_satellite/<int:id_satellite>', methods=['GET', 'POST'])
def delete_satellite(id_satellite):
    db_sess = db_session.create_session()
    satellite = db_sess.query(Satellite).filter(Satellite.id == id_satellite)
    satellite = satellite[0]
    if satellite.text:
        if os.path.isfile(satellite.text):
            os.remove(satellite.text)
    if satellite.photo:
        if os.path.isfile(satellite.photo):
            os.remove(satellite.photo)
    db_sess.delete(satellite)
    db_sess.commit()
    db_sess.close()
    return redirect('/planet/1')


@app.route('/galaxy/<int:page>', methods=['GET', 'POST'])
def galaxies(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Galaxies).filter(Galaxies.id != 1)
    arr = [x for x in arr]
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/galaxy/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/galaxy/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_planets.data:
        return redirect('/planet/1')
    if form.submit_star_systems.data:
        return redirect('/star_systems/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_satellites.data:
        return redirect('/satellites/1')
    return render_template('galaxy.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/star_systems/<int:page>', methods=['GET', 'POST'])
def star_systems(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Star_System).filter(Star_System.id != 1)
    arr = [x for x in arr]
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/star_systems/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/star_systems/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_planets.data:
        return redirect('/planet/1')
    if form.submit_satellites.data:
        return redirect('/satellites/1')
    return render_template('star_systems.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/planet/<int:page>', methods=['GET', 'POST'])
def planets(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Planet).filter(Planet.id != 1)
    arr = [x for x in arr]
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/planet/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/planet/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy/1')
    if form.submit_star_systems.data:
        return redirect('/star_systems/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_satellites.data:
        return redirect('/satellites/1')
    return render_template('planet.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/satellites/<int:page>', methods=['GET', 'POST'])
def satellites(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Satellite)
    arr = [x for x in arr]
    print(arr)
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/satellites/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/satellites/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy/1')
    if form.submit_planets.data:
        return redirect('/planet/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_star_systems.data:
        return redirect('/star_systems/1')
    return render_template('satellites.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/choise_create', methods=['GET', 'POST'])
def choise_create():
    form = Choise_Create_Form()
    if form.submit_create_galaxy.data:
        return redirect('/create_galaxy')
    if form.submit_create_star_system.data:
        return redirect('/create_star_systems')
    if form.submit_create_planet.data:
        return redirect('/create_planet')
    if form.submit_satellite.data:
        return redirect('/create_satellites')
    if form.submit_return.data:
        return redirect('/galaxy/1')
    return render_template('choise_create.html', form=form)


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
                user.user_level = 1
                db_sess.add(user)
                db_sess.commit()
                login_user(user)
                db_sess.close()
                return redirect('/')
            return render_template('register.html', form=form,
                                   message='С такой почтой пользователь уже есть')
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
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/check_galaxy/<int:id_galaxy>', methods=['GET', 'POST'])
def check_galaxy(id_galaxy):
    db_sess = db_session.create_session()
    form = Check_Galaxy_Form()
    galaxy = db_sess.query(Galaxies).filter(Galaxies.id == id_galaxy)[0]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/galaxy/1')
    text = ''
    if galaxy.text:
        if os.path.isfile(galaxy.text):
            with open(galaxy.text, 'r', encoding='utf-8') as file:
                text = file.readlines()
    photo = ''
    if galaxy.photo:
        if os.path.isfile(galaxy.photo):
            photo = galaxy.photo
    return render_template('check_galaxy.html', form=form, galaxy=galaxy, text=text, photo=photo)


@app.route('/check_star_system/<int:id_star_system>', methods=['GET', 'POST'])
def check_star_system(id_star_system):
    db_sess = db_session.create_session()
    form = Check_Star_System_Form()
    star_system = db_sess.query(Star_System).filter(Star_System.id == id_star_system)[0]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/star_systems/1')
    text = ''
    if star_system.text:
        if os.path.isfile(star_system.text):
            with open(star_system.text, 'r', encoding='utf-8') as file:
                text = file.readlines()
    photo = ''
    if star_system.photo:
        if os.path.isfile(star_system.photo):
            photo = star_system.photo
    return render_template('check_star_system.html', form=form, star_system=star_system, text=text, photo=photo)


@app.route('/check_planet/<int:id_planet>', methods=['GET', 'POST'])
def check_planet(id_planet):
    db_sess = db_session.create_session()
    form = Check_Planet_Form()
    planet = db_sess.query(Planet).filter(Planet.id == id_planet)[0]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/planet/1')
    text = ''
    if planet.text:
        if os.path.isfile(planet.text):
            with open(planet.text, 'r', encoding='utf-8') as file:
                text = file.readlines()
    photo = ''
    if planet.photo:
        if os.path.isfile(planet.photo):
            photo = planet.photo
    return render_template('check_planet.html', form=form, planet=planet, text=text, photo=photo)


@app.route('/check_satellite/<int:id_satellite>', methods=['GET', 'POST'])
def check_satellite(id_satellite):
    db_sess = db_session.create_session()
    form = Check_satellites_Form()
    satellite = db_sess.query(Satellite).filter(Satellite.id == id_satellite)[0]
    db_sess.close()
    if form.submit_return.data:
        return redirect('/satellites/1')
    text = ''
    if satellite.text:
        if os.path.isfile(satellite.text):
            with open(satellite.text, 'r', encoding='utf-8') as file:
                text = file.readlines()
    photo = ''
    if satellite.photo:
        if os.path.isfile(satellite.photo):
            photo = satellite.photo
    return render_template('check_satellite.html', form=form, satellite=satellite, text=text, photo=photo)


@app.route('/menu_login', methods=['GET', 'POST'])
def menu_login():
    form = MenuForm()
    if form.submit_return.data:
        return redirect('/')
    if form.submit.data:
        return redirect('/galaxy/1')
    if form.submit_leave.data:
        return redirect('/logout')
    return render_template('menu_login.html', form=form)

@app.route('/tg_get', methods=['GET'])
def tg_get():
    db_sess = db_session.create_session()
    all_data = db_sess.query(User)
    return jsonify([{'id': data.name, 'text': data.email} for data in all_data])


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
