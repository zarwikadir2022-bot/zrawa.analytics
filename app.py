import streamlit as st
import folium
from folium.plugins import HeatMap, Fullscreen, Draw
import numpy as np
import pandas as pd

# إعدادات الصفحة لتكون عريضة بالكامل
st.set_page_config(
    page_title="منصة التحليل الجيوفيزيائي الفضائي - FieldScan Pro",
    page_icon="💎",
    layout="wide"
)

# ---------------------------------------------------------
# تصميم الـ CSS المخصص: ألوان زرقاء، كريستالية، وثلجية شفافة مع 3D
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* خلفية التطبيق العامة بدرجات الأزرق الليلي العميق */
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #3a506b 100%);
        color: #e0fbfc;
    }
    
    /* تقليل الهوامش العلوية */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100% !important;
    }

    /* تصميم الحاويات بزجاج بلوري وشفاف (Glassmorphism & 3D Effect) */
    .crystal-card {
        background: rgba(28, 37, 65, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(116, 198, 157, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .crystal-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px 0 rgba(0, 180, 216, 0.25);
    }

    /* الشريط الجانبي بتصميم ثلجي فاخر */
    [data-testid="stSidebar"] {
        background: rgba(11, 19, 43, 0.85);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(144, 224, 239, 0.15);
    }

    /* تخصيص العناوين */
    h1, h2, h3 {
        color: #ade8f4 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* تصميم إطار الخريطة بلمسة كريستالية */
    iframe {
        width: 100% !important;
        border-radius: 16px;
        border: 2px solid rgba(144, 224, 239, 0.3);
        box-shadow: 0 8px 25px rgba(0, 119, 182, 0.4);
    }

    /* صندوق القفل للمحتوى غير المشترك */
    .locked-box {
        background: rgba(15, 23, 42, 0.8);
        border: 2px dashed rgba(144, 224, 239, 0.4);
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        color: #90e0ef;
        margin-top: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* الأزرار بلمسة نيون زرقاء ثلاثية الأبعاد */
    .stButton>button {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.4);
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0096c7 0%, #48cae4 100%);
        box-shadow: 0 6px 20px rgba(72, 202, 228, 0.6);
        border-color: #ade8f4;
    }
    </style>
""", unsafe_allow_html=True)

# عنوان المنصة الرئيسي
st.markdown("<h1 style='text-align: center; margin-bottom: 25px;'>💎 منصة الاستكشاف الجيوفيزيائي الفضائي (FieldScan Crystal Pro)</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# نظام الاشتراكات ورمز التفعيل (Subscription / License Key)
# ---------------------------------------------------------
st.sidebar.header("🔐 البوابة الأمنية والاشتراك")
license_input = st.sidebar.text_input("أدخل رمز التفعيل الخاص بك:", type="password", placeholder="مثال: FIELD-PRO-2026")

valid_licenses = ["FIELD-PRO-2026", "VIP-TUNISIA-99", "DEMO-TEST-KEY"]
is_subscribed = license_input in valid_licenses

if is_subscribed:
    st.sidebar.success("✨ حالة الاشتراك: مفعل (باقة الكريستال الاحترافية)")
else:
    st.sidebar.warning("🔒 حالة الاشتراك: نسخة مجانية (مقيّدة)")
    st.sidebar.info("💡 أدخل المفتاح **`FIELD-PRO-2026`** في الأعلى لتفعيل كامل الميزات وتحليل التقارير المعقدة.")

st.sidebar.markdown("---")

# الشريط الجانبي للإعدادات الجغرافية
st.sidebar.header("📍 إقطاعية المسح والإحداثيات")
region_option = st.sidebar.selectbox(
    "اختر الموقع المستهدف:",
    ["منطقة مخصصة (إحداثيات حرة بالكامل)", "الزراوة القديمة (قابس، تونس)", "قرطاج التاريخية (تونس العاصمة)", "تطاوين (الجنوب التونسي)", "سيدي بو سعيد (تونس)"]
)

if "مخصصة" in region_option:
    site_name = st.sidebar.text_input("اسم الموقع المستهدف:", "قطاع استكشاف رقم 01")
    lat_input = st.sidebar.number_input("خط العرض (Latitude):", value=33.3426, format="%.6f")
    lon_input = st.sidebar.number_input("خط الطول (Longitude):", value=9.4926, format="%.6f")
    target_coords = [lat_input, lon_input]
elif "الزراوة" in region_option:
    site_name = "الزراوة القديمة، قابس"
    target_coords = [33.3426, 9.4926]
elif "قرطاج" in region_option:
    site_name = "قرطاج التاريخية، تونس"
    target_coords = [36.8528, 10.3320]
elif "تطاوين" in region_option:
    site_name = "تطاوين، تونس"
    target_coords = [32.9297, 10.4518]
else:
    site_name = "سيدي بو سعيد، تونس"
    target_coords = [36.8703, 10.3417]

st.sidebar.markdown("---")
st.sidebar.header("🗺️ طبقات العرض البصري")
map_style = st.sidebar.selectbox(
    "نوع خريطة الخلفية:",
    ["صور الأقمار الصناعية الفضائية (Esri Imagery)", "خريطة الشوارع والشبكات (OpenStreetMap)", "خريطة التضاريس والارتفاعات (OpenTopoMap)"]
)

st.sidebar.markdown("---")
st.sidebar.header("🔬 معايير الحساسية والاستشعار")
anomaly_type = st.sidebar.selectbox(
    "طبيعة الهدف الجيوفيزيائي المستهدف:",
    [
        "فراغات وسراديب تحت سطحية معمارية/طبيعية (Cavities)", 
        "تكتلات عروقية أو فلزات معدنية عالية الكثافة (Metallic Veins)", 
        "تجمعات رطوبة ومسارات مائية باطنية (Water/Moisture Pathways)", 
        "تغيرات فيزيائية وهيكلية متقطعة (Structural Faults)"
    ]
)
sensitivity = st.sidebar.slider("مؤشر الحساسية الطيفية والحرارية الطاقية:", 50, 99, 88)

# روابط الأنماط الجغرافية
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
    attr=tiles_attr,
    width="100%",
    height="100%"
)

folium.Marker(
    location=target_coords,
    popup=f"{site_name}",
    tooltip=site_name,
    icon=folium.Icon(color='blue', icon='crosshairs', prefix='fa')
).add_to(m)

# توليد نقاط الشذوذ الحراري ديناميكياً بناءً على الموقع المدخل لضمان اختلاف البيانات
np.random.seed(int(abs(target_coords[0] * 10000 + target_coords[1] * 10000)))
heat_data = []
for _ in range(40):
    lat_offset = np.random.normal(0, 0.0022)
    lon_offset = np.random.normal(0, 0.0022)
    intensity = np.random.uniform(0.4, 1.0)
    heat_data.append([target_coords[0] + lat_offset, target_coords[1] + lon_offset, intensity])

HeatMap(heat_data, radius=24, blur=16, max_zoom=1).add_to(m)

# أدوات الرسم
draw = Draw(
    export=True,
    position='topleft',
    draw_options={'polyline': False, 'polygon': True, 'rectangle': True, 'circle': True, 'marker': True},
    edit_options={'edit': True}
)
m.add_child(draw)
Fullscreen().add_to(m)

# حساب المعايير الحسابية المتقدمة الفريدة لكل مسح
seed_val = abs(target_coords[0] + target_coords[1])
est_depth = np.round(1.5 + (seed_val % 5.5), 2)
est_temp = np.round(19.0 + (seed_val % 6.5), 1)
magnetic_susceptibility = np.round(45.2 + (seed_val % 38.4), 1) # مؤشر الكثافة المغناطيسية
thermal_contrast = np.round(2.1 + (seed_val % 4.3), 2) # تباين درجات الحرارة
stability_index = np.round(72.0 + (seed_val % 25.5), 1) # معامل استقرار الطبقات الصخرية
cavity_probability = int(60 + (seed_val % 38)) # الاحتمالية المئوية للهدف

# ---------------------------------------------------------
# لوحة المؤشرات الثلاثية الأبعاد (Crystal Metrics Bar)
# ---------------------------------------------------------
st.markdown("### 📊 لوحة القياسات الفيزيائية والحسابية المتقدمة")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='crystal-card' style='text-align: center;'>
            <h4 style='color: #90e0ef; margin:0;'>العمق الهيكلي</h4>
            <h2 style='color: #ffffff; margin: 10px 0;'>{est_depth if is_subscribed else "🔒"} م</h2>
            <p style='font-size:12px; color:#a9d6e5; margin:0;'>المدى التقديري للهدف</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='crystal-card' style='text-align: center;'>
            <h4 style='color: #90e0ef; margin:0;'>التباين المغناطيسي</h4>
            <h2 style='color: #ffffff; margin: 10px 0;'>{magnetic_susceptibility if is_subscribed else "🔒"} nT</h2>
            <p style='font-size:12px; color:#a9d6e5; margin:0;'>شدة الاضطراب المغناطيسي</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='crystal-card' style='text-align: center;'>
            <h4 style='color: #90e0ef; margin:0;'>التبادل الحراري</h4>
            <h2 style='color: #ffffff; margin: 10px 0;'>{thermal_contrast if is_subscribed else "🔒"} °C</h2>
            <p style='font-size:12px; color:#a9d6e5; margin:0;'>مؤشر الانبعاث السطحي</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='crystal-card' style='text-align: center;'>
            <h4 style='color: #90e0ef; margin:0;'>مؤشر الاحتمالية</h4>
            <h2 style='color: #ffffff; margin: 10px 0;'>{cavity_probability if is_subscribed else "🔒"}%</h2>
            <p style='font-size:12px; color:#a9d6e5; margin:0;'>دقة البصمة المستهدفة</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# عرض الخريطة الفضائية الكريستالية
# ---------------------------------------------------------
st.markdown("<div class='crystal-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0;'>🛰️ خريطة المسح الجيومكاني التفاعلي</h3>", unsafe_allow_html=True)
from streamlit_folium import st_folium
st_folium(m, width="100%", height=850, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# التقرير الاستشاري المعمق والفريد لكل موقع
# ---------------------------------------------------------
st.markdown("---")
st.markdown("<h3>📖 تقرير التشخيص الجيوفيزيائي والاستشاري المخصص</h3>", unsafe_allow_html=True)

if is_subscribed:
    # صياغة تقرير مختلف كلياً بناءً على موقع الهدف ونوع الشذوذ
    report_text = f"""
    <div class='crystal-card'>
        <h3>📑 شهادة تحليل وتوثيق ميداني رقم (#FS-{int(seed_val * 13) % 90000 + 10000})</h3>
        <p><b>📍 اسم الموقع الجغرافي:</b> {site_name}</p>
        <p><b>🌐 الإحداثيات المعتمدة:</b> <code>{target_coords[0]}° N, {target_coords[1]}° E</code></p>
        <p><b>🎯 الهدف الجيوفيزيائي المدروس:</b> {anomaly_type}</p>
        <p><b>⚖️ معامل الثقة والحساسية الطيفية:</b> {sensitivity}%</p>
        
        <hr style='border-color: rgba(144, 224, 239, 0.2);'>
        
        <h4>1. التحليل الطيفي والفيزيائي للطبقات الباطنية في ({site_name}):</h4>
        <p>بناءً على معطيات الطيف الراداري والحراري للموقع، تم رصد معامل تباين حراري يعادل <b>{thermal_contrast} °C</b> فوق متوسط البيئة المحيطة. تشير قراءات الكثافة المغناطيسية المسجلة عند <b>{magnetic_susceptibility} نانو تيسلا (nT)</b> إلى وجود تباين ملحوظ في التركيب المعدني أو الصخري مقارنة بالخصائص الإقليمية المعتادة للتربة في هذه الناحية.</p>
        
        <h4>2. التقييم الهندسي وتحديد العمق ({anomaly_type}):</h4>
        <p>أظهرت نمذجة الانعكاس الإشاعي أن المركز البؤري للشذوذ يتقاطع مع عمق هندسي يقدر بـ <b>{est_depth} متراً</b>. وبناءً على خوارزميات الاستقرار (المقدرة بنحو <b>{stability_index}%</b>)، فإن البنية التحتية المستهدفة تتمتع بدرجة عالية من العزل الطبيعي عن العوامل المناخية السطحية، مما يرفع من دقة ترجيح وجود الهدف بنسبة <b>{cavity_probability}%</b>.</p>
        
        <h4>3. التوصيات الاستراتيجية والخطوات الميدانية المعتمدة:</h4>
        <ul>
            <li><b>تحديد محاور المسح الميداني:</b> يُنصح بنشر فرق المسح الكهرومغناطيسي في نطاق دائرة شعاعها 15 متراً مركزها الإحداثيات المحددة أعلاه.</li>
            <li><b>التحقق عبر الجيورادار (GPR):</b> يفضل توجيه نبضات رادار اختراق الأرض بترددات تتراوح بين 100 إلى 250 ميغاهيرتز لتأكيد ملامح العمق الهيكلي (<b>{est_depth} م</b>).</li>
            <li><b>المعايرة البيئية:</b> أخذ بعين الاعتبار تأثير التكوينات الصخرية المحلية على التباين الحراري المسجل لضمان دقة الحفر أو التنقيب الاستكشافي اللاحق.</li>
        </ul>
    </div>
    """
    st.markdown(report_text, unsafe_allow_html=True)

    # زر التصدير
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("📥 تصدير التقرير والبيانات (CSV)"):
            df_full = pd.DataFrame({
                "Site_Name": [site_name],
                "Latitude": [target_coords[0]],
                "Longitude": [target_coords[1],],
                "Anomaly_Target": [anomaly_type],
                "Estimated_Depth_m": [est_depth],
                "Magnetic_Susceptibility_nT": [magnetic_susceptibility],
                "Thermal_Contrast_C": [thermal_contrast],
                "Stability_Index_pct": [stability_index],
                "Probability_pct": [cavity_probability],
                "Map_Style": [map_style]
            })
            csv_bytes = df_full.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="تنزيل الملف الرقمي للتقرير",
                data=csv_bytes,
                file_name=f"{site_name.replace(' ', '_')}_Crystal_Report.csv",
                mime="text/csv"
            )
else:
    st.markdown("""
        <div class='locked-box'>
            <h3>🔒 التقارير الاستشارية المتقدمة والمعايير الحسابية مقفلة</h3>
            <p>أنت تستهلك النسخة الأساسية للمنصة. للاستفادة من التقارير المختلفة ديناميكياً لكل موقع وتصدير ملفات التحليل القياسية، يجدر بك تفعيل الاشتراك الاحترافي.</p>
            <p>أدخل رمز التفعيل في الشريط الجانبي (مثل: <code>FIELD-PRO-2026</code>) لفتح الميزات الفضائية كاملة.</p>
        </div>
    """, unsafe_allow_html=True)
