import psycopg2
import random

conn = psycopg2.connect(dbname="postgres", user="postgres", password="2004")
cur = conn.cursor()
print('db: database connected')


class db1:
    def user_check(tg_id, tg_login):
        q = """select tg_login from users where tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        if not tmp:
            q2 = """insert into users(tg_id, tg_login) values(%s, %s)"""
            v = (tg_id, tg_login)
            cur.execute(q2, v)
            conn.commit()

    def categories_check():
        q = """select * from categories"""
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        return tmp

    def categories_num_check():
        q = """select * from categories"""
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        tmp2 = []
        for i in tmp:
            tmp2 += str(i[0])
        print(tmp2)
        return tmp2

    def categories_name_check(cat_id):
        q = """select * from categories where cat_id = '{}'""".format(cat_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        print(tmp)
        res = str(tmp[0][1]) + ', ' + str(tmp[0][2]) + ' KZT.'
        return res

    def order_set(tg_id, cat_id):
        q = """insert into orders(ord_tg_id, ord_cat_id) values(%s, %s)"""
        v = (tg_id, cat_id)
        cur.execute(q, v)
        conn.commit()

    def order_delete(tg_id):
        q = """delete from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        conn.commit()

    def order_add_amount(tg_id, amount):
        q = """UPDATE orders SET ord_amount = '{}' WHERE ord_tg_id = '{}'""".format(amount, tg_id)
        cur.execute(q)
        conn.commit()

    def orber_cat_id_check(tg_id):
        q = """select * from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = cur.fetchall()
        return tmp[0][2]

    def orber_check_summ(cat_id, amount):
        q = """select * from categories where cat_id = '{}'""".format(cat_id)
        cur.execute(q)
        tmp = cur.fetchall()
        return str(int(tmp[0][2]) * int(amount))

    def order_add_summ(tg_id, summ):
        q = """UPDATE orders SET ord_summ = '{}' WHERE ord_tg_id = '{}'""".format(summ, tg_id)
        cur.execute(q)
        conn.commit()

    def order_status_give(tg_id):
        q = """select ord_status from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        if not tmp[0][0]:
            q2 = """UPDATE orders SET ord_status = '{}' WHERE ord_tg_id = '{}'""".format('payment', tg_id)
            cur.execute(q2)
            conn.commit()

    def order_secret_code_check(tg_id):
        q = """select secret_code from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        if not tmp[0][0]:
            return True
        else:
            return False

    def order_secret_code(tg_id):
        q = """select secret_code from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        if not tmp[0][0]:
            code = str(random.randint(1, 1000))
            summ = db1.order_summ_give(tg_id)
            tmp = [code, summ]
            q2 = """UPDATE orders SET secret_code = '{}' WHERE ord_tg_id = '{}'""".format(code, tg_id)
            cur.execute(q2)
            conn.commit()
            return tmp

    def order_secret_code_give(tg_id):
        q = """select secret_code from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        return tmp[0][0]

    def order_summ_give(tg_id):
        q = """select ord_summ from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        return tmp[0][0]

    def order_status_give_done(code):
        q = """select ord_id from orders where secret_code = '{}'""".format(code)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        print(tmp)
        if not tmp:
            return 'Заказа с таким кодом оплаты не существует!'
        else:
            q2 = """UPDATE orders SET ord_status = '{}' WHERE secret_code = '{}'""".format('done', code)
            cur.execute(q2)
            conn.commit()
            return 'Заказ подтвержден!'

    def order_done_check(tg_id):
        q = """select ord_status from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = []
        tmp += cur.fetchall()
        print(tmp[0][0])
        if tmp[0][0] == 'done':
            return True
        else:
            return False

    def add_accounts(cat_id, accs):
        for i in range(len(accs)):
            q = """insert into accounts(acc_cat_id, acc) values(%s, %s)"""
            v = (cat_id, accs[i])
            cur.execute(q, v)
            conn.commit()

    def add_cat(name, price):
        q = """insert into categories(cat_name, price) values(%s, %s)"""
        v = (name, price)
        cur.execute(q, v)
        conn.commit()

    def delete_cat(cat_id):
        q = """delete from categories where cat_id = '{}'""".format(cat_id)
        cur.execute(q)
        conn.commit()

    def delete_accs(acc_cat_id):
        q = """delete from accounts where acc_cat_id = '{}'""".format(acc_cat_id)
        cur.execute(q)
        conn.commit()

    def check_accs_amount(acc_cat_id):
        q = """select acc_id from accounts where acc_cat_id = '{}'""".format(acc_cat_id)
        cur.execute(q)
        tmp = cur.fetchall()
        print(len(tmp))
        return len(tmp)

    def return_amount_mass(cat_id):
        len = db1.check_accs_amount(cat_id)
        a = list(range(1, len+1))
        m = map(str, a)
        mass = list(m)
        return mass

    def return_summ_code(code):
        q = """select ord_summ from orders where secret_code = '{}'""".format(code)
        cur.execute(q)
        tmp = cur.fetchall()
        return tmp[0][0]

    def return_code_ord(code):
        q = """select ord_summ from orders where secret_code = '{}'""".format(code)
        cur.execute(q)
        tmp = cur.fetchall()
        if not tmp:
            return False
        else:
            return True

    def give_acc_and_del(cat_id):
        q = """select acc, acc_id from accounts where acc_cat_id = '{}'""".format(cat_id)
        cur.execute(q)
        tmp = cur.fetchone()
        q2 = """delete from accounts where acc_id = '{}'""".format(tmp[1])
        cur.execute(q2)
        conn.commit()
        return tmp[0]

    def orber_amount_check1(tg_id):
        q = """select * from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        tmp = cur.fetchall()
        return tmp[0][3]

    def order_close(tg_id):
        q = """delete from orders where ord_tg_id = '{}'""".format(tg_id)
        cur.execute(q)
        conn.commit()
        q2 = """select orders_summ from users where tg_id = '{}'""".format(tg_id)
        cur.execute(q2)
        tmp = cur.fetchall()
        res = int(tmp[0][0]) + 1
        q3 = """update users set orders_summ = '{}' where tg_id = '{}'""".format(res, tg_id)
        cur.execute(q3)
        conn.commit()

    def return_orders_summ(tg_id):
        q2 = """select orders_summ from users where tg_id = '{}'""".format(tg_id)
        cur.execute(q2)
        tmp = cur.fetchall()
        return tmp[0][0]

    def user_id_check(username):
        try:
            q = """select tg_id from users where tg_login = '{}'""".format(username)
            cur.execute(q)
            tmp = cur.fetchall()
            print('tmp user id' + str(tmp[0][0]))
            return tmp[0][0]
        except:
            print('wow')
            return False
