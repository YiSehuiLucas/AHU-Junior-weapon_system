import datetime
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
import pymysql
from django.db import connection
from datetime import datetime


# Create your views here.
#
@require_http_methods(['GET', 'POST'])
def market(request):
    if request.method == "GET":
        user = request.GET.get('user')
        cursor = connection.cursor()
        sql = '''select  app00_reg_log_weapon.weapon_id as 武器编号,
                        app00_reg_log_weapon.weapon_type as 武器类型,
                        app00_reg_log_weapon.name as 名称,
                        app00_reg_log_weapon.weapon_price as 武器价格,
                        app00_reg_log_warehouse.warehouse_name as 仓库名,
                        app00_reg_log_weapon.src,
                        app00_reg_log_warehouse.warehouse_id 
                from app00_reg_log_weapon,app00_reg_log_warehouseweapon,app00_reg_log_warehouse
                where app00_reg_log_weapon.weapon_id = app00_reg_log_warehouseweapon.weapon_id
                and app00_reg_log_warehouseweapon.warehouse_id = app00_reg_log_warehouse.warehouse_id;'''
        cursor.execute(sql)
        cursor.close()
        rows = cursor.fetchall()  # 获取所有结果
        for row in rows:
            print(row)  # 输出每行结果
            print(row[0])
        return render(request, 'market.html', {"list": rows, 'user': user})

    # 点击购买按钮
    elif request.method == "POST":
        item_0 = request.POST.get('item_0')
        item_1 = request.POST.get('item_1')
        item_2 = request.POST.get('item_2')
        item_3 = request.POST.get('item_3')
        item_4 = request.POST.get('item_4')
        item_5 = request.POST.get('item_5')
        item_6 = request.POST.get('item_6')
        user = request.POST.get('user')
        print(f"{item_1} {item_0} {item_2} {item_3} {item_4} {user} /n {item_5}")
        cursor = connection.cursor()
        sql = '''
        INSERT INTO app00_reg_log_order (order_date, statement, user_name, warehouse_id, weapon_id)
         VALUES (%s, %s, %s, %s, %s);'''
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(formatted_time)  # 输出类似 '2024-12-13 12:00:00'
        cursor.execute(sql, (formatted_time, '未处理', user, int(item_6), int(item_0)))
        connection.commit()
        cursor.close()
        return HttpResponse("购买成功")

    else:
        return render(request, "404.html")


@require_http_methods(['GET', 'POST'])
def orders(request):
    if request.method == 'GET':
        print(request.GET.get('user'))
        user = request.GET.get('user')
        cursor = connection.cursor()
        sql = '''SELECT app00_reg_log_order.order_id      as 订单号,
                       app00_reg_log_order.weapon_id     as 武器号,
                       app00_reg_log_order.order_date    as 下单时间,
                       app00_reg_log_order.statement     as 订单状态,
                       app00_reg_log_order.warehouse_id  as 仓库编号,
                       app00_reg_log_weapon.weapon_type  as 武器类型,
                       app00_reg_log_weapon.weapon_price as 价格,
                       app00_reg_log_weapon.name         as 武器名称,
                       app00_reg_log_weapon.src          as 图片连接
                FROM app00_reg_log_order,
                     app00_reg_log_weapon
                WHERE user_name = %s
                  and app00_reg_log_order.weapon_id = app00_reg_log_weapon.weapon_id;'''
        cursor.execute(sql, user)
        cursor.close()
        rows = cursor.fetchall()  # 获取所有结果
        for row in rows:
            print(row)  # 输出每行结果
            print(row[2])
            print(type(row[2]))
        return render(request, 'orders.html', {"list": rows, 'user': user})

    elif request.method == 'POST':
        order_id = request.POST.get('order_id')
        statement = request.POST.get('statement')
        if statement == '未处理':
            cursor = connection.cursor()
            sql = '''DELETE FROM app00_reg_log_order
                    WHERE order_id=%s AND
                          statement='未处理';'''
            cursor.execute(sql, order_id)
            cursor.close()
            print(order_id)
            print(statement)
            return HttpResponse("撤销成功")
        elif statement == '已处理':
            return HttpResponse("已发货")
        else:
            return render(request, '404.html')


