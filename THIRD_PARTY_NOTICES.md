# Third-Party Notices

InSpyCutout itself is distributed under the MIT License. See [`LICENSE`](LICENSE).

InSpyCutout's release ZIP does **not** bundle the third-party Python packages or the InSPyReNet model checkpoint listed below. During setup, these components are downloaded and installed into the local `.venv` / application cache. They remain governed by their own licenses and are **not relicensed under the InSpyCutout MIT License**.

## Direct and principal runtime components

- **transparent-background 1.3.4** — background-removal package used by InSpyCutout. MIT License.  
  Upstream: https://github.com/plemeri/transparent-background

- **InSPyReNet** — salient-object detection model / implementation used through `transparent-background`. MIT License.  
  Upstream: https://github.com/plemeri/InSPyReNet

- **Albumentations 1.4.16** — image augmentation / preprocessing library required by the current InSpyCutout environment. MIT License.  
  Upstream: https://github.com/albumentations-team/albumentations

- **Albucore 0.0.17** — core image-processing helpers used by Albumentations. MIT License.  
  Upstream: https://github.com/albumentations-team/albucore

- **PyTorch** — machine-learning runtime installed by `setup.ps1`. PyTorch uses a BSD-style license and also contains / depends on third-party components with their own notices.  
  Upstream license: https://github.com/pytorch/pytorch/blob/main/LICENSE

- **torchvision** — PyTorch computer-vision package installed by `setup.ps1`. BSD 3-Clause License.  
  Upstream license: https://github.com/pytorch/vision/blob/main/LICENSE

- **Pillow (PIL fork)** — image loading, processing, and display support. Pillow/PIL MIT-CMU style license.  
  Upstream license: https://github.com/python-pillow/Pillow/blob/main/LICENSE

## Model checkpoint

The InSPyReNet model checkpoint is downloaded on demand by `transparent-background` / the setup process and is not stored in this repository or bundled in the release ZIP. Please refer to the upstream InSPyReNet and transparent-background projects for the authoritative terms applying to the implementation and distributed model files.

## Transitive dependencies

The packages above may install additional dependencies. Because `pip` resolves some transitive dependencies at setup time, the exact installed set can vary by platform and date. Each transitive dependency remains subject to its own license and copyright notices.

This notice is intended to identify InSpyCutout's direct and principal third-party components; it does not replace or override any upstream license text. When redistributing third-party packages themselves, review and preserve the license / notice files supplied by those packages as required by their respective licenses.
