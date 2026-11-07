import os, re, csv, io, html, base64, urllib.parse
from datetime import datetime
import streamlit as st

# ---------- CHANGE THESE ----------
SITE_NAME = "Dearson Barbing & Technology"
CEO_NAME = "A. O JUWON"
PHONE_1 = "08161999686"
PHONE_2 = "0811878687"
WHATSAPP = "08161999686"
ADMIN_PASSWORD = "Google123"
# ----------------------------------

st.set_page_config(page_title=SITE_NAME, page_icon="✂️", layout="centered")
BASE = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE, "users.csv")
FIELDS = ["name", "address", "phone", "date"]


def H(s):
    return " ".join(s.split())


def md(s):
    st.markdown(H(s), unsafe_allow_html=True)


def img_uri(*names):
    for n in names:
        p = os.path.join(BASE, n)
        if os.path.exists(p):
            mime = "image/png" if n.lower().endswith(".png") else "image/jpeg"
            with open(p, "rb") as f:
                return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())
    return ""


def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


WA_PATH = ("M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.3-.15-1.263-.465-2.403-1.485-.888-.795-1.484-1.77-1.66-2.07-.174-.3-.019-.465.13-.615.136-.135.301-.345.451-.523.146-.181.194-.301.297-.496.1-.21.049-.375-.025-.524-.075-.15-.672-1.62-.922-2.206-.24-.584-.487-.51-.672-.51-.172-.015-.371-.015-.571-.015-.2 0-.523.074-.797.359-.273.3-1.045 1.02-1.045 2.475s1.07 2.865 1.219 3.075c.149.18 2.095 3.195 5.076 4.483.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414-.074-.123-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z")
PH_PATH = ("M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z")
WA_ICON = svg_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#fff" d="%s"/></svg>' % WA_PATH)
PH_ICON = svg_uri('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#d4a017" d="%s"/></svg>' % PH_PATH)


def intl(n):
    n = re.sub(r"\D", "", n)
    return "234" + n[1:] if n.startswith("0") else n


def wa(text):
    return "https://wa.me/%s?text=%s" % (intl(WHATSAPP), urllib.parse.quote(text))


def wbtn(label, link, alt=False):
    cls = "wbtn alt" if alt else "wbtn"
    return ('<a class="%s" href="%s" target="_blank" rel="noopener"><img src="%s" alt="">%s</a>'
            % (cls, html.escape(link), WA_ICON, label))


def call_pill(num, label):
    return ('<a class="call" href="tel:%s"><img src="%s" alt=""><span><small>%s</small><b>%s</b></span></a>'
            % (num, PH_ICON, label, num))


def read_users():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_user(name, address, phone):
    rows = [r for r in read_users() if r["phone"] != phone]
    rows.append({"name": name, "address": address, "phone": phone,
                 "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


# ---------- STYLE ----------
md("""<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
.stApp{background:#e3eee6;font-family:'Poppins',sans-serif;}
.stApp p,.stApp li,.stApp label,.stApp input{font-family:'Poppins',sans-serif;}
div.block-container{max-width:720px;margin:3.2rem auto 1.5rem auto;padding:1.4rem 1.1rem 1.6rem 1.1rem !important;
background:#fffdf5;border:4px solid #064e2b;border-radius:18px;
box-shadow:inset 0 0 0 4px #fffdf5,inset 0 0 0 7px #d4a017,0 6px 18px rgba(6,78,43,.35);}
.hdr{display:flex;align-items:center;justify-content:space-between;gap:8px;
background:linear-gradient(135deg,#064e2b,#0b7a43);border-bottom:5px solid #d4a017;border-radius:12px;padding:12px;margin-bottom:14px;}
.hdr img{width:clamp(72px,24vw,104px);height:clamp(72px,24vw,104px);object-fit:contain;background:#fff;border-radius:12px;padding:4px;flex:none;}
.hn{flex:1;text-align:center;color:#fff;font-family:'Montserrat',sans-serif;font-weight:800;font-size:clamp(.95rem,4.2vw,1.4rem);line-height:1.2;}
.sec{font-family:'Montserrat',sans-serif;font-weight:800;color:#064e2b;font-size:1.4rem;border-bottom:3px solid #d4a017;display:inline-block;padding-bottom:2px;margin:6px 0 8px 0;}
.lead{font-weight:600;color:#1d2b22;font-size:1rem;line-height:1.6;}
.card{background:#fff;border:2px solid #0b7a43;border-left:8px solid #d4a017;border-radius:12px;padding:12px 14px;margin:12px 0;box-shadow:0 2px 6px rgba(0,0,0,.15);}
.ct{font-family:'Montserrat',sans-serif;font-weight:800;font-size:1.15rem;color:#064e2b;margin-bottom:4px;}
.card ul{margin:0 0 6px 0;padding-left:1.1rem;}
.card li{font-weight:600;color:#1d2b22;font-size:.98rem;line-height:1.7;}
.wbtn{display:flex;align-items:center;justify-content:center;gap:8px;background:#1fa855;color:#fff !important;font-weight:700;text-decoration:none !important;border-radius:10px;padding:11px 14px;margin:8px 0;font-size:.98rem;box-shadow:0 2px 4px rgba(0,0,0,.2);}
.wbtn.alt{background:#064e2b;border:2px solid #d4a017;}
.wbtn img{width:16px;height:16px;}
.calls{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0;}
.call{flex:1;min-width:140px;display:flex;align-items:center;gap:8px;background:#064e2b;border:2px solid #d4a017;border-radius:10px;padding:8px 10px;text-decoration:none !important;}
.call img{width:16px;height:16px;}
.call small{display:block;color:#d9e8dd;font-size:.65rem;font-weight:500;line-height:1.2;}
.call b{color:#fff;font-size:.95rem;font-weight:700;}
.ceo{display:flex;gap:12px;align-items:center;}
.ceo img{width:110px;height:130px;object-fit:cover;border-radius:12px;border:4px solid #d4a017;}
.cn{font-family:'Montserrat',sans-serif;font-weight:800;font-size:1.2rem;color:#064e2b;}
.cr{font-weight:600;color:#333;font-size:.9rem;line-height:1.5;}
.cert{border:6px double #c9a227;background:#fffdf3;text-align:center;padding:20px;color:#16221b;border-radius:6px;margin:12px 0;font-weight:600;}
.cert .big{font-family:'Montserrat',sans-serif;font-weight:800;font-size:1.3rem;color:#064e2b;margin:6px 0;}
.foot{text-align:center;font-weight:700;color:#064e2b;font-size:.85rem;margin-top:6px;}
[data-testid="stForm"]{border:2px solid #0b7a43;border-radius:12px;background:#fff;}
[data-testid="stWidgetLabel"] p{font-weight:700;color:#064e2b;}
div[role="radiogroup"] label p{font-weight:700;color:#064e2b;}
.stButton button,[data-testid="stFormSubmitButton"] button{background:#064e2b;border:2px solid #d4a017;border-radius:10px;}
.stButton button p,[data-testid="stFormSubmitButton"] button p{color:#fff !important;font-weight:700;}
</style>""")

# ---------- HEADER: logo left, name middle, coat of arms right ----------
logo = img_uri("logo.png")
coat = img_uri("coat.png")
md('<div class="hdr">%s<div class="hn">%s</div>%s</div>' % (
    '<img src="%s" alt="Logo">' % logo if logo else "",
    html.escape(SITE_NAME),
    '<img src="%s" alt="Nigeria coat of arms">' % coat if coat else ""))

user = st.session_state.get("user")

# ---------- WELCOME + REGISTRATION ----------
if not user:
    md('<div class="sec">Welcome</div>')
    md('<p class="lead">Barbing salon, phone &amp; gadget shop, and training academy. '
       'Register once to see our services and place orders.</p>')
    with st.form("register"):
        name = st.text_input("Full name")
        address = st.text_input("Address")
        phone = st.text_input("Phone number", placeholder="08012345678")
        go = st.form_submit_button("Enter site")
    if go:
        phone_c = re.sub(r"[\s-]", "", phone)
        if len(name.strip()) < 3 or len(address.strip()) < 5:
            st.error("Please enter your full name and full address.")
        elif not re.fullmatch(r"(0|\+?234)[789][01]\d{8}", phone_c):
            st.error("Enter a valid Nigerian phone number, e.g. 08012345678.")
        else:
            save_user(name.strip(), address.strip(), phone_c)
            st.session_state["user"] = {"name": name.strip(),
                                        "address": address.strip(), "phone": phone_c}
            st.rerun()
else:
    # ---------- MEMBERS-ONLY AREA ----------
    page = st.radio("Menu", ["Home", "Services", "Academy"], horizontal=True,
                    label_visibility="collapsed")
    who = "I'm %s (%s)" % (user["name"], user["phone"])

    if page == "Home":
        md('<div class="sec">Hello, %s</div>' % html.escape(user["name"].split()[0]))
        ceo = img_uri("ceo.jpg", "ceo.jpeg", "ceo.png")
        md('<div class="card ceo">%s<div><div class="cn">%s</div><div class="cr">Chief Executive Officer, %s.<br>'
           'Quality service, honest prices, skills that pay.</div></div></div>' % (
               '<img src="%s" alt="CEO">' % ceo if ceo else "",
               html.escape(CEO_NAME), html.escape(SITE_NAME)))
        md(wbtn("Chat on WhatsApp", wa("Hello %s, %s. I need help." % (SITE_NAME, who))))
        md(wbtn("Order Home Delivery",
                wa("HOME DELIVERY REQUEST\nName: %s\nPhone: %s\nAddress: %s\nItem/Service: "
                   % (user["name"], user["phone"], user["address"])), alt=True))

    elif page == "Services":
        md('<div class="sec">Our Services</div>')
        md('<div class="card"><div class="ct">Barbing Salon</div><ul><li>Haircut</li>'
           '<li>Beard trim and shaping</li><li>Hair dyeing</li><li>Kids haircut</li>'
           '<li>Home service barbing</li></ul>%s</div>' % wbtn(
               "Book barbing on WhatsApp",
               wa("Hello, %s. I want to book: Barbing.\nAddress: %s" % (who, user["address"]))))
        md('<div class="card"><div class="ct">Phone Tech &amp; Gadgets</div><ul><li>New and used phones</li>'
           '<li>Chargers, cables, earphones</li><li>Power banks and accessories</li>'
           '<li>Screen and battery repair</li><li>Software fixing and unlocking</li></ul>%s</div>' % wbtn(
               "Order gadgets on WhatsApp",
               wa("Hello, %s. I want to order: Phone/Gadgets.\nAddress: %s" % (who, user["address"]))))

    else:
        md('<div class="sec">Academy</div>')
        md('<p class="lead">Learn barbing and phone repair from working professionals. '
           'Every graduate receives a professional certificate.</p>')
        md(wbtn("Register for Academy",
                wa("Hello, %s. I want to join the Academy (barbing / phone repair)." % who)))
        md('<div class="cert"><div>%s Academy</div><div class="big">Professional Certificate</div>'
           '<div>This is to certify that</div><div class="big">%s</div>'
           '<div>has successfully completed training and is awarded this certificate.</div>'
           '<div style="margin-top:10px">Signed: %s</div></div>' % (
               html.escape(SITE_NAME), html.escape(user["name"]), html.escape(CEO_NAME)))

    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()

# ---------- FOOTER (always visible) ----------
md('<div class="foot">Contact us</div>')
md('<div class="calls">%s%s</div>' % (call_pill(PHONE_1, "Call line 1"),
                                       call_pill(PHONE_2, "Call line 2")))
md(wbtn("WhatsApp Chat", wa("Hello %s, I need help." % SITE_NAME)))
md('<div class="foot">&copy; %s</div>' % html.escape(SITE_NAME))

# ---------- ADMIN (password protected) ----------
with st.expander("Admin"):
    pw = st.text_input("Admin password", type="password")
    if pw and pw == ADMIN_PASSWORD:
        rows = read_users()
        st.write("Registered users: %d" % len(rows))
        st.dataframe(rows)
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
        st.download_button("Download users.csv", buf.getvalue(), "users.csv", "text/csv")
    elif pw:
        st.error("Wrong password.")
