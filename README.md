# AI-Based Emotional Support Conversation System

> **Research-oriented AI-based conversational system for context-aware non-clinical emotional support using emotional-state and support-strategy modeling.**

**Project Category:** Research Oriented
**Batch ID:** CSM-B4

---

## 1. Project Overview

The **AI-Based Emotional Support Conversation System** is a research-oriented conversational AI project that aims to generate more context-aware, emotionally appropriate, and support-strategy-aligned responses for users experiencing everyday emotional difficulties.

Large Language Models (LLMs) are capable of producing fluent and empathetic responses, but effective emotional support requires more than general response generation. A suitable response depends on understanding the user's emotional state, situation, conversation history, and the type of support intervention that is appropriate at a particular point in the conversation.

This project investigates whether explicitly modeling **emotional states, support actions, intervention patterns, and conversational context** can improve the quality of AI-generated emotional-support responses compared with a baseline LLM that generates responses directly from the conversation.

The project is based on the intervention-oriented perspective presented in the base paper **"ESC-Skills: Discovering and Self-Evolving Skills for Emotional Support Conversations."**

---

## 2. Problem Statement

Existing LLM-based emotional-support systems can produce natural-sounding responses, but they may:

* select an unsuitable support strategy for the user's current situation;
* repeatedly rely on commonly preferred strategies;
* fail to recognize changes in the user's emotional state;
* produce generic responses that do not address the underlying concern;
* provide interventions that may not lead to constructive conversational outcomes.

Therefore, there is a need to investigate methods that explicitly connect:

**User Context → Emotional State → Support Strategy → Intervention → Response Quality**

The project aims to study whether incorporating this structured information can lead to more appropriate and reliable emotional-support responses.

---

## 3. Motivation

Emotional-support conversations are dynamic. The user's emotional state may change after every intervention, and the same support action may not be equally effective in every situation.

The base paper models this interaction using an **Intervention Unit (IU)**:

**Intervention Unit = (Seeker State, Support Action, Resulting State)**

This formulation provides a way to study how a particular support intervention relates to the emotional state before the intervention and the resulting state afterward. The base paper extracts Intervention Units from both successful and unsuccessful emotional-support conversations to identify effective intervention patterns and failure-prone patterns.

Our project will use this concept as the research foundation for developing and evaluating a context-aware emotional-support conversation system.

---

## 4. Objectives

The major objectives of the project are:

1. To study publicly available emotional-support conversation datasets.
2. To analyze the relationship between conversational context, user emotional states, support strategies, and response outcomes.
3. To construct structured Intervention Units from emotional-support conversations.
4. To identify recurring effective and ineffective support-intervention patterns.
5. To develop a structured emotional-support Skill Bank based on identified intervention patterns.
6. To retrieve relevant support skills according to the user's current context and emotional state.
7. To generate responses using an LLM with the retrieved contextual and strategy information.
8. To establish a baseline system that generates responses without explicit skill guidance.
9. To compare the baseline and proposed approaches using quantitative and qualitative evaluation.
10. To analyze failure cases and investigate opportunities for improving support-strategy selection and response quality.
11. To maintain a clear non-clinical and safety-oriented scope throughout the project.

---

## 5. Research Foundation

The project is primarily inspired by the base paper:

**Jie Zhu, Huaixia Dou, Shuo Jiang, Junhui Li, Lifan Guo, Feng Chen, Chi Zhang, and Fang Kong. "ESC-Skills: Discovering and Self-Evolving Skills for Emotional Support Conversations." 2026.**

The paper proposes a skill-centric framework in which emotional-support interactions are represented using Intervention Units. These units capture the relationship between the seeker's state, the support intervention, and the subsequent emotional change. The paper then uses these units to construct an executable emotional-support Skill Bank and further refines the skills through simulated interactions and verification.

The proposed student project will study and implement a feasible research-oriented version of this overall methodology.

---

## 6. Dataset

The project will primarily investigate:

### ESConv

**Emotional Support Conversation (ESConv)** is a publicly available emotional-support conversation dataset used extensively in emotional-support dialogue research.

### FailedESConv

The project will additionally investigate unsuccessful emotional-support conversation examples, referred to as **FailedESConv**, to understand both effective and ineffective interventions.

The base paper uses the training split of ESConv containing **910 conversations** together with **196 FailedESConv conversations** for Intervention Unit extraction.

The exact dataset versions, preprocessing procedures, and usable subsets will be finalized during the dataset-analysis phase.

---

## 7. Proposed Methodology

The proposed research workflow is:

```text
             ESConv + FailedESConv
                       |
                       v
              Data Preprocessing
                       |
                       v
             Conversation Analysis
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
     Scenario      Emotional      Support
      Context        State          Action
        |              |              |
        +--------------+--------------+
                       |
                       v
              Response Change
                       |
                       v
             Intervention Units
             (State, Action, Outcome)
                       |
                       v
             Skill Pattern Mining
                       |
                       v
                 Skill Bank
                       |
                       v
              Relevant Skill Retrieval
                       |
                       v
             Context + Skill + LLM
                       |
                       v
              Generated Response
                       |
                       v
                  Evaluation
                       |
              +--------+--------+
              |                 |
              v                 v
          Quantitative      Qualitative
           Evaluation        Analysis
              |                 |
              +--------+--------+
                       |
                       v
                Failure Analysis
                       |
                       v
              Skill Refinement
```

The Intervention Unit formulation and skill-bank construction are directly motivated by the base paper.

---

## 8. Intervention Unit Construction

An Intervention Unit represents a localized support interaction.

Conceptually:

```text
Previous Seeker State
        +
Support Intervention
        +
Resulting Seeker State
        =
Intervention Unit
```

The base paper defines an Intervention Unit as:

**IU = (sₜ, aₜ, sₜ₊₁)**

where:

* `sₜ` = seeker emotional state before the intervention;
* `aₜ` = support action applied by the supporter;
* `sₜ₊₁` = resulting emotional state after the intervention.

The resulting change may be constructive, neutral, or negative.

For the planned implementation, conversations will be analyzed to identify:

* dialogue scenario;
* seeker emotional state;
* supporter intervention/action;
* response change;
* post-intervention state;
* positive, negative, or neutral direction where applicable.

The base paper uses 18 scenario categories, 15 seeker states, 17 support actions, and 14 response-change labels in its annotation framework. These categories will be studied and adapted only where appropriate for the scope and resources of this project.

---

## 9. Skill Bank

The project will investigate the construction of a structured **Emotional Support Skill Bank**.

A skill can contain information such as:

```text
Skill
├── Skill description
├── Activation conditions
├── Relevant emotional states
├── Applicable situations
├── Recommended support action
├── Expected conversational outcome
├── Potential risks / pitfalls
└── Representative examples
```

The base paper generates structured skill documents containing information such as skill overview, activation conditions, recommended actions, pitfalls to avoid, and examples.

The student implementation will develop a feasible version of this concept rather than claiming to reproduce the complete scale of the base paper.

---

## 10. Skill Retrieval

At response-generation time, the system will analyze the current conversation and identify relevant emotional/contextual information.

The planned process is:

```text
Current Conversation
        |
        v
Context / Emotional-State Analysis
        |
        v
Relevant Skills
        |
        v
Skill Retrieval
        |
        v
Selected Support Guidance
```

The retrieved skill information will then be provided to the response-generation component so that the LLM can generate a response that is more explicitly guided by the identified emotional state and support strategy.

---

## 11. Baseline System

A baseline system will be implemented for experimental comparison.

### Baseline

```text
Conversation History
       |
       v
      LLM
       |
       v
Generated Response
```

The baseline will not explicitly retrieve the proposed Skill Bank.

This provides a reference point for determining whether the additional contextual and strategy-aware components contribute measurable improvements.

---

## 12. Proposed System

The proposed approach will incorporate explicit emotional/contextual and skill information.

```text
Conversation History
       |
       v
Context & Emotional Analysis
       |
       v
Support Strategy / Action Identification
       |
       v
Skill Retrieval
       |
       v
Context + Retrieved Skill
       |
       v
      LLM
       |
       v
Generated Response
```

The main research question is:

> **Does explicit emotional-state and support-strategy awareness improve the quality and appropriateness of LLM-generated emotional-support responses compared with direct LLM response generation?**

---

## 13. Evaluation Plan

The project will evaluate the baseline and proposed approaches using a combination of automatic and qualitative assessment.

### Response-level evaluation

Potential metrics include:

* BLEU
* ROUGE
* METEOR
* BERTScore
* Support-strategy alignment / accuracy

The final set of metrics will be selected based on dataset availability, implementation feasibility, and relevance to the research question.

The base paper evaluates response-level performance using strategy prediction accuracy, BLEU, ROUGE, METEOR, and BERTScore.

### Qualitative evaluation

Generated responses will also be examined for:

* contextual relevance;
* emotional appropriateness;
* empathy;
* support-strategy alignment;
* response helpfulness;
* conversational coherence;
* safety.

### Comparative evaluation

The principal experiment will compare:

```text
             Same Evaluation Data
                    |
          +---------+---------+
          |                   |
          v                   v
       Baseline           Proposed
          |                   |
          +---------+---------+
                    |
                    v
              Evaluation
                    |
                    v
             Comparative Results
```

No improvement will be claimed until experiments are actually conducted.

---

## 14. Failure Analysis

An important component of the project will be analysis of unsuccessful responses.

Potential failure categories include:

* incorrect strategy selection;
* insufficient understanding of emotional state;
* generic or repetitive responses;
* inappropriate intervention;
* contextual mismatch;
* failure to respond to a change in emotional state;
* potentially unsafe or invalidating responses.

The base paper similarly analyzes simulated interaction traces to identify missing skills, unsafe interventions, and profile-specific failure patterns.

The identified failure patterns will be used to investigate possible improvements to the Skill Bank.

---

## 15. Skill Refinement

After the initial Skill Bank and response-generation system are implemented, the project will investigate whether observed failure patterns can be used to improve the skills.

The planned research cycle is:

```text
Initial Skill Bank
       |
       v
Response Generation
       |
       v
Evaluation
       |
       v
Failure Analysis
       |
       v
Skill Improvement
       |
       v
Re-evaluation
```

The base paper uses a generation-verification loop for refining and validating skills through simulated interactions.

For this project, the refinement process will be implemented at a scale appropriate to the available computational resources and project timeline.

---

## 16. Research Experiments

The project will progressively conduct the following experiments:

### Experiment 1 — Dataset Analysis

Study the structure and characteristics of ESConv and unsuccessful conversation examples.

### Experiment 2 — Intervention Unit Analysis

Identify relationships between:

**Seeker State → Support Action → Response Change**

### Experiment 3 — Baseline LLM

Generate responses directly from the conversation context.

### Experiment 4 — Strategy-Aware Generation

Provide explicit emotional/contextual and support-strategy information to the LLM.

### Experiment 5 — Skill-Based Generation

Retrieve relevant skills and incorporate them into response generation.

### Experiment 6 — Comparative Evaluation

Compare baseline and proposed approaches using the selected evaluation metrics.

### Experiment 7 — Failure Analysis

Analyze cases where the proposed system performs poorly.

### Experiment 8 — Skill Refinement

Investigate whether identified failure patterns can be converted into improved skill guidance.

---

## 17. Technology Stack

| Component               | Technology                                    |
| ----------------------- | --------------------------------------------- |
| Programming Language    | Python                                        |
| Development Environment | Visual Studio Code                            |
| Version Control         | Git / GitHub                                  |
| Data Processing         | Pandas, NumPy                                 |
| NLP                     | Hugging Face Transformers                     |
| Dataset Processing      | Hugging Face Datasets                         |
| Embeddings              | Sentence Transformers                         |
| Machine Learning        | Scikit-learn                                  |
| LLM Integration         | LLM API                                       |
| LLM Orchestration       | LangChain                                     |
| Evaluation              | ROUGE, METEOR, BERTScore and selected metrics |
| Visualization           | Matplotlib                                    |
| Backend                 | FastAPI                                       |
| Frontend                | HTML, CSS, JavaScript                         |

Exact package versions and model choices will be finalized after compatibility testing and initial experiments.

---

## 18. Project Development Plan

### Phase 1 — Literature Review

* Study the base paper in detail.
* Study recent emotional-support dialogue research.
* Understand ESConv and related datasets.
* Identify the research gap and formulate experimental questions.

### Phase 2 — Dataset Acquisition and Analysis

* Obtain the required publicly available datasets.
* Inspect their structure and fields.
* Analyze conversation format.
* Prepare preprocessing scripts.
* Separate training, validation, and evaluation data where appropriate.

### Phase 3 — Conversation and Intervention Analysis

* Analyze conversation scenarios.
* Identify seeker emotional states.
* Identify support actions.
* Identify post-response changes.
* Construct Intervention Units.

### Phase 4 — Skill Pattern Mining

* Group related Intervention Units.
* Identify recurring state-action patterns.
* Study positive and negative intervention outcomes.
* Generate initial structured skill representations.

### Phase 5 — Skill Bank Development

* Store structured emotional-support skills.
* Define activation conditions.
* Define recommended interventions.
* Record expected outcomes and potential pitfalls.
* Implement skill retrieval.

### Phase 6 — Baseline Development

* Integrate an LLM.
* Generate responses directly from conversation history.
* Store generated responses for evaluation.

### Phase 7 — Proposed System Development

* Implement contextual/emotional-state analysis.
* Implement support-strategy identification.
* Implement skill retrieval.
* Provide retrieved skill information to the LLM.
* Generate context-aware responses.

### Phase 8 — Evaluation

* Run baseline experiments.
* Run proposed-system experiments.
* Calculate selected automatic metrics.
* Conduct qualitative comparison.
* Prepare result tables and visualizations.

### Phase 9 — Failure Analysis and Refinement

* Identify poor responses.
* Categorize failure patterns.
* Investigate missing or inappropriate skills.
* Refine selected skills.
* Re-evaluate the improved system.

### Phase 10 — Final Application

* Develop a conversational interface.
* Connect the interface with the backend and response-generation pipeline.
* Add appropriate safety handling.
* Test the complete system.

### Phase 11 — Documentation and Research Output

* Analyze experimental findings.
* Prepare graphs and tables.
* Document methodology and results.
* Prepare the major project report.
* Prepare the research paper.
* Prepare the final presentation and demonstration.

---

## 19. Expected Outcomes

The expected outcome is an experimentally evaluated emotional-support conversation framework that investigates whether explicit contextual understanding and support-strategy/skill guidance can improve LLM-generated responses.

Expected deliverables include:

* cleaned and processed research datasets;
* Intervention Unit representation;
* structured emotional-support Skill Bank;
* baseline LLM response-generation system;
* proposed skill-aware response-generation system;
* evaluation pipeline;
* comparative experimental results;
* failure-analysis results;
* conversational application prototype;
* project report and research paper.

These are **planned outcomes** and will be validated through experiments.

---

## 20. Scope and Safety

The system is intended for **non-clinical conversational emotional support research**.

The system will not:

* diagnose mental-health conditions;
* provide medical treatment;
* provide psychological treatment;
* replace professional counsellors;
* make clinical decisions;
* be presented as a substitute for qualified mental-health professionals.

The base paper also emphasizes that emotional-support systems should not be deployed in clinical or crisis-intervention pipelines without appropriate expert oversight and safety auditing.

Therefore, safety considerations will be incorporated into the project's design and evaluation.

---

## 21. Project Repository Structure

The repository will progressively follow a structure similar to:

```text
AI-Based-Emotional-Support-Conversation-System/
│
├── README.md
├── ABSTRACT.md
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── preprocessing/
│   ├── analysis/
│   ├── intervention_units/
│   ├── skills/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   └── safety/
│
├── experiments/
├── results/
├── models/
├── backend/
├── frontend/
└── tests/
```

The structure will be expanded as implementation progresses.

---

## 22. Team Collaboration

The project will be maintained using Git and GitHub.

The final repository will have:

* **Project Guide — Repository Owner**
* **Project Students — Repository Members/Collaborators**

The repository will contain the project documentation, source code, experiment configurations, evaluation code, and appropriate research artifacts.

Sensitive credentials such as API keys will **never** be committed to the repository.

---

## 23. References

### Base Paper

Zhu, J., Dou, H., Jiang, S., Li, J., Guo, L., Chen, F., Zhang, C., & Kong, F. (2026). *ESC-Skills: Discovering and Self-Evolving Skills for Emotional Support Conversations.*

### Related References

1. Kang, D., Kim, S., Kwon, T., Moon, S., Cho, H., Yu, Y., Lee, D., & Yeo, J. (2024). *Can Large Language Models be Good Emotional Supporter? Mitigating Preference Bias on Emotional Support Conversation.* Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, 15232–15261.

2. Zhang, T., Zhang, X., Zhao, J., Zhou, L., & Jin, Q. (2024). *ESCoT: Towards Interpretable Emotional Support Dialogue Systems.* Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, 13395–13412.

3. Li, J., Peng, B., & Hsu, Y.-Y. (2024). *Emstremo: Adapting Emotional Support Response with Enhanced Emotion-Strategy Integrated Selection.* Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation, 5794–5805.

4. Zhao, H., Li, L., Chen, S., Kong, S., Wang, J., Huang, K., Gu, T., Wang, Y., Wang, J., Dandan, L., Li, Z., Teng, Y., Xiao, Y., & Wang, Y. (2024). *ESC-Eval: Evaluating Emotion Support Conversations in Large Language Models.* Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, 15785–15810.

---

## 24. Current Project Status

**Review 0 Preparation**

* [x] Project abstract prepared
* [x] Base paper identified
* [x] Related references identified
* [x] GitHub repository created
* [x] Abstract added to repository
* [x] Research methodology planned
* [ ] Guide ownership transfer
* [ ] Project members added
* [ ] Dataset acquisition and analysis
* [ ] Intervention Unit implementation
* [ ] Skill Bank implementation
* [ ] Baseline implementation
* [ ] Proposed system implementation
* [ ] Experimental evaluation
* [ ] Final application
* [ ] Project report and research paper

---

## 25. Research Goal

The central research goal of this project is to investigate:

> **Whether explicit modeling of emotional context and support strategies, combined with structured skill retrieval, can improve the contextual relevance, emotional appropriateness, and support-strategy alignment of LLM-generated emotional-support responses compared with direct LLM response generation.**
