# Red-Team Audit Before Defense

This document is written from the perspective of a strict committee member. Use it to prepare honest answers.

## 1. Requirement Audit

| Committee criticism | Current answer | Risk level |
|---|---|---|
| "Is this only a textbox returning a score?" | No. The app includes controlled samples, URL extraction, risk explanation, token contribution, suspicious keyword highlighting, history, feedback, dashboard, model benchmark, and case report export. | Low |
| "Where is the machine learning work?" | The project trains Logistic Regression, Linear SVM, Random Forest, and Naive Bayes with TF-IDF, then selects Linear SVM by validation F1 macro. | Low |
| "Where is the evaluation?" | The project reports accuracy, F1 macro, ROC-AUC, confusion matrices, and final test metrics after refit. | Low |
| "Where is the database?" | Supabase/PostgreSQL stores prediction history and feedback; local JSONL fallback supports offline demo. | Low |
| "Can this prove a news article is true?" | No. It is a decision-support tool for linguistic reliability screening, not a full evidence-based fact-checker. | Medium |
| "Why no PhoBERT/deep learning?" | Dataset size and deadline favor a stable, explainable baseline. PhoBERT is future work after dataset expansion. | Medium |
| "Why is dataset small?" | VFND is used as the primary dataset because it matches Vietnamese fake/real classification; feedback and external datasets are future expansion. | Medium |

## 2. Minimum, Should-Have, Advanced Modules

| Level | Modules | Status |
|---|---|---|
| Minimum | Text input, preprocessing, trained model, prediction result | Completed |
| Should-have | Metrics, confusion matrix, explanation, history, feedback, report-ready docs | Completed |
| Advanced | URL extraction, dashboard, case report export, product benchmark, reviewer workflow | Implemented as project-scope prototype |
| Future | Evidence retrieval, source credibility database, PhoBERT, admin authentication | Future work |

## 3. Weak Points To Admit

- The dataset is small, so the model may not generalize to every modern news domain.
- The tool detects linguistic and statistical patterns; it does not verify facts against external evidence.
- URL extraction is basic and depends on allowed domains and page structure.
- Lexical suspicious terms are manually designed and should be expanded.
- A production system should include authenticated reviewer/admin roles.

## 4. How To Defend Those Weak Points

"These limitations are intentional scope boundaries. The goal of this course project is to demonstrate a complete software engineering and ML pipeline: dataset preparation, preprocessing, feature extraction, model benchmark, explainable inference, database storage, feedback loop, and report-ready design. Evidence retrieval and transformer fine-tuning are clear future work, not hidden missing parts."

## 5. Self-Score Rubric

| Criterion | Self-score | Reason |
|---|---:|---|
| Problem relevance | 9/10 | Current and practical fake-news/clickbait problem. |
| Software architecture | 8.5/10 | Clear layered architecture and module separation. |
| ML methodology | 8.5/10 | Real dataset, 4 baselines, metrics, final artifact. |
| Explainability | 8.5/10 | Token contribution, lexical risk, risk explanation. |
| Database/workflow | 8/10 | History and feedback exist; full admin auth is future work. |
| Report/design artifacts | 8.5/10 | UML, ERD, pipeline, report draft, benchmark docs. |
| Demo readiness | 9/10 | Stable samples, dashboard, report export, script. |

Final honest assessment: the project is no longer an MVP. It is a solid specialized-project submission if the defense is delivered clearly and limitations are stated honestly. No score can be guaranteed.

