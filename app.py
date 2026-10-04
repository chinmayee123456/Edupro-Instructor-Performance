import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPro Instructor Performance",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

file_path = "data/EduPro Online Platform.xlsx"

users = pd.read_excel(file_path, sheet_name="Users")
teachers = pd.read_excel(file_path, sheet_name="Teachers")
courses = pd.read_excel(file_path, sheet_name="Courses")
transactions = pd.read_excel(file_path, sheet_name="Transactions")

# ============================================================
# DATA INTEGRATION
# ============================================================

master = (
    transactions
    .merge(courses, on="CourseID", how="left")
    .merge(teachers, on="TeacherID", how="left")
    .merge(users, on="UserID", how="left")
)

# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 EduPro Instructor Performance & Course Quality")

st.markdown(
    "Analysis of instructor performance, course quality, "
    "experience, expertise, and enrollment influence."
)

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

expertise_options = sorted(teachers["Expertise"].dropna().unique())

category_options = sorted(courses["CourseCategory"].dropna().unique())

level_options = sorted(courses["CourseLevel"].dropna().unique())

selected_expertise = st.sidebar.multiselect(
    "Instructor Expertise",
    expertise_options,
    default=expertise_options
)

selected_category = st.sidebar.multiselect(
    "Course Category",
    category_options,
    default=category_options
)

selected_level = st.sidebar.multiselect(
    "Course Level",
    level_options,
    default=level_options
)

rating_range = st.sidebar.slider(
    "Teacher Rating",
    min_value=float(teachers["TeacherRating"].min()),
    max_value=float(teachers["TeacherRating"].max()),
    value=(
        float(teachers["TeacherRating"].min()),
        float(teachers["TeacherRating"].max())
    ),
    step=0.1
)

# ============================================================
# FILTER DATA
# ============================================================

filtered_teachers = teachers[
    (teachers["Expertise"].isin(selected_expertise)) &
    (teachers["TeacherRating"].between(
        rating_range[0],
        rating_range[1]
    ))
].copy()

filtered_courses = courses[
    (courses["CourseCategory"].isin(selected_category)) &
    (courses["CourseLevel"].isin(selected_level))
].copy()

filtered_transactions = transactions[
    transactions["CourseID"].isin(filtered_courses["CourseID"]) &
    transactions["TeacherID"].isin(filtered_teachers["TeacherID"])
].copy()

# ============================================================
# KPI CALCULATIONS
# ============================================================

average_teacher_rating = teachers["TeacherRating"].mean()

average_course_rating = courses["CourseRating"].mean()

rating_std = teachers["TeacherRating"].std()

rating_consistency_index = (
    1 - (rating_std / 5)
) * 100

experience_correlation = teachers[
    ["YearsOfExperience", "TeacherRating"]
].corr().iloc[0, 1]

experience_impact_score = (
    experience_correlation * 100
)

# Instructor enrollment calculation
instructor_enrollments = (
    transactions
    .groupby("TeacherID")
    .size()
    .reset_index(name="EnrollmentCount")
)

instructor_performance = instructor_enrollments.merge(
    teachers,
    on="TeacherID",
    how="left"
)

# Rating tiers
instructor_performance["RatingTier"] = pd.cut(
    instructor_performance["TeacherRating"],
    bins=[0, 3, 4, 5],
    labels=["Low", "Medium", "High"],
    include_lowest=True
)

total_enrollments = instructor_performance[
    "EnrollmentCount"
].sum()

high_rating_enrollments = instructor_performance.loc[
    instructor_performance["RatingTier"] == "High",
    "EnrollmentCount"
].sum()

enrollment_influence_ratio = (
    high_rating_enrollments /
    total_enrollments
) * 100

# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Avg Teacher Rating",
    f"{average_teacher_rating:.2f}"
)

col2.metric(
    "Avg Course Rating",
    f"{average_course_rating:.2f}"
)

col3.metric(
    "Rating Consistency",
    f"{rating_consistency_index:.1f}%"
)

col4.metric(
    "Experience Impact",
    f"{experience_impact_score:.1f}"
)

col5.metric(
    "Enrollment Influence",
    f"{enrollment_influence_ratio:.1f}%"
)

st.divider()

# ============================================================
# INSTRUCTOR LEADERBOARD
# ============================================================

st.subheader("🏆 Top 10 Instructor Leaderboard")

leaderboard = (
    instructor_performance[
        [
            "TeacherName",
            "Expertise",
            "YearsOfExperience",
            "TeacherRating",
            "EnrollmentCount"
        ]
    ]
    .sort_values(
        "TeacherRating",
        ascending=False
    )
    .head(10)
    .reset_index(drop=True)
)

leaderboard.index = leaderboard.index + 1

st.dataframe(
    leaderboard,
    use_container_width=True
)

st.divider()

# ============================================================
# EXPERIENCE VS TEACHER RATING
# ============================================================

st.subheader("📈 Experience vs Teacher Rating")

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.scatterplot(
    data=filtered_teachers,
    x="YearsOfExperience",
    y="TeacherRating",
    s=80,
    ax=ax1
)

# Trendline
if len(filtered_teachers) >= 2:
    x = filtered_teachers["YearsOfExperience"]
    y = filtered_teachers["TeacherRating"]

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    x_line = np.linspace(
        x.min(),
        x.max(),
        100
    )

    ax1.plot(
        x_line,
        p(x_line),
        linestyle="--"
    )

ax1.set_title(
    "Instructor Experience vs Teacher Rating"
)

ax1.set_xlabel("Years of Experience")

ax1.set_ylabel("Teacher Rating")

st.pyplot(fig1)

st.divider()

# ============================================================
# COURSE QUALITY HEATMAP
# ============================================================

st.subheader("🔥 Course Quality by Category and Level")

heatmap_data = pd.pivot_table(
    filtered_courses,
    values="CourseRating",
    index="CourseCategory",
    columns="CourseLevel",
    aggfunc="mean"
)

fig2, ax2 = plt.subplots(
    figsize=(10, 7)
)

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    linewidths=0.5,
    ax=ax2
)

ax2.set_title(
    "Course Rating by Category and Course Level"
)

ax2.set_xlabel("Course Level")

ax2.set_ylabel("Course Category")

st.pyplot(fig2)

st.divider()

# ============================================================
# EXPERTISE PERFORMANCE
# ============================================================

st.subheader("🎓 Instructor Performance by Expertise")

expertise_performance = (
    filtered_teachers
    .groupby("Expertise")["TeacherRating"]
    .agg(["count", "mean"])
    .sort_values("mean", ascending=True)
    .reset_index()
)

fig3, ax3 = plt.subplots(
    figsize=(10, 6)
)

sns.barplot(
    data=expertise_performance,
    x="mean",
    y="Expertise",
    ax=ax3
)

ax3.set_title(
    "Average Teacher Rating by Expertise"
)

ax3.set_xlabel(
    "Average Teacher Rating"
)

ax3.set_ylabel(
    "Instructor Expertise"
)

st.pyplot(fig3)

st.divider()

# ============================================================
# COURSE LEVEL PERFORMANCE
# ============================================================

st.subheader("📚 Course Rating by Course Level")

level_rating = (
    filtered_courses
    .groupby("CourseLevel")["CourseRating"]
    .mean()
    .reset_index()
)

fig4, ax4 = plt.subplots(
    figsize=(8, 5)
)

sns.barplot(
    data=level_rating,
    x="CourseLevel",
    y="CourseRating",
    ax=ax4
)

ax4.set_title(
    "Average Course Rating by Course Level"
)

ax4.set_xlabel("Course Level")

ax4.set_ylabel("Average Course Rating")

st.pyplot(fig4)

st.divider()

# ============================================================
# GENDER VS COURSE LEVEL
# ============================================================

st.subheader("👥 Gender vs Course Level")

course_teacher = (
    transactions[
        ["CourseID", "TeacherID"]
    ]
    .drop_duplicates()
    .merge(
        courses[
            ["CourseID", "CourseLevel", "CourseRating"]
        ],
        on="CourseID",
        how="left"
    )
    .merge(
        teachers[
            ["TeacherID", "Gender"]
        ],
        on="TeacherID",
        how="left"
    )
)

gender_level_rating = (
    course_teacher
    .groupby(
        ["Gender", "CourseLevel"]
    )["CourseRating"]
    .mean()
    .reset_index()
)

fig5, ax5 = plt.subplots(
    figsize=(9, 5)
)

sns.barplot(
    data=gender_level_rating,
    x="CourseLevel",
    y="CourseRating",
    hue="Gender",
    ax=ax5
)

ax5.set_title(
    "Average Course Rating by Gender and Course Level"
)

ax5.set_xlabel("Course Level")

ax5.set_ylabel("Average Course Rating")

st.pyplot(fig5)

st.divider()

# ============================================================
# FOOTER
# ============================================================

st.caption(
    "EduPro Instructor Performance & Course Quality Evaluation | "
    "Data Analysis Project"
)