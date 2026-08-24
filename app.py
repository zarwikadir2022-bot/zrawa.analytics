import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="منصة التحليل الشمولي - الزراوة، قابس",
    page_icon="🌍",
    layout="wide"
)

# عنوان رئيسي واحترافي
st.title("🌍 منصة التحليل الجغرافي والشمولي - الزراوة (قابس، تونس)")
st.markdown("لوحة تحكم متقدمة لاستعراض صور الأقمار الصناعية، تحليل التضاريس، وقياس المسافات الميدانية.")

# الشريط الجانبي للإعدادات والتحكم
st.sidebar.header("🎛️ إعدادات التحليل")
analysis_mode = st.sidebar.selectbox(
    "اختر نوع الطبقة الأساسية:",
    ["أقمار صناعية عالية الدقة (Esri)", "خرائط الشوارع (OpenStreetMap)", "التضاريس الهضبية"]
)

# تحديد الإحداثيات الأساسية للزراوة
zrawa_coords = [33.3426, 9.4926]

# خيارات إضافية للشريط الجانبي
show_marker = st.sidebar.checkbox("إظهار علامة موقع الزراوة القديمة", value=True)
add_drawing = st.sidebar.checkbox("تفعيل أدوات الرسم وتحديد المضلعات", value=True)
zoom_level = st.sidebar.slider("مستوى التقريب (Zoom Level)", min_value=10, max_value=19, value=15)

# إنشاء الخريطة بناءً على اختيار المستخدم
if analysis_mode == "أقمار صناعية عالية الدقة (Esri)":
    tiles_choice = 'Esri.WorldImagery'
elif analysis_mode == "خرائط الشوارع (OpenStreetMap)":
    tiles_choice = 'openstreetmap'
else:
    tiles_choice = 'Stamen Terrain'

m = folium.Map(
    location=zrawa_coords,
    zoom_start=zoom_level,
    tiles=tiles_choice
)

# إضافة طبقات إضافية للتبديل السريع
folium.TileLayer('Esri.WorldImagery', name='أقمار صناعية').add_to(m)
folium.TileLayer('openstreetmap', name='شوارع').add_to(m)

# إضافة علامة الموقع إذا تم تفعيلها
if show_marker:
    popup_content = """
    <div style="font-family: Arial; width: 220px; direction: rtl;">
        <h4 style="color: #d9534f; margin-bottom: 5px;">الزراوة القديمة، قابس</h4>
        <p><b>الإحداثيات:</b> 33.3426° N, 9.4926° E</p>
        <p><b>الخصائص:</b> قرية جبلية قديمة، مساكن حفرية، وتضاريس وعرة.</p>
    </div>
    """
    folium.Marker(
        location=zrawa_coords,
        popup=folium.Popup(popup_content, max_width=300),
        tooltip="مركز الزراوة",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(m)

# إضافة أدوات القياس المتقدمة وملء الشاشة
m.add_child(plugins.MeasureControl(position='topleft', primary_length_unit='meters'))
m.add_child(plugins.Fullscreen())

# إضافة أدوات الرسم إذا تم تفعيلها
if add_drawing:
    draw = plugins.Draw(
        export=True,
        position='topleft',
        draw_options={'polyline': True, 'polygon': True, 'rectangle': True, 'circle': True, 'marker': True},
        edit_options={'edit': True}
    )
    m.add_child(draw)

# تفعيل التحكم بالطبقات
folium.LayerControl().add_to(m)

# عرض الخريطة داخل تطبيق Streamlit
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🗺️ الخريطة التفاعلية للمنطقة")
    # عرض الخريطة وجلب بيانات التفاعل
    map_data = st_folium(m, width=800, height=600)

with col2:
    st.subheader("📊 لوحة المعلومات")
    st.info("قم بتحريك الخريطة أو التكبير لاستكشاف سفح الجبل والمحيط الجغرافي للزراوة.")
    
    # معلومات تحليلية إضافية سريعة
    st.markdown("""
    * **المنطقة الإدارية:** مطماطة الجديدة، قابس.
    * **الارتفاع الجغرافي:** منطقة جبلية مرتفعة.
    * **الأدوات المتاحة:**
        * قياس المسافات الميدانية بالأمتار.
        * تحديد مضلعات ورسم مسارات.
        * حفظ المخرجات الجغرافية.
    """)

# قسم إضافي لتحليلات قادمة
st.markdown("---")
st.subheader("⚙️ الخطوات التطويرية القادمة للتحليل الشمولي:")
st.write("يمكننا لاحقاً ربط هذا التطبيق بـ APIs خاصة بسحب مؤشرات الغطاء النباتي (NDVI) ومقارنة صور الأقمار الصناعية تاريخياً بشكل آلي مباشر من داخل هذه المنصة.")
