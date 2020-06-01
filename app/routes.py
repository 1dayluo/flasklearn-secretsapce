from app import app,login
from flask import render_template, flash, redirect, url_for
from app.models import User,Post
from app.forms import LoginForm, RegisterForm,PostForm
from app.operation import *
from flask_login import login_user,logout_user, current_user,login_required

@app.route('/')
@app.route('/index')
def index():
    user = {
        'username':'hx'
    }

    if current_user.is_authenticated:
        flash("已经登陆啦")
        user = current_user
    return render_template('index.html', title='蛋憨 - Secret Space', user=current_user)
@app.route('/error')
def error():
    return render_template('error.html', title='Error- >-<哎呀出错啦！都怪憨憨太憨啦（bu')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('已经登陆啦！{}'.format(current_user))
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash('Login requested for user {},remember me={}'.format(form.username.data, form.remember_me.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # return redirect(url_for('error'))
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('已经登陆啦！{}'.format(current_user))
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Register success!注册成功！User:{}'.format(form.username.data))
        print(form.username.data)
        add_user(form.username.data, form.email.data, form.password.data)
        return redirect(url_for('login'))

    return render_template('register.html', title='蛋憨 - 注册用户 Secret Space', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/published', methods=['GET', 'POST'])
@login_required
def published():
    form = PostForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            print(current_user)
            post = Post(title=form.title.data,body=form.content.data, user_id=current_user.id, author=form.author.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post_page',pid=post.id))
    return render_template('published.html', title='发表新的文章', form=form)
@app.route('/post/<pid>')
@login_required
def post_page(pid):
    flash(current_user.id)
    post = Post.query.filter_by(user_id=current_user.id, id=pid).first_or_404()

    return render_template("post.html", title=post.title, post=post)
