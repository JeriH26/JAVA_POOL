# Training Workspace Guide

## Recommended way to open this repo

Open this file when you want to practice Python without auto suggestions:

- `JAVA_POOL.training.code-workspace`

## What happens in that workspace

- Files under `training/python` use quiet settings from `training/python/.vscode/settings.json`
- Other files in the repo use normal settings from `.vscode/settings.json`

## If you want normal suggestions everywhere

Use the regular folder workspace instead of the training workspace:

- Open the `Python_JAVA_Business_Simulation` folder directly

## If you want to restore suggestions inside training/python too

1. Open `training/python/.vscode/settings.json`
2. Set the Copilot and editor suggestion options to `true`
3. Run `Developer: Reload Window`
