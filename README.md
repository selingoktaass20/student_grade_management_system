# Student Grade Management System

A Python and SQLite console application for managing student records, course grades, weighted averages, and basic academic statistics.

## Features
- **Student Management (CRUD):** Add new students (with duplicate student ID validation), list all enrolled students, search by student ID, and delete student records along with their associated grades.
- **Grade Recording & Validation:** Assign midterm (`vize`) and final (`final`) grades for predefined courses (`Python`, `SQL`, `Matematik`, `Algoritma`) with 0–100 range validation.
- **Automated Calculations:** Computes course averages using weighted scoring (**40% Midterm + 60% Final**) and determines pass/fail status (`>= 50`).
- **Overall GPA & Status:** Calculates a student's overall average across all recorded courses and displays their general academic standing.
- **Department & System Statistics:** Lists unique departments and reports total students, total grade entries, and total departments in the database.

## Tech Stack & Concepts
- **Python 3** (Object-Oriented Programming with the `Ogrenci` class, tuples, sets, modular functions)
- **SQLite (`sqlite3`)** — Built-in relational database automatically initialized as `ogrenci_sistemi.db` with `ogrenciler` and `notlar` tables.

## Sample Menu
```text
=================================
      ÖĞRENCİ NOT SİSTEMİ
=================================
1 - Öğrenci Ekle
2 - Öğrencileri Listele
3 - Öğrenci Ara
4 - Not Ekle
5 - Öğrencinin Notlarını Göster
6 - Genel Ortalama Hesapla
7 - Öğrenci Sil
8 - Bölümleri Göster
9 - İstatistikleri Göster
0 - Çıkış
=================================
```

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/selingoktaass20/student_grade_management_system.git
   ```
2. Navigate to the project directory and run the script (no external packages required):
   ```bash
   cd student_grade_management_system
   python student_grade_system.py
   ```
