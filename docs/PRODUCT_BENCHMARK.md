# Product Benchmark

This benchmark explains why the project is more than a simple text classifier. It compares the implemented workflow with real fact-checking and news reliability systems.

## Benchmark Summary

| Reference product/system | Observed idea | Suitable project takeaway | Implemented in this project |
|---|---|---|---|
| Full Fact AI | AI helps fact-checkers identify, check, and challenge false information at scale. | The tool should support reviewers, not replace human judgment. | Risk score, explanation, history, feedback loop. |
| NewsGuard | News credibility is shown through visible ratings and supporting criteria. | A reliability label must be accompanied by explanation criteria. | Assessment Summary, risk band, ML risk, lexical risk. |
| Google Fact Check Explorer / ClaimReview | Fact checks are searchable and structured around claims and evaluations. | The system should preserve analysis records for later review. | Prediction history, Supabase storage, downloadable case report. |
| ClaimBuster | NLP/ML can prioritize check-worthy claims for fact-checkers. | ML should help screen suspicious text before manual review. | TF-IDF + ML classifier, suspicious term detection. |
| Modern AI fact-checking tools | Users expect source-backed reports and transparent reasoning. | Even a student project should expose evidence-like signals and limitations. | Highlighted terms, token contribution, report export, limitations section. |

## What The Project Covers

- Article/text input and optional URL extraction.
- ML reliability score using trained baseline models.
- Visual explanation through risk score, probability chart, token contribution, suspicious terms, and text statistics.
- Reviewer-oriented history and feedback loop.
- Model benchmark with accuracy, F1 macro, ROC-AUC, and confusion matrices.
- Downloadable per-case report for defense and review workflow.

## What The Project Does Not Claim

- It does not perform full professional fact-checking.
- It does not retrieve external evidence for every factual claim.
- It does not verify source credibility with a journalist-reviewed database.
- It does not guarantee truth; it provides a decision-support score.

## Defense Sentence

"Before designing the final workflow, I reviewed fact-checking and reliability systems such as Full Fact AI, NewsGuard, Google Fact Check Explorer, and ClaimBuster. The common pattern is that a reliability tool should not only output a label. It should provide a visible score, explanation criteria, history, reviewer feedback, and a report-like output. I implemented these ideas within the scope of a student NLP/ML project."

## References

- Full Fact AI: https://fullfact.ai/
- NewsGuard rating criteria: https://www.newsguardtech.com/ratings/rating-process-criteria/
- Google Fact Check tools: https://newsinitiative.withgoogle.com/resources/trainings/google-fact-check-tools/
- Google ClaimReview documentation: https://developers.google.com/search/docs/appearance/structured-data/factcheck
- ClaimBuster: https://idir.uta.edu/claimbuster
