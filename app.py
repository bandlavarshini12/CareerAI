import streamlit as st
import json

st.set_page_config(page_title="CareerAI", page_icon="🎓", layout="wide")

# Load data
with open("careers.json", encoding="utf-8") as f:
    careers = json.load(f)

# CSS
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#eef2ff,#fff,#f5f3ff)}
[data-testid="stSidebar"]{background:linear-gradient(#172554,#4c1d95)}
.hero{background:linear-gradient(135deg,#2563eb,#7c3aed);color:white;
padding:25px;border-radius:20px;text-align:center;margin-bottom:20px}
.hero h1, .hero p, .hero h2, .hero h3, .hero h4, .hero h5, .hero h6, .hero *{color:white!important}
.card{background:white;padding:20px;border-radius:15px;
margin:12px 0;box-shadow:0 4px 15px #0001}
.metric{text-align:center;background:white;padding:20px;border-radius:15px;
box-shadow:0 4px 15px #0001}.num{font-size:30px;font-weight:bold;color:#2563eb}
.skill{display:inline-block;background:#eff6ff;color:#2563eb;padding:6px 10px;
margin:3px;border-radius:15px}.missing{display:inline-block;background:#fef2f2;
color:#dc2626;padding:6px 10px;margin:3px;border-radius:15px}
.step{background:#f5f3ff;padding:10px;margin:5px;border-radius:8px;color:#4c1d95}.stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp .stMarkdown, .stApp .stTextInput, .stApp .stSelectbox, .stApp .stMultiselect,
.stApp .stSlider, .stApp .stRadio, .card, .metric, .step { color:#111!important; }
[data-testid="stSidebar"], [data-testid="stSidebar"] * { color:white!important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stRadio, [data-testid="stSidebar"] .stMarkdown { color:white!important; }</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center'>🎓 CareerAI</h1>"
        "<p style='text-align:center'>Smart Student Career Assistant</p>"
        "<p style='text-align:center'>🟢 Online</p>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🎯 Analyzer", "📊 Explorer", "ℹ️ About"]
    )


# Header function
def header(title, text):
    st.markdown(
        f"<div class='hero'><h1>{title}</h1><p>{text}</p></div>",
        unsafe_allow_html=True
    )


# HOME
if page == "🏠 Home":

    header("🎓 CareerAI", "Smart Student Career Assistant")

    st.markdown("""
    <div class="card">
    <h2>👋 Welcome to CareerAI</h2>
    <p>Find suitable technology careers using your skills and interests.</p>
    <h3>How it works</h3>
    <p>👨‍🎓 Profile → 💻 Skills → ❤️ Interest → 🎯 Matching →
    📚 Skill Gap → 🛣️ Roadmap</p>
    </div>
    """, unsafe_allow_html=True)

    a,b,c = st.columns(3)

    for col,num,text in [
        (a,"12+","Career Paths"),
        (b,"50+","Skills"),
        (c,"100%","Interactive")
    ]:
        col.markdown(
            f"<div class='metric'><div class='num'>{num}</div>{text}</div>",
            unsafe_allow_html=True
        )


# ANALYZER
elif page == "🎯 Analyzer":

    header("🎯 Career Analyzer","Find the career matching your profile")

    c1,c2 = st.columns(2)

    with c1:
        name = st.text_input("👤 Name")
        degree = st.selectbox(
            "🎓 Degree",
            ["B.Tech","B.Sc","BCA","MCA","M.Tech","MBA","Other"]
        )
        percentage = st.slider("📊 Percentage",0,100,75)

    extra_skills = [
        "C Programming", "C++", "Java", "Python", "JavaScript", "TypeScript",
        "C#", "PHP", "Ruby", "Go (Golang)", "Rust", "Kotlin", "Swift",
        "R Programming", "SQL", "HTML", "CSS", "Dart", "MATLAB",
        "Perl","Objective-C", "Visual Basic"
    ]

    skills_all = sorted({
        *{s for c in careers for s in c["skills"]},
        *extra_skills,
    })

    interests_all = sorted({
        i for c in careers for i in c["interests"]
    })

    with c2:
        skills = st.multiselect("💻 Your Skills", skills_all)
        interest = st.selectbox("❤️ Interest", interests_all)

    if st.button("🚀 ANALYZE CAREER", type="primary",
                 use_container_width=True):

        if not name or not skills:
            st.warning("Enter your name and select your skills.")

        else:
            results = []

            for c in careers:
                matches = len(set(skills) & set(c["skills"]))
                score = matches / len(c["skills"]) * 75
                score += 25 if interest in c["interests"] else 0

                results.append((
                    min(round(score),100),
                    c,
                    matches,
                    [s for s in c["skills"] if s not in skills]
                ))

            score,c,matches,missing = max(
                results,key=lambda x:x[0]
            )

            st.markdown(f"""
            <div class="hero">
            <h1>{c["icon"]} {c["career"]}</h1>
            <h1>{score}%</h1>
            <p>Career Match for {name}</p>
            </div>
            """, unsafe_allow_html=True)

            a,b,d = st.columns(3)

            a.metric("🎯 Match",f"{score}%")
            b.metric("💻 Matching Skills",matches)
            d.metric("📚 Skills to Learn",len(missing))

            st.markdown(
                "<div class='card'><h2>💻 Your Skills</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "".join(
                    f"<span class='skill'>✅ {s}</span>"
                    for s in skills
                ),
                unsafe_allow_html=True
            )

            st.markdown("</div>",unsafe_allow_html=True)

            st.markdown(
                "<div class='card'><h2>📚 Skills to Learn</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "".join(
                    f"<span class='missing'>❌ {s}</span>"
                    for s in missing
                ) or "🎉 No missing skills!",
                unsafe_allow_html=True
            )

            st.markdown("</div>",unsafe_allow_html=True)

            st.markdown(
                "<div class='card'><h2>🛣️ Learning Roadmap</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "".join(
                    f"<div class='step'>{i}️⃣ {s}</div>"
                    for i,s in enumerate(c["roadmap"],1)
                ),
                unsafe_allow_html=True
            )

            st.markdown("</div>",unsafe_allow_html=True)


# EXPLORER
elif page == "📊 Explorer":

    header("📊 Career Explorer","Explore available technology careers")

    for c in careers:
        with st.expander(f'{c["icon"]} {c["career"]}'):
            st.write("**Skills:**", ", ".join(c["skills"]))
            st.write("**Interests:**", ", ".join(c["interests"]))
            st.write("**Roadmap:**", " → ".join(c["roadmap"]))


# ABOUT
else:

    header("ℹ️ About CareerAI","Smart Student Career Assistant")

    st.markdown("""
    <div class="card">
    <h2>🎓 CareerAI</h2>
    <p>Career recommendation system for students.</p>
    <h3>🛠 Technologies</h3>
    <p>Python • Streamlit • JSON</p>
    <h3>🧠 Architecture</h3>
    <p>Profile → Skills → Matching → Career → Skill Gap → Roadmap</p>
    </div>
    """, unsafe_allow_html=True)