#!/usr/bin/python3
from logging.config import dictConfig

import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool


# postgres://{user}:{password}@{hostname}:{port}/{database-name}
DATABASE_URL = "postgres://db:db@postgres/db"

pool = ConnectionPool(conninfo=DATABASE_URL)
# the pool starts connecting immediately.

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
log = app.logger


@app.route("/", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def index():
    """WebUI homepage."""
    return render_template("index.html")


@app.route("/customer", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def customer():
    """Customer management page."""
    return render_template("customer/index.html")


#----------------------------------------
#               Order
#----------------------------------------


@app.route("/order", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def order_index():
    """Order management page."""
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
               SELECT order_no, cust_no, date
               FROM orders
               ORDER BY date DESC;
               """,
                {},
                # prepare=True,
            )
            orders = cur.fetchmany(10)
            log.debug(f"Found {cur.rowcount} rows.")
    
    
    return render_template("order/index.html", orders = orders)

@app.route("/order/add", methods=("GET", "POST"))
def order_add():
    """Add a new order."""
    if request.method == "POST":
        order_no = request.form["order_no"]
        cust_no = request.form["cust_no"]
        date = request.form["date"]
    
        error = None

        # VERIFICAR SE EXISTEM???
        if not order_no:
            error = "Order Number is required."

        if not cust_no:
            error = "Customer Number is required."

        if not date:
            error = "Date is required."


        if error is not None:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                
                    
                    cur.execute(
                        """
                       INSERT INTO orders (order_no, cust_no, date)
                       VALUES (%(order_no)s, %(cust_no)s, %(date)s);
                       """,
                        {"order_no": order_no, "cust_no": cust_no, "date": date},
                    )
                    
                    
                conn.commit()
            return redirect(url_for("order_index"))

    # get products
    with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    
                    products = cur.execute(
                        """
                       SELECT name, description, price, sku
                       FROM product
                       ORDER BY price DESC;
                       """,
                        {},
                    ).fetchall()
    
    return render_template("order/add.html", products = products)


#----------------------------------------
#               Product
#----------------------------------------


@app.route("/product", methods=("GET", "POST"))
# @app.route("/accounts", methods=("GET",))
def product_index():
    """Product management page."""
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
               SELECT SKU, name, description, price, ean
               FROM product
               ORDER BY price DESC;
               """,
                {},
                # prepare=True,
            )
            products = cur.fetchmany(10)
            log.debug(f"Found {cur.rowcount} rows.")
    return render_template("product/index.html", products=products)

@app.route("/product/add", methods=("GET", "POST"))
def product_add():
    """Add a new product."""
    if request.method == "POST":
        sku = request.form["sku"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        ean = request.form["ean"]

        error = None

        if not sku:
            error = "SKU is required."

        if not name:
            error = "Name is required."

        if not description:
            error = "Description is required."

        if not price:
            error = "Price is required."

        if not ean:
            error = "EAN is required."

        if error is not None:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                       INSERT INTO product (sku, name, description, price, ean)
                       VALUES (%(sku)s, %(name)s, %(description)s, %(price)s, %(ean)s);
                       """,
                        {"sku": sku, "name": name, "description": description, "price": price, "ean": ean},
                    )
                conn.commit()
            return redirect(url_for("product_index"))

    return render_template("product/add.html")


@app.route("/product/<sku>/update", methods=("GET", "POST"))
def product_update(sku):
    """Update the product."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
               SELECT sku, name, description, price, ean
               FROM product
               WHERE sku = %(sku)s;
               """,
                {"sku": sku},
            ).fetchone()
            log.debug(f"SKU")

    if request.method == "POST":

        try:
            price = float(request.form["price"])
        except ValueError as e:
            error = "Price must be numeric."

        description = request.form["description"]

        error = None

        if not price:
            error = "Price is required."

        if not description:
            error = "Description is required."

        if error is not None:
            log.debug(error)
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                       UPDATE product
                       SET price = %(price)s,
                       description = %(description)s
                       WHERE sku = %(sku)s;
                       """,
                        {"sku": sku, "price": price, "description": description},
                    )
                conn.commit()
            return redirect(url_for("product_index"))

    
    log.debug(product)

    return render_template("product/update.html", product=product)

@app.route("/product/delete/<sku>", methods=("GET",))
def product_delete(sku):
    """Delete the product."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            
            # delete all suppliers that supply this product
            suppliers = cur.execute(
             """ 
              SELECT tin FROM supplier
              WHERE sku = %(sku)s;
             """,
             {"sku": sku},
            ).fetchall()
            
            for supplier in suppliers:
                supplier_delete(supplier.tin)
            
            # delete contains entries that contain this product
            cur.execute(
                """
                DELETE FROM contains
                WHERE sku = %(sku)s;
                """,
                {"sku": sku},
            )
            
            # delete product
            cur.execute(
                """
                DELETE FROM product
                WHERE sku = %(sku)s;
                """,
                {"sku": sku},
            )
            
        conn.commit()
    return redirect(url_for("product_index"))


#---------------------------------------
#               Supplier
#----------------------------------------


@app.route("/supplier", methods=("GET", "POST"))
def supplier_index():
    """Supplier management page."""
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
               SELECT tin, name, address, sku, date
               FROM supplier
               ORDER BY name ASC;
               """,
                {},
                # prepare=True,
            )
            suppliers = cur.fetchmany(10)
            log.debug(len(suppliers))
    return render_template("supplier/index.html", suppliers=suppliers)


@app.route("/supplier/add", methods=("GET", "POST"))
def supplier_add():
    if request.method == "POST":
        tin = request.form["tin"]
        name = request.form["name"]
        address = request.form["address"]
        sku = request.form["sku"]
        date = request.form["date"]

        error = None

        if not tin:
            error = "TIN is required."

        if not name:
            error = "Name is required."

        if not address:
            error = "Address is required."

        if not sku:
            error = "SKU is required."

        if not date:
            error = "date is required."

        if error is not None:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                       INSERT INTO supplier (tin, name, address, sku, date)
                       VALUES (%(tin)s, %(name)s, %(address)s, %(sku)s, %(date)s);
                       """,
                        {"tin": tin, "name": name, "address": address, "sku": sku, "date": date},
                    )
                conn.commit()
            return redirect(url_for("supplier_index"))

    return render_template("supplier/add.html")

@app.route("/supplier/delete/<tin>", methods=("GET",))
def supplier_delete(tin):
    """Delete the supplier."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                    DELETE FROM delivery
                    WHERE tin = %(tin)s;
                """,
                {"tin": tin},  
            )
            
            cur.execute(
                """
                    DELETE FROM supplier
                    WHERE tin = %(tin)s;
                """,
                {"tin": tin},
            )
            
        conn.commit()
    return redirect(url_for("supplier_index"))

# TODO. maybe merge with order.
@app.route("/payment", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def payment():
    """Payment management page."""
    return render_template("payment/index.html")


# @app.route("/aaaa", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
# def index():
#    """Show all the accounts, most recent first."""

#    with pool.connection() as conn:
#        with conn.cursor(row_factory=namedtuple_row) as cur:
#            accounts = cur.execute(
#                """
#                SELECT account_number, branch_name, balance
#                FROM account
#                ORDER BY account_number DESC;
#                """,
#                {},
#            ).fetchall()
#            log.debug(f"Found {cur.rowcount} rows.")

#    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
#    if (  request.accept_mimetypes["application/json"]
#          and not request.accept_mimetypes["text/html"]
#     ):
#        return jsonify(accounts)

#    return render_template("account/index.html", accounts=accounts)


# @app.route("/accounts/<account_number>/update", methods=("GET", "POST"))
# def account_update(account_number):
#    """Update the account balance."""

#    with pool.connection() as conn:
#        with conn.cursor(row_factory=namedtuple_row) as cur:
#            account = cur.execute(
#                """
#                SELECT account_number, branch_name, balance
#                FROM account
#                WHERE account_number = %(account_number)s;
#                """,
#                {"account_number": account_number},
#            ).fetchone()
#            log.debug(f"Found {cur.rowcount} rows.")

#    if request.method == "POST":
#        balance = request.form["balance"]

#        error = None

#        if not balance:
#            error = "Balance is required."
#            if not balance.isnumeric():
#                error = "Balance is required to be numeric."

#        if error is not None:
#            flash(error)
#        else:
#            with pool.connection() as conn:
#                with conn.cursor(row_factory=namedtuple_row) as cur:
#                    cur.execute(
#                        """
#                        UPDATE account
#                        SET balance = %(balance)s
#                        WHERE account_number = %(account_number)s;
#                        """,
#                        {"account_number": account_number, "balance": balance},
#                    )
#                conn.commit()
#            return redirect(url_for("account_index"))

#    return render_template("account/update.html", account=account)


# @app.route("/accounts/<account_number>/delete", methods=("POST",))
# def account_delete(account_number):
#    """Delete the account."""

#    with pool.connection() as conn:
#        with conn.cursor(row_factory=namedtuple_row) as cur:
#            cur.execute(
#                """
#                DELETE FROM account
#                WHERE account_number = %(account_number)s;
#                """,
#                {"account_number": account_number},
#            )
#        conn.commit()
#    return redirect(url_for("account_index"))


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()


