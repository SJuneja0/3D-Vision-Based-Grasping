import torch
import torch.nn as nn
import torch.nn.functional as F


class StateEncoder():
    def __init__(self, out_dim=64):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(7, 64),   # e.g., joints + gripper
            nn.ReLU(),
            nn.Linear(64, out_dim),
            nn.ReLU()
        )

    def forward(self, s):
        return self.net(s)