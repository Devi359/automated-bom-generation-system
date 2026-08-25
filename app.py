from flask import Flask, redirect, request, session, Response, send_file, render_template
import requests
from collections import defaultdict
import os
import re
from urllib.parse import urlencode
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = "onshape_final_project_key"

# CONFIG
CLIENT_ID = os.environ.get("CLIENT_ID", "").strip()
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "").strip()
REDIRECT_URI = os.environ.get("REDIRECT_URI", "").strip() 

DOC_ID = "b1587e4dbf8a1c9022a6bb56"
WORK_ID = "9cf669ee555c6649d6218399"
TARGET_ASSEMBLY_ID = "8f6242fc71107313be94a7ff"


# ====================================================
# ADMIN PRICE UPDATES
# ====================================================

admin_price_updates = {}


# ====================================================
# PRICE ENGINE
# ====================================================

def get_price(part_name):

    default_prices = {
        "Base Plate": 500,
        "Bolt M6": 10,
        "Nut M6": 5,
        "Washer": 2,
        "Bracket": 150,
        "Frame": 1000,
        "Support Rod": 200,
        "Shaft": 100,
        "Bearing": 300,
        "Spacer": 20,
        "Clamp": 50,
        "Cover": 80,
        "Housing": 400,
        "Pin": 15
    }

    if part_name in admin_price_updates:
        return admin_price_updates[part_name]

    return default_prices.get(part_name, 0)




# ====================================================
# HOME
# ====================================================
@app.route("/")
def home():

    session.clear()

    return render_template("login.html")


# ====================================================
# USER LOGIN
# ====================================================
@app.route("/login")
def login():

    session.clear()

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }

    auth_url = (
        "https://oauth.onshape.com/oauth/authorize?"
        + urlencode(params)
    )

    return redirect(auth_url)


# ====================================================
# ADMIN LOGIN
# ====================================================
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "GET":

        session.clear()

        return render_template("admin_login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin123":

        session.clear()

        session["role"] = "admin"

        return redirect("/admin_dashboard")

    return "Invalid Credentials"


# ====================================================
# ONSHAPE CALLBACK
# ====================================================
@app.route("/callback")
def callback():

    code = request.args.get("code")

    if not code:
        return "Authorization code missing", 400

    response = requests.post(
        "https://oauth.onshape.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={
            "Accept": "application/json"
        }
    )

    if response.status_code != 200:
        return (
            f"OAuth Error: {response.text}",
            response.status_code
        )

    data = response.json()

    if "access_token" in data:

        session["access_token"] = data["access_token"]
        session["role"] = "user"

        return redirect("/dashboard")

    return f"Auth Failed: {response.text}", 400


# ====================================================
# USER DASHBOARD
# ====================================================
@app.route("/dashboard")
def dashboard():

    if session.get("role") != "user":
        return redirect("/")

    return render_template("dashboard.html")


# ====================================================
# ADMIN DASHBOARD
# ====================================================
@app.route("/admin_dashboard")
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect("/")

    return render_template("admin_dashboard.html")


# ====================================================
# ADMIN PRICE UPDATE
# ====================================================
@app.route("/update_price", methods=["GET", "POST"])
def update_price():

    if session.get("role") != "admin":
        return redirect("/")

    if request.method == "POST":

        part_name = request.form.get("part_name")
        price = int(request.form.get("price"))

        admin_price_updates[part_name] = price

        return redirect("/admin_dashboard")

    return render_template("update_price.html")


# ====================================================
# ONSHAPE FETCH
# ====================================================
def get_assembly_data(token):

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = (
        f"https://cad.onshape.com/api/assemblies/"
        f"d/{DOC_ID}/w/{WORK_ID}/e/{TARGET_ASSEMBLY_ID}"
    )

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        return None

    return response.json()


# ====================================================
# UTIL
# ====================================================
def clean_name(name):
    return re.sub(r"<.*?>", "", name).strip()


# ====================================================
# BOM ENGINE
# ====================================================
def generate_bom(data):

    part_count = defaultdict(int)

    part_name_map = {}

    for part in data.get("parts", []):

        part_name_map[
            part.get("partId")
        ] = part.get("name")

    def traverse(assembly):

        for inst in assembly.get("instances", []):

            part_id = inst.get("partId")

            name = part_name_map.get(part_id)

            if not name:
                name = clean_name(
                    inst.get("name", "Unknown")
                )

            name = re.sub(
                r"_\d+$",
                "",
                name
            )

            if inst.get("type") == "Part":

                part_count[name] += 1

            elif inst.get("type") == "Assembly":

                sub = next(
                    (
                        s for s in data.get(
                            "subAssemblies",
                            []
                        )
                        if s.get("id") == inst.get("id")
                    ),
                    None
                )

                if sub:
                    traverse(sub)

    traverse(
        data.get("rootAssembly", {})
    )

    result = []

    for name, qty in part_count.items():

        price = get_price(name)

        result.append({
            "name": name,
            "quantity": qty,
            "unit_price": price,
            "total_price": price * qty
        })

    return result


# ====================================================
# VIEW BOM
# ====================================================
@app.route("/fetch_details")
def fetch_details():

    token = session.get("access_token")

    if not token:
        return redirect("/")

    data = get_assembly_data(token)

    bom = generate_bom(data)

    total = sum(
        i["total_price"] for i in bom
    )

    return render_template(
        "bom.html",
        bom=bom,
        total=total
    )


# ====================================================
# CSV
# ====================================================
@app.route("/download_csv")
def download_csv():

    token = session.get("access_token")

    if not token:
        return redirect("/")

    data = get_assembly_data(token)

    bom = generate_bom(data)

    def generate():

        yield "Name,Qty,Price,Total\n"

        for item in bom:

            yield (
                f"{item['name']},"
                f"{item['quantity']},"
                f"{item['unit_price']},"
                f"{item['total_price']}\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=bom.csv"
        }
    )


# ====================================================
# PDF
# ====================================================
@app.route("/download_pdf")
def download_pdf():

    token = session.get("access_token")

    if not token:
        return redirect("/")

    data = get_assembly_data(token)

    bom = generate_bom(data)

    file_path = "bom_invoice.pdf"

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>BOM INVOICE</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    table_data = [
        ["Part", "Qty", "Price", "Total"]
    ]

    for item in bom:

        table_data.append([
            item["name"],
            item["quantity"],
            item["unit_price"],
            item["total_price"]
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(table)

    doc.build(elements)

    return send_file(
        file_path,
        as_attachment=True
    )


# ====================================================
# TREE
# ====================================================
def build_hierarchy(data):

    root = data.get("rootAssembly", {})

    return {
        "name": "Assembly",
        "children": root.get("instances", [])
    }


@app.route("/view_tree")
def view_tree():

    token = session.get("access_token")

    if not token:
        return redirect("/")

    data = get_assembly_data(token)

    hierarchy = build_hierarchy(data)

    return render_template(
        "tree.html",
        hierarchy=hierarchy
    )


# ====================================================
# LOGOUT
# ====================================================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ====================================================
# RUN
# ====================================================
if __name__ == "__main__":
    app.run(debug=True)
