# app.py
import io
import re
from datetime import datetime, time
from typing import List, Dict, Tuple

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---------- CONFIG ----------
st.set_page_config(page_title="Weekly Schedule Builder", layout="wide")

DAY_ORDER = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DAY_TO_ROW = {d: i for i, d in enumerate(DAY_ORDER)}

# Regex to parse entries like:
# "Sun 08:00-09:15", "Sun/Tue 8:00 AM - 9:15 AM", "Mon/Wed/Thu 13:30-15:00"
TIME_RE = re.compile(
    r"^\s*(?P<days>(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)(?:/(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat))*)\s+"
    r"(?P<start>\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*-\s*(?P<end>\d{1,2}:\d{2}\s*(?:AM|PM)?)\s*$",
    re.IGNORECASE
)

def to_time_obj(tstr: str) -> time:
    """Robust time parser for 'HH:MM' or 'HH:MM AM/PM'."""
    tstr = tstr.strip().upper()
    fmts = ["%H:%M", "%I:%M %p"]
    for f in fmts:
        try:
            return datetime.strptime(tstr, f).time()
        except ValueError:
            continue
    # last resort: try adding AM
    try:
        return datetime.strptime(tstr + " AM", "%I:%M %p").time()
    except Exception:
        pass
    raise ValueError(f"Unrecognized time format: {tstr}")

def parse_timeslots(cell: str) -> List[Dict]:
    """
    Parse Column H text into a list of {day, start, end} dicts.
    Accepts multiple entries separated by ';' or newlines.
    Example cells:
      "Sun/Tue 08:00-09:15"
      "Mon 13:00-14:15; Wed 13:00-14:15"
    """
    if pd.isna(cell) or str(cell).strip() == "":
        return []

    chunks = re.split(r"[;\n]+", str(cell))
    slots = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        m = TIME_RE.match(chunk)
        if not m:
            # try forgiving: remove extra spaces around dash
            chunk2 = re.sub(r"\s*-\s*", "-", chunk)
            m = TIME_RE.match(chunk2)
        if not m:
            # If still not matched, skip this piece but continue
            # (we'll show a warning later)
            continue

        days_str = m.group("days")
        start_str = m.group("start")
        end_str = m.group("end")
        try:
            start_t = to_time_obj(start_str)
            end_t   = to_time_obj(end_str)
        except Exception:
            continue

        for d in days_str.split("/"):
            d = d.title().strip()
            if d in DAY_TO_ROW:
                slots.append({"day": d, "start": start_t, "end": end_t})
    return slots

@st.cache_data(show_spinner=False)
def load_excel(file_bytes: bytes) -> pd.DataFrame:
    """
    Load either legacy .xls (requires xlrd==1.2.0) or .xlsx (openpyxl) into a DataFrame.
    """
    bio = io.BytesIO(file_bytes)
    try:
        # Try auto engine
        df = pd.read_excel(bio)
        return df
    except Exception:
        # Retry with xlrd (for old .xls)
        bio.seek(0)
        df = pd.read_excel(bio, engine="xlrd")
        return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make sure we have the columns we need with friendly names.
    A: code, B: name, H: datetime text, J: status, K: teacher, L: students
    """
    # If columns are unnamed, use letter-based fallback by position
    cols = list(df.columns)

    # Try to map by common names first (case-insensitive)
    lc = {str(c).strip().lower(): c for c in cols}

    def pick(*aliases, fallback_index=None):
        for a in aliases:
            if a in lc:
                return lc[a]
        if fallback_index is not None and fallback_index < len(cols):
            return cols[fallback_index]
        return None

    col_code    = pick("code", "subject code", "course code", fallback_index=0)
    col_name    = pick("name", "subject name", "course name", fallback_index=1)
    col_time    = pick("time", "date and time", "date & time", "datetime", fallback_index=7)
    col_status  = pick("status", fallback_index=9)
    col_teacher = pick("teacher", "instructor", fallback_index=10)
    col_students= pick("students", "enrolled", "no. of students", "number of students", fallback_index=11)

    need = [col_code, col_name, col_time, col_status, col_teacher, col_students]
    if any(c is None for c in need):
        st.error("Could not detect expected columns. Please make sure your sheet matches the described format.")
        st.stop()

    out = df.rename(columns={
        col_code: "Code",
        col_name: "Name",
        col_time: "Time",
        col_status: "Status",
        col_teacher: "Teacher",
        col_students: "Students",
    }).copy()

    # Keep only the columns we need (but don’t break if extras exist)
    return out[["Code", "Name", "Teacher", "Students", "Status", "Time"]]

def timetable_plot(rows: List[Dict], time_min: time = time(8, 0), time_max: time = time(21, 0)):
    """
    Draw a weekly grid and place colored blocks for each chosen subject meeting.
    rows: list of dicts with keys:
      'Code', 'Name', 'Teacher', 'Students', 'Status', 'TimeSlots' (list[{day,start,end}]), 'Color'
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Axes: x=time, y=days
    # Convert time to hours since midnight for simple numeric axis
    def t2h(t: time) -> float:
        return t.hour + t.minute / 60.0

    xmin = t2h(time_min)
    xmax = t2h(time_max)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.5, len(DAY_ORDER) - 0.5)
    ax.set_yticks(range(len(DAY_ORDER)))
    ax.set_yticklabels(DAY_ORDER)

    # Light grid for hours
    for h in range(int(xmin), int(xmax) + 1):
        ax.axvline(h, linewidth=0.5, alpha=0.3)

    # Horizontal lines for each day row
    for y in range(len(DAY_ORDER)):
        ax.axhline(y + 0.5, linewidth=0.5, alpha=0.3)

    # Plot blocks
    for r in rows:
        for slot in r["TimeSlots"]:
            y = DAY_TO_ROW[slot["day"]]
            x0 = t2h(slot["start"])
            x1 = t2h(slot["end"])
            width = max(0.2, x1 - x0)

            rect = Rectangle((x0, y - 0.4), width, 0.8, alpha=0.8)
            rect.set_facecolor(r["Color"])
            rect.set_edgecolor("black")
            ax.add_patch(rect)

            # Label inside the block
            label = f"{r['Code']}\n{slot['start'].strftime('%H:%M')}-{slot['end'].strftime('%H:%M')}"
            ax.text(x0 + 0.02, y, label, va="center", ha="left", fontsize=9)

    ax.set_xlabel("Time")
    ax.set_ylabel("Day")
    ax.set_title("Weekly Schedule")

    # Clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig, clear_figure=True)

def make_palette(n: int) -> List:
    """
    Generate n distinct colors using matplotlib's default cycle repeatedly.
    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key().get('color', ['#1f77b4'])
    if n <= len(colors):
        return colors[:n]
    reps = (n + len(colors) - 1) // len(colors)
    return (colors * reps)[:n]

# ---------- UI ----------
st.title("Student Weekly Schedule")

st.caption("Upload your **Courses Schedule.xls** (or .xlsx), choose subjects, and view your weekly timetable.")

uploaded = st.file_uploader("Upload: Courses Schedule.xls", type=["xls", "xlsx"])

if not uploaded:
    st.info("Please upload your file to continue.")
    st.stop()

# Load data
try:
    df_raw = load_excel(uploaded.read())
except Exception as e:
    st.error(
        "Failed to read the Excel file. If this is an old .xls, ensure `xlrd==1.2.0` is installed "
        "or re-save the sheet as .xlsx and try again."
    )
    st.stop()

df = normalize_columns(df_raw)

# Create a search/multi-select over Code and Name (combined label)
df["Label"] = df["Code"].astype(str).str.strip() + " — " + df["Name"].astype(str).str.strip()

# Optional quick filters
with st.expander("Filters (optional)"):
    status_filter = st.multiselect("Status", sorted(df["Status"].dropna().astype(str).unique().tolist()))
    teacher_filter = st.multiselect("Teacher", sorted(df["Teacher"].dropna().astype(str).unique().tolist()))
    if status_filter:
        df = df[df["Status"].astype(str).isin(status_filter)]
    if teacher_filter:
        df = df[df["Teacher"].astype(str).isin(teacher_filter)]

# Subject chooser
choices = st.multiselect(
    "Search & select subjects/sections",
    options=df["Label"].tolist(),
    placeholder="Type code or name…",
)

if not choices:
    st.info("Select at least one subject to view its details and schedule.")
    st.stop()

sel = df[df["Label"].isin(choices)].copy()

# Parse timeslots for each chosen row
sel["TimeSlots"] = sel["Time"].apply(parse_timeslots)

# Warning if something couldn't be parsed
bad = sel[sel["TimeSlots"].apply(len) == 0]
if not bad.empty:
    with st.warning("Some selected items have no recognizable time/day in Column H. They won't appear on the timetable."):
        st.dataframe(bad[["Code", "Name", "Time"]], use_container_width=True)

# Show details table
st.subheader("Selected Subjects")
st.dataframe(
    sel[["Code", "Name", "Teacher", "Students", "Status", "Time"]],
    use_container_width=True
)

# Build plotting rows
valid = sel[sel["TimeSlots"].apply(len) > 0]
if valid.empty:
    st.stop()

# Color per Code
codes = valid["Code"].astype(str).tolist()
palette = make_palette(len(codes))
code_to_color = {c: palette[i] for i, c in enumerate(codes)}

plot_rows = []
for _, r in valid.iterrows():
    plot_rows.append({
        "Code": r["Code"],
        "Name": r["Name"],
        "Teacher": r["Teacher"],
        "Students": r["Students"],
        "Status": r["Status"],
        "TimeSlots": r["TimeSlots"],
        "Color": code_to_color[str(r["Code"])]
    })

# Compute reasonable time bounds from data (with padding)
all_starts = []
all_ends = []
for pr in plot_rows:
    for s in pr["TimeSlots"]:
        all_starts.append(s["start"])
        all_ends.append(s["end"])

def min_time(ts: List[time]) -> time:
    m = min(ts)
    # pad to earlier hour
    return time(hour=max(0, m.hour - 1), minute=0)

def max_time(ts: List[time]) -> time:
    m = max(ts)
    # pad to next hour
    return time(hour=min(23, m.hour + 1), minute=0)

tmin = min_time(all_starts) if all_starts else time(8, 0)
tmax = max_time(all_ends) if all_ends else time(21, 0)

st.subheader("Weekly Timetable")
timetable_plot(plot_rows, tmin, tmax)

st.caption("Tip: If your Column H format differs (e.g., multiple lines or semicolons), this app tries to parse them. Supported day abbreviations: Sun, Mon, Tue, Wed, Thu, Fri, Sat.")
