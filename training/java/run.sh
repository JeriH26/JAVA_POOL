#!/usr/bin/env bash
set -euo pipefail

mkdir -p training/java/bin
javac -d training/java/bin src/main/java/training/*.java src/main/java/training/practice/*.java
java -cp training/java/bin training.Runner
