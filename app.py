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
st.markdown("لوحة تحكم تفاعلية لعرض صور الأقمار الصناعية الحقيقية وتحليل التضاريس الميدانية.")

# إحداثيات الزراوة (قابس، تونس)
zrawa_coords = [33.3426, 9.4926]

# إنشاء الخريطة باستخدام طبقة الأقمار الصناعية لشركة Esri بشكل مباشر وثابت
m = folium.Map(
    location=zrawa_coords,
    zoom_start=15,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
)

# علامة موقع الزراوة بدقة
popup_content = """
<div style="font-family: Arial; width: 200px; direction: rtl;">
    <h4 style="color: #d9534f; margin-bottom: 5px;">الزراوة القديمة</h4>
    <p><b>الإحداثيات:</b> 33.3426° N, 9.4926° E</p>
    <p>منطقة جبلية وسفح صخري.</p>
</div>
"""
folium.Marker(
    location=zrawa_coords,
    popup=folium.Popup(popup_content, max_width=250),
    tooltip="مركز الزراوة",
    icon=folium.Icon(color='red', icon='mountain', prefix='fa')
).add_to(m)

# إضافة أدوات قياس المسافات وملء الشاشة
m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='meters'))
m.add_child(plugins.Fullscreen())

# عرض الخريطة في الواجهة
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🗺️ خريطة الأقمار الصناعية الحية")
    # استدعاء الخريطة
    st_folium(m, width=700, height=550)

with col2:
    st.subheader("📊 بيانات الموقع والتحليل")
    st.info("تציד هذه الخريطة تفاصيل سطح الأرض، الجبال، والتضاريس مباشرة من الأقمار الصناعية.")
    st.markdown("""
    * **نوع العرض:** صور فضائية حقيقية (Satellite Imagery).
    * **الأداة:** استخدم مسطرة القياس لقياس المسافات الميدانية.
    """)
