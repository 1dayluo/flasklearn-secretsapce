from app import app,login
from flask import render_template, flash, redirect, url_for, request
from app.models import User,Post
from app.forms import LoginForm, RegisterForm,PostForm,UploadAvatar,EditProfileForm
from app.operation import *
from flask_login import login_user,logout_user, current_user,login_required
import os
from werkzeug.utils import secure_filename
from sqlalchemy import desc
@app.route('/')
@app.route('/index')
def index():
    page = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page',2))
    posts = Post.query.order_by(Post.id.desc())

    if current_user.is_authenticated:
        flash("已经登陆啦")
        user = current_user
    return render_template('index.html', title='蛋憨 - Secret Space', user=current_user,posts=posts)
@app.route('/error')
def error():
    return render_template('error.html', title='Error- >-<哎呀出错啦！都怪憨憨太憨啦（bu')


def allowed_file(filename):
    """
    对文件名安全过滤
    :param filename:
    :return:
    """
    return True
@login_required
@app.route('/<username>/avatar', methods=['GET','POST'])
def avatar_set(username):
    username = current_user.username
    form = EditProfileForm()
    if form.validate_on_submit():
        file = form.avatar.data

        # filename = secure_filename(file.filename)
        if file and allowed_file(file):
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], "{}.jpg".format(current_user.id))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "{}.jpg".format(current_user.id)))
            current_user.avatar = "{}.jpg".format(current_user.id)
            db.session.commit()
            # set_avatar(current_user.id, "{}.jpg".format(current_user.id))
            return redirect(url_for('userpage',username=username))


    return render_template('upload_avatar.html', title='上传你的头像把',form=form)
@login_required
@app.route('/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    username = current_user.username
    form = EditProfileForm()
    if form.validate_on_submit():
        file = form.avatar.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        # filename = secure_filename(file.filename)
        if file and allowed_file(file):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "{}.jpg".format(current_user.id)))
            set_avatar(current_user.id, "{}.jpg".format(current_user.id))

        if not file:
            pass
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.avatar.data = current_user.avatar
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='修改用户资料',form=form)

@login_required
@app.route('/<username>')
def userpage(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id)

    # posts = {}
    # print('-------------', posts.author.username)

    return render_template('userpage.html', user=user, posts=posts)

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
    mkd = '''
    # header
    ## header2
    [picture](http://www.example.com)
    * 1
    * 2
    * 3
    **bold**
    '''
    form = PostForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            print(current_user)
            post = Post(title=form.title.data,body=form.content.data, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('post_page',pid=post.id))
    return render_template('published.html', title='发表新的文章', form=form)
@app.route('/post/<pid>')
def post_page(pid):
    post = Post.query.filter_by(id=pid).first_or_404()

    return render_template("post.html", title=post.title, post=post)
