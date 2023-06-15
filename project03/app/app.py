#!/usr/bin/python3
from logging.config import dictConfig

# import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool
from math import ceil

ITEMS = 15

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
app.secret_key = b"CHANGE_ME_IN_PRODUCTION"
log = app.logger


def get_pages(cur_page, nr_pages):
    # Returns a list of pages to display in pagination.
    if nr_pages <= 10:
        return range(1, nr_pages + 1)
    if cur_page <= 5:
        return range(1, 10 + 1)

    if cur_page in range(nr_pages - 5, nr_pages + 1):
        return range(nr_pages - 10, nr_pages + 1)

    return range(max(cur_page - 5, 1), min(cur_page + 5, nr_pages + 1))


@app.route("/", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def index():
    """WebUI homepage."""
    return render_template("index.html")


# ----------------------------------------
#               Customer
# ----------------------------------------


@app.route("/customer", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def customer_index():
    try:
        page = request.args.get("page", type=int, default=1)
        """Customer management page."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                nr_items = (
                    cur.execute(
                        """
                    SELECT COUNT(*) as count
                    FROM customer;
                """
                    )
                    .fetchone()
                    .count
                )
                log.debug(f"nr_items = {nr_items}")

                nr_pages = ceil(nr_items / ITEMS)
                if page < 1:
                    page = 1
                elif page > nr_pages:
                    page = nr_pages
                cur.execute(
                    """
                SELECT cust_no, name, email, address, phone
                FROM customer
                ORDER BY name DESC
                OFFSET %(offset)s;
                """,
                    {"offset": (page - 1) * ITEMS},
                    prepare=True,
                )
                customers = cur.fetchmany(ITEMS)
        # Remove special customer that holds deleted customer's leftovers.
        for customer in customers:
            if customer.cust_no == -1:
                customers.remove(customer)

        return render_template(
            "customer/index.html",
            items=customers,
            cur_page=page,
            nr_pages=nr_pages,
            pages=get_pages(page, nr_pages),
        )

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return render_template(
            "customer/index.html",
            items=[],
            cur_page=1,
            nr_pages=1,
            pages=[1],
        )


@app.route("/customer/add", methods=("GET", "POST"))
def customer_add():
    try:
        """Add a new customer."""
        if request.method == "POST":
            cust_no = request.form["cust_no"]
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]

            error = None

            if not cust_no:
                error = "Customer Number is required."

            if not name:
                error = "Name is required."

            if not email:
                error = "Email is required."

            if not address:
                error = "Address is required."

            if not phone:
                error = "Phone is required."

            if error is not None:
                flash(error)
            else:
                with pool.connection() as conn:
                    with conn.cursor(row_factory=namedtuple_row) as cur:
                        cur.execute(
                            """
                        INSERT INTO customer (cust_no, name, email, phone, address)
                        VALUES (%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s);
                        """,
                            {
                                "cust_no": cust_no,
                                "name": name,
                                "email": email,
                                "phone": phone,
                                "address": address,
                            },
                        )
                    conn.commit()
                return redirect(url_for("customer_index"))

        return render_template("customer/add.html")

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("customer_index"))


@app.route("/customer/<cust_no>/update", methods=("GET", "POST"))
def customer_update(cust_no):
    try:
        """Update a customer."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                customer = cur.execute(
                    """
                SELECT cust_no, name, email, address, phone
                FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                    {"cust_no": cust_no},
                ).fetchone()
                log.debug(f"Found {cur.rowcount} rows.")

        if request.method == "POST":
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]

            error = None

            if not email:
                error = "Email is required."

            if not address:
                error = "Address is required."

            if not phone:
                error = "Phone is required."

            if error is not None:
                flash(error)
            else:
                with pool.connection() as conn:
                    with conn.cursor(row_factory=namedtuple_row) as cur:
                        cur.execute(
                            """
                        UPDATE customer
                        SET email = %(email)s, phone = %(phone)s, address = %(address)s
                        WHERE cust_no = %(cust_no)s;
                        """,
                            {
                                "cust_no": cust_no,
                                "email": email,
                                "phone": phone,
                                "address": address,
                            },
                        )
                    conn.commit()
                return redirect(url_for("customer_index"))
        return render_template("customer/update.html", customer=customer)

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("customer_index"))


@app.route("/customer/<int:cust_no>/delete", methods=("POST", "GET"))
def customer_delete(cust_no: int):
    try:
        if cust_no == -1:
            flash("Can't delete special customer.")
            return redirect(url_for("customer_index"))
        """Delete a customer."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                UPDATE orders
                SET cust_no = -1
                WHERE cust_no = %(cust_no)s;
                """,
                    {"cust_no": cust_no},
                )

                cur.execute(
                    """
                UPDATE pay
                SET cust_no = -1
                WHERE cust_no = %(cust_no)s;
                """,
                    {"cust_no": cust_no},
                )

                cur.execute(
                    """
                DELETE FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                    {"cust_no": cust_no},
                )
            conn.commit()
        flash(f"Deleted customer {cust_no}.")
        log.debug(f"Deleted {cur.rowcount} rows.")

        return redirect(url_for("customer_index"))
    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("customer_index"))


# ----------------------------------------
#               Order
# ----------------------------------------


@app.route("/order", methods=("GET",))
# @app.route("/accounts", methods=("GET",))
def order_index():
    try:
        page = request.args.get("page", type=int, default=1)
        """Order management page."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                nr_items = (
                    cur.execute(
                        """
                    SELECT COUNT(*) as count
                    FROM orders;
                """
                    )
                    .fetchone()
                    .count
                )

                nr_pages = ceil(nr_items / ITEMS)
                cur.execute(
                    """
                SELECT o.order_no, o.cust_no, o.date, p.order_no AS paid_order_no
                FROM orders o
                LEFT OUTER JOIN pay p ON o.order_no = p.order_no
                ORDER BY o.order_no ASC
                OFFSET %(offset)s;
                """,
                    {"offset": (page - 1) * ITEMS},
                    # prepare=True,
                )
                orders = cur.fetchmany(ITEMS)

        return render_template(
            "order/index.html",
            items=orders,
            cur_page=page,
            nr_pages=nr_pages,
            pages=get_pages(page, nr_pages),
        )
    except Exception as e:
        raise (e)
        flash(f"An error ocurred: {e}")
        return render_template("order/index.html", orders=[])


@app.route("/order/add", methods=("GET", "POST"))
def order_add():
    """Add a new order."""
    try:
        products_to_add = []
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

        if request.method == "POST":
            order_no = request.form["order_no"]
            cust_no = request.form["cust_no"]
            date = request.form["date"]
            product_qty = []
            for product in products:
                product_quantity = request.form[product.sku]
                if not product_quantity:
                    product_quantity = 0
                product_qty.append(product_quantity)
            log.debug("\n\n\n\n\n")
            log.debug(product_qty)

            i = 0
            for product in products:
                if int(product_qty[i]) > 0:
                    products_to_add.append((product.sku, int(product_qty[i])))
                i = i + 1

            error = None

            if not order_no:
                error = "Order Number is required."

            if not cust_no:
                error = "Customer Number is required."

            if not date:
                error = "Date is required."

            if not products_to_add:
                error = "At least 1 Product is required."

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

                        for product in products_to_add:
                            cur.execute(
                                """
                            INSERT INTO contains (order_no, sku, qty)
                            VALUES (%(order_no)s, %(sku)s, %(quantity)s);
                            """,
                                {
                                    "order_no": order_no,
                                    "sku": product[0],
                                    "quantity": product[1],
                                },
                            )

                    conn.commit()
                return redirect(url_for("order_index"))

        return render_template("order/add.html", products=products)

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("order_index"))


@app.route("/order/pay/<order_no>", methods=("GET",))
def order_pay(order_no):
    try:
        """Mark an order as paid."""

        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                order = cur.execute(
                    """
                SELECT cust_no
                FROM orders
                WHERE order_no = %(order_no)s;
                """,
                    {"order_no": order_no},
                ).fetchone()

                log.debug(order)
                log.debug(type(order))

                if not order:  # fetchone() returns None if nothing is returned
                    raise ValueError("TODO FIXME")  # FIXME
                cust_no = order.cust_no
                #'Pay' order.
                cur.execute(
                    """
                    INSERT INTO pay (order_no, cust_no)
                    VALUES (%(order_no)s, %(cust_no)s);
                    """,
                    {"order_no": order_no, "cust_no": cust_no},
                )
            conn.commit()
        flash(f"Order '{order_no}' marked as paid.")
        return redirect(url_for("order_index"))

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("order_index"))


# ----------------------------------------
#               Product
# ----------------------------------------


@app.route("/product", methods=("GET", "POST"))
# @app.route("/accounts", methods=("GET",))
def product_index():
    try:
        page = request.args.get("page", type=int, default=1)
        """Product management page."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                nr_items = (
                    cur.execute(
                        """
                    SELECT COUNT(*) as count
                    FROM product;
                """
                    )
                    .fetchone()
                    .count
                )

                nr_pages = ceil(nr_items / ITEMS)
                cur.execute(
                    """
                SELECT SKU, name, description, price, ean
                FROM product
                ORDER BY price DESC
                OFFSET %(offset)s;
                """,
                    {"offset": (page - 1) * ITEMS},
                    # prepare=True,
                )
                products = cur.fetchmany(ITEMS)
            return render_template(
                "product/index.html",
                items=products,
                cur_page=page,
                nr_pages=nr_pages,
                pages=get_pages(page, nr_pages),
            )

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return render_template(
            "product/index.html",
            items=[],
            cur_page=1,
            nr_pages=1,
            pages=[1],
        )


@app.route("/product/add", methods=("GET", "POST"))
def product_add():
    try:
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
                            {
                                "sku": sku,
                                "name": name,
                                "description": description,
                                "price": price,
                                "ean": ean,
                            },
                        )
                    conn.commit()
                return redirect(url_for("product_index"))

        return render_template("product/add.html")

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("product_index"))


@app.route("/product/<sku>/update", methods=("GET", "POST"))
def product_update(sku):
    try:
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

        if request.method == "POST":
            try:
                price = float(request.form["price"])
            except ValueError:
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

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("product_index"))


@app.route("/product/delete/<sku>", methods=("GET",))
def product_delete(sku):
    try:
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

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("product_index"))


# ---------------------------------------
#               Supplier
# ----------------------------------------


@app.route("/supplier", methods=("GET", "POST"))
def supplier_index():
    try:
        page = request.args.get("page", type=int, default=1)
        """Supplier management page."""
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                nr_items = (
                    cur.execute(
                        """
                    SELECT COUNT(*) as count
                    FROM product;
                    """
                    )
                    .fetchone()
                    .count
                )

                nr_pages = ceil(nr_items / ITEMS)
                cur.execute(
                    """
                SELECT tin, name, address, sku, date
                FROM supplier
                ORDER BY name ASC
                OFFSET %(offset)s;
                """,
                    {"offset": (page - 1) * ITEMS},
                    # prepare=True,
                )
                suppliers = cur.fetchmany(ITEMS)

            return render_template(
                "supplier/index.html",
                items=suppliers,
                cur_page=page,
                nr_pages=nr_pages,
                pages=get_pages(page, nr_pages),
            )

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return render_template(
            "supplier/index.html",
            items=[],
            cur_page=1,
            nr_pages=1,
            pages=[1],
        )


@app.route("/supplier/add", methods=("GET", "POST"))
def supplier_add():
    try:
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
                            {
                                "tin": tin,
                                "name": name,
                                "address": address,
                                "sku": sku,
                                "date": date,
                            },
                        )
                    conn.commit()
                return redirect(url_for("supplier_index"))

        return render_template("supplier/add.html")

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("supplier_index"))


@app.route("/supplier/delete/<tin>", methods=("GET",))
def supplier_delete(tin):
    try:
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

    except Exception as e:
        flash(f"An error ocurred: {e}")
        return redirect(url_for("supplier_index"))


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
