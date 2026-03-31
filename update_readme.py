# -*- coding: utf-8 -*-
with open(r'r:\work\gsoc_task_brain\README.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('## Final Results Assessment')
header = parts[0]

new_bottom = """## Final Interpretation of Results

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
"""

with open(r'r:\work\gsoc_task_brain\README.md', 'w', encoding='utf-8') as f:
    f.write(header + new_bottom)

print("Updated README.md")
