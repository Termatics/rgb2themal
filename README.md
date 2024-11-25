
# RGB to Thermal Model Training

This repository is for training models that convert RGB images to thermal images using two different methods: unpaired (CycleGAN) and paired (Pix2Pix). The project is based on [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

## Table of Contents
1. [Folder Structure](#folder-structure)
2. [Installation](#installation)
3. [Dataset Preparation](#dataset-preparation)
   - [Unpaired: CycleGAN](#unpaired-cyclegan)
   - [Paired: Pix2Pix](#paired-pix2pix)
4. [Training](#training)
   - [Unpaired: CycleGAN](#training-cyclegan)
   - [Paired: Pix2Pix](#training-pix2pix)
5. [Testing](#testing)
   - [Unpaired: CycleGAN](#testing-cyclegan)
   - [Paired: Pix2Pix](#testing-pix2pix)
6. [Fine-tuning](#fine-tuning)
7. [Adding a New Dataset](#adding-a-new-dataset)
8. [Download Datasets and Trained Models](#download-trained-models)

---

## Folder Structure

Create the following folders in your project directory:
- `checkpoints/`: For storing trained model weights.
- `results/`: For saving test results.

---

## Installation

Install the required libraries by running:
```bash
pip install torch>=1.4.0 torchvision>=0.5.0 dominate>=2.4.0 visdom>=0.1.8.8 wandb
```

---

## Dataset Preparation

### 1. Unpaired: CycleGAN

Unpaired data does not require one-to-one correspondence between images in domain A and domain B.  
- **A (RGB images)**: Images are collected using AirSim and Unreal Engine in a virtual environment, capturing road and house images.  
- **B (Thermal images)**: Use IR1, IR2, IR3, and IR4 datasets, with a total of 555 x 4 infrared images.

Organize the dataset into four folders under `datasets`:
- `trainA/`: Training RGB images.
- `trainB/`: Training thermal images.
- `testA/`: Testing RGB images.
- `testB/`: Testing thermal images.

### 2. Paired: Pix2Pix

Paired data requires a one-to-one correspondence between domain A (RGB) and domain B (Thermal) images.  
- **A (RGB images)**: RGB images are obtained from screen recordings using Horus, and processed using the provided scripts:
  - `video2image.py`: Extracts images from video.
  - `diff.py`: Removes consecutive similar images.
  - `rename.py`: Renames files sequentially.

Organize the paired dataset with the following structure:
- `A/`:
  - `train/`: Training images for A.
  - `val/`: Validation images.
  - `test/`: Testing images.
- `B/`:
  - `train/`: Training images B.
  - `val/`: Validation images.
  - `test/`: Testing images.

To combine images from domain A and B, use:
```bash
python datasets/combine_A_and_B.py --fold_A /path/to/data/A --fold_B /path/to/data/B --fold_AB /path/to/data
```
This will combine each pair of images (A,B) into a single image file, ready for training.


(Update) A cleaned and structured Karlsruhe Dataset has been used for pix2pix training. The dataset can be downloaded through the link at the end.

---

## Training

### 1. Unpaired: CycleGAN

Train the CycleGAN model using:
```bash
python train.py --dataroot "path_to_datasets" --name "model_name" --model cycle_gan
```
Example:
```bash
python train.py --dataroot ./datasets/rgb2thermal_cycle_gan_datasets --name rgb2thermal_cycle_gan --model cycle_gan
```
To select the generator direction after training:
- **A to B (RGB to Thermal)**:  
  ```bash
  cp ./checkpoints/rgb2thermal_cycle_gan/latest_net_G_A.pth ./checkpoints/rgb2thermal_cycle_gan/latest_net_G.pth
  ```
- **B to A (Thermal to RGB)**:  
  ```bash
  cp ./checkpoints/rgb2thermal_cycle_gan/latest_net_G_B.pth ./checkpoints/rgb2thermal_cycle_gan/latest_net_G.pth
  ```

### 2. Paired: Pix2Pix

Train the Pix2Pix model using:
```bash
python train.py --dataroot "path_to_datasets" --name "model_name" --model pix2pix --direction "BtoA or AtoB"
```
Example:
```bash
python train.py --dataroot ./datasets/rgb2thermal_pix2pix_datasets --name rgb2thermal_pix2pix --model pix2pix --direction AtoB --display_id -1
```

---

## Testing

### 1. Unpaired: CycleGAN

Test the CycleGAN model with:
```bash
python test.py --dataroot "path_to_testA" --name "model_name" --model test --no_dropout
```
Example:
```bash
python test.py --dataroot ./datasets/rgb2thermal_cycle_gan_datasets/testA --name rgb2thermal_cycle_gan --model test --no_dropout
```
Results will be saved in the `results` folder.

### 2. Paired: Pix2Pix

Test the Pix2Pix model with:
```bash
python test.py --dataroot "path_to_datasets" --direction "BtoA or AtoB" --model pix2pix --name "model_name"
```
Example:
```bash
python test.py --dataroot ./datasets/rgb2thermal_pix2pix_datasets --direction AtoB --model pix2pix --name rgb2thermal_pix2pix
```
---

## Fine-tuning

Fine-tuning allows you to further train a pre-trained model or resume training after interruption.  

### Steps for Fine-tuning:
1. Use the `--continue_train` flag to resume from a pre-trained model:
   ```bash
   python train.py --dataroot "path_to_new_datasets" --name "model_name" --model pix2pix --continue_train --epoch_count <starting_epoch>
   ```
   By default, the program will initialize the epoch count as 1. Set --epoch_count <int> to specify a different starting epoch count. Example (starting from epoch 101, previous training ends at epoch 100):
   ```bash
   python train.py --dataroot ./datasets/new_dataset --name rgb2thermal_pix2pix --model pix2pix --direction AtoB --continue_train --epoch_count 101
   ```

2. Lower the learning rate for fine-tuning (recommended):
   ```bash
   python train.py --dataroot ./datasets/new_dataset --name rgb2thermal_pix2pix --model pix2pix --direction AtoB --continue_train --lr 0.00005
   ```

3. Ensure training and testing configurations are consistent (e.g., `--netG`, `--norm`, `--no_dropout`).

---

## Adding a New Dataset

1. **Organize the dataset**: Follow the format for CycleGAN or Pix2Pix as described in [Dataset Preparation](#dataset-preparation).
2. **Generate Pix2Pix paired data**: Combine RGB and Thermal images using:
   ```bash
   python datasets/combine_A_and_B.py --fold_A ./datasets/new_paired_dataset/A                                       --fold_B ./datasets/new_paired_dataset/B                                       --fold_AB ./datasets/new_paired_dataset
   ```
3. **Train with the new dataset**:
   - For CycleGAN:
     ```bash
     python train.py --dataroot ./datasets/new_unpaired_dataset --name new_cyclegan_model --model cycle_gan
     ```
   - For Pix2Pix:
     ```bash
     python train.py --dataroot ./datasets/new_paired_dataset --name new_pix2pix_model --model pix2pix --direction AtoB
     ```

---

## Download Trained Models

The datasets and trained models for CycleGAN and Pix2Pix can be downloaded from the following [Google Drive link](https://drive.google.com/drive/folders/18QJaQ-h_MefTEfjMUPvytXDEaCUB_sTc?usp=sharing).

The trained models can be used as pre-trained model in future training.

---
