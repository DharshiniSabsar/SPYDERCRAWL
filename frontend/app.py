import streamlit as st
import plotly.express as px
import networkx as nx
import pandas as pd
from styles import apply_styles
from db_reader import load_market_data

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
# SESSION STATE DEFAULTS
# -------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "login"

def go_to(page):
    st.session_state.page = page
    st.rerun()

# -------------------------------------------------
# NAV BAR (shown on all authenticated pages)
# -------------------------------------------------
def nav_bar(current):
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
            width: 100%;
            white-space: nowrap;
        }
        </style>
    """, unsafe_allow_html=True)

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([4, 0.5, 2, 2])
    with col_nav1:
        st.markdown("### 🕷️ SpyderCrawl")
    with col_nav3:
        if st.button(
            "📊 Intelligence",
            disabled=(current == "dashboard"),
            use_container_width=True
        ):
            go_to("dashboard")
    with col_nav4:
        if st.button(
            "📈 Analytics",
            disabled=(current == "analytics"),
            use_container_width=True
        ):
            go_to("analytics")
    st.markdown("---")

# -------------------------------------------------
# PAGE: LOGIN
# -------------------------------------------------
def page_login():
    st.title("🕷️ SpyderCrawl")
    st.subheader("Biohacking Intelligence & Threat Monitoring Platform")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "spydercrawl":
                st.session_state.authenticated = True
                go_to("dashboard")
            else:
                st.error("Invalid credentials")

# -------------------------------------------------
# PAGE: INTELLIGENCE DASHBOARD (app1)
# -------------------------------------------------
def page_dashboard():
    nav_bar("dashboard")
    st.title("📊 Intelligence Dashboard")

    data = load_market_data()

    if data.empty:
        st.info("No biohacking intelligence collected yet. Run `scrapy crawl market`.")
        return

    # KPI CARDS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pages Monitored", len(data))
    c2.metric("High-Risk Pages", len(data[data["Threat Level"] == "HIGH"]))
    c3.metric("Sources Identified", data["Vendor"].nunique())
    c4.metric("Active Alerts", len(data[data["Threat Level"] == "HIGH"]))

    st.markdown("---")

    # INTELLIGENCE FEED TABLE
    st.subheader("🔍 Intelligence Feed")
    st.dataframe(
        data[["Title", "Vendor", "Threat Level", "URL"]],
        use_container_width=True
    )

    st.markdown("---")

    # TOP 10 ALERTS
    st.subheader("🚨 Top 10 High-Risk Alerts")

    high_risk = data[data["Threat Level"] == "HIGH"].reset_index(drop=True)

    if high_risk.empty:
        st.success("No high-risk biohacking activity detected.")
    else:
        top10 = high_risk.head(10)

        for _, row in top10.iterrows():
            st.warning(
                f"""
                {row['URL']}
                """
            )

        total_alerts = len(high_risk)

        if total_alerts > 10:
            st.markdown(f"*Showing 10 of **{total_alerts}** high-risk alerts.*")
            if st.button(f"🔍 See all {total_alerts} alerts →"):
                go_to("alerts")
        else:
            st.markdown(f"*Showing all **{total_alerts}** high-risk alerts.*")

# -------------------------------------------------
# PAGE: ANALYTICS & VISUALISATIONS (app2)
# -------------------------------------------------
def page_analytics():
    nav_bar("analytics")
    st.title("📈 Analytics & Visualisations")

    data = load_market_data()

    if data.empty:
        st.info("No biohacking intelligence collected yet. Run `scrapy crawl market`.")
        return

    # TIMELINE
    st.subheader("📈 Biohacking Activity Timeline")

    timeline_df = (
        data
        .groupby(pd.Grouper(key="Timestamp", freq="D"))
        .size()
        .reset_index(name="Pages")
    )

    fig_timeline = px.line(
        timeline_df,
        x="Timestamp",
        y="Pages",
        markers=True,
        title="Biohacking Intelligence Over Time"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("---")

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
# PAGE: ALL ALERTS
# -------------------------------------------------
def page_alerts():
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
            width: 100%;
            white-space: nowrap;
        }
        </style>
    """, unsafe_allow_html=True)

    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([4, 0.5, 2, 2])
    with col_nav1:
        st.markdown("### 🕷️ SpyderCrawl")
    with col_nav3:
        if st.button("← Intelligence Dashboard", use_container_width=True):
            go_to("dashboard")
    with col_nav4:
        if st.button("📈 Analytics", use_container_width=True):
            go_to("analytics")
    st.markdown("---")

    st.title("🚨 All High-Risk Alerts")

    data = load_market_data()

    if data.empty:
        st.info("No biohacking intelligence collected yet. Run `scrapy crawl market`.")
        return

    high_risk = data[data["Threat Level"] == "HIGH"].reset_index(drop=True)

    if high_risk.empty:
        st.success("No high-risk biohacking activity detected.")
        return

    st.markdown(f"**{len(high_risk)} high-risk alert(s) detected.**")
    st.markdown("---")

    search_query = st.text_input("🔎 Filter alerts by keyword (title, vendor, or URL)")

    if search_query:
        mask = (
            high_risk["Title"].str.contains(search_query, case=False, na=False)
            | high_risk["Vendor"].str.contains(search_query, case=False, na=False)
            | high_risk["URL"].str.contains(search_query, case=False, na=False)
        )
        filtered = high_risk[mask]
    else:
        filtered = high_risk

    if filtered.empty:
        st.warning("No alerts match your search.")
        return

    st.markdown(f"*Showing **{len(filtered)}** alert(s).*")

    for _, row in filtered.iterrows():
        st.warning(
            f"""
            **High-Risk Biohacking Activity Detected**

            • **Source:** {row['Vendor']}  
            • **Title:** {row['Title']}  
            • **URL:** {row['URL']}
            """
        )

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
    elif st.session_state.page == "alerts":
        page_alerts()
    else:
        page_dashboard()