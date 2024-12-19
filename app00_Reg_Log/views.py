from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Users, Admin
from .models import Weapon
import random
# 登陆/注册/登陆成功
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # 普通用户登陆
    elif request.POST.get('identity') == 'user':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = Users.objects.filter(user_name=username).first()
        use = user.check_password1(password)
        print(user)
        if use:
            gun_list1 = []
            gun_list2 = []
            for i in range(3):
                index = random.randint(1, 30)
                guns = Weapon.objects.get(weapon_id=index)
                temp1 = {
                    "name": guns.name,
                    "srd": guns.src,
                    "price": guns.weapon_price,
                    "type": guns.weapon_type
                }
                gun_list1.append(temp1)

                index = random.randint(1, 30)
                guns = Weapon.objects.get(weapon_id=index)
                temp2 = {
                    "name": guns.name,
                    "srd": guns.src,
                    "price": guns.weapon_price,
                    "type": guns.weapon_type
                }
                gun_list2.append(temp2)
                # print(f"{guns.weapon_id} {guns.weapon_type} {guns.weapon_price} {guns.name} {guns.src}")
            print(gun_list2)
            print(gun_list1)
            user = username
            return render(request, "user_main.html", {"row1": gun_list1, "row2": gun_list2, "user": user})
        else:
            return JsonResponse({"用户名或密码错误": "用户名或密码错误"})
    # 管理员登陆
    elif request.POST.get('identity') == 'admin':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = Admin.objects.filter(admin_name=username).first()
        use = user.check_password(password)
        if use:
            user = username
            return render(request, "admin_main.html", {"admin": user})
        else:
            return JsonResponse({"用户名或密码错误": "用户名或密码错误"})
    else:
        return render(request, '404.html')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    # 普通用户注册
    elif request.POST.get('identity') == 'user':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        # 确保不会存在相同用户名的用户
        if not Users.objects.filter(user_name=username).first():
            Users.objects.create_user(user_name=username, user_pwd=password)
            Users.objects.filter(user_name=username).update(user_pwd=password)
            return JsonResponse({"注册成功": "注册成功"})
        else:
            return JsonResponse({"用户已存在": "用户已存在"})
    # 管理员注册
    elif request.POST.get('identity') == 'admin':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        # 确保不会存在相同用户名的用户
        if not Admin.objects.filter(admin_name=username).first():
            Admin.objects.create_admin(admin_name=username, admin_pwd=password)
            Admin.objects.filter(admin_name=username).update(admin_pwd=password)
            return JsonResponse({"注册成功": "注册成功"})
        else:
            return JsonResponse({"管理员已存在": "管理员已存在"})
    else:
        return render(request, '404.html')
