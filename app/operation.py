from app.models import User
from app import db
def add_user(username, email, password):
    """
    :description
        增添新用户
    """
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print('Some Error!', e)
        return False
    finally:
        return True

def userslist():
    """
    :description
        获取用户表单
    """
    users = User.query.all()
    return users

def get_designated_user(user):
    """
    :description:
        获取指定用户
    :param user:
    :return:
    """
    user = User.query.get(user)
    return user

