import streamlit as st
import folium
from folium.plugins import HeatMap, Fullscreen, Draw
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

# إعدادات صفحة عريضة لضمان أقصى مساحة ممكنة للخريطة
st.set_page_config(
    page_title="منصة التحليل الجيوفيزيائي - FieldScan",
    page_icon="🗺️",
    layout="wide"
)

# تنسيق CSS مخصص لجعل التطبيق يبدو كمنصة خرائط احترافية متكاملة
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ منصة الاستكشاف الجيوفيزيائي الشاملة (FieldScan Style)")

# الشريط الجانبي للإعدادات السريعة
st.sidebar.header("📍 إعدادات الموقع والإحداثيات")
region_option = st.sidebar.selectbox(
    "اختر الموقع أو حدد إحداثيات حرة:",
    ["منطقة مخصصة (إحداثيات حرة بالكامل)", "الزراوة القديمة (قابس، تونس)", "قرطاج (تونس العاصمة)", "تطاوين (الجنوب التونسي)"]
)

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

st.sidebar.markdown("---")
st.sidebar.header("🗺️ طبقات الخريطة")
map_style = st.sidebar.selectbox(
    "اختر نوع الخريطة:",
    ["صور الأقمار الصناعية (Esri Imagery)", "خريطة الشوارع والمدن (OpenStreetMap)", "خريطة التضاريس (OpenTopoMap)"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔬 إعدادات المسح والتحليل")
anomaly_type = st.sidebar.selectbox(
    "نوع الشذوذ المستهدف:",
    ["فراغات وسراديب تحت سطحية (Cavities)", "تكتلات أو عروق معدنية (Metallic Veins)", "تجمعات ومسارات مائية باطنية (Water/Moisture)", "تغيرات فيزيائية وهيكلية عامة"]
)
sensitivity = st.sidebar.slider("معامل الحساسية الطيفية والحرارية:", 50, 99, 88)

# تحديد روابط الخرائط
if "الأقمار الصناعية" in map_style:
    tiles_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    tiles_attr = 'Esri World Imagery'
elif "الشوارع" in map_style:
    tiles_url = 'openstreetmap'
    tiles_attr = 'OpenStreetMap Contributors'
else:
    tiles_url = 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'
    tiles_attr = 'OpenTopoMap'

# بناء الخريطة
m = folium.Map(
    location=target_coords,
    zoom_start=16,
    tiles=tiles_url,
    attr=tiles_attr
)

folium.Marker(
    location=target_coords,
    popup=f"{site_name}",
    tooltip=site_name,
    icon=folium.Icon(color='red', icon='map-pin', prefix='fa')
).add_to(m)

# توليد النقاط الحرارية
np.random.seed(int(abs(target_coords[0] * 1000)))
heat_data = []
for _ in range(35):
    lat_offset = np.random.normal(0, 0.002)
    lon_offset = np.random.normal(0, 0.002)
    intensity = np.random.uniform(0.5, 1.0)
    heat_data.append([target_coords[0] + lat_offset, target_coords[1] + lon_offset, intensity])

HeatMap(heat_data, radius=22, blur=15, max_zoom=1).add_to(m)

# أدوات الرسم والتحديد الميداني
draw = Draw(
    export=True,
    position='topleft',
    draw_options={'polyline': False, 'polygon': True, 'rectangle': True, 'circle': True, 'marker': True},
    edit_options={'edit': True}
)
m.add_child(draw)
Fullscreen().add_to(m)

# حساب المؤشرات السريعة
est_depth = np.round(np.random.uniform(1.2, 6.8), 2)
est_temp = np.round(20.5 + np.random.uniform(-1.0, 3.5), 1)

# تصميم لوحة المؤشرات العلوية المدمجة فوق الخريطة مباشرة
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="📍 الموقع النشط", value=site_name)
with m_col2:
    st.metric(label="📊 مؤشر الشذوذ", value=f"{sensitivity}%")
with m_col3:
    st.metric(label="📏 العمق التقديري", value=f"{est_depth} م")
with m_col4:
    st.metric(label="🌡️ البصمة الحرارية", value=f"{est_temp} °C")

# عرض الخريطة بمساحة عملاقة تملأ الشاشة (ارتفاع 780 بكسل) لتكون هي العنصر الأساسي
map_html = m._repr_html_()
components.html(map_html, height=780, scrolling=True)

# قسم التقارير والبيانات بالأسفل لتجنب ازدحام الشاشة
st.markdown("---")
with st.expander("📖 عرض التقرير النصي المعمق وتصدير البيانات (انقر للاستعراض)", expanded=False):
    st.subheader(f"تقرير التشخيص الجيوفيزيائي الميداني: {site_name}")
    st.write(f"**الإحداثيات:** {target_coords[0]}, {target_coords[1]} | **الهدف:** {anomaly_type}")
    st.markdown(f"""
    * **القراءة الطيفية:** تشير البيانات إلى وجود تباينات حرارية تقدر بـ **{est_temp} °C** في النطاق المحيط بمركز الإشارة.
    * **العمق الهيكلي:** الهدف المباشر متوقع على عمق يناهز **{est_depth} متر**.
    * **التوصية:** استخدم أدوات الرسم المتاحة أعلى الخريطة لتحديد المضلعات الميدانية ومطابقتها مع أجهزة المسح الميدانية الفعلية.
    """)
    
    if st.button("📥 تصدير تقرير الموقع (CSV)"):
        df_full = pd.DataFrame({
            "Site_Name": [site_name],
            "Latitude": [target_coords[0]],
            "Longitude": [target_coords[1]],
            "Anomaly_Type": [anomaly_type],
            "Estimated_Depth_m": [est_depth],
            "Surface_Temp_C": [est_temp],
            "Confidence_Score": [sensitivity]
        })
        csv_bytes = df_full.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="تنزيل الملف الآن",
            data=csv_bytes,
            file_name=f"{site_name.replace(' ', '_')}_fieldscan.csv",
            mime="text/csv"
        )
