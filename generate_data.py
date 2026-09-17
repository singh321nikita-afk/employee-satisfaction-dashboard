"""
Creates employee_data.csv with 120 employee records for the dashboard.
Run once:  python generate_data.py
"""

import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

FIRST = ["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Ananya", "Vikram", "Sneha",
         "Arjun", "Priya", "Nikhil", "Tara", "Rahul", "Ishita", "Karan", "Neha",
         "Aditya", "Sanya", "Manav", "Ritika", "Siddharth", "Pooja", "Varun", "Kavya"]
LAST = ["Sharma", "Patel", "Iyer", "Nair", "Desai", "Joshi", "Mehta", "Rao",
        "Kulkarni", "Banerjee", "Gupta", "Reddy", "Chopra", "Bhatt", "Sinha"]

DEPARTMENTS = {
    "Human Resources": 14, "Finance": 16, "Marketing": 18, "Operations": 20,
    "Information Technology": 24, "Sales": 18, "Customer Support": 10,
}

DESIGNATIONS = ["Executive", "Senior Executive", "Associate", "Team Lead", "Manager"]

POSITIVE = [
    "Managers are approachable and my work gets noticed.",
    "Flexible hours make a real difference to my week.",
    "The team culture here is genuinely supportive.",
    "Good learning opportunities and clear targets.",
    "",
]
NEUTRAL = [
    "Work is fine, but growth feels slow.",
    "No major complaints, though communication could be better.",
    "Appraisals are regular but feedback stays vague.",
    "",
]
NEGATIVE = [
    "Workload is unrealistic and overtime has become normal.",
    "Recognition rarely reaches people outside the core team.",
    "Very little clarity on promotions.",
    "High attrition in the team has increased pressure on the rest of us.",
]


def comment(rating):
    if rating >= 4:
        return random.choice(POSITIVE)
    if rating == 3:
        return random.choice(NEUTRAL)
    return random.choice(NEGATIVE)


rows = []
emp = 1
base = datetime.now() - timedelta(days=45)

for dept, count in DEPARTMENTS.items():
    # a slight per-department tilt, so the charts show real variation
    tilt = {"Customer Support": -0.6, "Sales": -0.3, "Operations": -0.2,
            "Human Resources": 0.4, "Finance": 0.1}.get(dept, 0)
    for _ in range(count):
        weights = [4, 9, 25, 38, 24]
        shift = int(tilt * 10)
        weights = [max(1, w + (shift if i >= 3 else -shift)) for i, w in enumerate(weights)]
        rating = random.choices([1, 2, 3, 4, 5], weights=weights)[0]

        def near(r):
            return max(1, min(5, r + random.choice([-1, 0, 0, 1])))

        rows.append({
            "EmpID": f"EMP{emp:03d}",
            "Name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "Department": dept,
            "Designation": random.choice(DESIGNATIONS),
            "Experience": random.randint(1, 18),
            "WorkLifeBalance": near(rating),
            "Recognition": near(rating),
            "CareerGrowth": near(rating),
            "Rating": rating,
            "Feedback": comment(rating),
            "Date": (base + timedelta(days=random.randint(0, 45))).strftime("%Y-%m-%d"),
            "Source": "HR Survey",
        })
        emp += 1

df = pd.DataFrame(rows)
df.to_csv("employee_data.csv", index=False)
print(f"employee_data.csv created with {len(df)} employees "
      f"across {df['Department'].nunique()} departments.")
