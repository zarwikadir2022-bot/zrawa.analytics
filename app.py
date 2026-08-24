    import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="منصة التحليل الجيوفيزيائي المتقدم",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ المنصة الذكية للتحليل الجغرافي والجيوفيزيائي الشامل")
st.markdown("لوحة تحكم ديناميكية تتيح إدخال أي إحداثيات أو منطقة في العالم، مع توليد خرائط حرارية وتحليل نصي معمق.")

# قائمة بالمناطق المتاحة أو إمكانية إدخال منطقة حرة بالكامل
st.sidebar.header("📍 إعدادات الموقع والإحداثيات")
region_option = st.sidebar.selectbox(
    "اختر الموقع أو حدد إحداثيات حرة:",
    ["منطقة مخصصة (إحداثيات حرة بالكامل)", "الزراوة القديمة (قابس، تونس)", "قرطاج (تونس العاصمة)", "تطاوين (الجنوب التونسي)"]
)

# تحديد الإحداثيات والاسم بناءً على رغبة المستخدم
if "مخصصة" in region_option:
    site_name = st.sidebar.text_input("اسم الموقع المستهدف:", "منطقة استكشاف جديدة")
    lat_input = st.sidebar.number_input("خط العرض (Latitude):", value=33.3426, format="%.6f")
    lon_input = st.sidebar.number_input("خط الطول (Longitude):", value=9.4926, format="%.6f")
    target_coords = [lat_input, lon_input]
elif "الزراوة" in region_option:
    site_name = "الزراوة القديمة، قابس"
    target_coords = [33.3426, 9.4926]
elif "قرطاج" in region_option:
    site_name = "قرطاج التاريخية، تونس"
    target_coords = [36.8528, 10.3320]
else:
    site_name = "تطاوين، تونس"
    target_coords = [32.9297, 10.4518]

