# 🐍 Python for AI: Deep Dive Guide
> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Python for AI & ML

---

## 📋 Is Guide Se Kya Seekhoge

| Section | Content | Importance |
|---------|---------|------------|
| 1. Python Advanced Recap | Lists, Dicts, OOP in AI Context | ⭐⭐⭐⭐ |
| 2. NumPy Mastering | Arrays, Broadcasting, Matrix Math | ⭐⭐⭐⭐⭐ |
| 3. Pandas for Data Science | Cleaning, Grouping, Advanced Stats | ⭐⭐⭐⭐ |
| 4. PyTorch Tensors Depth | GPU, Autograd, NumPy Bridge | ⭐⭐⭐⭐⭐ |
| 5. Async & FastAPI | Serving AI Models with High performance | ⭐⭐⭐⭐ |
| 6. Mega Project | Neural Network from Scratch with NumPy | ⭐⭐⭐⭐⭐ |

---

## 1. 🧠 Python Advanced Recap (AI Edition)

AI development mein normal coding se thoda hatkar kaam hota hai. Yahan **Efficiency** aur **Clean Code** sabse upar hai.

### A. List Comprehensions & Generator expressions
Jab millions of data points process karne hon, toh slow loops ki jagah optimized syntax use karein.

```python
# Normal Loop (Slow)
squares = []
for i in range(1000):
    squares.append(i**2)

# List Comprehension (Fast & Clean)
squares = [i**2 for i in range(1000)]

# Generator Expression (Memory Efficient)
# Ye tab use karein jab data bahut bada ho aur memory bachani ho
squares_gen = (i**2 for i in range(1000000))
```

### B. OOP for AI Models
PyTorch aur TensorFlow hamesha Classes use karte hain. `nn.Module` ko samajhne ke liye OOP clear hona chahiye.

```python
class AIModel:
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    def predict(self, data):
        raise NotImplementedError("Subclasses must implement this!")

class SusaGPT(AIModel):
    def __init__(self, weights):
        super().__init__("SusaGPT", "v1.0")
        self.weights = weights
    
    def predict(self, data):
        return f"Predicting {data} using weights {self.weights}"

gpt = SusaGPT(0.95)
print(gpt.predict("Hello AI"))
```

---

## 2. 🔢 NumPy: The Backbone of AI

NumPy (Numerical Python) matrix operations ke liye gold standard hai. Iski speed C-level optimization se aati hai.

### A. Arrays & Shapes
AI mein hum hamesha dimensions (D) ki baat karte hain.
- **1D:** Vector
- **2D:** Matrix
- **3D+:** Tensor

```python
import numpy as np

# Create Multi-dimensional array
arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

print(f"Shape: {arr.shape}") # (2, 3)
print(f"Dimensions: {arr.ndim}") # 2
print(f"Total Elements: {arr.size}") # 6
```

### B. Broadcasting — Magical Feature
Broadcasting allow karta hai different shapes ke arrays par operations perform karna without copying data.

```python
# Scenario: Har image pixel ko normalize karna
pixels = np.array([[10, 20, 30], [40, 50, 60]]) # Shape (2, 3)
scaler = np.array([2, 5, 10]) # Shape (3,)

# Scalar broadcasting automatically duplicate ho jata hai dimension match karne ke liye
normalized = pixels / scaler 
# Result: [[5, 4, 3], [20, 10, 6]]
```

### C. Matrix Multiplication (Dot Product)
Neural networks ke forward pass mein sirf `@` (dot product) hota hai.

```python
A = np.random.rand(3, 2) # 3 inputs, 2 hidden neurons
B = np.random.rand(2, 1) # 2 hidden, 1 output

C = A @ B  # Dot product: Shape (3, 1)
```

---

## 3. 🐼 Pandas: Data Wrangling Master

Data clean nahi toh model bekar. Pandas CSV load karne aur structure banane mein kaam aata hai.

```python
import pandas as pd

# Load Data
# df = pd.read_csv("dataset.csv")

# Create Dummy Data
data = {
    'Epoch': [1, 2, 3, 4, 1, 2, 3, 4],
    'Model': ['GPT', 'GPT', 'GPT', 'GPT', 'BERT', 'BERT', 'BERT', 'BERT'],
    'Loss': [0.5, 0.4, 0.3, 0.2, 0.8, 0.7, 0.6, 0.5]
}
df = pd.DataFrame(data)

# Advanced Filtering
best_runs = df[df['Loss'] < 0.4]

# Grouping & Aggregation
summary = df.groupby('Model')['Loss'].mean()
print(summary)
```

---

## 4. 🔥 PyTorch Tensors Depth

NumPy arrays aur Tensors mein sabse bada fark hai: **GPU support aur Autograd.**

### A. CPU vs GPU
```python
import torch

t = torch.tensor([1, 2, 3])

if torch.cuda.is_available():
    t = t.to('cuda') # GPU pe bhej diya
    print("Running on GPU ⚡")
```

### B. Autograd — Automatic Differentiation
Backpropagation calculate karne ke liye PyTorch gradient track karta hai.

```python
x = torch.tensor([4.0], requires_grad=True)
y = x**3 + 2*x # y = x^3 + 2x
y.backward()   # dy/dx = 3x^2 + 2
print(f"Gradient of x: {x.grad}") # Output: 3(4^2) + 2 = 50.0
```

---

## 5. ⚡ Async Programming & FastAPI for AI

Normal Python APIs slow ho sakti hain. FastAPI `async` use karke concurrent requests handle karta hai.

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/predict")
async def get_prediction(query: str):
    # Simulate heavy model inference
    result = await heavy_model_call(query) 
    return {"status": "success", "result": result}

async def heavy_model_call(q):
    return f"AI Prediction for: {q}"

# Run command: uvicorn main:app --reload
```

---

## 🏗️ Mega Project: 2-Layer Neural Network from Scratch (No Library!)

Hum sirf NumPy use karke ek model banayenge jo nonlinear pattern (XOR) seekhega.

```python
import numpy as np

# 1. Activation Function
def sigmoid(x): return 1/(1+np.exp(-x))
def sigmoid_derivative(x): return x*(1-x)

# 2. Input/Output Data (XOR Logic)
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

# 3. Weights Initialization
np.random.seed(42)
weights0 = 2*np.random.random((2,4)) - 1 # Input to Hidden
weights1 = 2*np.random.random((4,1)) - 1 # Hidden to Output

# 4. Training Loop
for j in range(60000):
    # Forward Pass
    layer0 = X
    layer1 = sigmoid(np.dot(layer0, weights0))
    layer2 = sigmoid(np.dot(layer1, weights1))

    # Error Calculation (Backprop)
    layer2_error = y - layer2
    if j % 10000 == 0: print(f"Error: {np.mean(np.abs(layer2_error))}")

    # Backpropagation steps
    layer2_delta = layer2_error * sigmoid_derivative(layer2)
    layer1_error = layer2_delta.dot(weights1.T)
    layer1_delta = layer1_error * sigmoid_derivative(layer1)

    # Weight Updates
    weights1 += layer1.T.dot(layer2_delta)
    weights0 += layer0.T.dot(layer1_delta)

print("\nFinal Predictions:")
print(layer2)
```

---

## 🧪 Exercises — Challenge Yourself

### Q1: Matrix Math logic
Agar Matrix A ka shape (5, 3) hai aur Matrix B ka shape (3, 2), toh Resulting Matrix (A @ B) ka shape kya hoga?
<details><summary>Answer</summary>Resulting shape: **(5, 2)**</details>

### Q2: Broadcasting logic
`np.array([1, 2, 3]) + np.array([[10], [20]])` ka output kya hoga?
<details><summary>Answer</summary>
```
[[11, 12, 13],
 [21, 22, 23]]
```
Isse grid creation kehta hain.
</details>

---

## 🔗 Resources
- [Official NumPy Docs](https://numpy.org/doc/)
- [Pandas 10min Guide](https://pandas.pydata.org/docs/user_guide/10min.html)
- [PyTorch for Deep Learning](https://pytorch.org/tutorials/)
