# Filename: AI_Math_Primer_v2.md

# AI Math Primer v2: The Foundations (Advanced Edition)

AI sirf code nahi, Mathematics hai. Is guide mein hum Calculus, Linear Algebra, Probability, aur Optimization concepts detail mein dekhenge.

## 1. Calculus for AI: Gradients aur Chain Rule
Gradients ka matlab hota hai "Slope" yani weight badhane se error kam hoga ya badhega.
- **Chain Rule:** Backpropagation ke waqt model gradients ko peeche multiply karta jaata hai derivatives ke saath.

```python
import numpy as np

# Gradient Function
def f(x):
    return x**2

def df(x):
    # derivative of x^2 is 2x
    return 2 * x

# x = 10 model update logic
x = 10
learning_rate = 0.1
# Update: x = x - lr * df(x)
x = x - learning_rate * df(x)
print(f"Update: {x}") # value will decrease towards 0 (minimum)
```

## 2. Probability Deeper: Bayes aur Cross-Entropy
AI hamesha probability (0 and 1 ke beech) deal karta hai.
- **Bayes Theorem:** Purani info (prior) + Nayi info (likelihood) = New Result (posterior).
- **KL Divergence:** Do probability distributions ke beech ka difference.
- **Cross-Entropy Loss:** Model ki prediction aur true labes ke beech error measure karne ke liye probability logic.

```python
# Binary Cross Entropy check
def binary_cross_entropy(y_true, y_pred):
    return -(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# y_true = 1, y_pred = 0.9 (good prediction)
print(f"Loss: {binary_cross_entropy(1, 0.9)}")
```

## 3. Linear Algebra: Matrix ka Asli Kaam
Matrix multiplication transforms spaces. 
- **Eigenvalues/Eigenvectors:** PCA (Principal Component Analysis) mein direction aur scaling represent karte hain.
- **SVD (Singular Value Decomposition):** Data compression aur recommendations ke liye best hai.

```python
# Eigenvalues with NumPy
mat = np.array([[1, 2], [2, 1]])
eigenvalues, eigenvectors = np.linalg.eig(mat)
print(f"Values: {eigenvalues}")
```

## 4. Softmax aur Temperature: Sampling Maths
Softmax weights ko 0 aur 1 ke beech lata hai (sum should be 1). **Temperature** probability values ko "Sharp" (kam temp) ya "Diverse" (jyada temp) banata hai.

```python
def softmax(x, temp=1.0):
    e_x = np.exp(x / temp)
    return e_x / e_x.sum(axis=0)

logits = np.array([2.0, 1.0, 0.1])
print(f"T=1: {softmax(logits, 1.0)}")
print(f"T=0.5: {softmax(logits, 0.5)}") # Sharp
```

## 5. Attention Math: Transformers ka Dil
Transformers **Q (Query), K (Key), V (Value)** matrices use karte hain importance assign karne ke liye.
Formula: `Softmax( (QK^T) / sqrt(dk) ) * V`

## 6. Gradient Descent Variants: Optimizer ka Safar
Optimizer hamesha weight update karne ke liye rasta dikhata hai.
- **SGD (Stochastic Gradient Descent):** Simpler but noisy.
- **Adam:** Momentum + Adaptive learning rate (Sabse popular standard).
- **AdamW:** Adam + Weight Decay (Better generalization).

```python
# Adam optimizer update partial logic
# m = beta1 * m + (1 - beta1) * gradient
# v = beta2 * v + (1 - beta2) * (gradient^2)
# weight = weight - lr * m_hat / sqrt(v_hat + epsilon)
```

## 7. Practice Problems
1. **Problem:** Given $x=3$, find the update for $f(x)=x^3$ with $lr=0.01$.
   - **Solution:** $f'(x)=3x^2 = 3(3^2)=27$. Update: $3 - (0.01 \times 27) = 2.73$.
2. **Problem:** Compute Dot Product of $[1, 2]$ and $[3, 4]$.
   - **Solution:** $(1 \times 3) + (2 \times 4) = 3 + 8 = 11$.
3. **Problem:** Apply Softmax to $[1, 5, 10]$ and observe results.
   - **NumPy code check:** `np.exp([1, 5, 10]) / np.sum(np.exp([1, 5, 10]))`.
