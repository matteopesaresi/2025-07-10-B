from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categories():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from categories"

        cursor.execute(query)

        for row in cursor:
            results.append((row["category_id"],row["category_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_nodes(categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from products 
where category_id = %s"""

        cursor.execute(query,(categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_edges(category,data1,data2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select  p.product_id , SUM(oi.quantity) as peso
from order_items oi , products p , orders o 
where p.category_id = %s and p.product_id = oi.product_id and o.order_id =oi.order_id 
and o.order_date between %s and %s
group by p.product_id"""

        cursor.execute(query, (category, data1, data2,) )

        for row in cursor:
            results.append((row["product_id"],row["peso"]))

        cursor.close()
        conn.close()
        return results