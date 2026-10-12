# Outcome blind waveform morphology categories

The categorical Figure 6 analysis uses the six features already extracted for the continuous morphology analysis. Categories are calculated without reference error, failure status or disagreement outcomes.

## Classification rule

For each dataset, point type and participant, the feature median is calculated across all available beats and recorded conditions. A beat is `lower` when its value is below that participant median and `higher` when it is above. An exact median tie is `median_tie` and is excluded from the two-category contrast. A missing or non-measurable feature is `unavailable`. The same beat category is used for every algorithm within a dataset and point type. The rule is exploratory and does not define a clinical or physiological threshold.

## Features and regions

| Feature | Units | Measurement region | Category meaning |
|---|---|---|---|
| Peak or turning-point sharpness | Dataset-specific curvature units | HeartCycle: independent ECHO-event local value. IITB/ReBeat: candidate-independent B R-to-C or X C-to-next-R phase. | Lower versus higher curvature magnitude. |
| Local waveform slope | Dataset-specific slope units | Same independent local region as sharpness. | Lower versus higher absolute slope. |
| Signal amplitude or prominence | Dataset-specific signal units | Same independent local region as sharpness. | Lower versus higher local amplitude/prominence. |
| Signal-to-noise ratio | dB | Complete beat, using the existing filtered-signal/residual quality proxy. | Lower versus higher estimated SNR. |
| Competing peaks, minima or inflections | Count | Predefined B R-to-C or X C-to-next-R phase. | Fewer versus more counted competing features. Median ties are common because this is discrete. |
| Beat-to-beat morphological variability | Normalized RMSE | Standardized current-beat shape versus the preceding beat. | More consistent versus more variable morphology. The first beat or unavailable comparison is excluded. |

## Outcome-specific populations

- Reference error uses successful strict all-method common-reference beats. HeartCycle ECHO and ReBeat expert annotations remain separate; IITB has no reference-error category comparison.
- Peer disagreement uses all-method common-valid beats and is not ground-truth error.
- Failure uses feature-defined eligible attempted beats. Missed and invalid detections remain in the numerator; upstream ineligible records are not part of the attempted denominator.
- Failed detections never receive a timing error.

Participant category summaries require both lower and higher observations to enter a paired contrast. Bootstrap intervals resample participants. Two-sided Wilcoxon tests are reported only when at least five non-zero paired effects exist, and Benjamini-Hochberg adjustment is applied within dataset, condition, point type and outcome across every frozen algorithm and all six features.
