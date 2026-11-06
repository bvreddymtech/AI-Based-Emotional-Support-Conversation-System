# M1.2 – ESConv Dataset Exploration and Analysis

**Project:** AI-Based Emotional Support Conversation System  
**Module:** M1.2 – ESConv Dataset Exploration  
**Contributor:** Teja

## 1. Introduction

The ESConv (Emotional Support Conversation) dataset is used in our project to understand emotional-support conversations between help seekers and supporters.

The dataset is analysed to identify emotion categories, problem types, supporter strategies and conversation patterns.

## 2. Dataset Overview

The dataset was loaded from the Hugging Face repository `thu-coai/esconv`.

| Dataset Split | Number of Conversations |
|---|---:|
| Training | 910 |
| Validation | 195 |
| Testing | 195 |
| **Total** | **1,300** |

## 3. Emotion Analysis

The most frequently observed emotion categories across all splits are:

| Emotion | Count |
|---|---:|
| Anxiety | 354 |
| Depression | 334 |
| Sadness | 308 |
| Anger | 111 |
| Fear | 95 |
| Shame | 42 |
| Disgust | 40 |
| Nervousness | 13 |
| Guilt | 1 |
| Jealousy | 1 |
| Pain | 1 |

**Observation:** Anxiety, depression and sadness are the most frequently recorded emotion categories in the analysed dataset.

## 4. Problem Type Analysis

| Problem Type | Count |
|---|---:|
| Ongoing depression | 351 |
| Job crisis | 280 |
| Breakup with partner | 239 |
| Problems with friends | 179 |
| Academic pressure | 156 |
| Sleep Problems | 28 |
| Procrastination | 13 |
| Alcohol Abuse | 12 |
| Appearance Anxiety | 12 |
| Issues with Children | 10 |
| Conflict with parents | 10 |
| Issues with Parents | 8 |
| School Bullying | 2 |

**Observation:** Ongoing depression, job crisis and relationship breakups are the most frequently recorded problem types.

## 5. Supporter Strategy Analysis

| Supporter Strategy | Count |
|---|---:|
| Question | 3,801 |
| Others | 3,341 |
| Providing Suggestions | 2,954 |
| Affirmation and Reassurance | 2,827 |
| Self-disclosure | 1,713 |
| Reflection of feelings | 1,436 |
| Information | 1,215 |
| Restatement or Paraphrasing | 1,089 |

**Observation:** Question is the most frequently recorded supporter strategy. The analysis also identifies reassurance, suggestions and self-disclosure as commonly used strategies.

## 6. Dialogue Turn Statistics

| Metric | Result |
|---|---:|
| Minimum turns per conversation | 16 |
| Maximum turns per conversation | 120 |
| Average turns per conversation | 29.51 |
| Total seeker turns | 19,989 |
| Total supporter turns | 18,376 |
| Total dialogue turns | 38,365 |

## 7. Key Findings

1. The dataset contains 1,300 conversations across three splits.
2. Anxiety, depression and sadness are the leading emotion categories.
3. Ongoing depression is the most frequently recorded problem type.
4. Question is the most frequently recorded supporter strategy.
5. Conversations contain an average of approximately 29.51 dialogue turns.

## 8. Limitations

1. The analysis is based on the available ESConv dataset and its existing annotations.
2. The results describe dataset patterns and do not establish clinical conclusions.
3. The current analysis is descriptive; it does not evaluate the effectiveness of individual strategies.

## 9. Conclusion

The ESConv dataset analysis provides an understanding of emotional categories, user problems, supporter strategies and dialogue patterns.

These findings can support future development of the AI-Based Emotional Support Conversation System, including strategy selection and conversation generation.

**Contribution:** M1.2 – ESConv Dataset Exploration and Analysis.