# Autocomplete Toggle

## Current active file
- settings.json
- Single-file quick reference: `settings.minimal-switch.jsonc`

## Python training only
1. Open `JAVA_POOL.training.code-workspace`.
2. In that workspace, files under `training/python` use `training/python/.vscode/settings.json`.
3. Result: Python training files stay quiet, other repo files keep normal suggestions.

## Turn autocomplete off
1. Copy values from `settings.autocomplete-off.json` into `settings.json`.
2. Run `Developer: Reload Window`.

## Turn autocomplete back on
1. Copy values from `settings.autocomplete-on.json` into `settings.json`.
2. Run `Developer: Reload Window`.

## Notes
- `Disable (Workspace)` on the GitHub Copilot extension is stronger than settings alone.
- `Enable (Workspace)` restores it.
- These changes affect only this workspace.
