---
name: general-creating-skill
description: Creates new skill directories, defines skill workflows with proper structure, and adds guides to the skills repository. Use when creating or updating agent skills.
---

# Creating a Skill

This guide provides instructions for creating a new skill in the skills repository.

## 1. Plan the Skill

Identify the workflows and scope of the new skill:

```bash
# List existing skills to understand patterns
ls

# Read a well-structured skill for reference
cat nuttx-makefile-build/SKILL.md | head -100
```

Determine if the skill is:
- **Tech-stack specific** (e.g., `nuttx-`, `wamr-`)
- **General-purpose** (prefix with `general-`)

## 2. Create Skill Directory

```bash
# Create the skill directory with proper naming
mkdir -p {skill-name}

# Verify the directory was created
ls
```

Naming rules:
- Use **kebab-case** (lowercase with hyphens)
- Include domain prefix (`nuttx-`, `wamr-`, or `general-`)
- 1-64 characters, no leading/trailing/consecutive hyphens
- Must match the `name` field in SKILL.md frontmatter

## 3. Write SKILL.md Frontmatter

Create the SKILL.md file with YAML frontmatter:

```yaml
---
name: skill-name
description: Describes what the skill does and when to use it. Use when [specific triggering conditions].
---
```

**Required fields:**
- `name` (1-64 chars, lowercase letters, numbers, hyphens only, no leading/trailing/consecutive hyphens)
- `description` (1-1024 chars, must describe both what the skill does and when to use it)

**Optional fields:**
- `license` - License name or reference to license file
- `compatibility` - Environment requirements (max 500 chars)
- `metadata` - Arbitrary key-value mapping
- `allowed-tools` - Space-delimited list of pre-approved tools

**Description best practices:**
- Describe both what the skill does and when to use it
- Include searchable keywords for task identification
- Keep it concise but informative

**Good example:**
```yaml
description: Builds NuttX firmware with CMake for faster compilation and better dependency tracking. Use when building NuttX or managing multiple build configurations.
```

## 4. Write Skill Content

Structure the skill with numbered workflows:

```markdown
# Skill Title

## 1. First Workflow

```bash
# Complete, copy-pasteable commands
command --option value

# Comments explain why
```

## 2. Second Workflow

```bash
# More commands
command1
command2
```

## 3. Third Workflow

```bash
# Additional steps
command --flag
```
```

**Content guidelines:**
- Prioritize numbered workflow sections over explanatory text
- Make workflows copy-pasteable and complete
- Use realistic paths (`path/to/project`, not absolute paths)
- Include common options (`-j8`, `| tail -n 100`)
- Add inline comments to explain why

## 5. Add Quick Reference Sections

Include these sections if applicable:

```markdown
## Build Output Management

**NuttX builds generate 1000+ lines of output.** Commands use `| tail -n 100` to limit output.

## Configuration Syntax

```
CONFIG_PATTERN=value
```

Brief explanation of syntax components.

## Advanced Options

```bash
# Additional configuration options
command --advanced-flag
```
```

## 6. Add Troubleshooting Section

```markdown
## Troubleshooting

```bash
# Common issues and solutions
command --debug
```
```

## 7. Add When to Use Section

```markdown
## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3
```

## 8. Update README.md (If Applicable)

If adding a new skill category:

```markdown
# Update directory structure section
```
general-creating-agents-files/
general-creating-skill/     # New skill
nuttx-*/                     # Tech-stack specific skills
README.md
```

## 9. Reference Existing Skills

When creating a skill that relates to others:

```markdown
This skill requires the nuttx-config-management skill.

Related skills:
- nuttx-config-management - For modifying configurations
- nuttx-makefile-build - For building with make
```

## Common Mistakes to Avoid

1. **Too much prose** - Convert explanations to workflows showing "what" to do
2. **Missing context** - Mention prerequisites and required skills
3. **Incomplete workflows** - Each workflow should be end-to-end
4. **Overly specific paths** - Use generic paths
5. **Vague descriptions** - Be specific in skill descriptions, include what it does and when to use it
6. **Missing optional fields** - Add license, compatibility, or metadata when appropriate

## Skill Review Checklist

- [ ] YAML frontmatter has valid `name` (1-64 chars, lowercase, hyphens)
- [ ] Directory name matches frontmatter `name` field
- [ ] Description describes both what the skill does and when to use it
- [ ] Description includes searchable keywords (1-1024 chars)
- [ ] Main workflows are numbered sequentially
- [ ] Each workflow is complete and copy-pasteable
- [ ] Minimal descriptive text (focus on workflows)
- [ ] Troubleshooting section with actionable commands
- [ ] "When to Use" section with clear criteria
- [ ] Referenced skills exist
- [ ] Optional fields added when appropriate (license, compatibility, metadata)
- [ ] File is under 500 lines (spec recommendation)
