from typing import TYPE_CHECKING

import torch
from torch import nn
from torchvision import models

from src.networks.base import BaseNetwork

if TYPE_CHECKING:
    from src.config import NetworkConfig


class ResNet50(BaseNetwork):
    def __init__(self, config: "NetworkConfig", num_classes: int) -> None:
        super().__init__(config, num_classes)
        if self.network_config.pytorch_weights == "ImageNet":
            model = models.resnet50(weights="IMAGENET1K_V2")
        else:
            model = models.resnet50(weights=None)
            if self.network_config.pytorch_weights is not None:
                model.load_state_dict(torch.load(self.network_config.pytorch_weights))

        if not self.network_config.include_top:
            model.fc = nn.Linear(model.fc.in_features, self.num_classes)

        self.model = model

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)
