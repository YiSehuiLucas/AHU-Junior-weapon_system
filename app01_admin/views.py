from django.shortcuts import render, redirect, HttpResponse
#鲁正扬作品
#拼音都是CJA干的
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

        cursor = connection.cursor()
        sql = '''SELECT weapon_type as 武器类型,
                       COUNT(*) as 武器数量
                FROM app00_reg_log_warehouse, app00_reg_log_warehouseweapon, app00_reg_log_weapon
                WHERE app00_reg_log_warehouseweapon.weapon_id = app00_reg_log_weapon.weapon_id AND
                      app00_reg_log_warehouse.warehouse_id = app00_reg_log_warehouseweapon.warehouse_id AND
                      app00_reg_log_warehouse.warehouse_id = %s
                GROUP BY app00_reg_log_warehouse.warehouse_id, app00_reg_log_warehouse.warehouse_name, weapon_type ;'''
        cursor.execute(sql, int(warehouse_id))
        cursor.close()
        rowslei = cursor.fetchall()  # 获取所有结果

        for row in rows:
            print(row)  # 输出每行结果
        return render(request, 'warehouse.html', {"weapon_list": rows,"weapon_leilist": rowslei, "admin": admin})

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
        if Wtype and price and price and name and src and factor_id:
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
        else:
            return JsonResponse({"error": "数据不完整"}, status=400)


@require_http_methods(['GET', 'POST'])
def orders(request):
    if request.method == 'GET':
        admin = request.GET.get('admin')
        print(admin)

        cursor = connection.cursor()
        sql = '''select warehouse_id
                 from app00_reg_log_admin
                 where admin_name = %s'''
        cursor.execute(sql, admin)
        warehouse_id = cursor.fetchall()
        warehouse_id = warehouse_id[0][0]
        cursor.close()

        cursor = connection.cursor()
        sql = '''select app00_reg_log_order.order_id      as 订单号,
                       app00_reg_log_order.weapon_id     as 武器号,
                       app00_reg_log_order.order_date    as 下单时间,
                       app00_reg_log_order.statement     as 订单状态,
                       app00_reg_log_order.user_name     as 用户,
                       app00_reg_log_order.warehouse_id  as 仓库编号,
                       app00_reg_log_weapon.weapon_type  as 武器类型,
                       app00_reg_log_weapon.weapon_price as 价格,
                       app00_reg_log_weapon.name         as 武器名称,
                       app00_reg_log_factoryweapon.factory_id as 工厂号
                from app00_reg_log_order,
                     app00_reg_log_weapon,
                     app00_reg_log_factoryweapon
                WHERE warehouse_id = %s
                  and app00_reg_log_order.weapon_id = app00_reg_log_weapon.weapon_id
                  and app00_reg_log_order.weapon_id = app00_reg_log_factoryweapon.weapon_id;'''
        cursor.execute(sql, warehouse_id)
        order_list = cursor.fetchall()
        cursor.close()
        print(order_list)

        cursor = connection.cursor()
        sql = '''select app00_reg_log_weapon.weapon_type as 武器类型,
                       COUNT(*) as 武器数量
                from app00_reg_log_weapon
                where       app00_reg_log_weapon.weapon_id in
                (
                    SELECT app00_reg_log_order.weapon_id
                    from app00_reg_log_order
                    where order_date>=CURDATE()-1 AND
                          order_date < CURDATE() AND
                          statement = '已处理' and
                          app00_reg_log_order.warehouse_id = %s
                    )
                GROUP BY app00_reg_log_weapon.weapon_type ;'''
        cursor.execute(sql,warehouse_id)
        order_jinlist = cursor.fetchall()
        cursor.close()
        print(admin)
        return render(request, 'admin_orders.html', {'order_list': order_list,
                                                     'order_jinlist': order_jinlist,
                                                     'admin': admin,
                                                     'warehouse_id': warehouse_id})

    elif request.method == 'POST':
        # 出库功能
        order_id = request.POST.get('order_id')
        warehouse_id = request.POST.get('warehouse_id')
        weapon_id = request.POST.get('weapon_id')

        cursor = connection.cursor()
        sql = '''UPDATE app00_reg_log_order
                 SET statement='已处理'
                 where order_id=%s;
                 '''
        cursor.execute(sql, order_id)
        connection.commit()
        print(warehouse_id)
        print(weapon_id)
        cursor.close()
        cursor = connection.cursor()
        sql = '''delete from app00_reg_log_warehouseweapon
                 where weapon_id = %s and
                 warehouse_id = %s;
                 '''
        cursor.execute(sql, [weapon_id, warehouse_id])
        connection.commit()
        cursor.close()
        return render(request, 'deliver_goods_successsful.html')

@require_http_methods(['GET', 'POST'])
def warehouse_info(request):
    if request.method == "GET":
        username = request.GET.get('admin')
    else:
        username = request.POST.get('admin')
    user = username
    return render(request, 'warehouse_info.html', {"admin": user})

def backA(request):
    if request.method == "GET":
        username = request.GET.get('admin')
    else:
        username = request.POST.get('admin')
    user = username
    return render(request, "admin_main.html", {"admin": user})
