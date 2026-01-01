---
name: general-creating-skill
description: Use when creating a new skill directory, defining a skill workflow, or adding a new guide to the skills repository.
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

## 3. Write SKILL.md Frontmatter

Create the SKILL.md file with YAML frontmatter:

```yaml
---
name: skill-name
description: Use when [specific triggering conditions]. Keep it focused on WHEN to use, not WHAT the skill does.
---
```

**Description best practices:**
- Start with "Use when..."
- Describe triggering conditions and symptoms
- Include searchable keywords
- Keep under 200 characters

**Good example:**
```yaml
description: Use when building NuttX with CMake for faster compilation or managing multiple build configurations.
```

**Bad example (summarizes workflow):**
```yaml
description: Build NuttX using CMake with Ninja backend for faster builds and better dependency tracking.
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

## 8. Validate the Skill

Verify quality standards:

```bash
# Check YAML frontmatter is valid
head -5 {skill-name}/SKILL.md

# Verify directory name matches frontmatter name
skill_name=$(grep "^name:" SKILL.md | cut -d' ' -f2)
dir_name=$(basename $(pwd))
if [ "$skill_name" != "$dir_name" ]; then
  echo "ERROR: skill name '$skill_name' does not match directory name '$dir_name'"
fi

# Check description starts with "Use when..."
if ! grep -q "^description: Use when" SKILL.md; then
  echo "ERROR: description must start with 'Use when...'"
fi

# Count lines (aim for 150-250)
wc -l SKILL.md
```

## 9. Update README.md (If Applicable)

If adding a new skill category:

```markdown
# Update directory structure section
```
general-creating-agents-files/
general-creating-skill/     # New skill
nuttx-*/                     # Tech-stack specific skills
README.md
```

## 10. Reference Existing Skills

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
5. **Vague descriptions** - Be specific in skill descriptions
6. **Workflow summaries in descriptions** - Describe WHEN to use, not HOW it works

## Skill Review Checklist

- [ ] YAML frontmatter has valid `name` and `description`
- [ ] Directory name matches frontmatter `name` field
- [ ] Skill description starts with "Use when..."
- [ ] Description focuses on triggering conditions (not workflow)
- [ ] Main workflows are numbered sequentially
- [ ] Each workflow is complete and copy-pasteable
- [ ] Minimal descriptive text (focus on workflows)
- [ ] Troubleshooting section with actionable commands
- [ ] "When to Use" section with clear criteria
- [ ] Referenced skills exist
- [ ] File is 150-250 lines (unless domain requires more)
