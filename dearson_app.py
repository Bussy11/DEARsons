import os, re, csv, io, html, urllib.parse
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


def pic(name):
    p = os.path.join(BASE, name)
    return p if os.path.exists(p) else None


def wa(text):
    return "https://wa.me/%s?text=%s" % (WHATSAPP, urllib.parse.quote(text))


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


# ---------- HEADER: coat of arms | logo + name | coat of arms ----------
left, mid, right = st.columns([1, 2, 1])
with left:
    if pic("coat.png"):
        st.image(pic("coat.png"), width=80)
with mid:
    if pic("logo.png"):
        st.image(pic("logo.png"), width=80)
    st.markdown("<h3 style='text-align:center;margin:0'>%s</h3>" % html.escape(SITE_NAME),
                unsafe_allow_html=True)
with right:
    if pic("coat.png"):
        st.image(pic("coat.png"), width=80)
st.divider()

user = st.session_state.get("user")

# ---------- WELCOME + REGISTRATION ----------
if not user:
    st.header("Welcome")
    st.write("Barbing salon, phone & gadget shop, and training academy. "
             "Register once to see our services and place orders.")
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
        st.header("Hello, %s" % user["name"].split()[0])
        c1, c2 = st.columns([1, 2])
        with c1:
            if pic("ceo.jpg"):
                st.image(pic("ceo.jpg"), width=140)
        with c2:
            st.subheader(CEO_NAME)
            st.write("Chief Executive Officer, %s. Quality service, honest prices, skills that pay." % SITE_NAME)
        st.link_button("Chat on WhatsApp", wa("Hello %s, %s. I need help." % (SITE_NAME, who)),
                       use_container_width=True)
        st.link_button("Order Home Delivery",
                       wa("HOME DELIVERY REQUEST\nName: %s\nPhone: %s\nAddress: %s\nItem/Service: "
                          % (user["name"], user["phone"], user["address"])),
                       use_container_width=True)

    elif page == "Services":
        st.header("Our Services")
        st.subheader("Barbing Salon")
        st.write("- Haircut\n- Beard trim and shaping\n- Hair dyeing\n- Kids haircut\n- Home service barbing")
        st.link_button("Book barbing on WhatsApp",
                       wa("Hello, %s. I want to book: Barbing.\nAddress: %s" % (who, user["address"])))
        st.subheader("Phone Tech & Gadgets")
        st.write("- New and used phones\n- Chargers, cables, earphones\n- Power banks and accessories\n"
                 "- Screen and battery repair\n- Software fixing and unlocking")
        st.link_button("Order gadgets on WhatsApp",
                       wa("Hello, %s. I want to order: Phone/Gadgets.\nAddress: %s" % (who, user["address"])))

    else:
        st.header("%s Academy" % SITE_NAME)
        st.write("Learn barbing and phone repair from working professionals. "
                 "Every graduate receives a professional certificate.")
        st.link_button("Register for Academy",
                       wa("Hello, %s. I want to join the Academy (barbing / phone repair)." % who))
        st.markdown(
            "<div style='border:6px double #c9a227;background:#fffdf3;text-align:center;"
            "padding:20px;color:#16221b'><p>%s Academy</p>"
            "<h3 style='color:#06452a'>Professional Certificate</h3>"
            "<p>This is to certify that</p><p><b>%s</b></p>"
            "<p>has successfully completed training and is awarded this certificate.</p>"
            "<p>Signed: %s</p></div>"
            % (html.escape(SITE_NAME), html.escape(user["name"]), html.escape(CEO_NAME)),
            unsafe_allow_html=True)

    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()

# ---------- FOOTER (always visible) ----------
st.divider()
st.markdown("<p style='text-align:center'>Call: <a href='tel:%s'>%s</a> | <a href='tel:%s'>%s</a></p>"
            % (PHONE_1, PHONE_1, PHONE_2, PHONE_2), unsafe_allow_html=True)
st.link_button("WhatsApp Chat", wa("Hello %s, I need help." % SITE_NAME), use_container_width=True)

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
