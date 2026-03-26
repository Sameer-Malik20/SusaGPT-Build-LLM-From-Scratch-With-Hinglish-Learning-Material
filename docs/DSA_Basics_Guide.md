# 📈 Data Structures & Algorithms
> **Level:** Beginner → Intermediate | **Language:** Hinglish | **Goal:** Master DSA basics

---

## 🧭 Core Concepts (Concept-First)

- Arrays & Strings
- Linked Lists
- Trees & Graphs
- Sorting & Searching

---

## 1. 📊 Arrays

```python
# Find max
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val

# Binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 2. 🔗 Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```

---

## 🌳 Trees

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root):
    result = []
    if root:
        result += inorder_traversal(root.left)
        result.append(root.val)
        result += inorder_traversal(root.right)
    return result
```

---

## ✅ Checklist

- [ ] Basic operations implement kar sakte ho
- [ ] Searching aur sorting use kar sakte ho
- [ ] Trees traverse kar sakte ho