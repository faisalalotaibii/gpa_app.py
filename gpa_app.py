import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GPA Calculator",
    layout="wide",  # 🟢 This is the key setting
    initial_sidebar_state="collapsed"
)


# --- Class Definition ---
class GPACalculator:
    def __init__(self):
        self.subjects_data = [
            {"COURSE_CODE": "ENGL110", "COURSE_NAME": "Technical Writing for Engineering", "PREREQ_1": "",
             "PREREQ_2": "", "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "MATH100", "COURSE_NAME": "Calculus I", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "PHYS100", "COURSE_NAME": "Physics I", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CHEM100", "COURSE_NAME": "Chemistry I", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "MECH120", "COURSE_NAME": "Engineering Drawings", "PREREQ_1": "", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 1},
            {"COURSE_CODE": "ENGI100", "COURSE_NAME": "Introduction to Engineering", "PREREQ_1": "", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 1},
            {"COURSE_CODE": "CHEM109", "COURSE_NAME": "Chemistry I Lab", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "CHEM100", "CRD_HRS": 1},
            {"COURSE_CODE": "MATH101", "COURSE_NAME": "Calculus II", "PREREQ_1": "MATH100", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "PHYS101", "COURSE_NAME": "Physics II", "PREREQ_1": "PHYS100", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL100", "COURSE_NAME": "Statics", "PREREQ_1": "MATH100", "PREREQ_2": "PHYS100",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "AIEN120", "COURSE_NAME": "Computer Programming", "PREREQ_1": "MATH100", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "AIEN129", "COURSE_NAME": "Computer Programming Lab", "PREREQ_1": "", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "AIEN120", "CRD_HRS": 1},
            {"COURSE_CODE": "MECH100", "COURSE_NAME": "Workshop I", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "", "CRD_HRS": 1},
            {"COURSE_CODE": "PHYS109", "COURSE_NAME": "Physics Lab", "PREREQ_1": "PHYS100", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "PHYS101", "CRD_HRS": 1},
            {"COURSE_CODE": "CIVL200", "COURSE_NAME": "Surveying", "PREREQ_1": "MECH120", "PREREQ_2": "MATH101",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL210", "COURSE_NAME": "Strength of Materials", "PREREQ_1": "CIVL100", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL211", "COURSE_NAME": "Civil Engineering Materials", "PREREQ_1": "CHEM100",
             "PREREQ_2": "CIVL100", "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL250", "COURSE_NAME": "Hydraulics", "PREREQ_1": "MATH101", "PREREQ_2": "CIVL100",
             "PREREQ_3": "PHYS101", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL209", "COURSE_NAME": "Surveying Lab", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "CIVL200", "CRD_HRS": 1},
            {"COURSE_CODE": "CIVL259", "COURSE_NAME": "Hydraulics Lab", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "CIVL250", "CRD_HRS": 1},
            {"COURSE_CODE": "CIVL212", "COURSE_NAME": "Concrete Structures", "PREREQ_1": "CIVL210", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL230", "COURSE_NAME": "Highway and Pavement Engineering", "PREREQ_1": "CIVL200",
             "PREREQ_2": "CIVL211", "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL240", "COURSE_NAME": "Geotechnical Engineering", "PREREQ_1": "CIVL210",
             "PREREQ_2": "CIVL250", "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "CIVL249", "COURSE_NAME": "Geotechnical Engineering Lab", "PREREQ_1": "",
             "PREREQ_2": "CIVL211", "PREREQ_3": "", "CO_REQ": "CIVL240", "CRD_HRS": 1},
            {"COURSE_CODE": "CIVL290", "COURSE_NAME": "Project 1 (PBL)", "PREREQ_1": "CIVL211", "PREREQ_2": "",
             "PREREQ_3": "", "CO_REQ": "", "CRD_HRS": 3},
            {"COURSE_CODE": "ELE", "COURSE_NAME": "University Elective", "PREREQ_1": "", "PREREQ_2": "", "PREREQ_3": "",
             "CO_REQ": "", "CRD_HRS": 3}
        ]

        self.grade_to_gpa = {
            "A": 4.00, "A-": 3.67, "B+": 3.33, "B": 3.00,
            "B-": 2.67, "C+": 2.33, "C": 2.00, "C-": 1.67,
            "D+": 1.33, "D": 1.00, "F": 0.00, "I": 0.00, "": 0.00
        }

        self.df_subjects = pd.DataFrame(self.subjects_data)
        self.student_name = ""
        self.student_id = ""
        self.final_gpa = 0.0
        self.total_subject_effort = 0
        self.total_adjusted_load = 0

        for i in range(1, 6):
            self.df_subjects[f"Attempt{i}"] = ""

        self.df_subjects["REGISTRATION_STATUS"] = "Unknown"

    def load_csv_data(self, uploaded_file):
        try:
            df_info = pd.read_csv(uploaded_file, nrows=2, header=None)
            self.student_name = df_info.iat[1, 0]
            self.student_id = df_info.iat[1, 2]

            uploaded_file.seek(0)
            df_transcript = pd.read_csv(uploaded_file, skiprows=5)
            df_transcript.columns = df_transcript.columns.str.strip()
            df_transcript.iloc[:, 8] = df_transcript.iloc[:, 8].fillna("00").replace(r"^\s*$", "00", regex=True)

            df_subset = df_transcript.iloc[:, [3, 8]]
            df_subset.columns = ["COURSE_CODE", "COMMENT"]
            df_subset = df_subset.dropna(subset=["COURSE_CODE"])

            course_comments = {}
            for _, row in df_subset.iterrows():
                code = row["COURSE_CODE"].strip()
                comment = row["COMMENT"].strip()
                course_comments.setdefault(code, []).append(comment)

            for i in range(1, 6):
                self.df_subjects[f"Attempt{i}"] = ""

            for idx, row in self.df_subjects.iterrows():
                code = row["COURSE_CODE"]
                attempts = course_comments.get(code, [])
                for i in range(min(5, len(attempts))):
                    grade = attempts[i] if attempts[i] != "00" else ""
                    self.df_subjects.at[idx, f"Attempt{i + 1}"] = grade

            self.calculate_gpa()
            return True
        except Exception as e:
            st.error(f"Failed to load CSV file: {str(e)}")
            return False

    def calculate_gpa(self):
        for i in range(1, 6):
            self.df_subjects[f"Attempt{i}_GPA"] = self.df_subjects[f"Attempt{i}"].str.upper().map(
                self.grade_to_gpa).fillna(0)

        self.df_subjects["ADJUSTED_LOAD"] = self.df_subjects.apply(self.compute_adjusted_load, axis=1)
        self.df_subjects["SUBJECT_EFFORT"] = self.df_subjects.apply(self.compute_subject_effort, axis=1)

        self.total_subject_effort = self.df_subjects["SUBJECT_EFFORT"].sum()
        self.total_adjusted_load = self.df_subjects["ADJUSTED_LOAD"].sum()

        self.final_gpa = self.total_subject_effort / self.total_adjusted_load if self.total_adjusted_load > 0 else 0.0
        self.update_all_registration_status()

    def compute_adjusted_load(self, row):
        attempts = [row.get(f"Attempt{i}", "").strip() for i in range(1, 6)]
        valid_attempts = [a for a in attempts if a]
        crd = row["CRD_HRS"]
        if not valid_attempts:
            return 0
        return crd * (1 + (len(valid_attempts) - 2)) if len(valid_attempts) > 1 else crd

    def compute_subject_effort(self, row):
        crd = row["CRD_HRS"]
        gpas = [row.get(f"Attempt{i}_GPA", 0) for i in range(1, 6)]
        grades = [row.get(f"Attempt{i}", "").strip() for i in range(1, 6)]
        valid_attempts = [g for g in grades if g]
        total_effort = 0
        if len(valid_attempts) == 1:
            total_effort = crd * gpas[0]
        elif len(valid_attempts) > 1:
            for gpa_val in gpas[1:]:
                if gpa_val > 0:
                    total_effort += crd * gpa_val
        return total_effort

    def get_most_recent_gpa(self, row):
        for i in reversed(range(1, 6)):
            grade = str(row.get(f"Attempt{i}", "")).strip()
            if grade and grade != "" and grade in self.grade_to_gpa:
                return self.grade_to_gpa[grade]
        return None

    def update_all_registration_status(self):
        subject_dict = {row["COURSE_CODE"]: row for _, row in self.df_subjects.iterrows()}
        for idx, row in self.df_subjects.iterrows():
            self.df_subjects.at[idx, "REGISTRATION_STATUS"] = self.get_registration_status(row, subject_dict)

    def get_registration_status(self, row, subject_dict):
        recent_gpa = self.get_most_recent_gpa(row)
        if recent_gpa is not None and recent_gpa >= 1.00:
            return "✅ Passed"

        has_attempts = any(row.get(f"Attempt{i}", "").strip() for i in range(1, 6))
        prereqs = [p.strip() for p in [row.get("PREREQ_1", ""), row.get("PREREQ_2", ""), row.get("PREREQ_3", "")] if
                   p.strip()]

        if prereqs:
            for prereq_code in prereqs:
                prereq_row = subject_dict.get(prereq_code)
                if prereq_row is None:
                    continue
                prereq_gpa = self.get_most_recent_gpa(prereq_row)
                if prereq_gpa is None or prereq_gpa < 1.00:
                    return f"❌ Cannot Register (Prereq: {prereq_code})"

        if has_attempts:
            return "❌ Failed (Can Retake)"

        return "🟡 Can Register"

    def update_from_editor_data(self, edited_df):
        """Update the internal DataFrame with data from the editor"""
        attempt_cols = ['Attempt1', 'Attempt2', 'Attempt3', 'Attempt4', 'Attempt5']

        changes_made = False
        for i, row in edited_df.iterrows():
            for col in attempt_cols:
                new_val = str(row[col]).strip().upper() if pd.notna(row[col]) else ""
                old_val = str(self.df_subjects.iloc[i][col]).strip() if pd.notna(
                    self.df_subjects.iloc[i][col]) else ""
                if new_val != old_val:
                    self.df_subjects.iloc[i, self.df_subjects.columns.get_loc(col)] = new_val
                    changes_made = True

        if changes_made:
            self.calculate_gpa()

        return changes_made


# Initialize session state
if 'calculator' not in st.session_state:
    st.session_state.calculator = GPACalculator()
if 'last_editor_state' not in st.session_state:
    st.session_state.last_editor_state = None

calc = st.session_state.calculator

st.title("صبر جميل والله المستعان... ")

# --- Top Controls (No Sidebar) ---
st.markdown("### Load Transcript")
top_col1, top_col2 = st.columns([2, 8])

with top_col1:
    uploaded_file = st.file_uploader("Browse Transcript CSV", type="csv", label_visibility="collapsed")
    if uploaded_file is not None:
        if calc.load_csv_data(uploaded_file):
            st.success("Transcript loaded successfully!")
            st.session_state.last_editor_state = None
        else:
            st.error("Failed to process CSV.")

# --- Tabs ---
tab1, tab2 = st.tabs(["Grade Editor 📝", "Results Summary 📊"])

with tab1:
    st.header("Grade Editor")

    if not calc.df_subjects.empty:
        st.caption("Edit grades in the 'Attempt' columns. Changes are applied automatically.")

        # Create a copy for editing that includes the current data
        calc.update_all_registration_status()
        editor_df = calc.df_subjects[[
            'COURSE_CODE', 'COURSE_NAME', 'CRD_HRS',
            'Attempt1', 'Attempt2', 'Attempt3', 'Attempt4', 'Attempt5',
            'REGISTRATION_STATUS'
        ]].copy()

        # Use st.data_editor with better state management
        edited_df = st.data_editor(
            editor_df,
            key="grade_editor",
            disabled=['COURSE_CODE', 'COURSE_NAME', 'CRD_HRS', 'REGISTRATION_STATUS'],
            use_container_width=True,
            hide_index=True,
            height=len(editor_df) * 35 + 60,  # Dynamically scale based on number of rows
            on_change=lambda: st.session_state.update({'editor_changed': True})
        )

        # Check if the editor data has changed and update accordingly
        if 'editor_changed' in st.session_state and st.session_state.editor_changed:
            if calc.update_from_editor_data(edited_df):
                st.success("✅ Grades updated and GPA recalculated!")
            st.session_state.editor_changed = False

        # Display current metrics
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Current GPA", f"{calc.final_gpa:.4f}")
        with col2:
            st.metric("Total Courses", len(calc.df_subjects))
        with col3:
            # Manual refresh button as backup
            if st.button("🔄 Force Refresh", key="force_refresh"):
                if calc.update_from_editor_data(edited_df):
                    st.success("✅ Forced refresh completed!")
                else:
                    st.info("No changes detected.")
                st.rerun()

        # Status summary
        st.subheader("Registration Status Summary")
        status_counts = calc.df_subjects["REGISTRATION_STATUS"].value_counts()
        cols = st.columns(len(status_counts))
        for i, (status, count) in enumerate(status_counts.items()):
            with cols[i]:
                st.metric(status, count)

    else:
        st.write("Load data to see and edit grades.")

with tab2:
    st.header("Results Summary")
    if calc.student_name:
        # Student info
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Student:** {calc.student_name}")
            st.write(f"**Student ID:** {calc.student_id}")
        with col2:
            st.metric("Overall GPA", f"{calc.final_gpa:.4f}")
            st.write(f"**Total Subject Effort:** {calc.total_subject_effort:.2f}")
            st.write(f"**Total Adjusted Load:** {calc.total_adjusted_load:.2f}")

        st.markdown("---")

        # Registration status summary
        st.subheader("Registration Status Summary")
        status_counts = calc.df_subjects["REGISTRATION_STATUS"].value_counts().to_dict()
        cols = st.columns(4)
        col_idx = 0
        for status, count in status_counts.items():
            with cols[col_idx % 4]:
                st.metric(status, count)
            col_idx += 1

        st.markdown("---")

        # Full results table - this will now show updated data
        st.subheader("Detailed Course Results")
        summary_df = calc.df_subjects[[
            "COURSE_CODE", "COURSE_NAME", "CRD_HRS",
            "Attempt1", "Attempt2", "Attempt3", "Attempt4", "Attempt5",
            "ADJUSTED_LOAD", "SUBJECT_EFFORT", "REGISTRATION_STATUS"
        ]].copy()

        st.dataframe(summary_df, use_container_width=True, height=600)

        st.markdown("---")
        st.subheader("GPA Calculation Explanation")
        with st.expander("Click to see calculation details"):
            st.markdown("""
            **GPA = Total Subject Effort ÷ Total Adjusted Load**

            **Adjusted Load Calculation:**
            - If 0 or 1 attempt with a grade: Credit Hours
            - If >1 attempt with grades: Credit Hours × (1 + (Number of Graded Attempts - 2))

            **Subject Effort Calculation:**
            - If only 1 attempt: Credit Hours × Attempt1 GPA
            - If >1 attempt: Sum of (Credit Hours × Attempt GPA) for attempts *after* the first one that has a grade

            **Registration Status:**
            - ✅ Passed: Most recent grade GPA ≥ 1.00
            - ❌ Cannot Register: Prerequisites not met
            - ❌ Failed (Can Retake): Has attempts but recent GPA < 1.00
            - 🟡 Can Register: No attempts, prerequisites met
            """)
    else:
        st.write("Load data to see the results summary.")

# Add a footer with current calculation details
if calc.student_name:
    st.markdown("---")
    st.caption(
        f"Last updated: GPA={calc.final_gpa:.4f}, Total Effort={calc.total_subject_effort:.2f}, Total Load={calc.total_adjusted_load:.2f}")