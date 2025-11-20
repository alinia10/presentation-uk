import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import math
import numpy as np
from PIL import Image, ImageOps  # Added for image resizing

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Camden Borough Protection Strategy: Short-, Medium-, and Long-Term Planning Framework",
    page_icon="👮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a cleaner, presentation-like look

st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: #0E1117; }
    .stAlert { background-color: #f0f2f6; border: 1px solid #dbe1eb; }
    div[data-testid="stRadio"] > label { font-weight: bold; font-size: 1.1rem; }
    
    /* Add a card-like look to tabs in the cycle section */
    .stTabs {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS & DATA LOADING
# -----------------------------------------------------------------------------
def check_files():
    """
    Checks if required images and data exist. 
    """
    # Looking for .png files based on your images
    required_images = [f"{i}.png" for i in range(1, 8)]
    required_files = required_images + ["data.csv"]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        st.error(f"⚠️ Missing files: {', '.join(missing)}")
        st.warning(f"📂 Current Working Directory: `{os.getcwd()}`")
        st.write("⬇️ Files found in this folder:")
        st.code(os.listdir())
        st.stop()

def load_and_resize_image(image_path, size=(600, 400)):
    """
    Loads an image and crops/resizes it to a fixed size to ensure consistency.
    Uses ImageOps.fit to maintain aspect ratio while filling the size.
    """
    if os.path.exists(image_path):
        img = Image.open(image_path)
        # Image.Resampling.LANCZOS is high-quality downsampling filter
        img = ImageOps.fit(img, size, Image.Resampling.LANCZOS) 
        return img
    return None

# Run the file check first
check_files()

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df_incidents = load_data()

# -----------------------------------------------------------------------------
# 3. TITLE SLIDE
# -----------------------------------------------------------------------------
st.title("🛡️ Camden Borough Protection Strategy: Short-, Medium-, and Long-Term Planning Framework")
st.subheader("Camden has the opportunity to set a strong example in London by addressing a case that not only demands the attention of the government and the Mayor of London, but is also a pressing issue within the borough itself. Police records show that Camden ranks among the top London boroughs for drug dealing. Despite the council’s efforts to deploy more officers and increase police presence on the streets this year, Camden remains at the top of the list. This suggests a lack of strategic planning behind these measures.")
st.subheader("In this meeting, we aim to discuss and develop a comprehensive approach—divided into a one-year, three-year, and five-year plan—not only to tackle this issue in Camden, but also to share our learning with other boroughs.")
st.subheader("My research indicates that one of the key reasons Camden faces this challenge is its proximity to major transport hubs: St Pancras International and King's Cross Station. These stations provide easy access for visitors from across the UK and Europe, allowing individuals to travel to Camden, conduct business, and return home the same day. Please refer to the map and station details for further context.")
st.markdown("---")

# -----------------------------------------------------------------------------
# 4. INTERACTIVE STATION MAP (The Triangle)
# -----------------------------------------------------------------------------
st.header("📍 The Critical Transport Triangle")

# Layout: Map on the left, Details on the right
col_map, col_info = st.columns([1.2, 1])

with col_map:
    st.image("5.png", use_container_width=True, caption="Map of Key Transport Hubs")
    st.caption("👇 Select a station to view passenger statistics and details.")
    
    # Interactive selection
    station_selector = st.radio(
        "Select Location to Inspect:",
        ["St Pancras International", "Kings Cross Station", "Camden Town Station"],
        horizontal=True
    )

with col_info:
    st.markdown(f"### {station_selector}")
    
    if station_selector == "St Pancras International":
        st.image("1.png", use_container_width=True)
        st.metric(label="Yearly Usage", value="35,959,980", delta="High Volume")
        st.info("International trains: It’s the London terminal for the Eurostar, which runs high-speed trains to Paris, Brussels, Amsterdam, and other destinations in Europe.")

    elif station_selector == "Kings Cross Station":
        st.image("2.png", use_container_width=True)
        st.metric(label="Yearly Usage", value="24,483,824", delta="Major Interchange")
        st.info("Major UK rail hub: Trains from King’s Cross go mainly to the north and east of England, including: York, Newcastle, Leeds, Edinburgh (Scotland), and Other destinations along the East Coast Main Line.")

    elif station_selector == "Camden Town Station":
        st.image("3.png", use_container_width=True)
        
        # Growth Chart Data
        growth_data = pd.DataFrame({
            "Year": ["2020", "2021", "2022", "2023"],
            "Passengers (Millions)": [5.51, 9.12, 17.34, 18.81]
        })
        
        # Area Chart for Growth
        fig_growth = px.area(
            growth_data, 
            x="Year", 
            y="Passengers (Millions)", 
            title="📈 Explosive Passenger Growth",
            markers=True,
            color_discrete_sequence=['#1f77b4']  # Standard Blue
        )
        fig_growth.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_growth, use_container_width=True)
        st.info("Major UK rail hub: Trains from King’s Cross go mainly to the north and east of England, including: York, Newcastle, Leeds, Edinburgh (Scotland), and Other destinations along the East Coast Main Line.")
        st.info("")
st.markdown("---")

# -----------------------------------------------------------------------------
# 5. MARKET CONTEXT
# -----------------------------------------------------------------------------
st.header("🛍️ Inverness Street Market")

col_mkt_img, col_mkt_text = st.columns([1, 1])

with col_mkt_img:
    st.image("4.png", use_container_width=True, caption="Inverness Street Market")

with col_mkt_text:
    st.markdown("#### The Commerce-Crime Nexus")
    st.metric("Yearly Visitors", "14,000,000", delta="High Density Area")
    st.write("""
    According to CrystalRoof, for the postcode around Inverness Street (NW1 7HB) the estimated annual drug-crime rate is 139 per 1,000 (very high).    
    Business owners in Inverness Street (market traders, restaurants, cafés) have publicly complained that open drug dealing is “persistent” and part of a “nuisance” problem.
    """)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. EVIDENCE & POLICING CHALLENGES
# -----------------------------------------------------------------------------
st.header("⚖️ The Evidence Challenge")

col_cctv, col_find = st.columns(2)

# Using the resize function to ensure images match perfectly in height/aspect
img_exchange = load_and_resize_image("6.png")
img_drugs = load_and_resize_image("7.png")

with col_cctv:
    st.subheader("1. The Requirement")
    if img_exchange:
        st.image(img_exchange, use_container_width=True, caption="Hand-to-Hand Exchange")
    st.success("""
    **Actionable Evidence:**
    Police require clear footage of a **hand-to-hand exchange** (money for drugs).
    """)

with col_find:
    st.subheader("2. The Problem")
    if img_drugs:
        st.image(img_drugs, use_container_width=True, caption="Drugs Found in Bin")
    st.error("""
    **Insufficient Evidence:**
    Finding drugs in bins or on the ground is **not enough** without linking possession to a suspect.
    """)

st.markdown("---")
# -----------------------------------------------------------------------------
# 7. ECONOMIC SCALE (Imports vs Drugs)
# -----------------------------------------------------------------------------
st.header("💷 Economic Scale: Legal Imports vs. Illicit Market")

# Initialize session state for the reveal button if not present
if 'reveal_drug_market' not in st.session_state:
    st.session_state['reveal_drug_market'] = False

# Base Data (Legal Commodities)
import_data = [
    {"Commodity": "Mineral Fuels", "Value": 8.7, "Type": "Legal"},
    {"Commodity": "Mechanical Appliances", "Value": 6.4, "Type": "Legal"},
    {"Commodity": "Electronic Equipment", "Value": 5.3, "Type": "Legal"},
    {"Commodity": "Precious Metals", "Value": 4.2, "Type": "Legal"},
    {"Commodity": "Motor Vehicles", "Value": 4.1, "Type": "Legal"},
    {"Commodity": "Pharmaceutical Products", "Value": 2.0, "Type": "Legal"},
    {"Commodity": "Other Products", "Value": 1.6, "Type": "Legal"},
    {"Commodity": "Plastics", "Value": 1.5, "Type": "Legal"},
    {"Commodity": "Measuring Devices", "Value": 1.3, "Type": "Legal"},
    {"Commodity": "Knitwear", "Value": 1.3, "Type": "Legal"}
]

df_imports = pd.DataFrame(import_data)

# Calculate Custom Sort Order
# 1. Sort Legal Items by Value Ascending (so largest is at Top of chart, smallest at Bottom)
legal_order = df_imports.sort_values("Value", ascending=True)["Commodity"].tolist()

# 2. Handle Reveal Logic
if st.session_state['reveal_drug_market']:
    # Add Illicit Drugs to DataFrame
    new_row = pd.DataFrame([{"Commodity": "Illicit Drugs Market", "Value": 9.4, "Type": "Illegal"}])
    df_imports = pd.concat([df_imports, new_row], ignore_index=True)
    
    # Update Order: Prepend Drugs to the list so it appears at the visually BOTTOM (Index 0 in Plotly)
    final_order = ["Illicit Drugs Market"] + legal_order
else:
    final_order = legal_order

colors = {"Legal": "#1f77b4", "Illegal": "#DC3912"}

fig_imports = px.bar(
    df_imports,
    x="Value", 
    y="Commodity", 
    orientation='h',
    color="Type", 
    color_discrete_map=colors, 
    text="Value",
    title="Top UK Commodities vs. Illicit Drugs Market (£ Billions)",
    # Force specific category order to keep Drugs at the bottom
    category_orders={"Commodity": final_order} 
)

fig_imports.update_layout(
    showlegend=False, 
    height=500
)
fig_imports.update_traces(texttemplate='£%{text}B', textposition='outside')

# 1. Render the Chart First
st.plotly_chart(fig_imports, use_container_width=True)

# 2. Render the Button Below the Chart
col_btn, col_space = st.columns([1, 4])
with col_btn:
    if not st.session_state['reveal_drug_market']:
        if st.button("⚠️ Reveal Illicit Market Scale"):
            st.session_state['reveal_drug_market'] = True
            st.rerun()
    else:
        if st.button("Reset Chart"):
            st.session_state['reveal_drug_market'] = False
            st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 8. ADVANCED INCIDENT ANALYSIS
# -----------------------------------------------------------------------------
st.header("📊 Incidents by Location and Type (Top 20 Locations)")
if not df_incidents.empty:
    # 1. Calculate Total Incidents per Location to sort the chart
    location_totals = df_incidents.groupby("Location")["Count"].sum().sort_values(ascending=False)
    
    # 2. Get Top 20 Locations (or all if less than 20)
    top_locations = location_totals.tail(20).index.tolist()
    
    # 3. Filter the main dataframe to only include these top locations
    df_filtered = df_incidents[df_incidents["Location"].isin(top_locations)]
    
    # 4. Define Custom Color Map (Drugs = RED as requested)
    custom_colors = {
        "Drug Users/Dealers": "#DC3912",  # Red
        "Youths": "#FF9900",              # Orange
        "Noise": "#3366CC",               # Blue
        "Rough Sleeper": "#109618",       # Green
        "Smoking": "#990099",             # Purple
        "Loitering": "#0099C6",           # Teal
        "Public Indecency": "#DD4477",    # Pink
        "Intruder": "#AAAA11",            # Olive
        "Drinking/Drunk": "#66AA00"       # Light Green
    }

    # 5. Create the Stacked Horizontal Bar Chart
    fig_advanced = px.bar(
        df_filtered,
        x="Count",
        y="Location",
        color="Category",
        orientation='h',
        title=f"Total Incidents in Dataset: {df_incidents['Count'].sum()}",
        color_discrete_map=custom_colors,
        category_orders={"Location": top_locations} # Ensures chart is sorted by total volume
    )

    # 6. Custom Layout to match the "clean" reference image look
    fig_advanced.update_layout(
        height=700,
        legend_title_text="Incident Type",
        xaxis_title="Number of Incidents",
        yaxis_title="Location",
        legend=dict(yanchor="top", y=1, xanchor="left", x=1.02) # Move legend to side
    )
    
    st.plotly_chart(fig_advanced, use_container_width=True)
else:
    st.warning("No data available for analysis.")
st.write("Escalating drug-related costs for the council and rising crime rates have become a serious concern. Reports show a significant increase in resident complaints about various forms of anti-social behaviour across Camden.")
st.markdown("---")

# -----------------------------------------------------------------------------
# 9. THE VICIOUS CYCLE (INTERACTIVE & ENHANCED)
# -----------------------------------------------------------------------------
st.header("🔄 The Vicious Cycle: Supply, Demand, & Community Impact")
st.write("Explore the drug market cycle by selecting a stage below.")

# --- Setup Cycle Data (Circular Layout) ---
# We will position 5 nodes in a perfect circle
# Angle calculation: 360 / 5 = 72 degrees. Start at 90 (top).
center_x, center_y = 0, 0
radius = 1.2
num_points = 5
angles = np.linspace(90, 90 - 360, num_points, endpoint=False) # Start top, go clockwise
angles_rad = np.radians(angles)

x_coords = radius * np.cos(angles_rad)
y_coords = radius * np.sin(angles_rad)

# Labels matching the image exactly
cycle_nodes = [
    {"id": 1, "label": "1 Drug's provider", "desc": "1Drug's provider", "x": x_coords[0], "y": y_coords[0]},
    {"id": 2, "label": "2 Drug's distributor", "desc": "2Drug'sdistribut", "x": x_coords[1], "y": y_coords[1]}, # Keeping "distribut" style or fixing spacing for readability
    {"id": 3, "label": "3 Market", "desc": "3Market", "x": x_coords[2], "y": y_coords[2]},
    {"id": 4, "label": "4 Drug's buyers", "desc": "4 Drug'sbuyers", "x": x_coords[3], "y": y_coords[3]},
    {"id": 5, "label": "5 improve Drug's Market", "desc": "5 improve Drug's Market", "x": x_coords[4], "y": y_coords[4]}
]

# --- User Control ---
step_options = [n["label"] for n in cycle_nodes] + ["See Full Cycle"]
selected_step = st.radio("Select Cycle Stage:", step_options, horizontal=True, index=len(step_options)-1)

# --- Layout: Diagram (Left) + Details & Perspectives (Right) ---
col_cycle_viz, col_cycle_text = st.columns([1.3, 1.5])

with col_cycle_viz:
    # Build the Plotly Figure
    fig_cycle = go.Figure()

    # 1. Add Curved Arrows
    for i in range(len(cycle_nodes)):
        curr = cycle_nodes[i]
        nxt = cycle_nodes[(i + 1) % len(cycle_nodes)]
        
        fig_cycle.add_annotation(
            x=nxt["x"], y=nxt["y"],
            ax=curr["x"], ay=curr["y"],
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor="#888",
            standoff=15, startstandoff=15 
        )

    # 2. Add Central "COST" Node (Diamond) - Matching Yellow Box Text
    fig_cycle.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        marker=dict(symbol="diamond", size=85, color="#FFFF00", line=dict(width=1, color="black")),
        text=["Cost for<br>council &<br>Increase<br>crime"],
        textfont=dict(size=10, color="black"),
        hoverinfo="skip"
    ))

    # 3. Add Outer Nodes
    node_colors = []
    node_sizes = []
    node_lines = []
    
    for node in cycle_nodes:
        is_active = (selected_step == node["label"]) or (selected_step == "See Full Cycle")
        node_colors.append("#006699" if is_active else "#E0E0E0")
        node_sizes.append(65 if is_active else 45)
        node_lines.append(dict(width=3 if is_active else 1, color="black" if is_active else "gray"))

    fig_cycle.add_trace(go.Scatter(
        x=[n["x"] for n in cycle_nodes],
        y=[n["y"] for n in cycle_nodes],
        mode="markers+text",
        text=[f"<b>{n['desc']}</b>" for n in cycle_nodes],
        textposition="top center",
        textfont=dict(size=11, color="#333"),
        marker=dict(size=node_sizes, color=node_colors, line=dict(width=[l['width'] for l in node_lines], color=[l['color'] for l in node_lines])),
        hoverinfo="text"
    ))

    fig_cycle.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.8, 1.8]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.8, 1.8]),
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig_cycle, use_container_width=True)

# --- Right Column: Details Panel + Perspectives ---
with col_cycle_text:
    st.markdown(f"### 📌 {selected_step if selected_step != 'See Full Cycle' else 'Cycle Overview'}")
    
    # --- Dynamic Text Content ---
    if selected_step == "1 Drug's provider":
        st.info("**1Drug's provider:** The source of illicit substances.")
    
    elif selected_step == "2 Drug's distributor":
        st.info("**2Drug'sdistribut:** Key distributors in the network.")
    
    elif selected_step == "3 Market":
        st.info("**3Market:** The central hub for exchange.")
    
    elif selected_step == "4 Drug's buyers":
        st.info("**4 Drug'sbuyers:** The demand side of the market.")
        # RED BOX TEXT ADDED HERE
        st.error("""
        Individuals seeking drugs often congregate around this market, settling as rough sleepers, beggars, or street vendors, contributing to challenges for the Borough
        """)
    
    elif selected_step == "5 improve Drug's Market":
        st.info("**5 improve Drug's Market:** Expansion and reinforcement of the trade.")
    
    else: # Full Cycle
        st.warning("The cycle connects Providers, Distributors, the Market, and Buyers, leading to increased costs for the council and crime.")

    # --- INTEGRATED PERSPECTIVES SECTION (TEXT MATCHING IMAGE EXACTLY) ---
    st.markdown("---")
    
    # 1. Main Intro Sentence
    # st.write("**The best market is a bustling open-air hub, easily accessible by public transport, where beggars and rough sleepers mingle, and teenagers assist the dealers.**")

    # Interactive Tabs
    p_tab1, p_tab2, p_tab3 = st.tabs(["1. Neutral & Descriptive", "2. Gritty & Urban", "3. Narrative"])

    with p_tab1:
        st.markdown("""
        1. Neutral and Descriptive:The best market is a lively open-air space, easily reached by public transport, where beggars and rough sleepers linger, and teenagers assist the dealers.
        """)

    with p_tab2:
        st.markdown("""
        2. Gritty and Urban:the best market pulses with life—open to the streets, packed with people, accessible by bus or train, where beggars drift, rough sleepers rest, and teenagers hustle alongside the dealers."
        """)

    with p_tab3:
        st.markdown("""
        3. The finest market breathes chaos and charm—open to the sky, thrumming with footsteps, where the city’s forgotten mingle with the bold, and youth shadow the traders in a dance of survival."
        """)