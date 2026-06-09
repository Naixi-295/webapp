# ============================================================
# STRUCTURASAFE AI
# Integrated ICT Platform for Structural Safety
# Final Year Project
#
# Developer: Muhammad Aoun Ali
# Technologies: Streamlit, Plotly, Pandas, NumPy, OpenCV, Scikit-Learn
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import cv2
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime

# ML Imports
from sklearn.ensemble import RandomForestRegressor
# PDF Generation Imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StructuraSafe AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.metric-card {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
.title {
    color:#003366;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# MATERIAL DATABASE
# ============================================================

MATERIALS = {
    "Concrete": {
        "Density": 2400,
        "Young_Modulus": 30e9,
        "Yield_Strength": 40e6,
        "Compressive_Strength": 40e6,
        "Tensile_Strength": 4e6,
        "Safety_Limit": 2.5
    },
    "Reinforced Concrete": {
        "Density": 2500,
        "Young_Modulus": 35e9,
        "Yield_Strength": 420e6,
        "Compressive_Strength": 45e6,
        "Tensile_Strength": 5e6,
        "Safety_Limit": 3.0
    },
    "Structural Steel": {
        "Density": 7850,
        "Young_Modulus": 200e9,
        "Yield_Strength": 250e6,
        "Compressive_Strength": 250e6,
        "Tensile_Strength": 400e6,
        "Safety_Limit": 2.0
    },
    "Aluminum Alloy": {
        "Density": 2700,
        "Young_Modulus": 69e9,
        "Yield_Strength": 275e6,
        "Compressive_Strength": 275e6,
        "Tensile_Strength": 310e6,
        "Safety_Limit": 2.2
    },
    "Timber": {
        "Density": 600,
        "Young_Modulus": 12e9,
        "Yield_Strength": 40e6,
        "Compressive_Strength": 40e6,
        "Tensile_Strength": 80e6,
        "Safety_Limit": 1.8
    }
}

# ============================================================
# PDF REPORT GENERATOR FUNCTION
# ============================================================

def create_pdf_report(dataframe, title_text="StructuraSafe AI Report"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#003366'),
        spaceAfter=20
    )
    text_style = styles['Normal']
    
    story.append(Paragraph(title_text, title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", text_style))
    story.append(Spacer(1, 15))
    
    data = [dataframe.columns.tolist()] + dataframe.values.tolist()
    t = Table(data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f7fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<h1 style='text-align:center;color:#003366;'>🏗️ StructuraSafe AI</h1>
<h4 style='text-align:center;color:gray;'>Integrated ICT Platform for Structural Safety Assessment and Infrastructure Monitoring</h4>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2784/2784487.png",
    width=120
)
st.sidebar.title("Navigation")

module = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Dashboard",
        "🌉 Bridge Health Monitoring",
        "📈 Beam Deflection Visualizer",
        "🔍 Crack Detection",
        "🏢 Earthquake Simulator",
        "🚛 Load Capacity Predictor",
        "📊 Material Database"
    ]
)

# ============================================================
# MODULE 1: DASHBOARD
# ============================================================

if module == "🏠 Dashboard":
    st.subheader("Project Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Health Index", "92%", "+2%")
    c2.metric("Safety Factor", "3.1", "+0.2")
    c3.metric("Detected Cracks", "15", "-3")
    c4.metric("Remaining Life", "27 Years", "+1")

    st.markdown("---")
    st.subheader("Infrastructure Health Trend")
    time = np.arange(0, 100)
    health = 95 - np.random.normal(0.05, 0.2, 100).cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=health, mode='lines', name='Health Index', line=dict(color='#003366', width=3)))
    fig.update_layout(template="plotly_white", height=400, xaxis_title="Timeline (Days)", yaxis_title="Health Index (%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Project Modules")
    col1, col2 = st.columns(2)
    with col1:
        st.success("✔ Smart Bridge Monitoring\n\n✔ Beam Deflection Analysis\n\n✔ Crack Detection")
    with col2:
        st.info("✔ Earthquake Simulator\n\n✔ Load Predictor\n\n✔ Material Database")

# ============================================================
# MODULE 2: BRIDGE HEALTH MONITORING
# ============================================================

elif module == "🌉 Bridge Health Monitoring":
    st.header("🌉 Smart Bridge Health Monitoring System")
    col1, col2 = st.columns([1, 2])

    with col1:
        material = st.selectbox("Material", list(MATERIALS.keys()))
        applied_load = st.slider("Applied Load (kN)", 10, 5000, 500)
        span_length = st.slider("Span Length (m)", 5, 200, 30)
        temperature = st.slider("Temperature (°C)", -10, 60, 25)
        vehicle_load = st.slider("Vehicle Load (tons)", 1, 100, 20)
        safety_factor_input = st.slider("Safety Factor", 1.0, 5.0, 2.5)

    material_data = MATERIALS[material]
    E = material_data["Young_Modulus"]
    yield_strength = material_data["Yield_Strength"]

    # Engineering Calculations
    stress = (applied_load * 1000) / (span_length * 0.5)
    strain = stress / E
    deflection = (applied_load * 1000 * (span_length ** 3)) / (48 * E * 0.005)
    vibration_index = (vehicle_load * span_length) / 100
    health_index = max(0, min(100, 100 - (stress / 1e6) * 0.05 - vibration_index - abs(temperature - 25) * 0.2))

    with col2:
        st.subheader("Bridge Status Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Health Index", f"{health_index:.1f}%")
        c2.metric("Stress", f"{stress/1e6:.2f} MPa")
        c3.metric("Strain", f"{strain:.2e}")
        c4.metric("Deflection", f"{deflection:.4f} m")
        
        st.markdown("---")
        
        time = np.arange(100)
        vibration_data = np.sin(time / 8) + np.random.normal(0, 0.1, 100)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=time, y=vibration_data, name="Vibration", line=dict(color='orange')))
        fig1.update_layout(title="Real-Time Vibration Sensor Track", template="plotly_white", height=250)
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    st.subheader("Structural Health Gauge Evaluation")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_index,
        title={"text": "Current Structural Safety %"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "green" if health_index > 70 else "orange" if health_index > 40 else "red"}
        }
    ))
    gauge.update_layout(height=300)
    st.plotly_chart(gauge, use_container_width=True)

# ============================================================
# MODULE 3: BEAM DEFLECTION VISUALIZER
# ============================================================

elif module == "📈 Beam Deflection Visualizer":
    st.header("📈 Live Beam Deflection Visualizer")
    col1, col2 = st.columns([1, 2])

    with col1:
        load = st.number_input("Load (kN)", 1, 1000000, 100)
        beam_length = st.number_input("Beam Length (m)", 1, 5000, 10)
        I = st.number_input("Moment of Inertia (m⁴)", 0.0001, 1000.0, 0.005, format="%.4f")
        material = st.selectbox("Material", list(MATERIALS.keys()), key="beam_material")
        support = st.selectbox("Support Condition", ["Simply Supported", "Cantilever"])

    E = MATERIALS[material]["Young_Modulus"]
    yield_strength = MATERIALS[material]["Yield_Strength"]

    if support == "Simply Supported":
        delta = (load * 1000 * beam_length**3) / (48 * E * I)
    else:
        delta = (load * 1000 * beam_length**3) / (3 * E * I)

    bending_moment = (load * beam_length) / 4
    y = 0.15
    stress = (bending_moment * y) / I
    safety_factor = yield_strength / stress if stress > 0 else 999

    with col2:
        k1, k2, k3 = st.columns(3)
        k1.metric("Maximum Deflection", f"{delta:.6f} m")
        k2.metric("Bending Stress", f"{stress/1e6:.2f} MPa")
        k3.metric("Safety Factor", f"{safety_factor:.2f}")

        if safety_factor > 2:
            st.success("Structural Evaluation: SAFE")
        else:
            st.error("Structural Evaluation: UNSAFE / CRITICAL OVERLOAD")

        x = np.linspace(0, beam_length, 100)
        curve = delta * np.sin(np.pi * x / beam_length) if support == "Simply Supported" else delta * (1 - np.cos(np.pi * x / (2 * beam_length)))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=-curve, mode='lines', name='Deflected Shape', line=dict(width=4, color='red')))
        fig.update_layout(title="Elastic Deflection Curve Profile", xaxis_title="Length (m)", yaxis_title="Deflection (m)", template="plotly_white", height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    results_df = pd.DataFrame({
        "Parameter": ["Load (kN)", "Length (m)", "Max Deflection (m)", "Bending Stress (Pa)", "Safety Factor"],
        "Value": [load, beam_length, delta, stress, safety_factor]
    })
    
    pdf_data = create_pdf_report(results_df, "Beam Deflection Calculation Report")
    st.download_button(label="📥 Download Structural PDF Report", data=pdf_data, file_name="beam_analysis_report.pdf", mime="application/pdf")

# ============================================================
# MODULE 4: CRACK DETECTION
# ============================================================

elif module == "🔍 Crack Detection":
    st.header("🔍 Structural Crack Detection System")
    st.markdown("Upload an image of a structural concrete surface to isolate and calculate micro-cracking defects using Computer Vision processing matrices.")

    uploaded_file = st.file_uploader("Upload Structural Surface Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Original Image Instance", use_container_width=True)

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        crack_pixels = np.sum(edges > 0)
        total_pixels = edges.shape[0] * edges.shape[1]
        crack_percentage = (crack_pixels / total_pixels) * 100

        if crack_percentage < 2:
            severity, risk = "Minor Crack Matrix", "Low Risk Factor"
            recommendation = "Routine visual inspection schedule recommended. No immediate technical intervention required."
        elif crack_percentage < 5:
            severity, risk = "Moderate Fatigue Crack", "Medium Risk Factor"
            recommendation = "Surface epoxy structural patching recommended. Periodic crack propagation tracking advised."
        else:
            severity, risk = "Severe Degradation Frame", "High Structural Risk"
            recommendation = "Immediate retrofitting assessment required. Urgent structural field testing recommended."

        with col2:
            st.image(edges, caption="Isolated Computer Vision Structural Edge Map", use_container_width=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Calculated Damage Area", f"{crack_percentage:.2f}%")
        c2.metric("Severity Level", severity)
        c3.metric("Action Assessment", risk)

        st.info(f"**Structural Solution Command:** {recommendation}")

# ============================================================
# MODULE 5: EARTHQUAKE SIMULATOR
# ============================================================

elif module == "🏢 Earthquake Simulator":
    st.header("🏢 Earthquake Resistant Building Simulator")
    col1, col2 = st.columns([1, 2])

    with col1:
        building_height = st.slider("Building Height (m)", 5, 300, 50)
        floors = st.slider("Number of Floors", 1, 100, 15)
        magnitude = st.slider("Earthquake Magnitude (Richter Scale)", 1.0, 9.0, 6.5)
        damping_ratio = st.slider("Damping Structural Ratio (ζ)", 0.01, 0.30, 0.05)
        material = st.selectbox("Material Matrix Selection", list(MATERIALS.keys()), key="earthquake_material")

    density = MATERIALS[material]["Density"]
    E = MATERIALS[material]["Young_Modulus"]

    mass = density * building_height
    acceleration = magnitude * 0.35
    earthquake_force = mass * acceleration
    story_drift = (building_height * magnitude) / (E / 1e9)
    safety_rating = max(0, min(100, 100 - story_drift * 5))

    with col2:
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Calculated Seismic Mass", f"{mass:.0f} kg")
        mc2.metric("Total Lateral Force", f"{earthquake_force:.1f} N")
        mc3.metric("Dynamic Story Drift", f"{story_drift:.4f}")

        if safety_rating > 80:
            st.success(f"Seismic Rating: SAFE ({safety_rating:.1f}%)")
        elif safety_rating > 50:
            st.warning(f"Seismic Rating: MODERATE THRESHOLD ({safety_rating:.1f}%)")
        else:
            st.error(f"Seismic Rating: UNSTABLE FAILURE RISK ({safety_rating:.1f}%)")

        t = np.linspace(0, 20, 500)
        response = np.sin(magnitude * t) * np.exp(-damping_ratio * t)
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(x=t, y=response, mode='lines', name='Oscillation Decay'))
        fig_eq.update_layout(title="Structural Damped Structural Waveform Response", template="plotly_white", height=260)
        st.plotly_chart(fig_eq, use_container_width=True)

# ============================================================
# MODULE 6: LOAD CAPACITY PREDICTOR
# ============================================================

elif module == "🚛 Load Capacity Predictor":
    st.header("🚛 AI Bridge Load Capacity Predictor")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        bridge_age = st.slider("Bridge Structural Age (Years)", 1, 100, 20)
        material = st.selectbox("Material Component Type", list(MATERIALS.keys()), key="bridge_material")
        span_length = st.slider("Clear Span Span Length (m)", 5, 300, 40)
        traffic_load = st.slider("Traffic Volume Load (tons/day)", 1, 1000, 250)
        environment = st.selectbox("Environmental Exposure Index", ["Excellent", "Good", "Moderate", "Aggressive"])

    env_factor = {"Excellent": 1.0, "Good": 0.85, "Moderate": 0.70, "Aggressive": 0.50}
    material_factor = {"Concrete": 0.85, "Reinforced Concrete": 0.90, "Structural Steel": 1.00, "Aluminum Alloy": 0.80, "Timber": 0.65}

    rows = 200
    np.random.seed(42)
    age_data = np.random.randint(1, 100, rows)
    span_data = np.random.randint(5, 300, rows)
    traffic_data = np.random.randint(10, 1000, rows)
    capacity = 1200 - age_data * 4 - span_data * 1.2 - traffic_data * 0.3

    X = pd.DataFrame({"Age": age_data, "Span": span_data, "Traffic": traffic_data})
    y = capacity

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)

    input_features = pd.DataFrame([[bridge_age, span_length, traffic_load]], columns=["Age", "Span", "Traffic"])
    prediction = model.predict(input_features)[0]
    prediction *= env_factor[environment] * material_factor[material]

    remaining_life = max(5.0, 100.0 - bridge_age * 0.8 - traffic_load * 0.02)
    health_score = max(0.0, min(100.0, prediction / 12))
    safety_factor = max(0.1, prediction / 250)

    with col2:
        k1, k2, k3 = st.columns(3)
        k1.metric("Predicted Ultimate Load Limit", f"{prediction:.1f} Tons")
        k2.metric("Remaining Operational Life", f"{remaining_life:.1f} Years")
        k3.metric("Structural Health Score", f"{health_score:.1f}%")

        importance_df = pd.DataFrame({"Structural Variable": ["Structure Age", "Span Width", "Traffic Density"], "Weight Importance": model.feature_importances_})
        fig_imp = px.bar(importance_df, x="Structural Variable", y="Weight Importance", title="ML Engine Structural Feature Weight Profile Matrix", height=280)
        st.plotly_chart(fig_imp, use_container_width=True)

# ============================================================
# MODULE 7: MATERIAL DATABASE
# ============================================================

elif module == "📊 Material Database":
    st.header("Engineering Material Database")
    
    material = st.selectbox("Select Material Profile", list(MATERIALS.keys()))
    df_mat = pd.DataFrame(MATERIALS[material].items(), columns=["Engineering Property", "Value Specification"])
    
    st.dataframe(df_mat, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Global Mechanical Comparison Framework Matrix")
    comparison_df = pd.DataFrame(MATERIALS).T
    st.dataframe(comparison_df, use_container_width=True)
