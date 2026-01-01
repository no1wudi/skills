---
name: general-conventional-commit
description: Creates standardized git commits following Conventional Commits format. Covers identifying repos, checking changes, grouping files, proposing commits, and executing git operations. Use when creating git commits or reviewing changes before committing.
---

# Creating Git Commits

## 1. Identify Working Git Repository

```bash
# Check if current directory is a git repo
git rev-parse --is-inside-work-tree

# Get git root directory
git rev-parse --show-toplevel

# Get current branch
git branch --show-current

# Check remote tracking branch
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

## 2. Check Current Changes

```bash
# Show all untracked files
git status --porcelain | grep "^??"

# Show modified files (staged and unstaged)
git status --short

# Show detailed changes
git diff

# Show staged changes
git diff --staged

# Show changed files with statistics
git diff --stat
```

## 3. Read Original Files

```bash
# For files smaller than 10KB, read the whole file
# Check file size first
ls -lh path/to/file

# Read from git index for staged files
git show :path/to/file

# Read from HEAD for unstaged files
git show HEAD:path/to/file

# For large files, read only the diff
git diff HEAD path/to/file
```

## 4. Read Modified Files

```bash
# Use read tool with absolute path
# File content after modifications
read path/to/file
```

## 5. Group and Validate Files

```bash
# List all changed files
git status --short

# Group files by directory/module
git status --short | cut -c4- | cut -d/ -f1 | sort | uniq -c

# Ask user if unrelated changes should be separate commits
# "These files span multiple modules. Group them together or split?"
```

**Commit grouping rules:**
- Related functionality in same commit
- Separate commits for different concerns
- One logical change per commit
- Ask user if unsure about grouping

## 6. Create Commit Proposal

```bash
# Summarize changes for commit message
git diff --cached --stat  # For staged files
git diff --stat           # For unstaged files

# Draft commit message following Conventional Commits format
# <type>[optional scope]: <description>
# 
# [optional body]
# 
# [optional footer]
```

**Commit message types:**
```bash
feat     # New feature (MINOR version)
fix      # Bug fix (PATCH version)
docs     # Documentation only
style    # Code formatting
refactor # Code restructuring
perf     # Performance improvement
test     # Adding/modifying tests
chore    # Maintenance, deps update
build    # Build system changes
ci       # CI configuration changes
```

**Message format rules:**
- Imperative mood ("add" not "added")
- Keep description under 50 characters
- No period at end of description
- Add body for complex changes
- Reference issues in footer (Fixes #123)

**Present proposal to user:**
```
Commit message: feat(auth): add user login

Files to commit:
- src/auth/login.js
- src/auth/middleware.js

Body: Implemented JWT-based authentication with refresh tokens.

Approve this commit? (y/n)
```

## 7. Execute Git Operations

```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage all files in directory
git add path/to/directory/

# Stage interactively (review each hunk)
git add -i

# Stage with patch (review each change)
git add -p

# Create commit with message
git commit -m "feat(auth): add user login"

# Verify commit was created
git log -1 --stat

# Show commit details
git show HEAD
```

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

**Example:**
```bash
feat(auth): add user login

Implemented JWT-based authentication with refresh tokens.
Includes secure password hashing.

BREAKING CHANGE: authentication API now requires Bearer token

Fixes #123
```

## Troubleshooting

```bash
# Unstage files if user rejects commit
git restore --staged path/to/file

# Discard changes if user wants to start over
git restore path/to/file

# View last commit if need to amend
git log -1

# Amend last commit (if user wants to modify)
git commit --amend
```

## When to Use This Skill

- Creating a git commit from working tree changes
- Reviewing changes before committing
- Grouping related files into logical commits
- Writing standardized commit messages
- Verifying commit content before pushing
