from django.contrib.auth.backends import BaseBackend
from .models import Users, Admin

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, identity=None):
        """
        自定义认证逻辑。
        根据身份信息选择是查询 Users 表还是 Admin 表。
        """
        if identity == 'user':  # 如果是普通用户
            try:
                user = Users.objects.get(user_name=username)
                if user.check_password(password):  # 使用 Django 的密码校验方法
                    return user
            except Users.DoesNotExist:
                return None
        elif identity == 'admin':  # 如果是管理员
            try:
                admin = Admin.objects.get(admin_name=username)
                if admin.check_password(password):  # 使用 Django 的密码校验方法
                    return admin
            except Admin.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        """
        根据用户 ID 获取用户实例。
        """
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            try:
                return Admin.objects.get(pk=user_id)
            except Admin.DoesNotExist:
                return None
