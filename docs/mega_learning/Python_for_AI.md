# Filename: Python_for_AI.md

# Python for AI: Complete Guide (Hinglish)

AI Engineering ke liye Python sabse foundational language hai. Is guide mein hum basics se lekar Advanced concepts tak dekhenge jo AI models banane mein kaam aate hain.

## 1. Python Basics Recap (AI Perspective)
AI development mein clean aur efficient code likhna zaroori hai.

### Lists, Dicts, Functions, aur OOP
- **Lists:** Data storage aur manipulation ke liye.
- **Dictionaries:** Hyperparameters aur configurations ke liye.
- **OOP:** PyTorch models hamesha `nn.Module` se inherit karte hain, isliye classes ka concept clear hona chahiye.

```python
# Function with type hints (Production standard)
def calculate_loss(y_true: list, y_pred: list) -> float:
    return sum([(t - p)**2 for t, p in zip(y_true, y_pred)]) / len(y_true)

# OOP for Models
class SimpleNeuron:
    def __init__(self, weight: float, bias: float):
        self.w = weight
        self.b = bias
    
    def forward(self, x: float) -> float:
        return self.w * x + self.b

neuron = SimpleNeuron(0.5, 0.1)
print(f"Prediction: {neuron.forward(10)}")
```

## 2. NumPy — Matrix ka Baap
AI mein har cheez matrix (array) hoti hai. NumPy fast computation deta hai.

```python
import numpy as np

# Arrays aur Shapes
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Shape: {arr.shape}")

# Broadcasting: Different shapes ke arrays par operations
a = np.array([1, 2, 3])
b = 2
print(f"Broadcasting: {a * b}") # [2, 4, 6]

# Dot Product (Matrix Multiplication)
m1 = np.random.rand(3, 2)
m2 = np.random.rand(2, 4)
result = np.dot(m1, m2)
print(f"Dot Product Shape: {result.shape}")
```

## 3. Pandas — Data Cleaning & Analysis
Jab tak data clean nahi hoga, model achha perform nahi karega.

```python
import pandas as pd

# CSV Load aur basic cleaning
# df = pd.read_csv("dataset.csv")
data = {'feature': [1, 2, np.nan, 4], 'target': [10, 20, 30, 40]}
df = pd.DataFrame(data)

# Mean se fill karna
df['feature'] = df['feature'].fillna(df['feature'].mean())

# Groupby logic
avg_target = df.groupby('feature').mean()
```

## 4. PyTorch Tensors — Next Gen Arrays
Tensors NumPy arrays jaise hote hain lekin ye GPU pe run ho sakte hain.

```python
import torch

# NumPy to Tensor
np_arr = np.array([1, 2, 3])
tensor = torch.from_numpy(np_arr)

# Autograd Basics (Automatic Gradient)
x = torch.tensor([2.0], requires_grad=True)
y = x**2
y.backward()
print(f"Gradient: {x.grad}") # output: 4.0
```

## 5. Async Programming & FastAPI
AI models ko serve karte waqt non-blocking code zaroori hai.

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/predict")
async def predict():
    # Model inference simulate karna
    await asyncio.sleep(1) 
    return {"prediction": "Success", "status": 200}
```

## 6. Mini Project: Simple Neural Network NumPy se
Hum ek 2-layer neural network banayenge base NumPy se.

```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Input data
X = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
y = np.array([[0, 1, 1, 0]]).T

# Weights initialize
np.random.seed(1)
weights = 2 * np.random.random((3, 1)) - 1

# Training loop
for i in range(10000):
    output = sigmoid(np.dot(X, weights))
    error = y - output
    adjustment = np.dot(X.T, error * (output * (1 - output)))
    weights += adjustment

print("Trained Weights:")
print(weights)
```
