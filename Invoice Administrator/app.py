from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, usd
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///facturas.db")

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        user_id = session.get("user_id")
        mes = request.form.get("filtroMes")
        anio = request.form.get("filtroAnio")
        categoria = request.form.get("filtroCategoria")
        estado = request.form.get("filtroEstado")

        # Agregar condiciones según los parámetros proporcionados
        conditions = []
        params = []

        if mes:
            conditions.append("strftime('%m', date) = ?")
            params.append(mes)

        if anio:
            conditions.append("strftime('%Y', date) = ?")
            params.append(anio)

        if categoria:
            conditions.append("category LIKE ?")
            params.append(f"%{categoria}%")

        if estado:
            conditions.append("status = ?")
            params.append(estado)

        # Construir la consulta base
        facturas = "SELECT * FROM invoices WHERE user_id = ?"

        # Combina las condiciones usando AND
        if conditions:
            facturas += " AND " + " AND ".join(conditions)

        # Convertir la lista de parámetros a una tupla
        parametros_tupla = tuple(params)

        # Ejecutar la consulta SQL con la tupla de parámetros
        filtered = db.execute(facturas, user_id, *parametros_tupla)

        sum = 0
        quantity = 0
        for invoice in filtered:
            sum += invoice["amount"]
            quantity += 1
        
        return render_template("index.html", invoices = filtered, total_amount = usd(sum), total_quantity = quantity)
    else:
        user_id = session.get("user_id")
        facturas = db.execute("SELECT * FROM invoices WHERE user_id = ?", user_id)
        total = db.execute("SELECT SUM(amount) FROM invoices WHERE user_id = ?", user_id)
        quantity = 0
        for invoice in facturas:
            quantity += 1
        
        if not total[0]['SUM(amount)']:
            total[0]['SUM(amount)'] = 0
        return render_template("index.html", invoices = facturas, total_amount = usd(total[0]['SUM(amount)']), total_quantity = quantity)

@app.route("/login", methods = ["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #If the users try some tricks in the html
        if not username:
            return redirect("/login")
        if not password:
            return redirect("/login")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        #Checking if password and username are correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("login.html", error = "Invalid username or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not email or not password or not confirmation:
            return redirect("/register")
        
        used_username = db.execute("SELECT * FROM users WHERE username = ?", username)
        used_email = db.execute("SELECT * FROM users WHERE email = ?", email)

        if used_username:
            return render_template("register.html", error = "Nombre de usuario ya registrado.")
        
        if used_email:
            return render_template("register.html", error = "Correo electrónico ya registrado.")


        # Hash de la contraseña
        hashed_password = generate_password_hash(password)

         # Ejecutar la consulta SQL de forma segura usando parámetros
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        db.execute(query,username, email, hashed_password)
      
        return redirect("/login")

    else:
        return render_template("register.html")
    
@app.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        user_id = session.get("user_id")
        amount = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")
        status = request.form.get("status")

        if not amount or not category or not date or not status:
            return redirect("/add")

        amount = float(amount)
        if amount < 0:
            return render_template("add.html", error = "Monto invalido")
        
        if not description:
            description = "Sin descripcion"

        if len(description) > 120:
            return render_template("add.html", error = "Descripcion supero el numero de caracteres permitido")
        
        query = "INSERT INTO invoices (amount, category, date, description, user_id, status) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(query, amount, category, date, description, user_id, status)

        return render_template("add.html", exito = "Factura añadida correctamente")
    else:
        return render_template("add.html")


@app.route("/list")
@login_required
def list():
    user_id = session.get("user_id")
    pendiente_text =  "Pendiente"
    pagada_text = "Pagada"
    pendientes = db.execute("SELECT * FROM invoices WHERE status = ? AND user_id = ?", pendiente_text, user_id)
    pagadas = db.execute("SELECT * FROM invoices WHERE status = ? AND user_id = ?", pagada_text , user_id)

    #Mostrar monto en formato de dolar
    for i, row in enumerate(pagadas):
        pagadas[i]["amount"] = float(row["amount"])
        pagadas[i]["amount"] = usd(row["amount"])

    for i, row in enumerate(pendientes):
        pendientes[i]["amount"] = float(row["amount"])
        pendientes[i]["amount"] = usd(row["amount"])
    

    return render_template("list.html", pending_invoices = pendientes, paid_invoices = pagadas)

@app.route("/edit", methods = ["GET", "POST"])
@login_required
def edit_invoices():
    user_id = session.get("user_id")

    if request.method == "POST":
        invoice_id = request.form.get("campo_id")

        if not invoice_id:
            return redirect("/edit")

        invoice = db.execute("SELECT * FROM invoices WHERE user_id = ? AND id = ?", user_id, invoice_id)

        mensaje = f"La factura con ID {invoice_id} no existe"
        if not invoice:
            return render_template("edit.html", mensaje = mensaje)
        
        return render_template("edit.html", invoice = invoice[0])
    else:
        return render_template("edit_invoices.html")

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    user_id = session.get("user_id")
    invoice_id = request.form.get("campo_id")

    if not invoice_id:
        return redirect("/edit")

    # Verificar si la factura pertenece al usuario
    factura = db.execute("SELECT * FROM invoices WHERE user_id = ? AND id = ?", user_id, invoice_id)

    if not factura:
        return render_template("edit.html", mensaje="ID no existente")

    # Eliminar la factura
    db.execute("DELETE FROM invoices WHERE id = ?", invoice_id)

    return render_template("edit.html", mensaje="Factura eliminada correctamente")

@app.route("/save", methods=["POST"])
@login_required
def save():
    user_id = session.get("user_id")
    invoice_id = request.form.get("campo_id")
    if not invoice_id:
        return redirect("/edit")
    print("hallaron la mierda")
    # Verificar si la factura pertenece al usuario
    factura = db.execute("SELECT * FROM invoices WHERE user_id = ? AND id = ?", user_id, invoice_id)

    if not factura:
        return render_template("edit.html", error="ID no existente")

    # Guardar cambios en la base de datos
    nueva_descripcion = request.form.get("nueva_descripcion")
    nuevo_monto = request.form.get("nuevo_monto")
    nuevo_estado = request.form.get("nuevo_estado")
    nueva_fecha = request.form.get("nueva_fecha")
    nueva_categoria = request.form.get("nueva_categoria")

    # Corregir el orden de los parámetros en la consulta UPDATE
    db.execute("UPDATE invoices SET description = ?, amount = ?, status = ?, date = ?, category = ? WHERE id = ?", nueva_descripcion, nuevo_monto, nuevo_estado, nueva_fecha, nueva_categoria, invoice_id)   

    return render_template("edit.html", exito="Cambios guardados correctamente")


@app.route("/search", methods = ["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        id = request.form.get('campo_id')
        categoria = request.form.get('campo_categoria')
        monto_min = request.form.get('campo_monto_min')
        monto_max = request.form.get('campo_monto_max')
        estado = request.form.get('campo_estado')
        user_id = session.get("user_id")
        query = "SELECT * FROM invoices WHERE user_id = ?"

        # Utiliza una lista para almacenar los fragmentos de la consulta SQL
        conditions = []
        # Utiliza una lista para almacenar los valores de los parámetros
        params = []

        if categoria:
            conditions.append("category LIKE ?")
            params.append(f"%{categoria}%")
        

        if monto_min:
            conditions.append("amount >= ?")
            params.append(monto_min)

        if monto_max:
            conditions.append("amount <= ?")
            params.append(monto_max)
        
        if id:
            conditions.append("id = ?")
            params.append(id)

        

        # Combina las condiciones usando AND
        query += " AND " + " AND ".join(conditions)

        # Utiliza db.execute para ejecutar la consulta y pasar los parámetros como una tupla
        resultados = db.execute(query, user_id, *params)

        return jsonify(resultados)
    
    else:
        return render_template("search.html")
    