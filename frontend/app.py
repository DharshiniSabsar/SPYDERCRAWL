import streamlit as st
import plotly.express as px
import networkx as nx
import pandas as pd
from styles import apply_styles
from db_reader import load_market_data
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.nlp.image_classifier import classify_image_from_pil

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SpyderCrawl",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_styles()

# -------------------------------------------------
# 🔥 CUSTOM UI STYLES (Glow + Gradient)
# -------------------------------------------------
st.markdown("""
<style>
hr { display: none; }

.alert-card {
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 14px;
    transition: all 0.3s ease;
    cursor: pointer;
}

/* 🔴 HIGH */
.alert-high {
    background: linear-gradient(90deg, #2a0f0f, #4b1a1a);
    border-left: 5px solid #ff4b4b;
}

/* 🟠 MEDIUM */
.alert-medium {
    background: linear-gradient(90deg, #2a1f0f, #4b341a);
    border-left: 5px solid #ffb347;
}

/* 🟢 LOW */
.alert-low {
    background: linear-gradient(90deg, #0f2a1a, #1a4b2e);
    border-left: 5px solid #4bff88;
}

/* ✨ HOVER GLOW */
.alert-card:hover {
    transform: scale(1.015);
    box-shadow: 0 0 18px rgba(255, 75, 75, 0.35);
}

/* clickable links */
.alert-link {
    color: #ff6b6b;
    text-decoration: none;
}
.alert-link:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "login"


def go_to(page):
    st.session_state.page = page
    st.rerun()


# -------------------------------------------------
# NAV BAR
# -------------------------------------------------
def nav_bar(current):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

    with col1:
        st.markdown("### 🕷️ SpyderCrawl")

    with col2:
        if st.button("📊 Intelligence", disabled=current == "dashboard", use_container_width=True):
            go_to("dashboard")

    with col3:
        if st.button("📈 Analytics", disabled=current == "analytics", use_container_width=True):
            go_to("analytics")

    with col4:
        if st.button("🖼️ Images", disabled=current == "images", use_container_width=True):
            go_to("images")

    st.markdown("---")


# -------------------------------------------------
# PAGE: LOGIN
# -------------------------------------------------
def page_login():
    st.title("🕷️ SpyderCrawl")
    st.subheader("Biohacking Intelligence & Threat Monitoring Platform")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "spydercrawl":
            st.session_state.authenticated = True
            go_to("dashboard")
        else:
            st.error("Invalid credentials")


# -------------------------------------------------
# ALERT CARD RENDER FUNCTION
# -------------------------------------------------
def render_alert(row):
    level = row["Threat Level"]

    if level == "HIGH":
        css_class = "alert-high"
    elif level == "MEDIUM":
        css_class = "alert-medium"
    else:
        css_class = "alert-low"

    st.markdown(f"""
    <div class="alert-card {css_class}">
        🔴 <b>{level}-RISK ALERT</b><br><br>
        <b>Vendor:</b> {row['Vendor']}<br>
        <b>URL:</b> <a href="{row['URL']}" target="_blank" class="alert-link">{row['URL']}</a>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
def page_dashboard():
    nav_bar("dashboard")
    st.title("📊 Intelligence Dashboard")

    data = load_market_data()

    if data.empty:
        st.info("No data available.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pages Monitored", len(data))
    c2.metric("High-Risk Pages", len(data[data["Threat Level"] == "HIGH"]))
    c3.metric("Sources Identified", data["Vendor"].nunique())
    c4.metric("Active Alerts", len(data[data["Threat Level"] == "HIGH"]))

    st.markdown("---")

    st.subheader("🔍 Intelligence Feed")
    st.dataframe(data[["Title", "Vendor", "Threat Level", "URL"]])

    st.markdown("---")

    # ---------------- ALERTS ----------------
    st.subheader("🚨 Top 10 High-Risk Alerts")

    high_risk = data[data["Threat Level"] == "HIGH"]

    if high_risk.empty:
        st.success("No high-risk activity.")
        return

    top10 = high_risk.head(10)

    for _, row in top10.iterrows():
        st.warning(row["URL"])

    total_alerts = len(high_risk)

    if total_alerts > 10:
        st.markdown(f"*Showing 10 of {total_alerts} alerts*")

        if st.button(f"🔍 See all {total_alerts} alerts →"):
            go_to("alerts")


# -------------------------------------------------
# ALERTS PAGE
# -------------------------------------------------
def page_alerts():
    nav_bar("alerts")
    st.title("🚨 All High-Risk Alerts")

    data = load_market_data()
    alerts = data[data["Threat Level"] == "HIGH"]

    if alerts.empty:
        st.success("No high-risk activity.")
        return

    search = st.text_input("🔍 Search alerts")

    if search:
        alerts = alerts[
            alerts.apply(
                lambda row: search.lower() in str(row["Vendor"]).lower()
                or search.lower() in str(row["URL"]).lower()
                or search.lower() in str(row["Title"]).lower(),
                axis=1
            )
        ]

    st.markdown(f"### Showing {len(alerts)} results")

    for _, row in alerts.iterrows():
        render_alert(row)

    if st.button("⬅️ Back to Dashboard"):
        go_to("dashboard")


# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
def page_analytics():
    nav_bar("analytics")
    st.title("📈 Analytics")

    data = load_market_data()

    if data.empty:
        return

    timeline_df = (
        data.groupby(pd.Grouper(key="Timestamp", freq="D"))
        .size()
        .reset_index(name="Pages")
    )

    fig = px.line(timeline_df, x="Timestamp", y="Pages")
    st.plotly_chart(fig)

    # HEATMAP
    st.subheader("🔥 Domain-wise Risk Heatmap")

    heatmap_df = (
        data
        .groupby(["Vendor", "Threat Level"])
        .size()
        .reset_index(name="Count")
    )

    fig_heatmap = px.density_heatmap(
        heatmap_df,
        x="Vendor",
        y="Threat Level",
        z="Count",
        color_continuous_scale="Reds",
        title="Biohacking Risk Intensity by Domain"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("""
    <div style="background-color:#1a1a2e; border-left: 4px solid #ff4b4b; border-radius: 10px; padding: 14px 20px; margin-top:-8px; margin-bottom:8px; font-size:0.84rem; color:#cccccc; line-height:1.8;">
        <div style="font-size:0.95rem; font-weight:700; color:#ff6b6b; margin-bottom:8px;">🗺️ How to read this heatmap</div>
        <div style="display:flex; flex-wrap:wrap; gap:14px 28px;">
            <div>🌐 &nbsp;<b style="color:#e0e0e0;">Columns</b> — each column is a crawled website (domain)</div>
            <div>📊 &nbsp;<b style="color:#e0e0e0;">Rows</b> — threat level: <span style="color:#ff9999; font-weight:600;">HIGH</span> &nbsp;|&nbsp; <span style="color:#ffcc99; font-weight:600;">MEDIUM</span></div>
            <div>🟥 &nbsp;<b style="color:#e0e0e0;">Darker red</b> — higher concentration of risk-flagged content on that domain</div>
            <div>⬜ &nbsp;<b style="color:#e0e0e0;">Light / empty</b> — little to no flagged content detected</div>
        </div>
        <div style="margin-top:10px; color:#888888; font-style:italic;">💡 Domains with dark red in the <span style="color:#ff9999;">HIGH</span> row are top-priority sources for biosecurity review.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # NETWORK GRAPH
    st.subheader("🕸️ Biohacking Intelligence Network")

    def extract_keywords(desc):
        if not isinstance(desc, str):
            return []
        if "Matched keywords:" not in desc:
            return []
        return [k.strip() for k in desc.replace("Matched keywords:", "").split(",")]

    G = nx.Graph()

    for _, row in data.iterrows():
        domain = row["Vendor"]
        keywords = extract_keywords(row["Description"])
        G.add_node(domain, node_type="domain")
        for kw in keywords:
            G.add_node(kw, node_type="keyword")
            if G.has_edge(domain, kw):
                G[domain][kw]["weight"] += 1
            else:
                G.add_edge(domain, kw, weight=1)

    MAX_NODES = 30
    if G.number_of_nodes() > MAX_NODES:
        top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:MAX_NODES]
        G = G.subgraph([n for n, _ in top_nodes]).copy()

    pos = nx.spring_layout(G, seed=42, k=0.6)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = px.line(x=edge_x, y=edge_y).update_traces(
        line=dict(width=1, color="#888")
    )

    node_x, node_y, node_color, node_size, node_text = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        if G.nodes[node]["node_type"] == "domain":
            node_color.append("red")
            node_size.append(26)
        else:
            node_color.append("blue")
            node_size.append(16)

    node_trace = px.scatter(x=node_x, y=node_y, text=node_text).update_traces(
        mode="markers+text",
        marker=dict(size=node_size, color=node_color, opacity=0.85,
                    line=dict(width=1, color="black")),
        textposition="top center"
    )

    fig_network = {
        "data": edge_trace.data + node_trace.data,
        "layout": {
            "title": "Domain–Keyword Biohacking Intelligence Graph",
            "showlegend": False,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "height": 650,
        },
    }

    st.plotly_chart(fig_network, use_container_width=True)

    st.markdown("""
    <div style="background-color:#0d1b2a; border-left: 4px solid #00bcd4; border-radius: 10px; padding: 14px 20px; margin-top:-8px; margin-bottom:8px; font-size:0.84rem; color:#cccccc; line-height:1.8;">
        <div style="font-size:0.95rem; font-weight:700; color:#00e5ff; margin-bottom:10px;">🕸️ How to read this network graph</div>
        <div style="display:flex; flex-wrap:wrap; gap:14px 28px; margin-bottom:8px;">
            <div>🔴 &nbsp;<b style="color:#ff6b6b;">Red nodes</b> — websites / crawled domains</div>
            <div>🔵 &nbsp;<b style="color:#64b5f6;">Blue nodes</b> — biohacking keywords &amp; concepts extracted from page content</div>
            <div>➖ &nbsp;<b style="color:#e0e0e0;">Edges (lines)</b> — a keyword was found on that domain's page</div>
            <div>🫧 &nbsp;<b style="color:#e0e0e0;">Dense clusters</b> — highly interconnected domains and topics; hotspots of biosecurity-relevant activity</div>
        </div>
        <div style="color:#888888; font-style:italic;">💡 Domains sitting at the centre of a dense cluster are likely the most influential sources in the intelligence network.</div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# IMAGES
# -------------------------------------------------
def page_images():
    nav_bar("images")
    st.title("🖼️ Image Intelligence")

    from pymongo import MongoClient
    import gridfs
    from PIL import Image
    import io
    from bson import ObjectId

    client = MongoClient("mongodb://localhost:27017")
    db = client.spydercrawl
    fs = gridfs.GridFS(db)

    data = load_market_data()
    high = data[data["Threat Level"] == "HIGH"]

    for _, row in high.iterrows():
        for img_id in row.get("image_ids", [])[:2]:
            try:
                image_bytes = fs.get(ObjectId(img_id)).read()
                image = Image.open(io.BytesIO(image_bytes))

                if classify_image_from_pil(image) == "HIGH":
                    st.image(image, width=250)

            except:
                continue


# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if not st.session_state.authenticated:
    page_login()
else:
    if st.session_state.page == "dashboard":
        page_dashboard()
    elif st.session_state.page == "analytics":
        page_analytics()
    elif st.session_state.page == "images":
        page_images()
    elif st.session_state.page == "alerts":
        page_alerts()
    else:
        page_dashboard()