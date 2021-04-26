from flask import Flask, render_template, request, abort
from werkzeug.utils import redirect, secure_filename
from data import db_session
from forms.authorization import Authorization
from forms.registration import Registration
from forms.news_form import NewsForm
from forms.game_form import GameForm
from forms.game_view_form import GameViewForm
from forms.add_comment import AddCommentForm
from data.users import User
from data.news import News
from data.games import Game
from flask_login import login_user, LoginManager, current_user, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = './uploads'
db_session.global_init("db/TB.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/authorisation', methods=['GET', 'POST'])
def authorisation():
    form = Authorization()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main_menu")
        return render_template('authorization.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = Registration()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/main_menu')
    return render_template('registration.html', form=form)


@app.route('/main_menu')
def main_menu():
    return render_template("main_menu.html")


@app.route('/shop')
def shop():
    db_sess = db_session.create_session()
    games = db_sess.query(Game)
    return render_template("shop.html", games=games)


@app.route('/game', methods=['GET', 'POST'])
def game():
    db_sess = db_session.create_session()
    games = db_sess.query(Game)
    form = GameForm()
    if form.validate_on_submit():
        game2 = Game()
        game2.designation = form.title.data
        game2.short_description_of_game = form.short_content.data
        game2.full_description_of_game = form.full_content.data
        game2.price = form.price.data
        current_user.games.append(game2)
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            game2.icon = file_path
        file1 = request.files['file']
        if file1:
            filename1 = secure_filename(file1.filename)
            file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            file1.save(file_path1)
            game2.game_files = file_path1
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/shop')
    return render_template("game.html", form=form, games=games)


@app.route('/game/<int:id>', methods=['GET', 'POST'])
def game_view(id):
    db_sess = db_session.create_session()
    game1 = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
    form = GameViewForm()
    if form.validate_on_submit():
        current_user.library.append(game1)
        db_sess.merge(current_user)
        db_sess.commit()
    return render_template('game_view.html', game=game1, form=form)


@app.route('/game_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def game_edit(id):
    form = GameForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        game1 = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
        if game1:
            form.title.data = game1.designation
            form.short_content.data = game1.short_description_of_game
            form.full_content.data = game1.full_description_of_game
            form.price.data = game1.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game2 = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
        if game2:
            game2.designation = form.title.data
            game2.short_description_of_game = form.short_content.data
            game2.full_description_of_game = form.full_content.data
            game2.price = form.price.data
            db_sess.commit()
            return redirect('/shop')
        else:
            abort(404)
    return render_template('game.html', form=form)


@app.route('/game_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def game_delete(id):
    db_sess = db_session.create_session()
    game1 = db_sess.query(Game).filter(Game.id == id, Game.user == current_user).first()
    if news:
        db_sess.delete(game1)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/shop')


@app.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    db_sess = db_session.create_session()
    news1 = db_sess.query(News)
    return render_template("news.html", news=news1)


@app.route('/article', methods=['GET', 'POST'])
def article():
    db_sess = db_session.create_session()
    news1 = db_sess.query(News)
    form = NewsForm()
    if form.validate_on_submit():
        news2 = News()
        news2.title = form.title.data
        news2.description = form.content.data
        news2.href = form.href.data
        current_user.news.append(news2)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/news')
    return render_template("article.html", form=form, news=news1)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news1 = db_sess.query(News).filter(News.id == id,
                                           News.user == current_user
                                           ).first()
        if news1:
            form.title.data = news1.title
            form.content.data = news1.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news2 = db_sess.query(News).filter(News.id == id,
                                           News.user == current_user
                                           ).first()
        if news2:
            news2.title = form.title.data
            news2.description = form.content.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('article.html', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news')


@app.route('/library')
def library():
    return render_template("library.html")


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')