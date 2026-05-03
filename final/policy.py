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
            nn.Linear(128, 4)
        )

    def forward(self, pc, observation):
        pc_feat = self.pc_encoder(pc)
        observation_feat = self.state_encoder(observation)

        x = torch.cat([pc_feat, observation_feat], dim=-1)

        return self.mlp(x)