# 2026 Pro-Tip: nn.CrossEntropyLoss ke andar ki math ko samajhna
import torch
import torch.nn.functional as F

def manual_cross_entropy(logits, target_idx):
    # Logits model se aane wale raw scores hote hain
    probs = F.softmax(logits, dim=-1)
    # Cross Entropy = -log(correct class ki probability)
    loss = -torch.log(probs[target_idx])
    return loss

# Example
raw_logits = torch.tensor([1.2, 5.0, 0.3]) # Model sochta hai ki class 1 sabse zyada likely hai
correct_class = 1 # Indeed, ye class 1 hi hai

print(f"Manual CE Loss: {manual_cross_entropy(raw_logits, correct_class):.4f}")
print(f"PyTorch CE Loss: {F.cross_entropy(raw_logits.unsqueeze(0), torch.tensor([correct_class])):.4f}")