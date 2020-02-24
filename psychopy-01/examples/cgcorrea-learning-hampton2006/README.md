## Probabilistic Reversal Learning Task

Carlos coded up a task from Hampton et al 2006 where participants receive probabilistic reward in a reversal task with probabilistic reversals.

It might be helpful to start with some practice which will end after 3 reversals occur and have deterministic reward.
```
python psychopy/hampton2006.py --practice --deterministic_reward
```

Follow that up with a practice trial with probabilistic rewards.
```
python psychopy/hampton2006.py --practice
```

Finally, you're ready for the real task! Perform this in the scanner.
```
python psychopy/hampton2006.py
```
