from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import random
import datetime
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
import pymysql
from django.db import connection
from datetime import datetime
@require_http_methods(['GET', 'POST'])
def warehouse(request):
    if request.method == 'GET':
        admin = request.GET.get('admin')
        # 显示管理仓库中所有武器
        print(admin)
        cursor = connection.cursor()
        sql = '''SELECT app00_reg_log_admin.warehouse_id
                             from app00_reg_log_admin
                             where admin_name = %s;'''
        cursor.execute(sql, [admin])
        warehouse_id = cursor.fetchall()
        print(warehouse_id)
        warehouse_id = warehouse_id[0][0]


        print(warehouse_id)
        cursor = connection.cursor()
        sql = '''SELECT app00_reg_log_warehouse.warehouse_id   as 仓库编号,
                       app00_reg_log_warehouse.warehouse_name as 仓库名,
                       app00_reg_log_weapon.weapon_id         as 武器编号,
                       weapon_type                            as 武器类型,
                       weapon_price                           as 武器价格,
                       app00_reg_log_weapon.name              as 武器名,
                       app00_reg_log_weapon.src               as img
                FROM app00_reg_log_warehouse,
                     app00_reg_log_warehouseweapon,
                     app00_reg_log_weapon
                WHERE app00_reg_log_warehouseweapon.weapon_id = app00_reg_log_weapon.weapon_id
                  AND app00_reg_log_warehouse.warehouse_id = app00_reg_log_warehouseweapon.warehouse_id
                  AND app00_reg_log_warehouse.warehouse_id = %s;'''
        cursor.execute(sql, int(warehouse_id))
        cursor.close()
        rows = cursor.fetchall()  # 获取所有结果
        for row in rows:
            print(row)  # 输出每行结果
        return render(request, 'warehouse.html', {"weapon_list": rows, "admin": admin})

    elif request.method == 'POST':
        admin = request.POST.get('admin')
        cursor = connection.cursor()
        sql = '''SELECT      app00_reg_log_admin.warehouse_id
                             from app00_reg_log_admin
                             where admin_name = %s;'''
        cursor.execute(sql, [admin])
        print(admin)
        warehouse_id = cursor.fetchall()
        warehouse_id = warehouse_id[0][0]
        print(warehouse_id)
        Wtype = request.POST.get('type')
        price = request.POST.get('price')
        name = request.POST.get('name')
        src = request.POST.get('src')
        factor_id = request.POST.get('fac')
        print(f"{Wtype} {price} {name} {src}{factor_id}")
        cursor.close()
        cursor = connection.cursor()
        sql = '''INSERT INTO app00_reg_log_weapon(weapon_type, weapon_price, name, src)
                 VALUE (%s, %s, %s, %s);'''
        cursor.execute(sql, [Wtype, price, name, src])

        sql = '''select weapon_id FROM app00_reg_log_weapon
        where app00_reg_log_weapon.weapon_id not in(
        select weapon_id
        From app00_reg_log_factoryweapon)'''
        cursor.execute(sql)
        new_id = cursor.fetchall()
        new_id = new_id[0][0]
        cursor.close()
        print(new_id)

        cursor = connection.cursor()
        sql = '''INSERT INTO app00_reg_log_factoryweapon(factory_id, weapon_id)
                 VALUE (%s, %s);'''
        cursor.execute(sql, [factor_id, new_id])
        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        sql = '''    INSERT INTO app00_reg_log_warehouseweapon(warehouse_id, weapon_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE  weapon_id = VALUES(weapon_id);'''
        cursor.execute(sql, (int(warehouse_id), int(new_id)))
        connection.commit()
        cursor.close()

        return HttpResponse("入库成功")


@require_http_methods(['GET', 'POST'])
def orders(request):
    return render(request, 'admin_orders.html')

