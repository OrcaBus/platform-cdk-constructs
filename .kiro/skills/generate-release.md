---
inclusion: manual
---

# Generate Release Skill

Use this skill to generate a GitHub release for `@orcabus/platform-cdk-constructs`.

## Workflow

1. **Identify the range**: Determine the previous release tag and the target commit/tag for the new release.
2. **Gather commits**: Run `git log --oneline <previous_tag>..<target>` to list all commits in the range.
3. **Get commit details**: For each commit, use `git log --format="%H %s%n%b%n---"` to get full messages including PR numbers and descriptions.
4. **Categorize changes** into sections:
   - **Features** — new functionality (`feat:`, `feat(scope):`, or functional changes)
   - **Bug Fixes** — fixes (`fix:`, `fix(scope):`)
   - **Dependencies** — version bumps, dependency upgrades (`deps:`, `chore(deps):`)
   - **Documentation** — docstrings, README updates, typedoc changes (`docs:`)
   - **Internal** — CI, steering, tooling, refactors that don't affect consumers
   - **Breaking Changes** — anything with `BREAKING CHANGE` in the body or `!` in the type
5. **Format the release notes** using this template:

```markdown
## What's Changed

### Breaking Changes

* **description** by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

### Features

* **feat(scope):** Description by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

### Bug Fixes

* **fix(scope):** Description by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

### Dependencies

* **deps(scope):** Description by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

### Documentation

* **docs(scope):** Description by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

### Internal

* Description by @author in https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN

**Full Changelog**: https://github.com/OrcaBus/platform-cdk-constructs/compare/<previous_tag>...<new_tag>
```

6. **Omit empty sections** — only include category headers that have entries.
7. **Create the release** using the GitHub CLI:

```bash
gh release create <new_tag> \
  --target <commit_sha> \
  --title "<new_tag>" \
  --notes-file RELEASE_NOTES_<new_tag>.md
```

## Conventions

- Tag format: `X.Y.Z` (semver, no `v` prefix)
- PR links use format: `https://github.com/OrcaBus/platform-cdk-constructs/pull/NNN`
- Author attribution: `by @<github_username>`
- Keep descriptions concise but informative — one line per change
- For large documentation PRs, summarize the scope rather than listing every file
- The release targets the specific commit SHA, not a branch name

## Example Invocation

> Generate a release for 1.9.0 targeting commit abc123, comparing against 1.8.0

## Notes

- The release workflow (`.github/workflows/release.yml`) is triggered by GitHub release creation and handles npm publishing automatically via OIDC.
- Always verify the commit is on `main` before creating the release.
- Clean up the `RELEASE_NOTES_*.md` file after creating the release (it's only used as input to `gh release create`).
