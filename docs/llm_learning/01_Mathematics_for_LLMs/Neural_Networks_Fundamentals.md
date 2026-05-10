# 🧠 Neural Networks from Scratch — Complete Guide
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master perceptrons, backpropagation, and activation functions

---

## 🧭 Core Concepts (Concept-First)

- Perceptron: The basic building block of neural networks
- Activation Functions: ReLU, Sigmoid, Tanh, Softmax
- Backpropagation: How networks learn from errors
- Gradient Descent: Optimization fundamentals
- Layer stacking: Building deep networks

---

## 1. 🧩 Perceptron — The Basic Unit

Ek perceptron simple classifier hai jo inputs lekar output deta hai.

```python
import numpy as np

class Perceptron:
    """
    Simple perceptron: y = 1 if (w.x + b) > 0 else 0
    """
    def __init__(self, n_inputs):
        # Random weights initialize karo
        self.weights = np.random.randn(n_inputs)
        self.bias = 0
    
    def forward(self, x):
        """Forward pass - compute output"""
        z = np.dot(x, self.weights) + self.bias
        return 1 if z > 0 else 0

# Test perceptron
p = Perceptron(3)
x = np.array([1, 2, 3])
print(f"Output: {p.forward(x)}")
```

### Perceptron Learning Algorithm

```python
def train_perceptron(X, y, epochs=100, learning_rate=0.1):
    """
    Perceptron ko training karna
    """
    n_inputs = X.shape[1]
    weights = np.zeros(n_inputs)
    bias = 0
    
    for epoch in range(epochs):
        for xi, yi in zip(X, y):
            # Forward pass
            z = np.dot(xi, weights) + bias
            y_pred = 1 if z > 0 else 0
            
            # Update weights if prediction wrong
            error = yi - y_pred
            weights += learning_rate * error * xi
            bias += learning_rate * error
    
    return weights, bias
```

---

## 2. 🎯 Activation Functions

Activation functions neural networks mein non-linearity introduce karte hain.

### A. Sigmoid Function

```python
def sigmoid(x):
    """Sigmoid: 1 / (1 + e^-x)"""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """Sigmoid ka derivative"""
    s = sigmoid(x)
    return s * (1 - s)

# Plot ke liye
import matplotlib.pyplot as plt
x = np.linspace(-5, 5, 100)
plt.plot(x, sigmoid(x), label='Sigmoid')
plt.plot(x, sigmoid_derivative(x), label='Sigmoid Derivative')
plt.legend()
plt.grid()
plt.show()
```

### B. ReLU (Rectified Linear Unit)

```python
def relu(x):
    """ReLU: max(0, x)"""
    return np.maximum(0, x)

def relu_derivative(x):
    """ReLU derivative: 1 for x > 0, else 0"""
    return (x > 0).astype(float)
```

### C. Tanh Function

```python
def tanh(x):
    """Tanh: (e^x - e^-x) / (e^x + e^-x)"""
    return np.tanh(x)

def tanh_derivative(x):
    """Tanh derivative: 1 - tanh^2(x)"""
    return 1 - np.tanh(x) ** 2
```

### D. Softmax (Multi-class)

```python
def softmax(x):
    """Softmax for multi-class classification"""
    exp_x = np.exp(x - np.max(x))  # Numerical stability
    return exp_x / np.sum(exp_x)

# Example
scores = np.array([2.0, 1.0, 0.1])
probs = softmax(scores)
print(f"Probabilities: {probs}")  # Sum = 1.0
```

---

## 3. 🔄 Backpropagation — The Learning Algorithm

Backpropagation error ko peeche propagate karke weights update karta hai.

### Complete Neural Network Implementation

```python
class NeuralNetwork:
    """
    Simple feedforward neural network with backpropagation
    """
    def __init__(self, layer_sizes):
        """
        layer_sizes: [input, hidden1, hidden2, ..., output]
        """
        self.weights = []
        self.biases = []
        
        # Weights initialize karo (Xavier initialization)
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i+1]))
            self.weights.append(w)
            self.biases.append(b)
    
    def forward(self, X):
        """Forward pass through all layers"""
        self.activations = [X]
        
        for i in range(len(self.weights)):
            z = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            
            # Last layer ke liye softmax, middle ke liye ReLU
            if i == len(self.weights) - 1:
                a = softmax(z)
            else:
                a = relu(z)
            
            self.activations.append(a)
        
        return self.activations[-1]
    
    def backward(self, X, y, learning_rate):
        """
        Backpropagation - weights update karna
        """
        m = X.shape[0]  # Number of examples
        
        # Output layer error
        delta = self.activations[-1] - y
        
        # Backward pass
        for i in range(len(self.weights) - 1, -1, -1):
            # Weight gradients
            dw = np.dot(self.activations[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            # Update weights
            self.weights[i] -= learning_rate * dw
            self.biases[i] -= learning_rate * db
            
            # Previous layer ka delta (except first layer)
            if i > 0:
                delta = np.dot(delta, self.weights[i].T)
                # ReLU derivative apply karo
                delta = delta * relu_derivative(self.activations[i])
    
    def train(self, X, y, epochs=1000, learning_rate=0.1):
        """Training loop"""
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(X)
            
            # Compute loss (cross-entropy for classification)
            loss = -np.mean(y * np.log(output + 1e-8))
            
            # Backward pass
            self.backward(X, y, learning_rate)
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
```

---

## 4. 📉 Gradient Descent Optimization

```python
def gradient_descent(gradient, current_value, learning_rate):
    """Basic gradient descent step"""
    return current_value - learning_rate * gradient

def momentum(gradient, velocity, beta=0.9):
    """Momentum - helps escape local minima"""
    return beta * velocity + gradient

def adam(gradients, m, v, t, beta1=0.9, beta2=0.999, epsilon=1e-8):
    """Adam optimizer - adaptive learning rates"""
    # Bias correction
    m_hat = m / (1 - beta1 ** t)
    v_hat = v / (1 - beta2 ** t)
    
    # Update
    return m_hat / (np.sqrt(v_hat) + epsilon)
```

---

## 5. 🏗️ Building a Complete Network

```python
# XOR problem solve karo
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])  # XOR output

# Network with 2 input, 4 hidden, 1 output
nn = NeuralNetwork([2, 4, 1])
nn.train(X, y, epochs=5000, learning_rate=0.5)

# Test
for x in X:
    pred = nn.forward(x.reshape(1, -1))
    print(f"{x} -> {pred[0][0]:.4f}")
```

---

## 🧪 Exercises

### Exercise 1: Build a Digit Classifier
MNIST data use karke neural network train karo.

### Exercise 2: Visualize Hidden Layer Weights
Dekho hidden layers ne kya features learn kiye hain.

---

## ✅ Checklist

- [ ] Perceptron working samjho
- [ ] Activation functions distinguish kar sakte ho
- [ ] Backpropagation manually calculate kar sakte ho
- [ ] Gradient descent types compare kar sakte ho
- [ ] Complete network implement kar sakte ho

> **Tip:** Neural networks boil down to: Forward pass → Compute loss → Backward pass → Update weights!