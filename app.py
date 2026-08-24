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
st.markdown("لوحة تحكم تفاعلية لاستعراض التضاريس، الارتفاعات، والخرائط الميدانية.")

# إعدادات الشريط الجانبي للاختيار بين الطبقات المتاحة والمستقرة
st.sidebar.header("🎛️ خيارات العرض والتضاريس")
map_style = st.sidebar.selectbox(
    "اختر نوع الخريطة:",
    ["خريطة التضاريس والمعالم (OpenTopoMap)", "خريطة الشوارع الكلاسيكية (OpenStreetMap)"]
)

# إحداثيات الزراوة (قابس، تونس)
zrawa_coords = [33.3426, 9.4926]

# اختيار التايلز المناسب الذي لا يتوقف
if map_style == "خريطة التضاريس والمعالم (OpenTopoMap)":
    tiles_choice = 'OpenTopoMap'
else:
    tiles_choice = 'openstreetmap'

# إنشاء الخريطة
m = folium.Map(
    location=zrawa_coords,
    zoom_start=14,
    tiles=tiles_choice
)

# إضافة طبقات إضافية يمكن التبديل بينها مباشرة من الخريطة
folium.TileLayer('OpenTopoMap', name='التضاريس (Topography)').add_to(m)
folium.TileLayer('openstreetmap', name='الشوارع (OSM)').add_to(m)

# علامة موقع الزراوة
popup_content = """
<div style="font-family: Arial; width: 200px; direction: rtl;">
    <h4 style="color: #d9534f; margin-bottom: 5px;">الزراوة القديمة</h4>
    <p><b>الإحداثيات:</b> 33.3426° N, 9.4926° E</p>
    <p>منطقة جبلية ذات تضاريس وعرة.</p>
</div>
"""
folium.Marker(
    location=zrawa_coords,
    popup=folium.Popup(popup_content, max_width=250),
    tooltip="مركز الزراوة",
    icon=folium.Icon(color='red', icon='mountain', prefix='fa')
).add_to(m)

# إضافة أدوات القياس وملء الشاشة وأداة التحكم بالطبقات
m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='meters'))
m.add_child(plugins.Fullscreen())
folium.LayerControl().add_to(m)

# عرض الخريطة
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🗺️ خريطة التضاريس التفاعلية")
    # استدعاء الخريطة بشكل يضمن التحميل السريع
    st_folium(m, width=700, height=550)

with col2:
    st.subheader("📊 تفاصيل الموقع")
    st.info("خريطة التضاريس تظهر المرتفعات، الخطوط الكنتورية، وطبيعة سفح الجبل بدقة.")
    st.markdown("""
    * **الميزة:** تظهر التضاريس الجبلية بوضوح.
    * **الأداة:** استخدم مسطرة القياس في أعلى يسار الخريطة لقياس المسافات بين النقاط.
    """)
