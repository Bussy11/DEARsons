# Dearson Barbing & Technology - single-file Flask website
# Works on phone: Pydroid 3 (pip install flask) or Termux (pip install flask)
#
# Put these pictures in a folder named "static" next to this file:
#   logo.png   -> company logo
#   coat.png   -> Nigeria coat of arms
#   ceo.jpg    -> picture of the CEO
# Run, then open http://127.0.0.1:5000 in your phone browser.

import os, re, sqlite3, urllib.parse
from flask import (Flask, request, session, redirect, url_for,
                   render_template_string, flash)

# ---------- SETTINGS: CHANGE THESE ----------
SITE_NAME = "Dearson Barbing & Technology"
CEO_NAME = "Mr. OLUWABUSAYO JUWON A."                 # change to the CEO's name
PHONE_1 = "08161999686"                  # contact number 1
PHONE_2 = "08118786977"                  # contact number 2
WHATSAPP = "2348161999686"               # WhatsApp number, 234 format, no +
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Google123")
# --------------------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "dearson.db")
app = Flask(__name__, static_folder=os.path.join(BASE, "static"))
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


with db() as c:
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, address TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE,
        created TEXT DEFAULT CURRENT_TIMESTAMP)""")


def wa(text):
    return "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(text))


CSS = """
:root{--g:#0b6b3a;--gd:#06452a;--gold:#c9a227;--ink:#16221b;--bg:#f6f4ec}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;background:var(--bg);color:var(--ink);line-height:1.55}
header{background:var(--gd);color:#fff;padding:12px 10px;border-bottom:4px solid var(--gold)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:8px;max-width:900px;margin:auto}
.bar img{height:64px;width:64px;object-fit:contain;background:#fff;border-radius:8px;padding:3px}
.bar h1{font-size:1.15rem;text-align:center;margin:0;flex:1}
main{max-width:900px;margin:auto;padding:16px}
h2{color:var(--gd);border-bottom:2px solid var(--gold);padding-bottom:4px}
.card{background:#fff;border:1px solid #d8d2bd;border-radius:10px;padding:16px;margin:14px 0}
input{width:100%;padding:12px;margin:6px 0 12px;border:1px solid #9aa89f;border-radius:8px;font-size:1rem}
label{font-weight:bold}
.btn{display:inline-block;background:var(--g);color:#fff;text-decoration:none;border:0;
 padding:12px 18px;border-radius:8px;font-size:1rem;margin:4px 4px 4px 0;cursor:pointer}
.btn.wa{background:#1fa855}.btn.gold{background:var(--gold);color:#16221b}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.ceo{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.ceo img{width:130px;height:150px;object-fit:cover;border-radius:10px;border:3px solid var(--gold);background:#ddd}
.cert{border:6px double var(--gold);background:#fffdf3;text-align:center;padding:22px}
.cert h3{margin:.2em 0;color:var(--gd)}
.msg{background:#fff3cd;border:1px solid #e0c36a;padding:10px;border-radius:8px;margin:10px 0}
footer{text-align:center;padding:18px;background:var(--gd);color:#fff;margin-top:20px}
footer a{color:var(--gold)}
.wafloat{position:fixed;right:14px;bottom:14px;background:#1fa855;color:#fff;text-decoration:none;
 padding:14px 18px;border-radius:40px;font-family:sans-serif;box-shadow:0 2px 8px #0006}
table{width:100%;border-collapse:collapse;font-size:.9rem}td,th{border:1px solid #ccc;padding:6px;text-align:left}
"""

LAYOUT = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ site }}</title><style>{{ css|safe }}</style></head><body>
<header><div class="bar">
 <img src="{{ url_for('static', filename='coat.png') }}" alt="Nigeria coat of arms" onerror="this.style.visibility='hidden'">
 <div style="flex:1;text-align:center">
  <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="height:48px;width:48px" onerror="this.style.display='none'">
  <h1>{{ site }}</h1></div>
 <img src="{{ url_for('static', filename='coat.png') }}" alt="Nigeria coat of arms" onerror="this.style.visibility='hidden'">
</div></header>
<main>
{% with m = get_flashed_messages() %}{% for x in m %}<div class="msg">{{ x }}</div>{% endfor %}{% endwith %}
{{ body|safe }}
</main>
<footer>
 <p>Call: <a href="tel:{{ p1 }}">{{ p1 }}</a> &nbsp;|&nbsp; <a href="tel:{{ p2 }}">{{ p2 }}</a></p>
 <p>&copy; {{ site }}</p>
</footer>
<a class="wafloat" href="{{ chat }}" target="_blank">WhatsApp Chat</a>
</body></html>"""


def page(body_tpl, **ctx):
    body = render_template_string(body_tpl, **ctx)
    chat = wa("Hello %s, I need help." % SITE_NAME)
    return render_template_string(LAYOUT, body=body, site=SITE_NAME, css=CSS,
                                  p1=PHONE_1, p2=PHONE_2, chat=chat)


def logged_in():
    return "phone" in session


# ---------- WELCOME + REGISTRATION ----------
@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        phone = re.sub(r"[\s-]", "", request.form.get("phone", ""))
        if len(name) < 3 or len(address) < 5:
            flash("Please enter your full name and full address.")
        elif not re.fullmatch(r"(0|\+?234)[789][01]\d{8}", phone):
            flash("Enter a valid Nigerian phone number, e.g. 08012345678.")
        else:
            with db() as c:
                c.execute("""INSERT INTO users(name,address,phone) VALUES(?,?,?)
                    ON CONFLICT(phone) DO UPDATE SET name=excluded.name,address=excluded.address""",
                          (name, address, phone))
            session.update(name=name, address=address, phone=phone)
            return redirect(url_for("home"))
    return page("""
<div class="card" style="text-align:center">
 <h2>Welcome to {{ site }}</h2>
 <p>Barbing salon, phone &amp; gadget shop, and training academy.
 Register once to see our services, prices and place orders.</p>
</div>
<div class="card">
 <form method="post">
  <label>Full name</label><input name="name" required autocomplete="name">
  <label>Address</label><input name="address" required autocomplete="street-address">
  <label>Phone number</label><input name="phone" type="tel" required placeholder="08012345678">
  <button class="btn" type="submit">Enter site</button>
 </form>
</div>""", site=SITE_NAME)


# ---------- MEMBERS-ONLY HOME ----------
@app.route("/home")
def home():
    if not logged_in():
        flash("Please register first to enter.")
        return redirect(url_for("welcome"))
    return page("""
<h2>Hello, {{ name }}</h2>
<div class="card ceo">
 <img src="{{ url_for('static', filename='ceo.jpg') }}" alt="CEO" onerror="this.style.visibility='hidden'">
 <div><h3 style="margin:0">{{ ceo }}</h3><p>Chief Executive Officer, {{ site }}.<br>
 Quality service, honest prices, skills that pay.</p></div>
</div>
<a class="btn" href="{{ url_for('services') }}">Our Services</a>
<a class="btn gold" href="{{ url_for('academy') }}">Academy</a>
<a class="btn wa" href="{{ chat }}" target="_blank">Chat on WhatsApp</a>
<a class="btn" href="{{ deliver }}" target="_blank">Order Home Delivery</a>
<a class="btn" href="{{ url_for('logout') }}" style="background:#777">Log out</a>
""", name=session["name"].split()[0], ceo=CEO_NAME, site=SITE_NAME,
        chat=wa("Hello %s, I'm %s. I need help." % (SITE_NAME, session["name"])),
        deliver=wa("HOME DELIVERY REQUEST\nName: %s\nPhone: %s\nAddress: %s\nItem/Service: "
                   % (session["name"], session["phone"], session["address"])))


@app.route("/services")
def services():
    if not logged_in():
        return redirect(url_for("welcome"))
    items = {
        "Barbing Salon": ["Haircut", "Beard trim and shaping", "Hair dyeing",
                          "Kids haircut", "Home service barbing"],
        "Phone Tech & Gadgets": ["New and used phones", "Chargers, cables, earphones",
                                 "Power banks and accessories", "Screen and battery repair",
                                 "Software fixing and unlocking"],
    }
    return page("""
<h2>Our Services</h2>
<div class="grid">
{% for title, lst in items.items() %}
 <div class="card"><h3>{{ title }}</h3><ul>{% for i in lst %}<li>{{ i }}</li>{% endfor %}</ul>
 <a class="btn wa" target="_blank" href="{{ links[title] }}">Book / Order on WhatsApp</a></div>
{% endfor %}
</div>
<a class="btn" href="{{ url_for('home') }}">Back</a>""", items=items,
        links={k: wa("Hello, I'm %s (%s). I want: %s.\nAddress: %s" %
                     (session["name"], session["phone"], k, session["address"]))
               for k in items})


@app.route("/academy")
def academy():
    if not logged_in():
        return redirect(url_for("welcome"))
    return page("""
<h2>{{ site }} Academy</h2>
<div class="card"><p>Learn barbing and phone repair from working professionals.
Every graduate receives a professional certificate.</p>
<a class="btn wa" target="_blank" href="{{ link }}">Register for Academy</a></div>
<div class="cert">
 <p>{{ site }} Academy</p>
 <h3>Professional Certificate</h3>
 <p>This is to certify that</p>
 <p><b>{{ name }}</b></p>
 <p>has successfully completed training and is awarded this certificate.</p>
 <p>Signed: {{ ceo }}</p>
</div>
<a class="btn" href="{{ url_for('home') }}">Back</a>""", site=SITE_NAME,
        name=session["name"], ceo=CEO_NAME,
        link=wa("Hello, I'm %s (%s). I want to join the Academy (barbing / phone repair)."
                % (session["name"], session["phone"])))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))


# ---------- ADMIN (strict access): see registered users ----------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
        else:
            flash("Wrong password.")
    if not session.get("admin"):
        return page("""<div class="card"><h2>Admin</h2><form method="post">
        <label>Password</label><input type="password" name="password" required>
        <button class="btn">Login</button></form></div>""")
    with db() as c:
        rows = c.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    return page("""<h2>Registered users ({{ rows|length }})</h2>
    <div style="overflow-x:auto"><table><tr><th>Name</th><th>Phone</th><th>Address</th><th>Date</th></tr>
    {% for r in rows %}<tr><td>{{ r.name }}</td><td>{{ r.phone }}</td><td>{{ r.address }}</td><td>{{ r.created }}</td></tr>{% endfor %}
    </table></div><a class="btn" href="{{ url_for('admin_logout') }}">Admin logout</a>""", rows=rows)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "static"), exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
