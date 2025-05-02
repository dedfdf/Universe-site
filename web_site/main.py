from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from data import db_session
import os
from data.satellites import Satellite
from data.planet import Planet
from data.star_system import Star_System
from data.galaxies import Galaxies
from data.user import User
from forms.base_form import Base_Form
from forms.chooise_create import Choise_Create_Form
from forms.check_kosmos_body import Check_Kosmos_Body_Form
from forms.create_satellite_form import Create_Satellite_Form
from forms.create_star_system_form import Create_Star_System_Form
from forms.create_planet_form import Create_Planet_Form
from forms.create_galaxy_form import Create_Galaxy_Form
from forms.login_form import LoginForm
from forms.catalog_form import CatalogForm
from forms.menu_login import MenuForm
from forms.register_form import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'universe_site_Akim_and_Val_secret_key'  # секретный ключ
app.config['UPLOAD_PATH'] = 'static/uploads'


@app.route('/')  # Начало сайта
def index():
    return render_template('main_window.html')


@app.route('/logout')  # Логирование пользователя
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    db_sess.close()
    return db_sess.query(User).get(user_id)


# Создание космических тел, всё расписаны по каждой категории: create_satellites - создание спутника,
# create_planet - создание планеты, create_star_system -
# создание звездной системы, create_galaxy - создание галактики
# create_satellites - создание спутника
@app.route('/create_satellite', methods=['GET', 'POST'])
def create_satellite():
    form = Create_Satellite_Form()
    form1 = Base_Form()
    if request.method == 'POST':
        if form1.submit_planets.data:
            return redirect('/create_planet')
        if form1.submit_galaxy.data:
            return redirect('/create_galaxy')
        if form1.submit_satellites.data:
            return redirect('/create_satellite')
        if form1.submit_star_systems.data:
            return redirect('/create_star_system')
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
                                       message='Нет такой планеты', form1=form1)
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
                return redirect('/satellite/1')
            db_sess.close()
            return render_template('create_satellite.html', form=form, message='Такой спутник уже есть', form1=form1)
    return render_template('create_satellite.html', form=form, form1=form1)


# create_galaxy - создание галактики
@app.route('/create_galaxy', methods=['GET', 'POST'])
def create_galaxy():
    form = Create_Galaxy_Form()
    form1 = Base_Form()
    if request.method == 'POST':
        if form1.submit_planets.data:
            return redirect('/create_planet')
        if form1.submit_galaxy.data:
            return redirect('/create_galaxy')
        if form1.submit_satellites.data:
            return redirect('/create_satellite')
        if form1.submit_star_systems.data:
            return redirect('/create_star_system')
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
                                   message='Такая галактика уже есть', form1=form1)
    return render_template('create_galaxy.html', form=form, form1=form1)


# create_planet - создание планеты
@app.route('/create_planet', methods=['GET', 'POST'])
def create_planet():
    form = Create_Planet_Form()
    form1 = Base_Form()
    if request.method == 'POST':
        if form1.submit_planets.data:
            return redirect('/create_planet')
        if form1.submit_galaxy.data:
            return redirect('/create_galaxy')
        if form1.submit_satellites.data:
            return redirect('/create_satellite')
        if form1.submit_star_systems.data:
            return redirect('/create_star_system')
        if form.submit_return.data:
            return redirect('/choise_create')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            planet = Planet()
            star_system = db_sess.query(Star_System).filter(Star_System.name == form.star_system.data)
            if not [x for x in star_system]:
                db_sess.close()
                return render_template('create_planet.html', form=form, message='Такой системы нет',
                                       form1=form1)
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
            return render_template('create_planet.html', form=form, form1=form1,
                                   message='Такая планета уже есть')
    return render_template('create_planet.html', form=form, form1=form1)


# create_star_system - создание звездной системы
@app.route('/create_star_system', methods=['GET', 'POST'])
def create_star_system():
    form = Create_Star_System_Form()
    form1 = Base_Form()
    if request.method == 'POST':
        if form1.submit_planets.data:
            return redirect('/create_planet')
        if form1.submit_galaxy.data:
            return redirect('/create_galaxy')
        if form1.submit_satellites.data:
            return redirect('/create_satellite')
        if form1.submit_star_systems.data:
            return redirect('/create_star_system')
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
                return render_template('create_star_system.html', form=form, message='Такой галактики нет', form1=form1)
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
                return redirect('/star_system/1')
            db_sess.close()
            return render_template('create_star_system.html', form=form,
                                   message='Такая звездная система уже есть', form1=form1)
    return render_template('create_star_system.html', form=form, form1=form1)


# Редактирование космических тел, всё расписаны по каждой категории: edit_satellites - редактирование спутника,
# edit_planet - редактирование планеты, edit_star_system -
# редактирование звездной системы, edit_galaxy - редактирование галактики
# edit_galaxy - редактирование галактики
@app.route('/edit_galaxy/<int:id_galaxy>', methods=['GET', 'POST'])
def edit_galaxy(id_galaxy):
    form = Create_Galaxy_Form()
    form1 = Base_Form()
    db_sess = db_session.create_session()
    galaxy = db_sess.query(Galaxies).filter(Galaxies.id == id_galaxy)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/galaxy/1')
    galaxy = galaxy[0]
    if not form.submit.data:
        form.name.data = galaxy.name
        if galaxy.text:
            if os.path.isfile(galaxy.text):
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
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            os.rename('static/uploads/' + filename, 'static/uploads/' + f"{galaxy.name}.{filename.split('.')[-1]}")
            galaxy.photo = 'static/uploads/' + f"{galaxy.name}.{filename.split('.')[-1]}"
        with open('static/uploads_txt/' + galaxy.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        galaxy.text = 'static/uploads_txt/' + galaxy.name + '.txt'
        galaxy.name = form.name.data
        db_sess.add(galaxy)
        db_sess.commit()
        db_sess.close()
        return redirect('/galaxy/1')
    db_sess.close()
    return render_template('create_galaxy.html', form=form, form1=form1)


# edit_star_system - редактирование звездной системы
@app.route('/edit_star_system/<int:id_star_system>', methods=['GET', 'POST'])
def edit_star_system(id_star_system):
    form = Create_Star_System_Form()
    form1 = Base_Form()
    db_sess = db_session.create_session()
    star_system = db_sess.query(Star_System).filter(Star_System.id == id_star_system)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/star_system/1')
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
            return render_template('create_star_system.html', form=form, message='Такой галактики нет')
        else:
            star_system.galaxy = galaxy[0].id
        if uploaded_file.filename:
            if uploaded_file.filename != '':
                if star_system.photo:
                    if os.path.isfile(star_system.photo):
                        os.remove(star_system.photo)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                os.rename('static/uploads/' + filename,
                          'static/uploads/' + f"{star_system.name}.{filename.split('.')[-1]}")
                star_system.photo = 'static/uploads/' + f"{star_system.name}.{filename.split('.')[-1]}"
        with open('static/uploads_txt/' + star_system.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        star_system.text = 'static/uploads_txt/' + star_system.name + '.txt'
        star_system.name = form.name.data
        db_sess.add(star_system)
        db_sess.commit()
        db_sess.close()
        return redirect('/star_system/1')
    db_sess.close()
    return render_template('create_star_system.html', form=form, form1=form1)


# edit_planet - редактирование планеты
@app.route('/edit_planet/<int:id_planet>', methods=['GET', 'POST'])
def edit_planet(id_planet):
    form = Create_Planet_Form()
    form1 = Base_Form()
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
            if uploaded_file.filename != '':
                if planet.photo:
                    if os.path.isfile(planet.photo):
                        os.remove(planet.photo)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                os.rename('static/uploads/' + filename,
                          'static/uploads/' + f"{planet.name}.{filename.split('.')[-1]}")
                planet.photo = 'static/uploads/' + f"{planet.name}.{filename.split('.')[-1]}"
        with open('static/uploads_txt/' + planet.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        planet.text = 'static/uploads_txt/' + planet.name + '.txt'
        planet.name = form.name.data
        db_sess.add(planet)
        db_sess.commit()
        db_sess.close()
        return redirect('/planet/1')
    db_sess.close()
    return render_template('create_planet.html', form=form, form1=form1)


# edit_satellites - Редактирование спутника

@app.route('/edit_satellite/<int:id_satellite>', methods=['GET', 'POST'])
def edit_satellite(id_satellite):
    form = Create_Satellite_Form()
    form1 = Base_Form()
    db_sess = db_session.create_session()
    satellite = db_sess.query(Satellite).filter(Satellite.id == id_satellite)
    if form.submit_return.data:
        db_sess.close()
        return redirect('/satellite/1')
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
            if uploaded_file.filename != '':
                if satellite.photo:
                    if os.path.isfile(satellite.photo):
                        os.remove(satellite.photo)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                os.rename('static/uploads/' + filename,
                          'static/uploads/' + f"{satellite.name}.{filename.split('.')[-1]}")
                satellite.photo = 'static/uploads/' + f"{satellite.name}.{filename.split('.')[-1]}"
        with open('static/uploads_txt/' + satellite.name + '.txt', 'w', encoding='utf-8') as file:
            file.write(form.text.data)
        satellite.text = 'static/uploads_txt/' + satellite.name + '.txt'
        satellite.name = form.name.data
        db_sess.add(satellite)
        db_sess.commit()
        db_sess.close()
        return redirect('/satellite/1')
    db_sess.close()
    return render_template('create_satellite.html', form=form, form1=form1)


# Удаление космических тел, всё расписаны по каждой категории: delete_satellites - удаление спутника,
# delete_planet - удаление планеты, delete_star_system -
# удаление звездной системы, delete_galaxy - удаление галактики
# delete_galaxy - удаление галактики
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


# delete_star_system - удаление звездной системы
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
    return redirect('/star_system/1')


# delete_planet - удаление планеты
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


# delete_satellites - удаление спутника
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
    return redirect('/satellite/1')


# Страницы каталогов для космических тел: satellites - спутник, planet - планета, star_system - звездная система,
# galaxy - галактика
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
        return redirect('/star_system/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_satellites.data:
        return redirect('/satellite/1')
    return render_template('galaxy.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/star_system/<int:page>', methods=['GET', 'POST'])
def star_system(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Star_System).filter(Star_System.id != 1)
    arr = [x for x in arr]
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/star_system/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/star_system/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_planets.data:
        return redirect('/planet/1')
    if form.submit_satellites.data:
        return redirect('/satellite/1')
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
        return redirect('/star_system/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_satellites.data:
        return redirect('/satellite/1')
    return render_template('planet.html', form=form, arr=arr, len_arr=len(arr), page=page)


@app.route('/satellite/<int:page>', methods=['GET', 'POST'])
def satellite(page):
    form = CatalogForm()
    db_sess = db_session.create_session()
    arr = db_sess.query(Satellite)
    arr = [x for x in arr]
    n = abs(-len(arr) // 8)
    arr = [x for x in arr[(page - 1) * 8:page * 8]]
    db_sess.close()
    if form.submit_left_page.data:
        if page > 1:
            return redirect(f'/satellite/{page - 1}')
    if form.submit_right_page.data:
        if page < n:
            return redirect(f'/satellite/{page + 1}')
    if form.submit_return.data:
        return redirect('/')
    if form.submit_galaxy.data:
        return redirect('/galaxy/1')
    if form.submit_planets.data:
        return redirect('/planet/1')
    if form.submit_choise_create.data:
        return redirect('/choise_create')
    if form.submit_star_systems.data:
        return redirect('/star_system/1')
    return render_template('satellites.html', form=form, arr=arr, len_arr=len(arr), page=page)


#  Выбор создания космических тел
@app.route('/choise_create', methods=['GET', 'POST'])
def choise_create():
    form = Choise_Create_Form()
    if form.submit_create_galaxy.data:
        return redirect('/create_galaxy')
    if form.submit_create_star_system.data:
        return redirect('/create_star_system')
    if form.submit_create_planet.data:
        return redirect('/create_planet')
    if form.submit_satellite.data:
        return redirect('/create_satellite')
    if form.submit_return.data:
        return redirect('/galaxy/1')
    return render_template('choise_create.html', form=form)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    message = [-1, '']
    if form.submit_return.data:
        return redirect('/')
    if form.validate_on_submit():
        message = [1, 'Пароль должен быть: больше 8 символов, минимум 1 латинаская буква,'
                      ' минимум 1 цифра']
        password = form.password.data
        flag_lat = False
        flag_len = len(password) > 8
        flag_enum = False
        flag_digit = False
        if not flag_len:
            return render_template('register.html', form=form, message=message)
        aplh = 'abcdefghijklmnopqrstuvwxyz'
        for x in password.lower():
            if flag_enum and flag_len and flag_lat and flag_digit:
                break
            if x.isdigit():
                flag_digit = True
            if x in aplh:
                flag_lat = True
            if x.isalnum():
                flag_enum = True
        if not (flag_enum and flag_len and flag_lat and flag_digit):
            return render_template('register.html', form=form, message=message)
        if form.password.data != form.password_repeat.data:
            message = [2, 'Пароли не совпадают']
            return render_template('register.html', form=form,
                                   message=message)
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
        message = [3, 'Пользователь с такой почтой уже есть']
        return render_template('register.html', form=form, message=message)
    return render_template('register.html', form=form, message=message)


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = [-1, '']
    if form.submit_return.data:
        return redirect('/')
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.login_email.data).first()
        db_sess.close()
        message = [1, 'Неправильный пароль']
        if not user:
            message = [0, 'Нет пользователя с такой почтой']
            return render_template('login.html', form=form, message=message)
        if user.check_password(form.password.data):
            login_user(user)
            return redirect('/')
        return render_template('login.html', message=message, form=form)
    return render_template('login.html', form=form, message=message)


# Рассмотр космических объектов

@app.route('/check_kosmos_body/<int:id_kosmos_body>/<name>', methods=['GET', 'POST'])
def check_kosmos_body(id_kosmos_body, name):
    db_sess = db_session.create_session()
    form = Check_Kosmos_Body_Form()
    title = ''
    kosmos_body = ''
    if name == 'galaxy':
        kosmos_body = Galaxies
        title = 'Галактика'
    if name == 'planet':
        kosmos_body = Planet
        title = 'Планета'
    if name == 'satellite':
        kosmos_body = Satellite
        title = 'Спутник'
    if name == 'star_system':
        kosmos_body = Star_System
        title = 'Звездная система'
    if form.submit_return.data:
        return redirect(f'/{name}/1')
    kosmos_body = db_sess.query(kosmos_body).filter(kosmos_body.id == id_kosmos_body)[0]
    db_sess.close()
    text = ''
    if kosmos_body.text:
        if os.path.isfile(kosmos_body.text):
            with open(kosmos_body.text, 'r', encoding='utf-8') as file:
                text = file.readlines()
    photo = ''
    if kosmos_body.photo:
        if os.path.isfile(kosmos_body.photo):
            photo = kosmos_body.photo
    return render_template(f'check_kosmos_body.html', form=form, kosmos_body=kosmos_body, text=text, photo=photo,
                           title=title)


# Профиль авторизованного человека
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


# Запрос для тг бота
@app.route('/tg_get', methods=['GET'])
def tg_get():
    db_sess = db_session.create_session()
    all_data = db_sess.query(User)
    return jsonify([{'id': data.name, 'text': data.email} for data in all_data])


if __name__ == '__main__':
    db_session.global_init(f"db/universe_site.sqlite")  # В глобальную переменную для бд кладу бд
    app.run(port=8080, host='127.0.0.1')  # Запуск сайта
