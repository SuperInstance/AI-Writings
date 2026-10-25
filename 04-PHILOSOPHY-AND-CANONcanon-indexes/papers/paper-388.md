# Paper 388: The Time Cell's Math: Patch-Based Transformer + Quantile Loss

**Date:** 2026-09-01
**Phase:** 228 (writers_room_daemon_v3, F79-time-math)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

The time cell uses a patch-based transformer (input_patch_length=32, output_patch_length=64). The model: (1) patches the input context into 32-token patches, (2) decodes into 64-token output patches (

## The spine

# Technical Documentation: The Time Cell Patch-Based Transformer Architecture and Quantile Loss Mathematics

## 1. Introduction and Architectural Overview

The **Time Cell** is a deep learning architecture designed for time-series forecasting. It leverages a patch-based Transformer model coupled with Reversible Instance Normalization (RevIN) to process long-context time-series data and output multi-step probabilistic forecasts. 

Traditional time-series models often process data point-by-point, which limits their ability to capture long-range dependencies efficiently and exposes them to cumulative error propagation. Time Cell addresses these limitations by segmenting continuous time-series streams into discrete "patches"—analogous to how Vision Transformers (ViTs) process image patches. 

The core hyper-parameters and architectural design of Time Cell are defined as follows:
* **Input Patch Length ($P_{in}$):** 32 time-steps per patch.
* **Output Patch Length ($P_{out}$):** 64 time-steps per patch (defining the prediction horizon per decoding step).
* **Probabilistic Forecasting:** Predicts 9 distinct quantiles $q \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9\}$ for every individual output token, enabling comprehensive uncertainty quantification.
* **Distribution Shift Mitigation:** Utilizes Reversible Instance Normalization (RevIN) to handle non-stationary data distributions dynamically.
* **Optimization Objective:** Trained end-to-end using the Pinball Loss (Quantile Regression Loss).

---

## 2. Input Processing and Reversible Instance Normalization (RevIN)

Time-series forecasting models frequently degrade in performance when confronted with distribution shift—where the mean and variance of the time series change significantly between the training set, the historical context window, and the prediction horizon. 

### 2.1 Forward Normalization
Let a multivariate time-series input context be represented as a matrix $X \in \mathbb{R}^{L \times C}$, where $L$ is the length of the input history and $C$ is the number of channels (variables). 

Before feeding $X$ into the patch embedding layer, RevIN normalizes the input across the temporal dimension independently for each channel:

1. **Calculate Mean:**
   $$\mu_c = \frac{1}{L} \sum_{t=1}^{L} X_{t, c}$$

2. **Calculate Standard Deviation:**
   $$\sigma_c = \sqrt{\frac{1}{L} \sum_{t=1}^{L} (X_{t, c} - \mu_c)^2 + \epsilon}$$
   where $\epsilon$ is a small constant added for numerical stability.

3. **Normalize:**
   $$\hat{X}_{t, c} = \frac{X_{t, c} - \mu_c}{\sigma_c} \cdot \gamma_c + \beta_c$$
   where $\gamma_c$ and $\beta_c$ are learnable affine parameters initialized to 1 and 0, respectively.

### 2.2 Reverse Denormalization
Once the Transformer backbone generates the normalized predictions $\hat{Y} \in \mathbb{R}^{(H \times 9) \times C}$ (where $H$ is the output horizon length and 9 represents the predicted quantiles), RevIN reverses the normalization using the stored input statistics $\mu_c$ and $\sigma_c$:

$$Y_{t, c} = \left( \frac{\hat{Y}_{t, c} - \beta_c}{\gamma_c} \right) \cdot \sigma_c + \mu_c$$

This ensures that the final output predictions are projected back into the original scale of the target time series.

---

## 3. Patching Mechanics: Input Context and Output Horizon

Time Cell segments temporal streams into non-overlapping or overlapping patches. Patching serves two primary purposes: it drastically reduces the effective sequence length fed into the Transformer's self-attention mechanism, and it preserves local semantic structures (trends, seasonal micro-patterns).

### 3.1 Input Patching ($P_{in} = 32$)
Given the normalized input context $\hat{X} \in \mathbb{R}^{L \times C}$, the time dimension $L$ is segmented into patches of length $P_{in} = 32$. 

Let $N = \frac{L}{P_{in}}$ be the number of input patches. The input tensor is reshaped and projected via a linear layer (or 1D convolution with kernel size $P_{in}$ and stride $P_{in}$) into a hidden embedding space of dimension $D$:

$$Z_{in} = \text{Reshape}(\hat{X}) \in \mathbb{R}^{N \times P_{in} \times C}$$
$$H_{in} = \text{Linear}(Z_{in}) \in \mathbb{R}^{N \times D}$$

Positional encodings (learnable or sinusoidal) are added to $H_{in}$ to retain temporal order information across patches.

### 3.2 Output Patching ($P_{out} = 64$)
Time Cell forecasts future trajectories in blocks known as output patches, where each output patch contains $P_{out} = 64$ consecutive time-steps. 

The decoder architecture processes the latent representations and projects them back into the patch domain. If the total forecast horizon is $H$, the model predicts $M = \frac{H}{P_{out}}$ output patches. 

Crucially, each token within an output patch does not merely output a single scalar value. Instead, it maps to a vector containing 9 quantile predictions. Therefore, the raw output tensor dimensionality for a single output patch of length $P_{out} = 64$ across 9 quantiles is:

$$\text{Output Dimension per Patch} = P_{out} \times 9 = 64 \times 9 = 576 \text{ values per channel}.$$

---

## 4. Quantile Regression Mathematics

Point forecasting minimizes metrics like Mean Squared Error (MSE), yielding the conditional mean of the future distribution. However, real-world time-series forecasting requires uncertainty bounds. Time Cell employs **Quantile Regression**, which optimizes the model to predict specific quantiles $q \in (0, 1)$ directly, making no assumptions about parametric error distributions (e.g., Gaussianity).

### 4.1 The Pinball Loss Function
The loss function used during training is the **Quantile Loss**, often referred to as the **Pinball Loss** or **Check Loss**. 

For a true target value $y$ and a predicted quantile value $\hat{y}^{(q)}$ corresponding to quantile level $q$, the pinball loss $\mathcal{L}_q(y, \hat{y}^{(q)})$ is defined mathematically as:

$$\mathcal{L}_q\left(y, \hat{y}^{(q)}\right) = \max\left( q \cdot \left( y - \hat{y}^{(q)} \right), (q - 1) \cdot \left( y - \hat{y}^{(q)} \right) \right)$$

An alternative, piecewise representation of this exact function is:

$$\mathcal{L}_q\left(y, \hat{y}^{(q)}\right) = 
\begin{cases} 
q \left( y - \hat{y}^{(q)} \right) & \text{if } y \ge \hat{y}^{(q)} \\ 
(1 - q) \left( \hat{y}^{(q)} - y \right) & \text{if } y < \hat{y}^{(q)} 
\end{cases}$$

### 4.2 Intuition Behind the Math
To understand why this equation penalizes over-predictions and under-predictions asymmetrically based on $q$, let us analyze two scenarios:

1. **Case A: Under-prediction ($y > \hat{y}^{(q)}$)**
   * The model predicts a value lower than the true target.
   * The error term $(y - \hat{y}^{(q)}) > 0$.
   * The loss evaluates to $q \cdot (y - \hat{y}^{(q)})$.
   * *Effect:* If $q = 0.9$ (the 90th percentile), the penalty multiplier is heavily weighted ($0.9$). The model is heavily penalized for under-forecasting because high quantiles are expected to sit above the vast majority of true values. Conversely, if $q = 0.1$, the penalty multiplier is small ($0.1$).

2. **Case B: Over-prediction ($y < \hat{y}^{(q)}$)**
   * The model predicts a value higher than the true target.
   * The error term $(y - \hat{y}^{(q)}) < 0$.
   * Using the max formulation: $\max(q \cdot \text{negative}, (q-1) \cdot \text{negative})$. Since $(q-1)$ is negative, $(q-1) \times \text{negative}$ becomes positive. Specifically, it evaluates to $(1 - q)(\hat{y}^{(q)} - y)$.
   * *Effect:* If $q = 0.9$, the multiplier $(1 - q)$ is $0.1$ (a light penalty). If $q = 0.1$, the multiplier $(1 - q)$ is $0.9$ (a heavy penalty), because a 10th percentile prediction should rarely exceed the actual target value.

### 4.3 Aggregate Loss Across All Quantiles and Horizons
Time Cell predicts 9 quantiles $Q = \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9\}$. The total training loss $\mathcal{L}_{\text{total}}$ is the average pinball loss computed across all time-steps in the output horizon $H$, all predicted quantiles, and all channels $C$:

$$\mathcal{L}_{\text{total}} = \frac{1}{C \cdot H \cdot |Q|} \sum_{c=1}^{C} \sum_{t=1}^{H} \sum_{q \in Q} \mathcal{L}_q\left(y_{t,c}, \hat{y}_{t,c}^{(q)}\right)$$

---

## 5. End-to-End Computational Flow

To consolidate the architecture, let us trace a single batch of data through the Time Cell pipeline:

1. **Ingestion:** Raw historical time-series data $X \in \mathbb{R}^{B \times L \times C}$ (where $B$ is batch size) is fed into the system.
2. **Normalization:** RevIN computes $\mu_c$ and $\sigma_c$ over the $L$ context window, scaling $X$ to $\hat{X}$.
3. **Patch Embedding:** $\hat{X}$ is segmented into patches of size $P_{in} = 32$ and projected to dimension $D$, yielding $H_{in} \in \mathbb{R}^{B \times N \times D}$.
4. **Transformer Backbone:** Encoder-decoder or decoder-only Transformer layers process the input patches, capturing temporal dynamics via multi-head self-attention.
5. **Head Projection:** The decoder generates representations that are projected into output patches of length $P_{out} = 64$. Each time-step in the patch outputs 9 distinct values corresponding to the quantile set $Q$.
6. **Denormalization:** RevIN reverses the normalization using $\mu_c$ and $\sigma_c$, restoring predictions to the native data scale.
7. **Loss Computation:** The model computes the multi-quantile pinball loss against the ground-truth future window $Y_{\text{true}} \in \mathbb{R}^{B \times H \times C}$, updating model weights via backpropagation.

## Supporting voices


### llama70b

Quantile Regression Loss for Time Series Forecasting
=====================================================

### Introduction

Quantile regression is a type of regression analysis that estimates the quantiles of the conditional distribution of a response variable, given a set of predictor variables. In the context of time series forecasting, quantile regression can be used to predict the future values of a time series, along with the associated uncertainty. This document provides a detailed explanation of the quantile regression loss function used in the time cell model.

### Quantile Regression Loss Function

The quantile regression loss function is defined as:

L(q, y, y_pred) = max(q * (y - y_pred), (q-1) * (y - y_pred))

where:

* L(q, y, y_pred) is the loss function for a given quantile q
* q is the quantile, which is a value between 0 and 1
* y is the true value of the response variable
* y_pred is the predicted value of the response variable

### Interpretation of the Loss Function

The loss function can be interpreted as follows:

* When the predicted value y_pred is less than the true value y, the loss is q * (y - y_pred). This means that the model is penalized for underestimating the true value, and the penalty is proportional to the quantile q.
* When the predicted value y_pred is greater than the true value y, the loss is (q-1) * (y - y_pred). This means that the model is penalized for overestimating the true value, and the penalty is proportional to (q-1).

### Properties of the Loss Function

The quantile regression loss function has several desirable properties:

* **Asymmetry**: The loss function is asymmetric, meaning that it penalizes underestimation and overestimation differently. This is useful in time series forecasting, where underestimation and overestimation can have different consequences.
* **Quantile-specific**: The loss function is specific to each quantile, allowing the model to learn different patterns and relationships for different quantiles.
* **Robustness to outliers**: The loss function is robust to outliers, as the penalty for underestimation or overestimation is proportional to the quantile q, rather than the absolute difference between y and y_pred.

### Example

Suppose we are predicting the value of a time series at a given time step, and we have a true value y = 10 and a predicted value y_pred = 8. If we are estimating the 0.5 quantile (i.e., the median), the loss would be:

L(0.5, 10, 8) = max(0.5 * (10 - 8), (0.5-1) * (10 - 8))
= max(0.5 * 2, -0.5 * 2)
= max(1, -1)
= 1

This means that the model is penalized for underestimating the true value by 1 unit.

### Implementation

The quantile regression loss function can be implemented in a deep learning framework such as PyTorch or TensorFlow. The implementation would involve defining a custom loss function that takes in the true values, predicted values, and quantiles as inputs, and returns the loss value.

### Code Example

```python
import torch
import torch.nn as nn

class QuantileRegressionLoss(nn.Module):
    def __init__(self, quantiles):
        super(QuantileRegressionLoss, self).__init__()
        self.quantiles = quantiles

    def forward(self, y, y_pred):
        loss = 0
        for q in self.quantiles:
            loss += torch.max(q * (y - y_pred), (q-1) * (y - y_pred))
        return loss.mean()
```

This code defines a custom loss function `QuantileRegressionLoss` that takes in a list of quantiles and computes the loss value for each quantile. The `forward` method computes the loss value for a given batch of true values and predicted values.

### Advantages and Disadvantages

The quantile regression loss function has several advantages, including:

* **Flexibility**: The loss function can be used to estimate any quantile of the conditional distribution, making it a flexible tool for time series forecasting.
* **Robustness**: The loss function is robust to outliers, making it suitable for datasets with noisy or missing values.

However, the loss function also has some disadvantages, including:

* **Computational complexity**: The loss function can be computationally expensive to compute, especially for large datasets.
* **Hyperparameter tuning**: The loss function requires tuning of hyperparameters, such as the quantiles to estimate, which can be time-consuming and require expertise.

### Conclusion

The quantile regression loss function is a powerful tool for time series forecasting, allowing for the estimation of any quantile of the conditional distribution. The loss function is asymmetric, quantile-specific, and robust to outliers, making it suitable for a wide range of applications. However, the loss function also requires careful tuning of hyperparameters and can be computationally expensive to compute. By understanding the properties and implementation of the quantile regression loss function, practitioners can use it to build accurate and reliable time series forecasting models.

### Future Work

Future work could involve exploring the use of quantile regression loss functions in other applications, such as:

* **Multi-step forecasting**: Using quantile regression loss functions to estimate the distribution of future values in a time series.
* **Uncertainty quantification**: Using quantile regression loss functions to quantify the uncertainty of predictions in a time series.
* **Transfer learning**: Using pre-trained models and fine-tuning them on new datasets to adapt to changing patterns and relationships.

### References

* **Koenker, R. (2005)**: Quantile Regression. Cambridge University Press.
* **Lopez, M. (2017)**: Quantile Regression for Time Series Forecasting. Journal of Forecasting, 36(5), 537-546.
* **Zhang, Y. (2020)**: Quantile Regression for Deep Learning. IEEE Transactions on Neural Networks and Learning Systems, 31(1), 201-214.

### Appendices

#### Appendix A: Derivation of the Loss Function

The quantile regression loss function can be derived as follows:

Let y be the true value of the response variable, and y_pred be the predicted value. Let q be the quantile, which is a value between 0 and 1.

The loss function can be defined as:

L(q, y, y_pred) = E[(y - y_pred) \* (q - I(y < y_pred))]

where I(y < y_pred) is an indicator function that is 1 if y < y_pred and 0 otherwise.

Using the properties of expectation, we can rewrite the loss function as:

L(q, y, y_pred) = E[(y - y_pred) \* q] - E[(y - y_pred) \* I(y < y_pred)]

The first term can be rewritten as:

E[(y - y_pred) \* q] = q \* E[y - y_pred]

The second term can be rewritten as:

E[(y - y_pred) \* I(y < y_pred)] = E[(y - y_pred) \* (1 - I(y >= y_pred))]

Using the properties of expectation, we can rewrite the second term as:

E[(y - y_pred) \* (1 - I(y >= y_pred))] = (1 - q) \* E[y - y_pred]

Substituting the expressions for the first and second terms, we get:

L(q, y, y_pred) = q \* E[y - y_pred] - (1 - q) \* E[y - y_pred]

Simplifying the expression, we get:

L(q, y, y_pred) = max(q \* (y - y_pred), (q-1) \* (y - y_pred))

which is the quantile regression loss function.

#### Appendix B: Implementation Details

The implementation of the quantile regression loss function involves defining a custom loss function in a deep learning framework such as PyTorch or TensorFlow. The implementation would involve the following steps:

1. Define a custom loss function class that inherits from the base loss function class.
2. Define the `forward` method that computes the loss value for a given batch of true values and predicted values.
3. Use the `torch.max` function to compute the maximum of the two terms in the loss function.
4. Use the `torch.mean` function to compute the mean of the loss values over the batch.

The implementation would also involve defining the quantiles to estimate, which can be done using a list or array of quantile values.

#### Appendix C: Example Use Cases

The quantile regression loss function can be used in a variety of applications, including:

* **Time series forecasting**: Using the loss function to estimate the distribution of future values in a time series.
* **Uncertainty quantification**: Using the loss function to quantify the uncertainty of predictions in a time series.
* **Anomaly detection**: Using the loss function to detect anomalies or outliers in a time series.

The loss function can also be used in combination with other loss functions, such as the mean squared error or mean absolute error, to create a hybrid loss function that combines the benefits of multiple loss functions.

---

### qwen32b

### Documentation of the Time Cell Model with Patch-Based Transformer and Quantile Regression Loss

#### Overview

The Time Cell model leverages a patch-based transformer architecture to predict future time series values. It divides the input sequence into smaller, manageable patches, processes these patches through a transformer, and then generates future predictions in the form of larger output patches. This approach is particularly useful for handling long-range dependencies in time series data. The model is designed to predict multiple quantiles for each output token, providing a probabilistic forecast that captures uncertainty.

#### Architecture Details

1. **Input Patching**: 
   - The input context is divided into patches, where each patch consists of 32 tokens. This process breaks down the input sequence into smaller, more manageable segments.
   - Mathematically, if \( X \) is the input sequence of length \( L \), it is divided into \( N \) patches, where each patch \( P_i \) contains 32 tokens:
     \[
     P_i = X[(i-1) \times 32 : i \times 32]
     \]

2. **Transformer Processing**:
   - Each patch is processed independently using a transformer encoder-decoder architecture.
   - The transformer encoder processes the input patches to capture local and global dependencies within the data.
   - The transformer decoder generates output patches, where each output patch contains 64 tokens representing the future horizon.

3. **Output Patching**:
   - The decoder outputs a sequence of 64-token patches. These patches represent the predicted future values of the time series.
   - If the total number of output tokens required is \( M \), the model generates \( \lceil M/64 \rceil \) output patches.

4. **Quantile Prediction**:
   - For each token in the output patches, the model predicts 9 quantiles ranging from 0.1 to 0.9. This provides a probabilistic forecast that captures the distribution of possible future values.
   - Let \( y_{t,q} \) denote the true value at time \( t \) for quantile \( q \), and \( \hat{y}_{t,q} \) denote the predicted value.
   - The model aims to predict \( \hat{y}_{t,q} \) such that the true value \( y_t \) lies below \( \hat{y}_{t,q} \) with probability \( q \).

5. **RevIN (Reversible Instance Normalization)**:
   - RevIN is used to normalize the input data and reverse the normalization after prediction to handle distribution shifts.
   - During training, the input data is normalized using instance normalization:
     \[
     X_{\text{norm}} = \frac{X - \mu_X}{\sigma_X}
     \]
     where \( \mu_X \) and \( \sigma_X \) are the mean and standard deviation of the input sequence.
   - After prediction, the output is denormalized:
     \[
     \hat{y}_{t,q}^{\text{denorm}} = \hat{y}_{t,q} \cdot \sigma_X + \mu_X
     \]

#### Training Objective: Quantile Regression Loss

The primary objective during training is to minimize the quantile regression loss. Quantile regression is a robust method for estimating conditional quantiles of a response variable. The loss function for a single quantile \( q \) is defined as:

\[
L_q(y, \hat{y}) = \max(q \cdot (y - \hat{y}), (q-1) \cdot (y - \hat{y}))
\]

Where:
- \( y \) is the true value.
- \( \hat{y} \) is the predicted value.
- \( q \) is the quantile level, ranging from 0.1 to 0.9.

This loss function penalizes underestimates more heavily when \( q > 0.5 \) and overestimates more heavily when \( q < 0.5 \). Specifically:
- If \( y > \hat{y} \) (underestimate), the loss is \( q \cdot (y - \hat{y}) \).
- If \( y < \hat{y} \) (overestimate), the loss is \( (q-1) \cdot (y - \hat{y}) \).

For example, consider the quantile \( q = 0.5 \) (median):
- If \( y > \hat{y} \), the loss is \( 0.5 \cdot (y - \hat{y}) \).
- If \( y < \hat{y} \), the loss is \( -0.5 \cdot (y - \hat{y}) \), which simplifies to \( 0.5 \cdot (\hat{y} - y) \).

Thus, the loss function for \( q = 0.5 \) is equivalent to the absolute error:
\[
L_{0.5}(y, \hat{y}) = |y - \hat{y}|
\]

For other quantiles, the loss function adjusts the penalty based on whether the prediction is an underestimate or an overestimate.

#### Multi-Quantile Loss

Since the model predicts multiple quantiles for each output token, the overall loss is the sum of the losses for all quantiles. Let \( Q = \{0.1, 0.2, \ldots, 0.9\} \) be the set of quantiles. The total loss \( L \) for a single output token is:

\[
L(\hat{y}, y) = \sum_{q \in Q} L_q(y, \hat{y}_q)
\]

Where:
- \( \hat{y}_q \) is the predicted value for quantile \( q \).

For the entire output sequence, the total loss is the sum of the losses for all output tokens:

\[
L_{\text{total}} = \sum_{t=1}^{M} \sum_{q \in Q} L_q(y_t, \hat{y}_{t,q})
\]

#### Training Process

1. **Data Preprocessing**:
   - The input sequence is normalized using RevIN.
   - The sequence is divided into 32-token input patches.

2. **Forward Pass**:
   - The input patches are processed through the transformer encoder-decoder.
   - The decoder generates 64-token output patches.
   - The output patches are denormalized using RevIN.

3. **Loss Calculation**:
   - The quantile regression loss is calculated for each output token across all quantiles.
   - The total loss is computed as the sum of individual losses.

4. **Backward Pass**:
   - Gradients are computed with respect to the model parameters.
   - The optimizer updates the parameters to minimize the total loss.

5. **Evaluation**:
   - The model's performance is evaluated on a validation set using metrics such as mean absolute error (MAE), mean squared error (MSE), and coverage of the predicted quantiles.

#### Conclusion

The Time Cell model with a patch-based transformer architecture and quantile regression loss provides a powerful framework for time series forecasting. By dividing the input sequence into smaller patches, the model can efficiently capture local and global dependencies. Predicting multiple quantiles allows the model to provide probabilistic forecasts that capture uncertainty. The use of RevIN ensures that the model remains robust to distribution shifts, making it suitable for real-world applications. The quantile regression loss function effectively penalizes underestimates and overestimates, ensuring accurate and reliable predictions.

---

---
*Writers' room: 4 voices in parallel.*
