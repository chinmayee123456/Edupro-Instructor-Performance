# 📊 EduPro Instructor Performance & Course Quality

A data analysis and Streamlit dashboard project that evaluates instructor performance and course quality on the EduPro online learning platform.

The project analyzes instructor experience, teacher ratings, expertise, course ratings, course levels, gender-based patterns, and enrollment influence to identify factors associated with instructor and course performance.

---

## 🎯 Project Objectives

The main objectives of this project are to:

- Analyze instructor profiles and performance.
- Examine the relationship between instructor experience and teacher ratings.
- Evaluate course quality across different categories and levels.
- Compare course ratings by instructor gender and course level.
- Analyze instructor performance across different expertise areas.
- Examine enrollment volume across instructor rating tiers.
- Identify high-performing instructors.
- Develop an interactive Streamlit dashboard for exploring the results.

---

## 📂 Dataset

The project uses the **EduPro Online Platform** dataset stored in an Excel workbook.

The workbook contains four datasets:

### 1. Users

Contains learner information.

Important columns:

- `UserID`
- `UserName`
- `Age`
- `Gender`
- `Email`

### 2. Teachers

Contains instructor information.

Important columns:

- `TeacherID`
- `TeacherName`
- `Age`
- `Gender`
- `Expertise`
- `YearsOfExperience`
- `TeacherRating`

### 3. Courses

Contains course information.

Important columns:

- `CourseID`
- `CourseName`
- `CourseCategory`
- `CourseType`
- `CourseLevel`
- `CoursePrice`
- `CourseDuration`
- `CourseRating`

### 4. Transactions

Contains course enrollment/transaction information.

Important columns:

- `TransactionID`
- `UserID`
- `CourseID`
- `TransactionDate`
- `Amount`
- `PaymentMethod`
- `TeacherID`

---

## 🔗 Data Integration

The datasets were integrated using:

- `UserID`
- `CourseID`
- `TeacherID`

The integrated dataset contains transaction, course, instructor, and user information.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Streamlit
- Jupyter Notebook
- Excel

---

## 📊 Analysis Performed

### Instructor Profile Analysis

The project analyzes:

- Number of instructors
- Instructor age
- Years of experience
- Teacher ratings
- Gender distribution
- Expertise distribution

### Experience vs Performance

The relationship between:

**Years of Experience → Teacher Rating**

was analyzed using Pearson correlation.

The observed correlation was approximately:

**0.598**

This indicates a moderate positive relationship between instructor experience and teacher rating.

---

### Instructor Enrollment Analysis

Instructor enrollment volume was calculated using transaction records.

The analysis identifies instructors with the highest enrollment volumes and compares enrollment activity with teacher rating.

A strong concentration of enrollments was observed among highly rated instructors.

---

### Instructor Rating Tiers

Instructors were grouped into three rating tiers:

- Low: ≤ 3
- Medium: >3 to ≤4
- High: >4

High-rated instructors accounted for approximately:

**68.2% of total enrollments**

This metric is used as the project's **Enrollment Influence Ratio**.

---

### Course Quality Analysis

Course quality was evaluated using course ratings.

The analysis includes:

- Average course rating
- Course rating by category
- Course rating by course level
- Category × course-level comparison

The category × course-level analysis was visualized using a heatmap.

---

### Gender vs Course Level

Average course ratings were compared across:

- Female-associated instructors
- Male-associated instructors

and across:

- Beginner
- Intermediate
- Advanced

course levels.

---

### Expertise Performance

Instructor ratings were compared across different expertise areas.

The analysis helps identify expertise areas with relatively higher and lower average instructor ratings.

---

## 📌 Key Performance Indicators

The Streamlit dashboard includes five project KPIs.

### Average Teacher Rating

The mean rating of all instructors.

### Average Course Rating

The mean rating of all courses.

### Rating Consistency Index

A project-defined measure based on the standard deviation of teacher ratings.

Formula:

```text
Rating Consistency Index =
(1 - Teacher Rating Standard Deviation / 5) × 100