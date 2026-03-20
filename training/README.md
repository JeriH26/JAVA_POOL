# Training: Python + Java Interview Coding

This folder contains a 7-day coding practice pack with 10 high-frequency interview problems.

## Structure

- `python/`: Python solutions (`p001` to `p010`)
- `python/practice/`: Python TODO templates (`p001` to `p010`) and `practice_runner.py`
- `../src/main/java/training/`: Java solutions (`P001` to `P010`) and `Runner`
- `../src/main/java/training/practice/`: Java TODO templates (`P001` to `P010`) and `PracticeRunner`
- `common_patterns.md`: Quick pattern notes
- `progress_template.md`: Daily tracking template

## 7-Day Mapping

- Day 1: p001, p002
- Day 2: p003, p004, p005
- Day 3: p006
- Day 4: p007, p008
- Day 5: p009
- Day 6: p010
- Day 7: timed mock and review

## Run Python

```bash
bash training/python/run.sh
```

Or run one file:

```bash
python3 training/python/p001_two_sum.py
```

Run Python practice entry:

```bash
bash training/python/run_practice.sh
```

## Run Java

```bash
bash training/java/run.sh
```

Run one Java practice template (after implementing `solve`):

```bash
javac -d training/java/bin src/main/java/training/practice/P001TwoSumPractice.java
java -cp training/java/bin training.practice.P001TwoSumPractice
```

## Practice Rules

1. Solve first without looking.
2. Explain approach and complexity in 2-3 minutes.
3. Implement in both Python and Java for at least one problem per day.
4. Log mistakes in `progress_template.md`.
