# NeuroDyads CEBRA Pre-Task Analysis

## Task Overview

This analysis evaluates four iterative versions of a GSoC 2026 NeuroDyads pre-task submission. The task involves:

1. **Preprocessing** EEG data from a conversational dyad (Listener/Speaker)
2. **Applying CEBRA** (contrastive representation learning) to joint neural activity
3. **Evaluating** affect classification (positive vs negative conversation)
4. **Interpreting** embedding geometry and limitations

---

## Version Comparison Summary

| Version | KNN Accuracy (Main) | KNN Accuracy (Control) | GoF Score | Key Changes |
|---------|---------------------|------------------------|-----------|-------------|
| V1 | **1.0000** (100%) | 0.5010 | NaN | Basic train_test_split |
| V2 | 0.9764 | 0.8500 | NaN | Epoch-based, GroupKFold, 2D output |
| V3 | 0.9889 | 0.9613 | NaN | Refined permutation testing |
| V4 | 0.9850 | 0.9709 | 1.87 | 3D output, proxy GoF metric |

---

## Detailed Version Analysis

### Version 1: Baseline Implementation

**Approach:**
- Simple train_test_split (70/30) on continuous time samples
- Direct concatenation of positive/negative segments
- 3D CEBRA embedding with `time_delta` conditional

**Results:**
```
Main     -> KNN accuracy: 1.0000
Control  -> KNN accuracy: 0.5010
```

**Critical Issue: Data Leakage**
- The 100% accuracy is indicating severe overfitting
- Using `train_test_split` on temporally continuous data causes leakage because adjacent time points are highly correlated
- A test sample at time `t` has training neighbors at `t-1` and `t+1` that are nearly identical

**Control Interpretation:**
- The ~50% control accuracy is expected for shuffled labels (near chance)
- However, this masks the underlying leakage problem in the main analysis

---

### Version 2: Epoch-Based Processing (First Fix)

**Key Improvements:**
1. **Bandpass filtering** (0.5-45 Hz) after ICA to remove residual drift
2. **Epoch segmentation** (5-second windows) to create independent samples
3. **GroupKFold cross-validation** preventing data leakage across epochs
4. **Interleaved epochs** (alternating pos/neg) to minimize temporal bias

**Results:**
```
Main     -> CV KNN accuracy: 0.9764
Control  -> CV KNN accuracy: 0.8500
```

**Assessment:**
- More realistic accuracy after fixing leakage
- **Concern:** Control accuracy (85%) is still high, suggesting confounds remain
- Output dimension changed to 2D (should be 3D per task requirements)

---

### Version 3: Refined Permutation Testing

**Key Changes:**
- Fixed permutation test to shuffle at epoch level (not sample level)
- Maintained GroupKFold structure during permutation

**Results:**
```
Main     -> CV KNN: 0.9889
Control  -> CV KNN: 0.9613
```

**Critical Concern:**
- Control accuracy (96%) is **very high** - only 3% below main
- This suggests CEBRA is learning temporal structure that correlates with labels, not necessarily affect-specific neural signatures
- The within-session shuffle doesn't break the temporal autocorrelation

---

### Version 4: Final Implementation

**Key Improvements:**
1. **3D output dimension** (as required by task)
2. **Proxy GoF metric** using cosine similarity separation between classes
3. **Extended analyses:**
   - Alpha-band Amplitude Envelope Correlation (AEC) as classical baseline
   - Proper permutation testing with epoch-level shuffling

**Results:**
```
Main     -> CV KNN: 0.9850, GoF (Separation): 1.8679
Control  -> CV KNN: 0.9709, GoF (Separation): 1.7722
```

**Permutation Test:**
```
Original Classification Score: 0.9850
Permutation p-value: 0.0099
```

---

## Final Interpretation of Results

While the preprocessing pipeline and CEBRA implementation follow standard practices, the results reveal a critical limitation in the analysis.

The main model achieved a KNN accuracy of **98.5%**, but the shuffled control achieved **97.1%**, resulting in only a **1.4% performance gap**. This small difference indicates that the majority of the learned structure is not driven by affect labels, but by underlying temporal dynamics present in the data.

This behavior can be explained by two key factors:

1. **Temporal Contiguity of Conditions**
   The positive and negative affect segments are arranged as continuous blocks. Any slow drift, non-stationarity, or adaptation effects across the recording can introduce separable structure unrelated to affect.

2. **CEBRA's Temporal Inductive Bias**
   The use of temporal conditioning encourages the model to learn smooth trajectories in time. As a result, the embedding likely captures the evolution of neural activity over time rather than discrete affective states.

Even after epoch-based segmentation and GroupKFold validation, these temporal dependencies persist. The control analysis, which shuffles labels at the epoch level, does not disrupt this structure because the temporal ordering of the data remains intact.

---

## What the Embedding Likely Represents

The learned embedding should therefore be interpreted as a **low-dimensional trajectory of joint neural dynamics across the conversation**, rather than a clean separation of affective states.

* Dense regions likely correspond to stable neural states
* Transitions may reflect conversational shifts or changes in engagement
* The apparent class separation is largely aligned with temporal progression rather than affect-specific neural signatures

---

## Technical Evaluation and Baselines

### Amplitude Envelope Correlation (AEC)

Classical inter-brain synchrony measure in alpha band (8-12 Hz):
`
Mean Interbrain Alpha AEC: -0.0137
`
**Interpretation:** The near-zero AEC suggests weak linear inter-brain synchrony in the alpha band, indicating that classical measures may not capture the structure learned by CEBRA.

### Re-evaluating Statistical Significance (Permutation Testing)

100-iteration permutation test with epoch-level shuffling:
* **Original Score:** 0.9850
* **P-value:** 0.0099 (Significant)

**Refined Interpretation:** Although statistically significant (p ≈ 0.01), this result should be interpreted cautiously. The permutation scheme preserves temporal structure, meaning the null distribution is not fully independent of the confound. Therefore, statistical significance does not imply that the model has successfully isolated affect-specific information.

---

## Critical Reflection: True Limitation of the Analysis

The most significant limitation is:

> **The confounding of affect labels with temporal structure due to contiguous condition blocks within a single dyad.**

This limitation cannot be resolved through preprocessing or within-session validation alone. Cross-participant alignment issues (e.g., EEG synchronization errors, clock drift, and marker misalignment) can also introduce artifacts that CEBRA might latch onto.

---

## What Would Improve the Analysis

To properly disentangle affect from temporal structure, the following would be required:

1. **Multiple Dyads with Counterbalanced Conditions:** Ensures that affect is not tied to a fixed temporal position.
2. **Leave-One-Dyad-Out Validation:** Tests whether learned representations generalize across independent sessions.
3. **Temporal Block Permutation Controls:** Breaks within-condition temporal continuity while preserving label distribution.
4. **Participant Swap Control:** Distinguishes true inter-brain synchrony from individual neural dynamics.
5. **Cross-Entropy or Distributional Comparisons:** Enables comparison of embedding structure beyond classification accuracy.

---

## Final Takeaway

Rather than demonstrating successful affect decoding, this analysis highlights how easily high-capacity models can exploit temporal structure in continuous neural data. The results emphasize the importance of carefully designed controls and validation strategies when applying contrastive learning to naturalistic time-series datasets.
