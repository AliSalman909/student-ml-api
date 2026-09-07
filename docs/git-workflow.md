# Git Workflow and Branch Protection

This document records the repository settings chosen to enforce the
development policy, and the reasoning behind each choice.

## Development policy

```
feature branch -> commits -> push -> Pull Request -> CI -> review -> merge
                                                                       |
                                                                       v
                                              version tag -> release workflow
```

Direct development on `main` is not permitted. Every change reaches `main`
through a pull request whose automated checks have passed.

## Branch protection settings for `main`

A **classic branch protection rule** is applied to the branch pattern `main`.

| Setting                                              | State | Reason |
| ---------------------------------------------------- | ----- | ------ |
| Require a pull request before merging                | On    | Forces every change through review and CI. Prevents commits landing on `main` without scrutiny. |
| Required approvals                                   | 0     | See note below. |
| Require status checks to pass before merging         | On    | A pull request cannot be merged while CI is failing, so `main` stays releasable. |
| Required check: `Unit Tests`                         | On    | Blocks a merge if `pytest` fails. |
| Required check: `Docker Build Validation`            | On    | Blocks a merge if the image fails to build or the container fails to serve `/health`. |
| Require branches to be up to date before merging    | On    | Forces a stale branch to incorporate the latest `main` before merging, so the code that was tested is the code that lands. |
| Do not allow bypassing the above settings           | On    | Applies the rules to administrators too. Without this, a repository owner can merge past a failing check and the protection enforces nothing. |
| Allow force pushes                                   | Off   | Prevents history on `main` from being rewritten, keeping commit SHAs stable for traceability. |
| Allow deletions                                      | Off   | Prevents `main` from being deleted. |
| Require signed commits                               | Off   | Requires GPG key distribution; out of scope for this exercise. |
| Require linear history                               | Off   | Would forbid merge commits, which are the chosen merge strategy (see below). |

### Note on required approvals

Required approvals is deliberately set to `0`. This repository has a single
contributor, and GitHub does not permit a user to approve their own pull
request. A non-zero approval requirement would make merging impossible rather
than improving review quality.

The requirement that changes arrive **via a pull request** is still enforced,
which is the property the policy depends on. In a team repository this value
would be at least `1`.

## Verification

A direct push to `main` is rejected by the remote:

```
! [remote rejected] main -> main (protected branch hook declined)
error: failed to push some refs to 'https://github.com/AliSalman909/student-ml-api.git'
```

This confirms the rule prevents accidental direct development on `main`
rather than merely documenting the intention.

## Merge strategy

**Selected strategy: merge commit.**

Justification:

1. **It preserves the branch history.** Each commit on the feature branch
   describes one coherent step (`feat:`, `test:`, `build:`, `ci:`, `fix:`).
   Squashing would collapse them into a single commit and discard that
   narrative, including the deliberate CI failure and its correction, which is
   a required demonstration for this exercise.

2. **It produces a distinct merge commit SHA.** That SHA is the link between a
   pull request and the state of `main` that a version tag is applied to, and
   is required for the traceability chain:

   ```
   Pull Request -> Merge Commit SHA -> Git Tag -> Docker Image Tag -> Image Digest
   ```

   Squash and rebase merges rewrite commits and produce no merge commit, which
   makes that chain harder to reconstruct.

3. **It keeps the shape of the workflow visible.** The graph shows where a
   feature branch diverged from `main` and where it rejoined, which is the
   behaviour this exercise is intended to demonstrate.

Squash and merge is a reasonable default on projects with noisy commit
histories ("wip", "fix typo"), because it keeps `main` readable. That is not
the case here: the commits are already meaningful, and their preservation is
part of the deliverable.
