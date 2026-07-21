# Repository Workflow

## Feature development

- Before starting any new feature, create and switch to a dedicated branch. Do not develop new features directly on the repository's default branch.
- After implementation and the relevant tests are complete, stage only the files that belong to the feature, commit the changes, push the feature branch to `origin`, and open a pull request against the default branch.
- Never include secrets, `.env`, personal runtime configuration, or local backup files in a commit or pull request.
