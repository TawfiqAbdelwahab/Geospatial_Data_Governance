import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعدادات مظهرية متقدمة للمنصة
st.set_page_config(page_title="منصة حوكمة البيانات الجيومكانية", layout="wide", initial_sidebar_state="expanded")

# تحسين وتكبير الخطوط وتنسيق الألوان عبر CSS مخصص لتغيير التصميم بالكامل
st.markdown("""
    <style>
        /* تكبير عناوين القوائم والنصوص الرئيسية */
        .big-font { font-size:24px !important; font-weight: bold; color: #1E3A8A; }
        html, body, [data-testid="stSidebar"] { font-size: 18px !important; }
        h1 { font-size: 42px !important; color: #1E3A8A; text-align: center; margin-bottom: 30px; font-weight: 800; }
        h2 { font-size: 30px !important; color: #0D9488; font-weight: 700; border-bottom: 2px solid #E2E8F0; padding-bottom: 10px; }
        h3 { font-size: 24px !important; color: #475569; }
        
        /* تحسين مظهر الأزرار وجعلها بارزة */
        .stButton>button {
            font-size: 20px !important;
            font-weight: bold !important;
            background-color: #0D9488 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0F766E !important;
            transform: scale(1.02);
        }
        
        /* تنسيق الجداول لتكون واضحة وكبيرة */
        .dataframe { font-size: 16px !important; }
        
        /* تحسين التبويبات العلوبة */
        .stTabs [data-baseweb="tab"] { font-size: 20px !important; font-weight: 600; padding: 12px 20px; }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = "data_repository"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

FILES = {
    "incidents": os.path.join(BASE_DIR, "Geospatial_Incident_Tracker.xlsx"),
    "docs_review": os.path.join(BASE_DIR, "Documents_Review_Tracker.xlsx"),
    "gov_docs": os.path.join(BASE_DIR, "Geospatial_Governance_Documents_Tracker.xlsx"),
    "risks": os.path.join(BASE_DIR, "Non_Compliance_Risk_Tracker.xlsx")
}

# دالة ذكية لتهيئة وحقن نموذج بيانات واقعي داخل الملفات لكي لا تظهر فارغة
def initialize_and_populate_data():
    # 1. سجل الحوادث الجيومكانية مع بيانات افتراضية مسبقة
    if not os.path.exists(FILES["incidents"]) or os.path.getsize(FILES["incidents"]) < 1000:
        inc_data = [
            {"Incident_ID": "CG260303001", "PCP": "1002345678901234", "email": "user1@domain.gov.sa", "Request_Date": "2026-06-15", "Current_Status": "مكتمل", "Geospatial_Review": "تم فحص التداخل الطوبولوجي مع الأراضي المجاورة والطبقات مطابقة لمعايير الامتثال.", "Reviewer_Name": "توفيق عبد الوهاب", "Current_Custodian": "العمليات", "Is_Signed": "تم التوقيع"},
            {"Incident_ID": "CG260303002", "PCP": "1002987654321098", "email": "user2@domain.gov.sa", "Request_Date": "2026-06-28", "Current_Status": "قيد Mراجعة", "Geospatial_Review": "يوجد إزاحة بمقدار 1.5 متر في الحدود الشمالية للمخطط، يحتاج إعادة رفع مساحي.", "Reviewer_Name": "أنس الحارس", "Current_Custodian": "حوكمة البيانات الجيومكانية", "Is_Signed": "جاري التوقيع"},
            {"Incident_ID": "CG260303003", "PCP": "1002445566778899", "email": "user3@domain.gov.sa", "Request_Date": "2026-07-01", "Current_Status": "قيد المراجعة", "Geospatial_Review": "المعاملة مستلمة حديثاً وجاري مطابقتها مع مصورات البلدية المحدثة.", "Reviewer_Name": "ريما الدوسري", "Current_Custodian": "حوكمة البيانات الجيومكانية", "Is_Signed": "جاري التوقيع"}
        ]
        pd.DataFrame(inc_data).to_excel(FILES["incidents"], index=False)
        
    # 2. سجل مراجعة الوثائق التشغيلية
    if not os.path.exists(FILES["docs_review"]) or os.path.getsize(FILES["docs_review"]) < 1000:
        docs_data = [
            {"Record_ID": "DOC-001", "Document_Name": "تقرير الرفع المساحي لمشروع شمال الرياض", "Department": "المساحة والخرائط", "Submission_Date": "2026-06-20", "Reviewer": "نوف السهيمي", "Status": "معتمد", "Comments": "التقرير مستوفي لكافة المتطلبات الهندسية وجداول الـ Attribute ممتازة."},
            {"Record_ID": "DOC-002", "Document_Name": "مخطط البنية التحتية للمنطقة الصناعية", "Department": "تخطيط المدن", "Submission_Date": "2026-06-25", "Reviewer": "توفيق عبد الوهاب", "Status": "مرفوض", "Comments": "نظام الإحداثيات المستخدم قديم ويجب التحويل إلى WGS84 / UTM Zone 38N."}
        ]
        pd.DataFrame(docs_data).to_excel(FILES["docs_review"], index=False)

    # 3. وثائق الحوكمة وسياسات NDMO
    if not os.path.exists(FILES["gov_docs"]) or os.path.getsize(FILES["gov_docs"]) < 1000:
        gov_data = [
            {"Policy_ID": "POL-NDMO-01", "Policy_Name": "سياسة تصنيف البيانات الجيومكانية الوطنية", "Version": "v2.0", "NDMO_Domain": "حوكمة البيانات", "Effective_Date": "2025-01-01", "Custodian": "إدارة الحوكمة"},
            {"Policy_ID": "POL-NDMO-02", "Policy_Name": "معيار مشاركة البيانات المفتوحة والجيوداتا", "Version": "v1.1", "NDMO_Domain": "مشاركة البيانات", "Effective_Date": "2025-08-12", "Custodian": "مكتب إدارة البيانات DMO"}
        ]
        pd.DataFrame(gov_data).to_excel(FILES["gov_docs"], index=False)

    # 4. سجل مخاطر عدم الامتثال
    if not os.path.exists(FILES["risks"]) or os.path.getsize(FILES["risks"]) < 1000:
        risks_data = [
            {"Risk_ID": "RSK-09", "Violation_Type": "تداخل حدودي جسيم", "Spatial_Layer", "المخططات المعتمدة", "Severity": "عالي", "Resolution_Status": "تحت الإجراء"},
            {"Risk_ID": "RSK-10", "Violation_Type": "فقدان البيانات الوصفية (Missing Metadata)", "Spatial_Layer", "شبكة الطرق", "Severity": "متوسط", "Resolution_Status": "محلولة"}
        ]
        pd.DataFrame(risks_data).to_excel(FILES["risks"], index=False)

initialize_and_populate_data()

# عنوان المنصة الرئيسي بتنسيق فخم
st.write("<h1>💼 المنصة المركزية الموحدة لحوكمة البيانات والامتثال الجيومكاني</h1>", unsafe_allow_html=True)
st.markdown("---")

menu = ["سجل تتبع الحوادث الجيومكانية", "مراجعة الوثائق التشغيلية", "وثائق الحوكمة وسياسات NDMO", "مخاطر عدم الامتثال الفني"]
choice = st.sidebar.radio("قائمة مستودعات التتبع المركزية", menu)

# =========================================
# التبويب الأول: سجل الحوادث الجيومكانية (المطور)
# =========================================
if choice == "سجل تتبع الحوادث الجيومكانية":
    st.write("<h2>🗂️ سجل تتبع حوادث ومعاملات البيانات الجيومكانية</h2>", unsafe_allow_html=True)
    
    df = pd.read_excel(FILES["incidents"])
    
    # بطاقات الإحصائيات (KPIs) بشكل مكبر ومنظم
    c1, c2, c3 = st.columns(3)
    c1.metric("📊 إجمالي الحوادث المسجلة", len(df))
    c2.metric("⏳ قيد المراجعة الفنية", len(df[df["Current_Status"] == "قيد المراجعة"]))
    c3.metric("✅ المعاملات المكتملة", len(df[df["Current_Status"] == "مكتمل"]))
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["👁️ استعراض وجدولة البيانات الحية", "➕ تسجيل حادثة جديدة", "📝 تحديث وتعديل الحالات"])
    
    with tab1:
        search = st.text_input("🔍 ابحث السريع برقم المعاملة أو رقم العقار (PCP):")
        if search:
            filtered_df = df[df["Incident_ID"].astype(str).str.contains(search) | df["PCP"].astype(str).str.contains(search)]
            st.dataframe(filtered_df, use_container_width=True, height=350)
        else:
            st.dataframe(df, use_container_width=True, height=350)
            
    with tab2:
        st.write("### ➕ نموذج إدخال سجل جديد لمحور الحوكمة")
        with st.form("add_incident_form", clear_on_submit=True):
            f_inc_id = st.text_input("رقم الحادثة (Incident_ID):", placeholder="مثال: CG260303005")
            f_pcp = st.text_input("رقم العقار / المعرّف الجغرافي (PCP):")
            f_email = st.text_input("البريد الإلكتروني لمقدم المعاملة:")
            f_geo_review = st.text_area("نتائج الفحص الطوبولوجي الأولي للطبقات الجغرافية:")
            
            submit = st.form_submit_button("💾 حفظ السجل فوراً")
            if submit:
                if not f_inc_id or not f_pcp:
                    st.error("❌ الحقول الرئيسية فارغة!")
                else:
                    new_row = {
                        "Incident_ID": f_inc_id, "PCP": f_pcp, "email": f_email,
                        "Request_Date": datetime.now().strftime("%Y-%m-%d"),
                        "Current_Status": "قيد المراجعة", "Geospatial_Review": f_geo_review,
                        "Reviewer_Name": "", "Current_Custodian": "حوكمة البيانات الجيومكانية",
                        "Is_Signed": "جاري التوقيع"
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=False)
                    df.to_excel(FILES["incidents"], index=False)
                    st.success("✅ تم حفظ السجل وتأمين مسار البيانات بنجاح!")
                    st.rerun()

    with tab3:
        st.write("### 📝 تعديل حالات الامتثال وفصل الصلاحيات المعتمد")
        if len(df) == 0:
            st.warning("لا توجد سجلات حالياً.")
        else:
            selected_id = st.selectbox("اختر رقم المعاملة المراد مراجعتها وتعديلها الآن:", df["Incident_ID"].unique())
            idx = df[df["Incident_ID"] == selected_id].index[0]
            
            status_options = ["قيد المراجعة", "مكتمل"]
            reviewer_options = ["أنس الحارس", "توفيق عبد الوهاب", "ريما الدوسري", "نوف السهيمي"]
            custodian_options = ["حوكمة البيانات الجيومكانية", "العمليات"]
            sign_options = ["تم التوقيع", "جاري التوقيع"]
            
            col1, col2 = st.columns(2)
            with col1:
                curr_stat = st.selectbox("الحالة الحالية (Current_Status):", status_options, index=status_options.index(df.at[idx, 'Current_Status']) if df.at[idx, 'Current_Status'] in status_options else 0)
                curr_rev = st.selectbox("المراجع المسؤول المعين (Reviewer_Name):", reviewer_options, index=reviewer_options.index(df.at[idx, 'Reviewer_Name']) if df.at[idx, 'Reviewer_Name'] in reviewer_options else 0)
            with col2:
                curr_cust = st.selectbox("الأمين الحالي على الملف (Current_Custodian):", custodian_options, index=custodian_options.index(df.at[idx, 'Current_Custodian']) if df.at[idx, 'Current_Custodian'] in custodian_options else 0)
                curr_sign = st.selectbox("اعتماد توقيع الحوكمة (Is_Signed):", sign_options, index=sign_options.index(df.at[idx, 'Is_Signed']) if df.at[idx, 'Is_Signed'] in sign_options else 0)
                
            curr_notes = st.text_area("تحديث تقرير الفحص والتدقيق الطوبولوجي الفني للطبقة الجغرافية:", value=str(df.at[idx, 'Geospatial_Review']))
            
            if st.button("🔄 اعتماد التعديلات وحفظ في الإكسيل"):
                df.at[idx, 'Current_Status'] = curr_stat
                df.at[idx, 'Reviewer_Name'] = curr_rev
                df.at[idx, 'Current_Custodian'] = curr_cust
                df.at[idx, 'Is_Signed'] = curr_sign
                df.at[idx, 'Geospatial_Review'] = curr_notes
                df.to_excel(FILES["incidents"], index=False)
                st.success(f"✅ تم تحديث بيانات المعاملة {selected_id} بنجاح تام.")
                st.rerun()

# =========================================
# باقي التبويبات المعبأة بالبيانات النموذجية
# =========================================
elif choice == "مراجعة الوثائق التشغيلية":
    st.write("<h2>📄 سجل تتبع مراجعة الوثائق التشغيلية والفنية</h2>", unsafe_allow_html=True)
    df_docs = pd.read_excel(FILES["docs_review"])
    st.dataframe(df_docs, use_container_width=True, height=400)

elif choice == "وثائق الحوكمة وسياسات NDMO":
    st.write("<h2>📜 مستودع وثائق الحوكمة وسياسات مكتب البيانات الوطني</h2>", unsafe_allow_html=True)
    df_gov = pd.read_excel(FILES["gov_docs"])
    st.dataframe(df_gov, use_container_width=True, height=400)

elif choice == "مخاطر عدم الامتثال الفني":
    st.write("<h2>⚠️ سجل تتبع مخاطر عدم الامتثال للمواصفات الجيومكانية</h2>", unsafe_allow_html=True)
    df_risks = pd.read_excel(FILES["risks"])
    st.dataframe(df_risks, use_container_width=True, height=400)
