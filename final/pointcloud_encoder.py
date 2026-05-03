import torch
import torch.nn as nn
import torch.nn.functional as F

class PointCloudEncoder(nn.Module):
    def __init__(self, out_dim=128):
        super().__init__()

        self.l1 = nn.Linear(3, 64)
        self.l2 = nn.Linear(64, 128)
        self.l3 = nn.Linear(128, out_dim)


    def forward(self, x):
        # x: (B, N, 3)

        x = F.relu(self.l1(x)) # (B, N, 64)
        x = F.relu(self.l2(x)) # (B, N, 128)
        x = self.l3(x) # (B, N, 128)

        # max pooling over points to get correct shape
        x = torch.max(x, dim=1)[0] # (B, 128)

        return x
