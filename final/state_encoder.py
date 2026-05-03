import torch
import torch.nn as nn
import torch.nn.functional as F


class StateEncoder(nn.Module):
    def __init__(self, out_dim=64):
        super().__init__()

        self.encode = nn.Sequential(
            nn.Linear(25, 64), # TODO: Fill in_dim for observation size
            nn.ReLU(),
            nn.Linear(64, out_dim),
            nn.ReLU()
        )

    def forward(self, s):
        return self.encode(s)