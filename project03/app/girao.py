
             #Get orders to be deleted.
                cur.execute(
                    """
                SELECT o.order_no, o.cust_no
                FROM orders o
                WHERE o.cust_no = %(cust_no)s;
                """,
                    {"cust_no": cust_no},
                    # prepare=True,
                )
                orders = cur.fetchall()

                full_process_sql = ""
                # Delete those orders from 'process'.
                for order in orders:
                    #order_no is not user-controlled input: statement doesn't need further  psycopg3 sanitization.
                    full_process_sql += f"DELETE from process WHERE process.order_no={order.order_no}"

                cur.execute(full_process_sql)