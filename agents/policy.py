import torch
import torch.nn as nn
import torch.nn.functional as F

from pointcloud_encoder import PointCloudEncoder
from state_encoder import StateEncoder

class Policy(nn.Module):
    def __init__(self):
        super().__init__()

        self.pc_encoder = PointCloudEncoder(128)
        self.state_encoder = StateEncoder(64)

        self.mlp = nn.Sequential(
            nn.Linear(192, 128),
            nn.ReLU(),
            nn.Linear(128, 7)  # action dim
        )

    def forward(self, pc, state):
        pc_feat = self.pc_encoder(pc)
        state_feat = self.state_encoder(state)

        x = torch.cat([pc_feat, state_feat], dim=-1)

        return self.mlp(x)