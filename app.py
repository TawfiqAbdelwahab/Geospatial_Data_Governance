import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعدادات الصفحة المظهرية والجمالية للمنصة
st.set_page_config(page_title="منصة حوكمة البيانات الجيومكانية", layout="wide", initial_sidebar_state="expanded")

# المسار الافتراضي للملفات - تم تحويله محلياً ليعمل أونلاين عبر ملفات وهمية في حال عدم وجود السيرفر
BASE_DIR = "data_repository"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

FILES = {
    "incidents": os.path.join(BASE_DIR, "Geospatial_Incident_Tracker.xlsx"),
    "docs_review": os.path.join(BASE_DIR, "Documents_Review_Tracker.xlsx"),
    "gov_docs": os.path.join(BASE_DIR, "Geospatial_Governance_Documents_Tracker.xlsx"),
    "risks": os.path.join(BASE_DIR, "Non_Compliance_Risk_Tracker.xlsx")
}

# دالة برمجية لتهيئة ملفات الإكسيل تلقائياً إذا كانت فارغة لمنع انهيار النظام
def initialize_excel_files():
    if not os.path.exists(FILES["incidents"]):
        df = pd.DataFrame(columns=["Incident_ID", "PCP", "email", "Request_Date", "Current_Status", "Geospatial_Review", "Reviewer_Name", "Current_Custodian", "Is_Signed"])
        df.to_excel(FILES["incidents"], index=False)
    if not os.path.exists(FILES["docs_review"]):
        df = pd.DataFrame(columns=["Record_ID", "Document_Name", "Department", "Submission_Date", "Reviewer", "Status", "Comments"])
        df.to_excel(FILES["docs_review"], index=False)
    if not os.path.exists(FILES["gov_docs"]):
        df = pd.DataFrame(columns=["Policy_ID", "Policy_Name", "Version", "NDMO_Domain", "Effective_Date", "Custodian"])
        df.to_excel(FILES["gov_docs"], index=False)
    if not os.path.exists(FILES["risks"]):
        df = pd.DataFrame(columns=["Risk_ID", "Violation_Type", "Spatial_Layer", "Severity", "Resolution_Status"])
        df.to_excel(FILES["risks"], index=False)

initialize_excel_files()

# العنوان الرئيسي للمنصة الشاملة
st.title("💼 المنصة المركزية الموحدة لحوكمة البيانات والامتثال الجيومكاني")
st.markdown("---")

# القائمة الجانبية للتنقل بين الأنظمة الأربعة
menu = ["سجل تتبع الحوادث الجيومكانية", "مراجعة الوثائق التشغيلية", "وثائق الحوكمة وسياسات NDMO", "مخاطر عدم الامتثال الفني"]
choice = st.sidebar.radio("قائمة مستودعات التتبع المركزية", menu)

# =========================================
# التبويب الأول: سجل الحوادث الجيومكانية (المطلوب بالتفصيل)
# =========================================
if choice == "سجل تتبع الحوادث الجيومكانية":
    st.header("🗂️ سجل تتبع حوادث ومعاملات البيانات الجيومكانية")
    
    # قراءة البيانات الحالية
    df = pd.read_excel(FILES["incidents"])
    
    # عرض إحصائيات سريعة في الأعلى (KPI Cards)
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الحوادث المسجلة", len(df))
    c2.metric("قيد المراجعة", len(df[df["Current_Status"] == "قيد المراجعة"]))
    c3.metric("المعاملات المكتملة", len(df[df["Current_Status"] == "مكتمل"]))
    
    st.markdown("---")
    
    # قسّمنا الصفحة داخلياً إلى: عرض البيانات، إضافة حادثة، تعديل حادثة
    tab1, tab2, tab3 = st.tabs(["👁️ عرض وجدولة البيانات", "➕ إضافة سجل حادثة جديد", "📝 تعديل وتحديث سجل قائم"])
    
    with tab1:
        search = st.text_input("🔍 ابحث في السجل بواسطة رقم الحادثة أو رقم العقار (PCP):")
        if search:
            filtered_df = df[df["Incident_ID"].astype(str).str.contains(search) | df["PCP"].astype(str).str.contains(search)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
            
    with tab2:
        st.subheader("نموذج إدخال حادثة جيومكانية جديدة")
        with st.form("add_incident_form", clear_on_submit=True):
            inc_id = st.text_input("رقم الحادثة (Incident_ID):", placeholder="مثال: CG260303005")
            pcp = st.text_input("رقم العقار / المعرّف الجغرافي (PCP - مكون من 16 خانة):")
            email = st.text_input("البريد الإلكتروني للمقدم (Email):")
            geo_review = st.text_area("نتائج الفحص الطوبولوجي وملاحظات المراجعة الفنية:")
            
            # حقول الحوكمة التلقائية المحمية
            st.info("💡 سيتم تعيين التاريخ تلقائياً باليوم، والحالة الافتراضية 'قيد المراجعة'، والأمين الحالي 'حوكمة البيانات الجيومكانية'.")
            
            submit = st.form_submit_button("💾 حفظ وتسجيل الحادثة في قاعدة البيانات")
            if submit:
                if not inc_id or not pcp:
                    st.error("❌ عذراً يا هندسة، رقم الحادثة ورقم العقار حقول إجبارية!")
                else:
                    new_row = {
                        "Incident_ID": inc_id,
                        "PCP": pcp,
                        "email": email,
                        "Request_Date": datetime.now().strftime("%Y-%m-%d"),
                        "Current_Status": "قيد المراجعة",
                        "Geospatial_Review": geo_review,
                        "Reviewer_Name": "",
                        "Current_Custodian": "حوكمة البيانات الجيومكانية",
                        "Is_Signed": "جاري التوقيع"
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=False)
                    df.to_excel(FILES["incidents"], index=False)
                    st.success("✅ تم حفظ السجل بنجاح ومحوكمته برمجياً!")
                    st.rerun()

    with tab3:
        st.subheader("تحديث حالة الحادثة وفصل الصلاحيات (الدومين والفالديشن)")
        if len(df) == 0:
            st.warning("لا توجد سجلات حالياً للتعديل.")
        else:
            selected_id = st.selectbox("اختر رقم الحادثة المراد تحديثها:", df["Incident_ID"].unique())
            idx = df[df["Incident_ID"] == selected_id].index[0]
            
            # عرض البيانات الحالية قبل التعديل
            st.write(f"المعاملة الحالية تتبع للعقار رقم: **{df.at[idx, 'PCP']}**")
            
            # تطبيق القوائم المنسدلة الصارمة (Domain validation) المتفق عليها مع قطاع الأعمال
            status_options = ["قيد المراجعة", "مكتمل"]
            reviewer_options = ["أنس الحارس", "توفيق عبد الوهاب", "ريما الدوسري", "نوف السهيمي"]
            custodian_options = ["حوكمة البيانات الجيومكانية", "العمليات"]
            sign_options = ["تم التوقيع", "جاري التوقيع"]
            
            # جلب المواقع الافتراضية في الاختيار
            curr_stat = st.selectbox("حالة التقرير (Current_Status):", status_options, index=status_options.index(df.at[idx, 'Current_Status']) if df.at[idx, 'Current_Status'] in status_options else 0)
            curr_rev = st.selectbox("اسم المراجع الجيومكاني المختص (Reviewer_Name):", reviewer_options, index=reviewer_options.index(df.at[idx, 'Reviewer_Name']) if df.at[idx, 'Reviewer_Name'] in reviewer_options else 0)
            curr_cust = st.selectbox("موقع التقرير الحالي (Current_Custodian):", custodian_options, index=custodian_options.index(df.at[idx, 'Current_Custodian']) if df.at[idx, 'Current_Custodian'] in custodian_options else 0)
            curr_sign = st.selectbox("حالة التوقيع (Is_Signed):", sign_options, index=sign_options.index(df.at[idx, 'Is_Signed']) if df.at[idx, 'Is_Signed'] in sign_options else 0)
            curr_notes = st.text_area("تحديث ملاحظات المراجعة الفنية الجيومكانية:", value=str(df.at[idx, 'Geospatial_Review']))
            
            if st.button("🔄 اعتماد التعديلات وحفظ التغييرات"):
                df.at[idx, 'Current_Status'] = curr_stat
                df.at[idx, 'Reviewer_Name'] = curr_rev
                df.at[idx, 'Current_Custodian'] = curr_cust
                df.at[idx, 'Is_Signed'] = curr_sign
                df.at[idx, 'Geospatial_Review'] = curr_notes
                
                df.to_excel(FILES["incidents"], index=False)
                st.success(f"✅ تم تحديث الحادثة رقم {selected_id} بنجاح وفق محددات الحوكمة المعتمدة.")
                st.rerun()

# =========================================
# التبويبات الأخرى (هياكل الأنظمة المتبقية)
# =========================================
elif choice == "مراجعة الوثائق التشغيلية":
    st.header("📄 سجل تتبع مراجعة الوثائق التشغيلية والفنية")
    df_docs = pd.read_excel(FILES["docs_review"])
    st.dataframe(df_docs, use_container_width=True)
    st.info("نظام عرض وبناء تقارير الوثائق والمستندات الواردة لقطاع الحوكمة.")

elif choice == "وثائق الحوكمة وسياسات NDMO":
    st.header("📜 مستودع وثائق الحوكمة الجيومكانية ومعايير الامتثال الوطنية")
    df_gov = pd.read_excel(FILES["gov_docs"])
    st.dataframe(df_gov, use_container_width=True)
    st.info("نظام حصر سياسات جودة البيانات المفتوحة والميتا داتا بالتوافق مع مكتب إدارة البيانات DMO.")

elif choice == "مخاطر عدم الامتثال الفني":
    st.header("⚠️ سجل تتبع مخاطر عدم الامتثال للمواصفات الجيومكانية")
    df_risks = pd.read_excel(FILES["risks"])
    st.dataframe(df_risks, use_container_width=True)
    st.info("نظام رصد وتحليل التداخلات والتشوهات الحدودية لقطع الأراضي التي تخالف المعايير.")
