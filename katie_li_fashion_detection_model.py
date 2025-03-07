# -*- coding: utf-8 -*-
"""Katie Li Fashion Detection Model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YPVdtzcD_Nv0Z1tmB28bwPqXk_-omzHz

# FashionMNISTModel

# Classifies random clothing into 10 types - sandal, sneakers, shirt, t-shirt, etc.
"""

import torch
from torch import nn

import torchvision
from torchvision import datasets
from torchvision import transforms
from torchvision.transforms import ToTensor

import matplotlib.pyplot as plt

"""Getting the FashionMNIST dataset that contains 60,000 images"""

from torchvision import datasets
train_data = datasets.FashionMNIST(
    root = "data",
    train = True,
    download = True,
    transform = ToTensor(),
    target_transform = None
)
test_data = datasets.FashionMNIST(
    root = "data",
    train = False,
    download = True,
    transform = ToTensor(),
    target_transform = None
)

"""Turning the large data into batches of smaller data

Purpose: Computer will not have to handle too much data at once
"""

#Turning data into batches for effiency so computer doesn't have to store so many images at once
from torch.utils.data import DataLoader
BATCH_SIZE = 32
train_dataloader = DataLoader(dataset = train_data,
                              batch_size = BATCH_SIZE,
                              shuffle = True)

test_dataloader = DataLoader(dataset = test_data,
                              batch_size = BATCH_SIZE,
                              shuffle = False)
class_names = train_data.classes

"""Importing helper functions

"""

import requests
from pathlib import Path
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
device

#download helper functions from learn pytorch repo
if Path("helper_functions.py").is_file():
  print("helper_functions.py already exists, skipping download...")
else:
  print("Downloading...")
  request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py")
  with open("helper_functions.py","wb") as f:
    f.write(request.content)

from helper_functions import accuracy_fn

"""----------------------------------
# Function for Training
"""

def train_step(model: torch.nn.Module,
               data_loader: torch.utils.data.DataLoader,
               loss_fn: torch.nn.Module,
               optimizer: torch.optim.Optimizer,
               accuracy_fn,
               device: torch.device = device):
  train_loss, train_acc = 0,0
  model.train()
  for batch, (X, y) in enumerate(data_loader):
    #0. Put data on target device GPU not CPU for faster computation
    X, y = X.to(device), y.to(device)

    #1. Forward pass. aka, pass in the data and make a prediction
    y_pred = model(X)

    #2. Calculate the loss (how wrong the model is) and accuracy
    loss = loss_fn(y_pred, y)
    train_loss += loss
    train_acc += accuracy_fn(y_true = y,
                             y_pred = y_pred.argmax(dim = 1))
    #3. Optimizer zero grad
    optimizer.zero_grad()
    #4. Perform backpropagation
    loss.backward()
    #5. Step – change parameters in the best direction with gradient descen
    optimizer.step()

  #To find AVG loss and accuracy, divide by the total # of times
  train_loss /= len(data_loader)
  train_acc /= len(data_loader)
  print(f"Train loss: {train_loss:.5f} | Train acc: {train_acc:.2f}")

"""----------------------------------------
Convolutional Neural Network (CNN) Model
----------------------------------------
"""

class FashionMNISTModelV2(nn.Module):
  def __init__(self, input_shape: int, hidden_units: int, output_shape:int):
    super().__init__()
    self.conv_block_1 = nn.Sequential(
        nn.Conv2d(in_channels = input_shape,
                  out_channels = hidden_units,
                  kernel_size = 3,
                  stride = 1,
                  padding = 1),
        nn.ReLU(),
        nn.Conv2d(in_channels = hidden_units,
                  out_channels = hidden_units,
                  kernel_size = 3,
                  stride = 1,
                  padding = 1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size = 2)
    )
    self.conv_block_2 = nn.Sequential(
        nn.Conv2d(in_channels = hidden_units,
                  out_channels = hidden_units,
                  kernel_size = 3,
                  stride = 1,
                  padding = 1),
        nn.ReLU(),
        nn.Conv2d(in_channels = hidden_units,
                  out_channels = hidden_units,
                  kernel_size = 3,
                  stride = 1,
                  padding = 1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size = 2)
    )
    self.classifier = nn.Sequential(
        nn.Flatten(),
        nn.Linear(in_features = hidden_units*7*7,
                  out_features = output_shape)
    )
  def forward(self, x):
    x = self.conv_block_1(x)
    x = self.conv_block_2(x)
    x = self.classifier(x)
    return x

"""------------------------------------
# Initializing: Model, Loss, Optimizer
"""

model_2 = FashionMNISTModelV2(input_shape = 1,
                              hidden_units = 10,
                              output_shape = len(class_names)).to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params = model_2.parameters(),
                            lr = 0.1)

"""-------------
# TRAINING LOOP
"""

from tqdm.auto import tqdm #progress bar
epochs = 3
for epoch in tqdm(range(epochs)):
  print(f"Epoch: {epoch}\n-------")
  train_step(model = model_2,
             data_loader = train_dataloader,
             loss_fn = loss_fn,
             optimizer = optimizer,
             accuracy_fn = accuracy_fn,
             device = device)

"""-------
# Visualize Model Predictions
"""

def make_predictions(model: torch.nn.Module,
                     data: list,
                     device: torch.device = device):
  pred_probs = []
  model.to(device)
  model.eval()
  with torch.inference_mode():
    for sample in data:
      sample = torch.unsqueeze(sample, dim = 0).to(device)
      pred_logit = model(sample)
      pred_prob = torch.softmax(pred_logit.squeeze(), dim = 0)
      pred_probs.append(pred_prob.cpu())
  return torch.stack(pred_probs) #turns list into tensor

"""Make predictions down below and look at results"""

import random

test_samples = []
test_labels = []
for sample, label in random.sample(list(test_data), k = 9):
  test_samples.append(sample)
  test_labels.append(label)

#Forward pass - make predictions
pred_probs = make_predictions(model = model_2,
                              data = test_samples)
pred_classes = pred_probs.argmax(dim = 1)

plt.figure(figsize =(9,9))
nrows = 3
ncols = 3
for i, sample in enumerate(test_samples):
  plt.subplot(nrows,ncols, i+1)

  #plot target image
  plt.imshow(sample.squeeze(), cmap = "gray")

  #find the prediction in text form, e.g. "Sandal"
  pred_label = class_names[pred_classes[i]]

  #get the truth label (in text form)
  truth_label = class_names[test_labels[i]]

  #create a title for the plot
  title_text = f"Pred: {pred_label} | Truth: {truth_label}"

  #check for equality between pred and truth
  if pred_label == truth_label:
    plt.title(title_text, fontsize = 10, c = "g")
  else:
    plt.title(title_text, fontsize = 10, c = "r")
  plt.axis(False)