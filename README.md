Autonomous CI/CD Failure Triage Agent

What this project does

When a CI pipeline fails, most systems just say “build failed”.  
We build an agent that actually investigates why it failed before deciding what to do.
It looks at the real failure logs and the code diff, then classifies the failure into one of four categories:
Genuine Regression
Flaky Test
Environment Issue
Unclear
If it thinks the test is flaky, it retries a limited number of times and checks the result.  
Only genuinely unclear cases get escalated to a human, with a short useful summary.

Why we are building this

Software teams waste a lot of time and compute re-running everything or treating every failure as a real bug.  
The real value is deciding the correct category first, then acting only when needed.

Our approach for the hackathon

We keep the scope tight so we can ship a working demo in 24 hours.
Core flow:
Receive a failed CI run
Collect the failure logs + the relevant code diff
Extract evidence from both
Classify with confidence and supporting evidence
If flaky candidate → bounded retry (max 2) → re-classify
Output clear result or escalate with summary
We will use a small real GitHub repository with GitHub Actions so the failures are genuine, not mocked.

Tech we plan to use

GitHub Actions for real CI failures
Python for log/diff analysis and classification logic
Simple rules + evidence scoring (LLM only for summary help if needed)
Streamlit or a basic web page for the live dashboard
JSON files or SQLite to keep retry history

Classification logic (starting point)

Flaky Test
Same test failed in recent unrelated builds
Code diff does not touch the failing test or related logic
Passes on retry

Genuine Regression
Stack trace points to changed code
Failure is consistent across retries
Diff clearly related to the failing area

Environment Issue
Missing secrets, network errors, runner problems, dependency download failures
No connection to the code change
Unclear
Conflicting signals or not enough evidence → escalate with short summary
Every classification must show the exact log lines and diff parts that were used.

Retry policy
Maximum 2 retries
Only when flaky score is high and the diff does not touch the test
After retries we re-evaluate and update the classification

Current status (CP1)
Project started
Problem fully understood
Architecture and classification rules defined
First commit: this README + project skeleton
Next steps after CP1:
Set up the real GitHub repo and three failure scenarios (genuine, flaky, environment)
Build the log + diff collector
Implement first version of the classifier

How to run (will be updated)
Coming in the next commits.  
For now this repo is the starting point of the agent.

Team notes
We are focusing on a clean, working demo that judges can see live.  
Evidence first, then classification, then action.  
No forced categories. Unclear is a valid and useful result.
