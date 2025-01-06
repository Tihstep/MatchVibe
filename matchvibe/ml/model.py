from dataclasses import dataclass
import numpy as np
from torchvision.models import convnext_tiny, ConvNeXt_Tiny_Weights
import torchvision.transforms as transforms
import torch.nn as nn


@dataclass
class SimilarityPrediction:
    """Class representing a similarity prediction."""

    embedding: list


def load_model():
    """Load a pre-trained image classification model.

    Returns:
        pass
    """

    class Model(nn.Module):
        def __init__(self, base_model):
            super().__init__()
            self.base_model = base_model

        def forward(self, img):
            return self.base_model(img)

    base_model = convnext_tiny(weights=ConvNeXt_Tiny_Weights.DEFAULT)
    convnext = Model(base_model)

    def model(image: np.array) -> SimilarityPrediction:
        pred = convnext(image)

        return SimilarityPrediction(embedding=pred)

    return model


def load_transform():
    base_preprocess = ConvNeXt_Tiny_Weights.DEFAULT.transforms()
    preprocess = transforms.Compose([transforms.PILToTensor(), base_preprocess])
    return preprocess
