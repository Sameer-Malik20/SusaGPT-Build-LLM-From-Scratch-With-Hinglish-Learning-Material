# 📊 NumPy & Pandas Complete Guide
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master NumPy and Pandas

---

## 🧭 Core Concepts (Concept-First)

- NumPy Arrays: Fast numerical computing
- Pandas DataFrames: Tabular data
- Operations: Filtering, aggregation

---

## 1. 🔢 NumPy Basics

```python
import numpy as np

# Create array
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape)  # (5,)

# 2D array
matrix = np.array([[1, 2], [3, 4]])
print(matrix.shape)  # (2, 2)

# Operations
arr * 2  # Multiply
arr.sum()  # Sum
arr.mean()  # Mean

# Slicing
arr[1:3]  # Elements 1 and 2
matrix[0, :]  # First row
```

---

## 2. 🐼 Pandas Basics

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

# Read CSV
df = pd.read_csv('file.csv')

# Select columns
df['name']
df[['name', 'age']]

# Filter
df[df['age'] > 25]

# Group by
df.groupby('city').mean()
```

---

## ✅ Checklist

- [ ] NumPy arrays use kar sakte ho
- [ ] Pandas DataFrame use kar sakte ho
- [ ] Data operations perform kar sakte ho