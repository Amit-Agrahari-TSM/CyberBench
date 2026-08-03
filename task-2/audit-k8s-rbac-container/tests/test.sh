#!/bin/bash
mkdir -p /logs/verifier
python3 /workspace/grader.py
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
