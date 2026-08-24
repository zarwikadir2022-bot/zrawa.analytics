import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import plugins
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="منصة التحليل الجغرافي والجيوفيزيائي",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ منصة التحليل الجغرافي والجيوفيزيائي (نمط VeldScan)")
st.markdown("لوحة تحكم متقدمة لتحديد نطاقات المسح الجغرافي، تحليل التضاريس، واستخراج مؤشرات الشذوذ.")

# إحداثيات الزراوة الافتراضية
zrawa_coords = [33.3426, 9.4926]

# الشريط الجانبي للإعدادات
st.sidebar.header("🎛️ إعدادات المسح والتحليل")
scan_mode = st.sidebar.selectbox(
    "نوع التحليل الميداني:",
    ["تحليل التضاريس والانحدار (Topographic)", "مسح الشذوذ الحراري والمغناطيسي (Anomalies)"]
)

sensitivity = st.sidebar.slider("حساسية الكشف (Sensitivity)", min_value=50, max_value=99, value=85)

# إنشاء الخريطة
m = folium.Map(
    location=zrawa_coords,
    zoom_start=15,
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery'
)

# علامة الموقع
folium.Marker(
    location=zrawa_coords,
    popup="الزراوة القديمة، قابس",
    tooltip="مركز الزراوة",
    icon=folium.Icon(color='red', icon='mountain', prefix='fa')
).add_to(m)

# إضافة أداة الرسم لتحديد نطاق المسح
draw = plugins.Draw(
    export=True,
    position='topleft',
    draw_options={
        'polyline': False,
        'polygon': True,
        'rectangle': True,
        'circle': True,
        'marker': True
    },
    edit_options={'edit': True}
)
m.add_child(draw)
m.add_child(plugins.Fullscreen())

# عرض الواجهة
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ خريطة الاستكشاف وتحديد النطاق")
    st.info("💡 استخدم أداة الرسم (المربع أو المضلع) على الخريطة لتحديد المنطقة المراد فحصها وتحليلها.")
    map_data = st_folium(m, width=650, height=550, key="map")

with col2:
    st.subheader("📊 لوحة النتائج والقياسات")
    
    # التحقق مما إذا قام المستخدم برسم شيء على الخريطة
    if map_data and map_data.get("last_active_drawing"):
        drawing = map_data["last_active_drawing"]
        geom_type = drawing.get("geometry", {}).get("type")
        coords = drawing.get("geometry", {}).get("coordinates")
        
        st.success(f"تم رصد نطاق مسح جديد ({geom_type}) بنجاح!")
        
        # محاكاة تحليل جيوفيزيائي متقدم بناءً على النطاق المحدد
        st.markdown("### 🔬 تقرير التحليل الأولي:")
        
        # توليد قيم تحليلية واقعية للمحاكاة بناءً على الحساسية
        depth_est = np.round(np.random.uniform(1.2, 5.8), 2)
        temp_val = np.round(20.5 + np.random.uniform(-1.5, 2.5), 1)
        confidence = sensitivity - np.random.randint(0, 5)
        
        st.metric(label="درجة الحرارة السطحية التقديرية", value=f"{temp_val} °C")
        st.metric(label="العمق المحتمل للهدف/الفراغ", value=f"{depth_est} متر")
        st.metric(label="نسبة الثقة والشذوذ", value=f"{confidence}%")
        
        if confidence > 80:
            st.warning("⚠️ تنبيه: تم رصد تغير ملحوظ في البصمة الحرارية وتدرج التضاريس في هذا النطاق.")
        else:
            st.info("ℹ️ النطاق طبيعي، تدرج مستقر في التربة.")
            
        # زر لتصدير التقرير
        if st.button("📥 تحميل تقرير التحليل (CSV)"):
            df_report = pd.DataFrame({
                "Parameter": ["Latitude", "Longitude", "Estimated Depth (m)", "Surface Temp (°C)", "Confidence (%)"],
                "Value": [zrawa_coords[0], zrawa_coords[1], depth_est, temp_val, confidence]
            })
            csv_data = df_report.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="اضغط هنا لتنزيل الملف",
                data=csv_data,
                file_name="zrawa_scan_report.csv",
                mime="text/csv"
            )
    else:
        st.warning("الرجاء رسم شكل (مربع أو مضلع) على الخريطة لتفعيل التحليل الفوري للمنطقة.")
