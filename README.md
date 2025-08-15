# Fashion Clothing Classifier

A CNN that classifies grayscale fashion images into 10 categories (T-shirt/top, trouser, pullover, dress, coat, sandal, shirt, sneaker, bag, ankle boot) using the [FashionMNIST dataset](https://github.com/zalandoresearch/fashion-mnist).

---

## Model Architecture
1. **Conv Block 1**: Conv2D(1→10) → ReLU → Conv2D(10→10) → ReLU → MaxPool(2×2)  
2. **Conv Block 2**: Conv2D(10→10) → ReLU → Conv2D(10→10) → ReLU → MaxPool(2×2)  
3. **Classifier**: Flatten → Linear(490→10)
**Loss:** CrossEntropyLoss
**Optimizer:** SGD (lr=0.1) 

## Dataset
- **Train:** 60,000 images  
- **Test:** 10,000 images   
- **Classes:**  
  0. T-shirt/top  
  1. Trouser  
  2. Pullover  
  3. Dress  
  4. Coat  
  5. Sandal  
  6. Shirt  
  7. Sneaker  
  8. Bag  
  9. Ankle boot



## RESULT EXAMPLE

<img width="570" height="582" alt="Screenshot 2025-08-15 at 1 54 24 PM" src="https://github.com/user-attachments/assets/957c8f7a-fbcd-420a-81bb-463f7366c155" />
