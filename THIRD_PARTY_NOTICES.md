# Third-Party Notices

InSpyCutout itself is distributed under the MIT License. The setup script installs the following third-party software into an isolated local virtual environment. These projects are **not vendored in this repository** and remain governed by their own licenses.

- **transparent-background** — background removal package powered by InSPyReNet. MIT License. https://github.com/plemeri/transparent-background
- **InSPyReNet** — salient-object detection model used by transparent-background. MIT License. https://github.com/plemeri/InSPyReNet
- **PyTorch / torchvision** — installed as dependencies of transparent-background. BSD-style license. https://github.com/pytorch/pytorch
- **Pillow** — image processing library. HPND License. https://python-pillow.org/

The InSPyReNet model checkpoint is downloaded by `transparent-background` when needed and is not stored in this repository.

Please review the upstream projects for complete license texts and attribution requirements.
