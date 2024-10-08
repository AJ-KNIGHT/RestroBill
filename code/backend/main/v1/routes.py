from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    make_response,
)
from flask_login import login_user, logout_user, current_user, login_required

from datetime import datetime

from models import Users, Products


def register_routes(app, db, bcrypt):

    # ---------------- login page -----------------------

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            if "username" in request.form.keys() and "password" in request.form.keys():
                username = request.form["username"]
                password = request.form["password"]

                user = Users.query.filter_by(username=username).first()

                if user and bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    if user.role == "admin":
                        return redirect(url_for("dashboard"))
                    elif user.role == "user":
                        return redirect(url_for("billing"))
                else:
                    flash("username and password is incorrect")
                    return redirect(url_for("login"))
            else:
                flash("username and password is incorrect")
                return redirect(url_for("login"))

    @app.route("/logout/")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    # ---------------- billing page -----------------------

    # billing page
    # @app.route('/billig/<uid>')
    # @login_required
    # def billing(uid):
    #     if current_user.role == 'user':
    #         return 'Billing page'
    #     else:
    #         return "Access Denied"

    @app.route("/billing")
    @login_required
    def billing():
        if current_user.role == "user":
            return render_template("billing.html", username=current_user.username)
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the users can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/search")
    @login_required
    def product_search():
        products = Products.query.all()
        products_list = [product.to_dict() for product in products]
        text = request.args.get("searchText", "").lower()
        result = [item for item in products_list if text in item["name"].lower()]
        return jsonify(results=result)

    @app.route("/print-bill", methods=["POST"])
    @login_required
    def print_bill():
        if current_user.role == "user":
            if request.is_json:
                cart = request.get_json()
                # get date and time in fomat Date: 08/09/24 02:20 PM
                now = datetime.now()
                formatted_date_time = now.strftime("%d/%m/%y %I:%M %p")

                context = {
                    "items": cart["list"],
                    "payment": cart["payment"],
                    "username": current_user.username,
                    "date_time": formatted_date_time,
                }

                rendered_html = render_template("bill-template.html", **context)

                return rendered_html, 200  # Return the HTML and a success status code

            else:
                return (
                    jsonify({"error": "Request must be JSON"}),
                    400,
                )  # Handle non-JSON requests

        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the users can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/test")
    @login_required
    def test():
        cart = {
            "list": {
                "1": {"product": "Tea", "qty": "2", "mrp": "₹10", "price": "₹20.00"},
                "2": {
                    "product": "Boiled Egg",
                    "qty": "4",
                    "mrp": "₹8",
                    "price": "₹32.00",
                },
                "3": {"product": "Coffee", "qty": "1", "mrp": "₹13", "price": "₹13.00"},
                "4": {
                    "product": "Chicken Biriyani",
                    "qty": "1",
                    "mrp": "₹100",
                    "price": "₹100.00",
                },
            },
            "payment": {
                "paytype": "CASH",
                "discount": "5",
                "total": 160,
                "tendered": "200",
                "change": "₹40.00",
            },
        }
        now = datetime.now()
        formatted_date_time = now.strftime("%d/%m/%y %I:%M %p")

        rendered_html = render_template(
            "bill-template.html",
            items=cart["list"],
            payment=cart["payment"],
            username=current_user.username,
            date_time=formatted_date_time,
        )

        return rendered_html

    # ---------------- dashboard page -----------------------

    @app.route("/dashboard")
    @login_required
    def dashboard():
        if current_user.role == "admin":
            return render_template(
                "/dashboard/dashboard.html", username=current_user.username
            )
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    # user management
    @app.route("/dashboard/user-management")
    @login_required
    def user_management():
        if current_user.role == "admin":
            user_data = Users.query.all()
            return render_template(
                "/dashboard/user_managment.html",
                username=current_user.username,
                users=user_data,
            )
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/user/insert", methods=["POST"])
    @login_required
    def user_insert():
        if current_user.role == "admin":
            if request.method == "POST":
                if (
                    "username" in request.form.keys()
                    and "password" in request.form.keys()
                ):
                    username = request.form["username"]
                    password = request.form["password"]
                    role = "user"

                    hashed_password = bcrypt.generate_password_hash(password)

                    new_user_data = Users(
                        username=username, password=hashed_password, role=role
                    )
                    db.session.add(new_user_data)
                    db.session.commit()

                    flash("User inserted successfully")

                    return redirect(url_for("user_management"))
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/user/update", methods=["GET", "POST"])
    @login_required
    def user_update():
        if current_user.role == "admin":
            if request.method == "POST":
                if (
                    "username" in request.form.keys()
                    and "password" in request.form.keys()
                ):
                    data = Users.query.get(request.form.get("uid"))

                    if (
                        request.form["username"].strip() != ""
                        and request.form["username"].strip() != data.username
                    ):
                        data.username = request.form["username"]

                    elif request.form["password"].strip() != "":
                        password = request.form["password"]
                        hashed_password = bcrypt.generate_password_hash(password)
                        data.password = hashed_password

                    db.session.commit()

                    flash("User data updated successfully")
                    return redirect(url_for("user_management"))
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/user/delete/<uid>/", methods=["GET", "POST"])
    @login_required
    def user_delete(uid):
        if current_user.role == "admin":
            data = Users.query.get(uid)
            if data:
                if uid.strip() != "1" and data.role != "admin":
                    db.session.delete(data)
                    db.session.commit()
                    flash("User deleted successfully")
                    return redirect(url_for("user_management"))
                else:
                    return "Cannot delete admin user"
            else:
                return "User not found"
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    # product management
    @app.route("/dashboard/product-management")
    @login_required
    def product_management():
        if current_user.role == "admin":
            product_data = Products.query.all()
            return render_template(
                "/dashboard/product_managment.html",
                username=current_user.username,
                products=product_data,
            )
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/product/insert", methods=["POST"])
    @login_required
    def product_insert():
        if current_user.role == "admin":
            if request.method == "POST":
                if (
                    "name" in request.form.keys()
                    and "category" in request.form.keys()
                    and "price" in request.form.keys()
                ):
                    name = request.form["name"]
                    category = request.form["category"]
                    price = float(request.form["price"])

                    new_product_data = Products(
                        name=name, category=category, price=price
                    )
                    db.session.add(new_product_data)
                    db.session.commit()

                    flash("Product inserted successfully")

                    return redirect(url_for("product_management"))
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/product/update", methods=["GET", "POST"])
    @login_required
    def product_update():
        if current_user.role == "admin":
            if request.method == "POST":
                if (
                    "name" in request.form.keys()
                    and "category" in request.form.keys()
                    and "price" in request.form.keys()
                ):
                    data = Products.query.get(request.form.get("pid"))

                    if (
                        request.form["name"].strip() != ""
                        and request.form["name"].strip() != data.name
                    ):
                        data.name = request.form["name"]

                    elif (
                        request.form["category"].strip() != ""
                        and request.form["category"].strip() != data.category
                    ):
                        data.category = request.form["category"]

                    elif (
                        request.form["price"] != 0
                        and float(request.form["price"]) != data.price
                    ):
                        data.price = float(request.form["price"])

                    db.session.commit()

                    flash("Product data updated successfully")
                    return redirect(url_for("product_management"))
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    @app.route("/product/delete/<pid>/", methods=["GET", "POST"])
    @login_required
    def product_delete(pid):
        if current_user.role == "admin":
            data = Products.query.get(pid)
            db.session.delete(data)
            db.session.commit()

            flash("Product deleted successfully")
            return redirect(url_for("product_management"))
        else:
            return redirect(
                url_for(
                    "auth_error",
                    msg="Only the admin can access this page. Please try logging in again to continue.",
                )
            )

    # ---------------- Error pages -----------------------

    @app.route("/auth_error/<msg>")
    def auth_error(msg):
        return render_template("error/auth-error.html", msg=msg)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("error/404.html"), 404
