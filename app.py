import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import math
import numpy as np
from PIL import Image, ImageOps  # Added for image resizing
import graphviz

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Camden Strategy Framework",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed", # Collapsed gives more room for the presentation
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Camden Borough Protection Strategy Presentation"
    }
)

# -----------------------------------------------------------------------------
# 2. GLOBAL STYLING & THEME
# -----------------------------------------------------------------------------

# Define a color palette for use in Python charts later
THEME = {
    "primary": "#0e1b3c",    # Camden Navy
    "accent": "#d92828",     # Alert Red
    "background": "#ffffff",
    "text": "#0E1117",
    "secondary_text": "#5d6d7e"
}

st.markdown(f"""
    <style>
    /* Import a clean, professional font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
    }}

    /* Remove top padding to maximize screen real estate for presentation */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {THEME['primary']};
        font-weight: 700;
    }}

    /* Professional Alert/Info Boxes */
    .stAlert {{
        background-color: #f8f9fa;
        border-left: 5px solid {THEME['primary']};
        border-radius: 4px;
    }}

    /* Remove Streamlit Branding for clean presentation mode */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Custom Tab styling to look like folders */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        color: {THEME['primary']};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {THEME['primary']};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS & DATA LOADING
# -----------------------------------------------------------------------------

def check_system_integrity():
    """
    Verifies that all critical assets (Data and Images) are present.
    Stops execution with a polished error message if critical data is missing.
    """
    # Required assets
    required_images = [f"{i}.png" for i in range(1, 9)] # Added 8.png for logo
    required_data = ["data.csv"]
    
    # Check Data (Critical)
    missing_data = [f for f in required_data if not os.path.exists(f)]
    if missing_data:
        st.error(f"⛔ **CRITICAL ERROR: System Data Missing**\n\nThe following core files could not be found: `{', '.join(missing_data)}`")
        st.stop()

    # Check Images (Non-critical, but warn)
    missing_images = [f for f in required_images if not os.path.exists(f)]
    if missing_images:
        st.warning(f"⚠️ **Asset Warning:** Some visual assets are missing: `{', '.join(missing_images)}`. Placeholders will be used.")

# Run integrity check immediately
check_system_integrity()

@st.cache_resource
def load_and_resize_image(image_path, size=(600, 400)):
    """
    Loads, resizes, and caches an image.
    Returns None if image is not found, preventing crashes.
    """
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            # High-quality resampling for professional look
            img = ImageOps.fit(img, size, Image.Resampling.LANCZOS) 
            return img
        except Exception as e:
            st.error(f"Error loading image {image_path}: {e}")
            return None
    return None

@st.cache_data
def load_data():
    """
    Loads the dataset with error handling.
    """
    try:
        df = pd.read_csv("data.csv")
        # Optional: Convert standard date columns if they exist to datetime objects
        # if 'date' in df.columns:
        #     df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"⛔ **Data Load Error:** Could not read `data.csv`. \n\nError details: {e}")
        st.stop()

# Load data into session
df_incidents = load_data()
# -----------------------------------------------------------------------------
# 3. TITLE SLIDE
# -----------------------------------------------------------------------------
# st.title("🛡️ Camden Borough Protection Strategy: Short-, Medium-, and Long-Term Planning Framework")
# st.subheader("Camden has the opportunity to set a strong example in London by addressing a case that not only demands the attention of the government and the Mayor of London, but is also a pressing issue within the borough itself. Police records show that Camden ranks among the top London boroughs for drug dealing. Despite the council’s efforts to deploy more officers and increase police presence on the streets this year, Camden remains at the top of the list. This suggests a lack of strategic planning behind these measures.")
# st.subheader("In this meeting, we aim to discuss and develop a comprehensive approach—divided into a one-year, three-year, and five-year plan—not only to tackle this issue in Camden, but also to share our learning with other boroughs.")
# st.subheader("My research indicates that one of the key reasons Camden faces this challenge is its proximity to major transport hubs: St Pancras International and King's Cross Station. These stations provide easy access for visitors from across the UK and Europe, allowing individuals to travel to Camden, conduct business, and return home the same day. Please refer to the map and station details for further context.")
# st.markdown("---")
# -----------------------------------------------------------------------------
# 3. TITLE SLIDE - OPTIMIZED LAYOUT
# -----------------------------------------------------------------------------

# 1. Custom CSS for Bolder Text and Title Box
st.markdown("""
    <style>
    /* --- TITLE BOX STYLING --- */
    .header-box {
        background-color: #0e1b3c; /* Camden Navy */
        padding: 30px;
        border-radius: 10px;
        border-left: 12px solid #d92828; /* Red Accent */
        color: white;
        text-align: left;
        box-shadow: 0px 6px 10px rgba(0,0,0,0.2);
        /* Ensure box fills height to match logo visual weight */
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Large Title Font */
    .header-title {
        font-size: 42px !important;
        font-weight: 800;
        font-family: 'Helvetica Neue', 'Arial', sans-serif;
        margin-bottom: 10px;
        line-height: 1.1;
    }
    
    /* Subtitle Font */
    .header-subtitle {
        font-size: 22px !important;
        font-weight: 400;
        color: #e0e0e0;
        margin: 0;
    }

    /* --- BODY TEXT STYLING (Make it Bolder) --- */
    
    /* Make standard paragraphs darker and heavier */
    .stMarkdown p {
        font-size: 18px !important;
        font-weight: 500 !important; /* 500 is semi-bold */
        color: #000000 !important;   /* Pure black for contrast */
        line-height: 1.6;
    }
    
    /* Make bullet points darker */
    .stMarkdown li {
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #000000 !important;
    }
    
    /* Make the Executive Summary headers pop */
    h3 {
        font-weight: 800 !important;
        color: #0e1b3c !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Create the Layout [1, 3]
# This gives the Logo 1 part width, and the Title 3 parts width.
# The logo will naturally look smaller and "lower" in visual weight.
col_logo, col_title = st.columns([1, 3], gap="medium", vertical_alignment="center")

with col_logo:
    # The logo is now restricted to the smaller column width
    st.image("8.png", use_container_width=True)

with col_title:
    st.markdown("""
        <div class="header-box">
            <div class="header-title">Camden Borough Protection Strategy</div>
            <div class="header-subtitle">Short-, Medium-, and Long-Term Strategic Planning Framework</div>
        </div>
    """, unsafe_allow_html=True)

# 3. Executive Summary Content
st.markdown("---")
st.subheader("📋 Executive Summary")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("**The Strategic Challenge**")
    st.write(
        """
        Camden faces a critical opportunity to lead London in public safety. 
        Current data indicates that despite increased police presence, 
        **Camden remains a top-ranking borough for drug dealing offenses.** This persistence suggests that tactical deployment alone is insufficient 
        and a robust strategic overhaul is required.
        """
    )
    # Using warning/info box for emphasis
    st.info(
        "**Meeting Objective:** Develop a comprehensive **1-3-5 Year Plan** "
        "to tackle local issues and establish a blueprint for cross-borough learning."
    )

with col2:
    st.markdown("**Key Driver: Transport Infrastructure**")
    st.write(
        """
        Our analysis identifies a primary structural catalyst for this issue:
        **Proximity to Major Transport Hubs.**
        """
    )
    st.markdown("""
    * 🚄 **St Pancras International**
    * 🚆 **King's Cross Station**
    """)
    st.caption(
        "These hubs facilitate rapid 'in-and-out' access for offenders from across "
        "the UK and Europe."
    )

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
    {"Commodity": "Pharmaceuticals", "Value": 2.0, "Type": "Legal"}, # Shortened name for better vertical fit
    {"Commodity": "Other Products", "Value": 1.6, "Type": "Legal"},
    {"Commodity": "Plastics", "Value": 1.5, "Type": "Legal"},
    {"Commodity": "Measuring Devices", "Value": 1.3, "Type": "Legal"},
    {"Commodity": "Knitwear", "Value": 1.3, "Type": "Legal"}
]

df_imports = pd.DataFrame(import_data)

# 1. Handle Reveal Logic
if st.session_state['reveal_drug_market']:
    # Add Illicit Drugs to DataFrame
    new_row = pd.DataFrame([{"Commodity": "Illicit Drugs", "Value": 9.4, "Type": "Illegal"}])
    df_imports = pd.concat([df_imports, new_row], ignore_index=True)

# 2. Sort by Value Descending (Highest on Left)
df_imports = df_imports.sort_values("Value", ascending=False)

# Define Colors
colors = {"Legal": "#1f77b4", "Illegal": "#DC3912"}

# 3. Build Chart (Vertical)
# Note: We swapped x and y. x is now Commodity, y is Value.
fig_imports = px.bar(
    df_imports,
    x="Commodity", 
    y="Value", 
    color="Type", 
    color_discrete_map=colors, 
    text="Value",
    title="<b>Top UK Commodities vs. Illicit Drugs Market (£ Billions)</b>",
)

# 4. Apply Styling (Thicker, Bolder, Larger)
fig_imports.update_layout(
    showlegend=False, 
    height=600, # Increased height for vertical breathing room
    bargap=0.15, # <--- This makes columns THICKER by reducing the gap between them
    
    # Global Font Settings
    font=dict(
        family="Arial, sans-serif",
        size=14,  # Base font size increased
        color="black"
    ),
    
    # X-Axis Styling (The Categories)
    xaxis=dict(
        title=None,
        tickfont=dict(
            size=14, 
            family="Arial Black" # Bold font for labels
        ),
        tickangle=-45 # Angle labels to prevent overlapping
    ),
    
    # Y-Axis Styling (The Numbers)
    yaxis=dict(
        title=dict(text="<b>Value (£ Billions)</b>", font=dict(size=16)),
        tickfont=dict(size=14),
        showgrid=True,
        gridcolor='lightgray'
    )
)

# 5. Update Bar Text (The numbers on top of bars)
fig_imports.update_traces(
    texttemplate='<b>£%{text}B</b>', # <b> tag makes it bold
    textposition='outside',
    textfont=dict(
        size=18, # Significantly larger
        family="Arial Black"
    ),
    cliponaxis=False # Ensures top labels don't get cut off
)

# Render Chart
st.plotly_chart(fig_imports, use_container_width=True)

# Render Button
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
    # 1. Calculate Totals to find the ACTUAL Top 20
    # Sort Ascending so .tail(20) grabs the largest values
    location_totals = df_incidents.groupby("Location")["Count"].sum().sort_values(ascending=True)
    
    # 2. Get Top 20 Locations
    top_locations = location_totals.tail(20).index.tolist()
    
    # 3. Filter main dataframe
    df_filtered = df_incidents[df_incidents["Location"].isin(top_locations)]
    
    # 4. Custom Color Map (Kept as requested)
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

    # 5. Create Chart
    fig_advanced = px.bar(
        df_filtered,
        x="Count",
        y="Location",
        color="Category",
        orientation='h',
        text="Count", # This adds the number inside the bar
        title=f"<b>Total Incidents: {df_incidents['Count'].sum()}</b>", # Bold Title
        color_discrete_map=custom_colors,
        # Ensure the largest bars are at the top visual position
        category_orders={"Location": top_locations} 
    )

    # 6. Advanced Styling
    fig_advanced.update_layout(
        height=800, # Taller to accommodate thicker bars
        bargap=0.15, # <--- This makes the columns/bars THICKER (closer to 0 is thicker)
        barmode='stack', # Ensures bars collapse when items are removed via legend
        
        # Legend Styling
        legend_title_text="<b>Incident Type</b>",
        legend=dict(
            yanchor="top", 
            y=1, 
            xanchor="left", 
            x=1.01,
            font=dict(size=14)
        ),
        
        # Global Font
        font=dict(family="Arial", size=14, color="black"),
        
        # X-Axis (Numbers)
        xaxis=dict(
            title="<b>Number of Incidents</b>",
            tickfont=dict(size=14, family="Arial Black"),
            showgrid=True, 
            gridcolor='lightgray'
        ),
        
        # Y-Axis (Locations)
        yaxis=dict(
            title=None, # Remove "Location" label as it's obvious
            tickfont=dict(
                size=15, 
                family="Arial Black" # Very bold labels for readability
            )
        )
    )
    
    # 7. Style the numbers inside the bars
    fig_advanced.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial Black",
            size=14,
            color="white" # White text on colored bars for contrast
        )
    )
    
    st.plotly_chart(fig_advanced, use_container_width=True)
else:
    st.warning("No data available for analysis.")

st.write("Escalating drug-related costs for the council and rising crime rates have become a serious concern. Reports show a significant increase in resident complaints about various forms of anti-social behaviour across Camden.")
st.markdown("---")

# -----------------------------------------------------------------------------
# 9. THE VICIOUS CYCLE (INTERACTIVE & ENHANCED)
# -----------------------------------------------------------------------------


# st.header("🔄 The Cycle of Supply & Local Impact")

# # 1. Layout: Equal columns (1:1) and Vertically Centered
# col_diagram, col_text = st.columns([1, 1], gap="large", vertical_alignment="center")

# with col_diagram:
#     # Initialize Graphviz
#     dot = graphviz.Digraph(comment='Drug Market Cycle')
    
#     # --- COMPACT GRAPH STYLING ---
#     # rankdir='LR' (Left-to-Right) often fits presentations better than Top-Bottom
#     # newrank='true' helps align nodes better
#     dot.attr(rankdir='TB', newrank='true') 
#     dot.attr(splines='curved') # Curved lines look cleaner and take less space
#     dot.attr(nodesep='0.3')    # Reduce space between nodes width-wise
#     dot.attr(ranksep='0.4')    # Reduce space between levels height-wise
#     dot.attr(bgcolor='transparent')
    
#     # Node Style (Smaller and sharper)
#     dot.attr('node', shape='box', style='filled, rounded', 
#              fillcolor='#0e1b3c', # Camden Navy
#              fontcolor='white', 
#              fontname='Arial', 
#              fontsize='10',       # Smaller font
#              margin='0.1,0.1',    # Tighter margins inside boxes
#              height='0.4')

#     # --- NODES ---
#     # Using shorter labels to keep boxes small
#     dot.node('A', '1. Providers')
#     dot.node('B', '2. Distributors')
#     dot.node('C', '3. The Market\n(Hub)')
#     dot.node('D', '4. Buyers')
#     dot.node('E', '5. Reinforcement')

#     # Impact Node (Red)
#     dot.attr('node', fillcolor='#d92828', fontcolor='white')
#     dot.node('Impact', 'SOCIAL IMPACT:\nRough Sleepers,\nCongregation')

#     # Cost Node (Yellow)
#     dot.attr('node', fillcolor='#ffcc00', fontcolor='black')
#     dot.node('Cost', '$$ Council Costs\n& Crime Rates')

#     # --- EDGES ---
#     dot.attr('edge', color='#555555', arrowsize='0.6', penwidth='1.2')
    
#     # Main Cycle
#     dot.edge('A', 'B')
#     dot.edge('B', 'C')
#     dot.edge('C', 'D')
#     dot.edge('D', 'E')
#     dot.edge('E', 'A')

#     # Consequences (Dotted)
#     dot.attr('edge', style='dashed', color='#d92828')
#     dot.edge('D', 'Impact')
#     dot.edge('E', 'Cost')

#     # Render with a specific height/width constraint via Streamlit
#     st.graphviz_chart(dot, use_container_width=True)

# with col_text:
#     # --- TEXT CONTENT ---
#     # This box is designed to visually balance the graph size
#     st.markdown("""
#     <div style="
#         background-color: #f8f9fa; 
#         padding: 25px; 
#         border-radius: 8px; 
#         border-left: 8px solid #0e1b3c;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#     ">
#         <h3 style="color: #0e1b3c; margin-top: 0; font-size: 20px;">Operational Context</h3>
        
#         <p style="font-size: 16px; line-height: 1.5;">
#             <b>1. The "Perfect" Storm:</b><br>
#             The diagram illustrates a self-sustaining loop. The location serves as a logistics hub (Kings Cross) rather than just a street corner.
#         </p>
        
#         <p style="font-size: 16px; line-height: 1.5;">
#             <b>2. The Human Cost (Red Box):</b><br>
#             Buyers don't just leave; they congregate. This creates a permanent settlement of rough sleepers and beggars, directly impacting borough resources.
#         </p>

#         <div style="
#             margin-top: 20px; 
#             padding: 10px; 
#             background-color: #ffeded; 
#             border-radius: 5px; 
#             color: #d92828; 
#             font-weight: bold; 
#             font-size: 14px;
#             text-align: center;
#         ">
#             ⚠️ Strategic Priority: Break the link between <br>Step 3 (Market) and Step 4 (Buyers).
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
# import streamlit as st
# import graphviz

st.header("🔄 The Cycle of Supply & Local Impact")

# Initialize Graphviz
dot = graphviz.Digraph(comment='Drug Market Cycle')

# --- GRAPH STYLING ---
dot.attr(rankdir='LR', newrank='true') 
dot.attr(splines='curved') 
dot.attr(nodesep='0.4')    
dot.attr(ranksep='0.5')    
dot.attr(bgcolor='transparent')

# Node Style
dot.attr('node', shape='box', style='filled, rounded', 
         fillcolor='#0e1b3c', fontcolor='white', fontname='Arial', 
         fontsize='10', margin='0.1,0.1', height='0.4')

# --- NODES ---
dot.node('A', '1. Providers')
dot.node('B', '2. Distributors')
dot.node('C', '3. The Market\n(Hub)')
dot.node('D', '4. Buyers')
dot.node('E', '5. Reinforcement')

# Impact/Cost Nodes
dot.attr('node', fillcolor='#d92828', fontcolor='white')
dot.node('Impact', 'SOCIAL IMPACT:\nRough Sleepers')

dot.attr('node', fillcolor='#ffcc00', fontcolor='black')
dot.node('Cost', '$$ Costs')

# --- EDGES ---
dot.attr('edge', color='#555555', arrowsize='0.6', penwidth='1.2')

# 1. THE BOTTOM PATH (1 -> 2 -> 3 -> 4 -> 5)
# Force A -> B to go "down" by leaving A from South ('s') and entering B from West ('w')
dot.edge('A', 'B', tailport='s', headport='w')

dot.edge('B', 'C')
dot.edge('C', 'D')

# Force D -> E to go "up" by entering E from South ('s')
dot.edge('D', 'E', tailport='e', headport='s')

# 2. THE TOP ARCH (5 -> 1)
# This creates the loop over the top using North ('n') ports
dot.attr('edge', color='#555555', penwidth='1.5')
dot.edge('E', 'A', tailport='n', headport='n', label=' Cycle Returns')

# 3. SIDE CONSEQUENCES
dot.attr('edge', style='dashed', color='#d92828', penwidth='1.0')
dot.edge('D', 'Impact', dir='forward') # From Buyers
dot.edge('E', 'Cost', dir='forward')   # From Reinforcement

st.graphviz_chart(dot, use_container_width=True)

