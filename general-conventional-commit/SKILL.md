---
name: general-conventional-commit
description: Use when writing or reviewing git commit messages that follow the Conventional Commits specification for standardized, machine-readable commit history.
---

# Writing Conventional Commit Messages

## Format

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

## Types

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

**Version mapping:** `feat`→MINOR, `fix`→PATCH, `BREAKING CHANGE`→MAJOR

## Scopes

Add scope in parentheses to specify affected module:
```bash
feat(auth): add password reset
fix(database): resolve connection leak
docs(readme): update instructions
```

Scopes can be: module name, component, file/directory, or layer (frontend/backend)

## Description & Body

**Description rules:**
- Use imperative mood ("add" not "added")
- Keep under 50 characters
- No period at the end
- Start lowercase

**When to add body:**
- Complex changes needing explanation
- Why the change was made
- Technical details or performance impact

```bash
feat(search): implement fuzzy search

Fuzzy matching now uses Levenshtein distance with configurable
threshold. Improves search accuracy by 40% for typo-heavy queries.

Performance: ~10ms overhead per query
```

## Breaking Changes & Issues

**Breaking changes:** Add at the start of footer:
```bash
BREAKING CHANGE: environment variables now take precedence over config files
BREAKING CHANGE: removed deprecated `user.getProfile()` method
```

**Issue references in footer:**
```bash
Fixes #123    # Closes and resolves
Closes #456   # Alternative to Fixes
Refs #789     # References without closing
Related: #100 # Related but not directly fixing
```

## Git Commands

```bash
# Create commit
git commit -m "feat(api): add user endpoint"

# Multi-line message
git commit -m "feat(api): add user endpoint

- GET /users/{id}
- POST /users

Closes #123"

# Amend last commit
git commit --amend -m "feat(auth): fix token expiration bug"

# Interactive rebase to edit messages
git rebase -i HEAD~3
```

## When to Use This Skill

- Writing any git commit message
- Reviewing pull requests for proper commit structure
