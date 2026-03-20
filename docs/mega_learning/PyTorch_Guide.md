# Filename: PyTorch_Guide.md

# PyTorch: Deep Learning ka King (Complete Guide)

PyTorch aaj ke time ka sabse flexible aur popular AI framework hai. Is guide mein hum detail mein tensors, autograd, nn.Module aur training loop dekhenge.

## 1. PyTorch kya hai aur Kyun?
PyTorch ek dynamic computational graph banata hai, yani debug karna aasan hai. TensorFlow purane waqt mein static graph use karta tha (ab Eager mode mein aa gaya hai). PyTorch hamesha control-flow (if/else) ko model ke andar handle kar leta hai efficiently.

## 2. Tensors — Foundation of AI
Tensor ek N-dimensional array hai. NumPy array aur Tensor mein fark ye hai ki Tensor GPU ke capabilities ko utilize kar sakta hai.

```python
import torch

# Random sample tensor (Numpy se match hota hai functionality mein)
t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

# GPU/CUDA pe tensor bhejna
if torch.cuda.is_available():
    t_gpu = t.to('cuda')
    print("Moving tensor to CUDA device")

# Operations
t_sum = torch.sum(t)
t_mean = torch.mean(t)
t_flat = t.view(-1) # reshape technique
```

## 3. Autograd: Magic of Backpropagation
Jab hum model train karte hain, humein gradients calculate karne hote hain. PyTorch ka autograd engine ise apne aap kar leta hai jab hum `requires_grad=True` set karte hain.

```python
x = torch.tensor([5.0], requires_grad=True)
y = x**2 + 10  # y = x^2 + 10
y.backward()   # dy/dx = 2x
print(f"Gradient dy/dx: {x.grad}") # output: 10
```

## 4. nn.Module — Custom Models banana
Jab hum neural networks banate hain, hum ek class banate hain jo `nn.Module` se inherit karti hai. Isme hum base layers define karte hain aur forward pass likhte hain.

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

model = SimpleNet(10, 5)
print(model)
```

## 5. Training Loop: AI Dil (Heart)
AI model train karne ke liye 5 basic steps hote hain:
1. **Forward Pass:** Input data model mein jaata hai prediction banane ke liye.
2. **Loss Calculation:** Pred aur true labes ke beech error check karna.
3. **Zero Gradients:** Purane gradients ko clear karna `optimizer.zero_grad()`.
4. **Backward Pass:** Errors ko peeche propagate karna `loss.backward()`.
5. **Optimizer Step:** Weights update karna `optimizer.step()`.

```python
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Training block
# optimizer.zero_grad()
# outputs = model(inputs)
# loss = criterion(outputs, labels)
# loss.backward()
# optimizer.step()
```

## 6. Dataset aur DataLoader
Batching aur data load karne ke liye PyTorch utilities provide karta hai.

```python
from torch.utils.data import Dataset, DataLoader

class CustomData(Dataset):
    def __init__(self, x_data, y_data):
        self.x = x_data
        self.y = y_data
    
    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
```

## 7. Mini Project: MNIST Digit Classifier (Partial Layout)
Hum ek basic CNN (Convolutional Neural Network) model dekhenge jo hand-written digits recognize karega.

```python
class MNISTModel(nn.Module):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 13 * 13, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(-1, 32 * 13 * 13)
        return self.fc1(x)

# Note: Training loop same logic par kaam karega jo upar point 5 mein hai.
```
