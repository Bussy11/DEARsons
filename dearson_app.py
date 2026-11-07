import os, re, csv, io, html, base64, urllib.parse
from datetime import datetime
import streamlit as st

# ================= CHANGE THESE =================
SITE_NAME = "Dearson Barbing & Technology"
CEO_NAME = "A. O.  JUWON"
PHONE_1 = "08161999686"
PHONE_2 = "0811878687"
WHATSAPP = "08161999686"
ADMIN_PASSWORD = "Google123"
LOCK_ACADEMY = True   # True = admin must approve, False = open to all

CERTS = [
    ("CAC", "Corporate Affairs Commission"),
    ("SMEDAN Certificate", "Small and Medium Enterprises Development Agency"),
    ("Training Certificate", "Professional training"),
    ("NCE", "National Certificate in Education"),
    ("BSc", "Bachelor of Science"),
    ("University of Ibadan", "University of Ibadan certificate"),
]
# ================================================

st.set_page_config(page_title=SITE_NAME, page_icon="✂️", layout="centered")
BASE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE, "users.csv")
ACC_FILE = os.path.join(BASE, "approvals.csv")
FIELDS = ["name", "address", "phone", "date"]
ACC_FIELDS = ["phone", "name", "status", "date"]


def H(s):
    return " ".join(s.split())


def md(s):
    st.markdown(H(s), unsafe_allow_html=True)


def img_uri(*names):
    for n in names:
        p = os.path.join(BASE, n)
        if os.path.exists(p):
            if n.lower().endswith(".png"):
                mime = "image/png"
            else:
                mime = "image/jpeg"
            with open(p, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return "data:%s;base64,%s" % (mime, data)
    return ""


def num_files(prefix):
    found = []
    for i in (1, 2, 3):
        for ext in ("jpg", "jpeg", "png"):
            p = os.path.join(BASE, "%s%d.%s" % (prefix, i, ext))
            if os.path.exists(p):
                found.append(p)
                break
    return found


def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


WA_PATH = "".join([
    "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15",
    "-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.3-.15-1.263-.465",
    "-2.403-1.485-.888-.795-1.484-1.77-1.66-2.07-.174-.3-.019-.465.13-.615",
    ".136-.135.301-.345.451-.523.146-.181.194-.301.297-.496.1-.21.049-.375",
    "-.025-.524-.075-.15-.672-1.62-.922-2.206-.24-.584-.487-.51-.672-.51",
    "-.172-.015-.371-.015-.571-.015-.2 0-.523.074-.797.359-.273.3-1.045 1.02",
    "-1.045 2.475s1.07 2.865 1.219 3.075c.149.18 2.095 3.195 5.076 4.483",
    ".709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719",
    " 2.006-1.413.248-.695.248-1.29.173-1.414-.074-.123-.272-.198-.57-.347",
    "m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982",
    ".998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884",
    " 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994",
    "c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0",
    "C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24",
    "l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335",
    " 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z",
])

PH_PATH = "".join([
    "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24",
    " 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17",
    " 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25",
    " 1.02l-2.2 2.2z",
])

SVG_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
WA_ICON = svg_uri(SVG_OPEN + '<path fill="#fff" d="' + WA_PATH + '"/></svg>')
PH_ICON = svg_uri(SVG_OPEN + '<path fill="#d4a017" d="' + PH_PATH + '"/></svg>')


def intl(n):
    n = re.sub(r"\D", "", n)
    if n.startswith("0"):
        return "234" + n[1:]
    return n


def wa(text):
    return "https://wa.me/%s?text=%s" % (intl(WHATSAPP), urllib.parse.quote(text))


def wbtn(label, link, alt=False):
    cls = "wbtn alt" if alt else "wbtn"
    return (
        '<a class="%s" href="%s" target="_blank" rel="noopener">'
        '<img src="%s" alt="">%s</a>'
    ) % (cls, html.escape(link), WA_ICON, label)


def call_pill(num, label):
    return (
        '<a class="call" href="tel:%s"><img src="%s" alt="">'
        '<span><small>%s</small><b>%s</b></span></a>'
    ) % (num, PH_ICON, label, num)


def certs_table():
    rows = ""
    for i, (a, b) in enumerate(CERTS, 1):
        rows += "<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (
            i, html.escape(a), html.escape(b))
    return (
        '<div class="card"><div class="ct">Certificates Acquired</div>'
        '<table class="tbl"><tr><th>No.</th><th>Certificate</th>'
        '<th>Details</th></tr>%s</table></div>'
    ) % rows


# ---------------- registered users (users.csv) ----------------
def read_users():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_user(name, address, phone):
    rows = [r for r in read_users() if r["phone"] != phone]
    rows.append({
        "name": name,
        "address": address,
        "phone": phone,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


# ------------- certificate permission (approvals.csv) -------------
def read_acc():
    if not os.path.exists(ACC_FILE):
        return []
    with open(ACC_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_acc(rows):
    with open(ACC_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ACC_FIELDS)
        w.writeheader()
        w.writerows(rows)


def get_status(phone):
    for r in read_acc():
        if r["phone"] == phone:
            return r["status"]
    return None


def request_access(user):
    rows = read_acc()
    if not any(r["phone"] == user["phone"] for r in rows):
        rows.append({
            "phone": user["phone"],
            "name": user["name"],
            "status": "pending",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        write_acc(rows)


def set_status(phone, status):
    new = []
    for r in read_acc():
        if r["phone"] == phone:
            if status == "removed":
                continue
            r["status"] = status
        new.append(r)
    write_acc(new)


def locked_box(user):
    status = get_status(user["phone"])
    md('<div class="card"><div class="ct">🔒 Academy Certificate is locked</div>'
       '<div class="cr">Permission from the admin is required to view it.'
       '</div></div>')
    if status is None:
        st.button("Request Permission", key="req",
                  on_click=request_access, args=(user,))
    else:
        st.info("Your request is waiting for admin approval. "
                "Tap Check Again after the admin approves.")
        st.button("Check Again", key="chk")
    msg = ("Hello, I'm %s (%s). Please approve my permission to view "
           "the Academy Certificate." % (user["name"], user["phone"]))
    md(wbtn("Tell admin on WhatsApp", wa(msg)))


# ---------------- viewer button actions ----------------
def pick_cert(view):
    st.session_state["cert_view"] = view
    st.session_state["cert_i"] = 0


def step_cert(step):
    st.session_state["cert_i"] = st.session_state.get("cert_i", 0) + step


def toggle_env():
    st.session_state["env_open"] = not st.session_state.get("env_open", False)
    st.session_state["env_i"] = 0


def step_env(step):
    st.session_state["env_i"] = st.session_state.get("env_i", 0) + step


# ======================= STYLE =======================
md("""<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800;900&display=swap');
html,body,.stApp{overflow-x:hidden;max-width:100vw;}
.stApp{background:#e3eee6;font-family:'Poppins',sans-serif;}
.stApp p,.stApp li,.stApp label,.stApp input{font-family:'Poppins',sans-serif;}
div.block-container{
  box-sizing:border-box;width:calc(100% - 14px);max-width:720px;
  margin:2.8rem auto 1rem auto;
  padding:1rem .8rem 1.2rem .8rem !important;
  background:#fffdf5;border:4px solid #064e2b;border-radius:16px;
  box-shadow:inset 0 0 0 3px #fffdf5,inset 0 0 0 6px #d4a017,
  0 6px 18px rgba(6,78,43,.35);}
.hdr{
  box-sizing:border-box;width:100%;
  display:flex;align-items:center;justify-content:space-between;gap:6px;
  background:linear-gradient(135deg,#064e2b,#0b7a43);
  border-bottom:5px solid #d4a017;border-radius:12px;
  padding:8px;margin-bottom:12px;}
.hdr img{
  width:clamp(52px,18vw,92px);height:clamp(52px,18vw,92px);
  object-fit:contain;background:#fff;border-radius:10px;
  padding:3px;flex:0 0 auto;}
.hn{
  flex:1 1 0;min-width:0;text-align:center;padding:6px 4px;
  border-radius:12px;
  background:linear-gradient(135deg,#f7d96b,#d4a017 55%,#b8860b);
  border:3px solid #fff;box-shadow:0 3px 8px rgba(0,0,0,.35);}
.hn1{
  font-family:'Playfair Display',serif;font-weight:900;
  font-size:clamp(1.05rem,5.6vw,2.1rem);color:#064e2b;
  line-height:1;letter-spacing:.5px;}
.hn2{
  font-family:'Montserrat',sans-serif;font-weight:800;
  font-size:clamp(.58rem,2.8vw,.9rem);color:#12301f;
  margin-top:3px;line-height:1.2;}
.sec{
  font-family:'Montserrat',sans-serif;font-weight:800;color:#064e2b;
  font-size:1.3rem;border-bottom:3px solid #d4a017;display:inline-block;
  padding-bottom:2px;margin:6px 0 8px 0;}
.lead{font-weight:600;color:#1d2b22;font-size:.95rem;line-height:1.6;}
.card{
  box-sizing:border-box;
  background:#fff;border:2px solid #0b7a43;border-left:8px solid #d4a017;
  border-radius:12px;padding:10px 12px;margin:12px 0;
  box-shadow:0 2px 6px rgba(0,0,0,.15);}
.ct{
  font-family:'Montserrat',sans-serif;font-weight:800;font-size:1.1rem;
  color:#064e2b;margin-bottom:4px;}
.card ul{margin:0 0 6px 0;padding-left:1.1rem;}
.card li{font-weight:600;color:#1d2b22;font-size:.92rem;line-height:1.7;}
.wbtn{
  display:flex;align-items:center;justify-content:center;gap:8px;
  background:#1fa855;color:#fff !important;font-weight:700;
  text-decoration:none !important;border-radius:10px;padding:10px 12px;
  margin:8px 0;font-size:.92rem;box-shadow:0 2px 4px rgba(0,0,0,.2);}
.wbtn.alt{background:#064e2b;border:2px solid #d4a017;}
.wbtn img{width:16px;height:16px;}
.calls{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0;}
.call{
  flex:1;min-width:130px;display:flex;align-items:center;gap:8px;
  background:#064e2b;border:2px solid #d4a017;border-radius:10px;
  padding:8px 10px;text-decoration:none !important;}
.call img{width:16px;height:16px;}
.call small{
  display:block;color:#d9e8dd;font-size:.65rem;font-weight:500;line-height:1.2;}
.call b{color:#fff;font-size:.92rem;font-weight:700;}
.ceo{display:flex;gap:10px;align-items:center;}
.ceo img{
  width:95px;height:115px;object-fit:cover;border-radius:12px;
  border:4px solid #d4a017;flex:0 0 auto;}
.cn{
  font-family:'Montserrat',sans-serif;font-weight:800;font-size:1.1rem;
  color:#064e2b;}
.cr{font-weight:600;color:#333;font-size:.85rem;line-height:1.5;}
.foot{text-align:center;font-weight:700;color:#064e2b;font-size:.85rem;margin-top:6px;}
.cnt{text-align:center;font-weight:700;color:#064e2b;font-size:.9rem;margin:4px 0;}
.tbl{width:100%;border-collapse:collapse;font-size:.8rem;}
.tbl th{
  background:#064e2b;color:#fff;font-family:'Montserrat',sans-serif;
  font-weight:700;padding:6px;text-align:left;border:1px solid #d4a017;}
.tbl td{padding:6px;border:1px solid #cfd8cf;font-weight:600;color:#1d2b22;}
.tbl tr:nth-child(even) td{background:#f1f6f2;}
[data-testid="stHorizontalBlock"]{flex-wrap:nowrap !important;gap:.5rem !important;}
[data-testid="stHorizontalBlock"]>div{
  min-width:0 !important;flex:1 1 0 !important;width:auto !important;}
[data-testid="stForm"]{
  border:2px solid #0b7a43;border-radius:12px;background:#fff;}
[data-testid="stWidgetLabel"] p{font-weight:700;color:#064e2b;}
div[role="radiogroup"]{flex-wrap:wrap;gap:.2rem .9rem;}
div[role="radiogroup"] label p{font-weight:700;color:#064e2b;font-size:.9rem;}
.stButton button,[data-testid="stFormSubmitButton"] button{
  background:#064e2b;border:2px solid #d4a017;border-radius:10px;width:100%;}
.stButton button p,[data-testid="stFormSubmitButton"] button p{
  color:#fff !important;font-weight:700;font-size:.9rem;}
</style>""")

# ====== HEADER: logo left, gold name plate middle, coat right ======
logo = img_uri("logo.png")
coat = img_uri("coat.png")
logo_html = '<img src="%s" alt="Logo">' % logo if logo else ""
coat_html = '<img src="%s" alt="Coat of arms">' % coat if coat else ""
md('<div class="hdr">%s<div class="hn"><div class="hn1">DEARson</div>'
   '<div class="hn2">Barbing Salon &amp; Technology</div></div>%s</div>'
   % (logo_html, coat_html))

user = st.session_state.get("user")

# ================= WELCOME + REGISTRATION =================
if not user:
    md('<div class="sec">Welcome</div>')
    md('<p class="lead">Barbing salon, phone &amp; gadget shop, and training '
       'academy. Register once to see our services and place orders.</p>')
    with st.form("register"):
        name = st.text_input("Full name")
        address = st.text_input("Address")
        phone = st.text_input("Phone number", placeholder="08012345678")
        submitted = st.form_submit_button("Enter site")
    if submitted:
        phone_c = re.sub(r"[\s-]", "", phone)
        if len(name.strip()) < 3 or len(address.strip()) < 5:
            st.error("Please enter your full name and full address.")
        elif not re.fullmatch(r"(0|\+?234)[789][01]\d{8}", phone_c):
            st.error("Enter a valid Nigerian phone number, e.g. 08012345678.")
        else:
            save_user(name.strip(), address.strip(), phone_c)
            st.session_state["user"] = {
                "name": name.strip(),
                "address": address.strip(),
                "phone": phone_c,
            }
            st.rerun()
else:
    # ================= MEMBERS-ONLY AREA =================
    page = st.radio("Menu", ["Home", "Services", "Academy"],
                    horizontal=True, label_visibility="collapsed")
    who = "I'm %s (%s)" % (user["name"], user["phone"])

    if page == "Home":
        first = user["name"].split()[0]
        md('<div class="sec">Hello, %s</div>' % html.escape(first))
        ceo = img_uri("ceo.jpg", "ceo.jpeg", "ceo.png")
        ceo_img = '<img src="%s" alt="CEO">' % ceo if ceo else ""
        md('<div class="card ceo">%s<div><div class="cn">%s</div>'
           '<div class="cr">Chief Executive Officer, %s.<br>'
           'Quality service, honest prices, skills that pay.</div></div></div>'
           % (ceo_img, html.escape(CEO_NAME), html.escape(SITE_NAME)))
        md(wbtn("Chat on WhatsApp",
                wa("Hello %s, %s. I need help." % (SITE_NAME, who))))
        delivery = ("HOME DELIVERY REQUEST\nName: %s\nPhone: %s\n"
                    "Address: %s\nItem/Service: "
                    % (user["name"], user["phone"], user["address"]))
        md(wbtn("Order Home Delivery", wa(delivery), alt=True))

    elif page == "Services":
        md('<div class="sec">Our Services</div>')

        # ---- view environment ----
        env_open = st.session_state.get("env_open", False)
        if env_open:
            env_label = "Hide Environment"
        else:
            env_label = "View Environment"
        st.button(env_label, key="b_env", on_click=toggle_env)
        if env_open:
            files = num_files("environment")
            if not files:
                st.info("No environment pictures uploaded yet.")
            else:
                i = st.session_state.get("env_i", 0)
                i = min(max(i, 0), len(files) - 1)
                st.session_state["env_i"] = i
                md('<div class="cnt">Our Environment: %d of %d</div>'
                   % (i + 1, len(files)))
                st.image(files[i])
                e1, e2 = st.columns(2)
                e1.button("◀ Previous", key="env_prev", on_click=step_env,
                          args=(-1,), disabled=(i == 0))
                e2.button("Next ▶", key="env_next", on_click=step_env,
                          args=(1,), disabled=(i >= len(files) - 1))

        barb_msg = "Hello, %s. I want to book: Barbing.\nAddress: %s" % (
            who, user["address"])
        md('<div class="card"><div class="ct">Barbing Salon</div><ul>'
           '<li>Haircut</li><li>Beard trim and shaping</li>'
           '<li>Hair dyeing</li><li>Kids haircut</li>'
           '<li>Home service barbing</li></ul>%s</div>'
           % wbtn("Book barbing on WhatsApp", wa(barb_msg)))
        tech_msg = "Hello, %s. I want to order: Phone/Gadgets.\nAddress: %s" % (
            who, user["address"])
        md('<div class="card"><div class="ct">Phone Tech &amp; Gadgets</div><ul>'
           '<li>New and used phones</li><li>Chargers, cables, earphones</li>'
           '<li>Power banks and accessories</li>'
           '<li>Screen and battery repair</li>'
           '<li>Software fixing and unlocking</li></ul>%s</div>'
           % wbtn("Order gadgets on WhatsApp", wa(tech_msg)))

    else:
        md('<div class="sec">Academy</div>')
        md('<p class="lead">Learn barbing and phone repair from working '
           'professionals. Every graduate receives a professional '
           'certificate.</p>')
        acad_msg = ("Hello, %s. I want to join the Academy "
                    "(barbing / phone repair)." % who)
        md(wbtn("Register for Academy", wa(acad_msg)))

        # ---- certificate viewer ----
        md('<div class="sec">Our Certificates</div>')
        b1, b2 = st.columns(2)
        b1.button("Professional", key="b_pro",
                  on_click=pick_cert, args=("pro",))
        if LOCK_ACADEMY:
            acad_label = "Academy 🔒"
        else:
            acad_label = "Academy"
        b2.button(acad_label, key="b_acad",
                  on_click=pick_cert, args=("academy",))

        view = st.session_state.get("cert_view")
        if view:
            if view == "pro":
                title = "Professional Certificate"
                files = num_files("pro_cert")
                allowed = True
            else:
                title = "Academy Certificate"
                files = num_files("academy_cert")
                allowed = True
                if LOCK_ACADEMY:
                    allowed = get_status(user["phone"]) == "approved"

            if not allowed:
                locked_box(user)
            elif not files:
                st.info("No %s uploaded yet." % title.lower())
            else:
                i = st.session_state.get("cert_i", 0)
                i = min(max(i, 0), len(files) - 1)
                st.session_state["cert_i"] = i
                md('<div class="cnt">%s: %d of %d</div>'
                   % (title, i + 1, len(files)))
                st.image(files[i])
                p1, p2 = st.columns(2)
                p1.button("◀ Previous", key="prev", on_click=step_cert,
                          args=(-1,), disabled=(i == 0))
                p2.button("Next ▶", key="next", on_click=step_cert,
                          args=(1,), disabled=(i >= len(files) - 1))

        # ---- certificates acquired table ----
        md(certs_table())

    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()

# ================= FOOTER (always visible) =================
md('<div class="foot">Contact us</div>')
md('<div class="calls">%s%s</div>' % (
    call_pill(PHONE_1, "Call line 1"), call_pill(PHONE_2, "Call line 2")))
md(wbtn("WhatsApp Chat", wa("Hello %s, I need help." % SITE_NAME)))
md('<div class="foot">&copy; %s</div>' % html.escape(SITE_NAME))

# ================= ADMIN (password protected) =================
with st.expander("Admin"):
    pw = st.text_input("Admin password", type="password")
    if pw and pw == ADMIN_PASSWORD:
        # ---- certificate permission requests ----
        st.subheader("Academy certificate requests")
        acc = read_acc()
        if not acc:
            st.write("No requests yet.")
        for r in acc:
            st.write("%s | %s | %s" % (
                r["name"], r["phone"], r["status"].upper()))
            a1, a2 = st.columns(2)
            a1.button("Approve", key="ap_" + r["phone"],
                      on_click=set_status, args=(r["phone"], "approved"))
            a2.button("Remove", key="rm_" + r["phone"],
                      on_click=set_status, args=(r["phone"], "removed"))

        # ---- registered users ----
        st.subheader("Registered users")
        rows = read_users()
        st.write("Total: %d" % len(rows))
        st.dataframe(rows)
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        st.download_button("Download users.csv", buf.getvalue(),
                           "users.csv", "text/csv")
    elif pw:
        st.error("Wrong password.")
