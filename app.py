import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="منصة التحليل الجغرافي - الزراوة، قابس",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 منصة التحليل الجغرافي والشمولي - الزراوة (قابس، تونس)")
st.markdown("لوحة تحكم تفاعلية لاستعراض صور الأقمار الصناعية وقياس المسافات الميدانية.")

# إعدادات الشريط الجانبي
st.sidebar.header("🎛️ خيارات العرض")
map_style = st.sidebar.selectbox(
    "اختر نوع الخريطة الأساسية:",
    ["أقمار صناعية عالية الدقة (Esri)", "خرائط الشوارع (OpenStreetMap)"]
)

# إحداثيات الزراوة (قابس، تونس)
zrawa_coords = [33.3426, 9.4926]

# تحديد نوع التايلز (Tiles)
if map_style == "أقمار صناعية عالية الدقة (Esri)":
    tiles_choice = 'Esri.WorldImagery'
else:
    tiles_choice = 'openstreetmap'

# إنشاء الخريطة
m = folium.Map(
    location=zrawa_coords,
    zoom_start=15,
    tiles=tiles_choice
)

# إضافة طبقة بديلة لقمر صناعي أو شوارع
folium.TileLayer('Esri.WorldImagery', name='أقمار صناعية').add_to(m)
folium.TileLayer('openstreetmap', name='شوارع').add_to(m)

# علامة موقع الزراوة
popup_content = """
<div style="font-family: Arial; width: 200px; direction: rtl;">
    <h4 style="color: #d9534f; margin-bottom: 5px;">الزراوة القديمة</h4>
    <p><b>الإحداثيات:</b> 33.3426° N, 9.4926° E</p>
</div>
"""
folium.Marker(
    location=zrawa_coords,
    popup=folium.Popup(popup_content, max_width=250),
    tooltip="مركز الزراوة",
    icon=folium.Icon(color='red', icon='home', prefix='fa')
).add_to(m)

# إضافة أدوات القياس وملء الشاشة
m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='meters'))
m.add_child(plugins.Fullscreen())
folium.LayerControl().add_to(m)

# تقسيم الشاشة وعرض الخريطة باستخدام st_folium بشكل آمن
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🗺️ الخريطة التفاعلية")
    # استدعاء الخريطة مع تحديد العرض والارتفاع لضمان عدم توقفها
    st_folium(m, width=700, height=550)

with col2:
    st.subheader("📊 معلومات الموقع")
    st.info("الزراوة (قابس، تونس): منطقة جبلية عريقة تتميز بتضاريسها الصخرية ومساكنها الحفرية.")
    st.markdown("""
    * **خط العرض:** 33.3426° N
    * **خط الطول:** 9.4926° E
    * **الأداة:** قياس المسافات بالأمتار متاحة أعلى الخريطة.
    """)
