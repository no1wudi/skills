# Skills

Skills are directories containing domain-specific knowledge and guides for performing particular tasks. Each skill is organized as a directory with a `SKILL.md` file containing YAML frontmatter for OpenCode skill discovery.

## Directory Structure

```
skills/
├── creating-agents-files/
│   └── SKILL.md
├── nuttx-cmake-build/
│   └── SKILL.md
├── nuttx-config-management/
│   └── SKILL.md
├── nuttx-makefile-build/
│   └── SKILL.md
├── nuttx-creating-applications/
│   └── SKILL.md
├── wamr-aot-compilation/
│   └── SKILL.md
├── ...
└── README.md
```

## Naming Conventions

All skill directories under `skills/` follow consistent naming rules:

### Skill Directory Names
- Use **kebab-case** (lowercase letters with hyphens separating words)
- Include domain prefix for disambiguation (e.g., `nuttx-creating-applications`, `wamr-aot-compilation`)
- 1-64 characters, no leading/trailing hyphens, no consecutive hyphens

### Skill File Names
- Must be named `SKILL.md` (all caps)
- Contains YAML frontmatter with `name` and `description` fields
- All original markdown content preserved below frontmatter

### Path Structure Pattern
```
skills/{domain}-{descriptive-name}/SKILL.md
```
- `{domain}`: Technology domain prefix (e.g., `nuttx`, `wamr`, or omitted for general skills)
- `{descriptive-name}`: Hyphenated description of the skill's purpose
- Example: `skills/nuttx-creating-sensor-drivers/SKILL.md`

## How to Pick a Proper Skill File

To find the appropriate skill guide for your task:

1. **Identify the domain** - Determine which domain your task belongs to by looking for domain prefixes:
   - `nuttx-*` - For NuttX RTOS-related tasks (applications, boards, drivers)
   - `wamr-*` - For WebAssembly Micro Runtime tasks
   - No prefix - For general-purpose skills (e.g., `creating-agents-files`)

2. **Browse available skills** - List the skills directory to see all available skills:
   ```bash
   ls skills/
   ```

3. **Read skill descriptions** - Each skill's `SKILL.md` frontmatter includes a description:
    ```yaml
    ---
    name: nuttx-creating-sensor-drivers
    description: Use when adding support for new I2C or SPI sensors like accelerometers, gyroscopes, magnetometers, or barometers, or when implementing sensor drivers that publish data via the uORB framework.
    ---
    ```

4. **Use the skill tool** - Load skills dynamically using the skill tool:
   ```bash
   skill nuttx-creating-sensor-drivers
   ```

The domain-prefixed naming and descriptive skill names make it straightforward to locate the right guide for your specific task.

## How to Write a Skill

### Skill File Structure

Each `SKILL.md` file follows this structure:

```yaml
---
name: skill-name
description: Use when [specific triggering conditions and symptoms]. Keep it focused on WHEN to use, not WHAT the skill does.
---

# Skill Title

## Build Output Management (if applicable)

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output...

## Configuration Syntax (if applicable)

```
<configuration-pattern>
```

Brief explanation of syntax components.

### Description Best Practices

The `description` field is critical for skill discovery. It should:

**DO:**
- Start with "Use when..." to focus on triggering conditions
- Describe specific situations, symptoms, or contexts that signal the skill applies
- Include searchable keywords (error messages, tool names, file paths)
- Be technology-agnostic unless the skill IS technology-specific
- Keep descriptions under 200 characters if possible

**DON'T:**
- Summarize the skill's workflow or process (this causes Claude to take shortcuts)
- Use first person ("I can help you with...")
- Be overly abstract ("For async testing")
- Include implementation details ("using CMake with Ninja backend")

**Good Example:**
```yaml
description: Use when building NuttX with CMake for faster compilation, managing multiple build configurations, or setting up out-of-tree build directories.
```

**Bad Example (summarizes workflow):**
```yaml
description: Build NuttX RTOS firmware using the modern CMake build system with Ninja backend for faster builds and better dependency tracking.
```

The key insight: Claude reads the description to decide whether to load the skill. If the description summarizes the workflow, Claude may follow that summary instead of reading the full skill content.

## Essential Workflows

### 1. Workflow Name

```bash
# Clear, actionable commands
command --option value

# Comments explain why
```

### 2. Another Workflow

```bash
# Complete, copy-pasteable sequences
command1
command2
```

## Advanced Options (if applicable)

```bash
# Additional configuration options
command --advanced-flag
```

## Troubleshooting

```bash
# Common issues and solutions
command --debug
```

## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3
```

### Writing Guidelines

**1. Focus on Workflows, Not Descriptions**

- Prioritize numbered workflow sections over explanatory text
- Make workflows copy-pasteable and complete
- Remove redundant explanations and lengthy prose

**Good:**
```markdown
### 3. Apply Configuration Changes

```bash
# Modify .config using kconfig-tweak
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO

# Apply changes and rebuild
make olddefconfig
make -j8
```

**Bad:**
```markdown
### 3. Applying Configuration Changes

In this section, we will discuss how to apply configuration changes to your NuttX build. First, you need to use kconfig-tweak to modify the configuration file. After modifying the configuration, you should apply the changes using make olddefconfig, and then rebuild the system using make -j8. This process ensures that...
```

**2. Number Workflows Sequentially**

- Use numbered sections (1, 2, 3...) for main workflows
- Keep workflow names action-oriented: "Find Configurations", "Build Firmware", "Apply Changes"
- Include all necessary steps in each workflow

**3. Keep Commands Practical**

- Use realistic paths (`path/to/nuttx`, `path/to/build`)
- Include common options (`-j8`, `| tail -n 100`)
- Add inline comments to explain why commands are needed

**4. Minimize Descriptive Sections**

- Remove feature comparison tables
- Avoid lengthy introductions
- Skip "What is..." or "How it works" sections
- Keep troubleshooting focused on commands

**5. Use Consistent Formatting**

- Code blocks for all commands
- Consistent spacing in examples
- Clear section hierarchy (# for title, ## for main sections, ### for workflows)

**6. Reference Related Skills**

- Mention other skills when needed (e.g., "requires nuttx-config-management skill")
- Avoid duplicating content across skills
- Keep each skill focused on its domain

**7. Provide Quick Reference Sections**

- Build Output Management (if applicable) - for tail command usage
- Configuration Syntax - for parameter patterns
- Advanced Options - for less common features

### Examples to Follow

**Well-structured skills:**
- `nuttx-makefile-build/SKILL.md` - 8 numbered workflows, minimal description
- `nuttx-cmake-build/SKILL.md` - 11 numbered workflows, action-focused

**Key characteristics:**
- 150-250 lines total
- 6-15 numbered workflows
- Commands ready to copy-paste
- Clear "When to Use" section

### Common Mistakes to Avoid

1. **Too much prose** - If a section explains "how" something works, convert it to a workflow showing "what" to do
2. **Missing context** - Don't assume readers know prerequisites; mention required skills
3. **Incomplete workflows** - Each workflow should be end-to-end (configure → build → verify)
4. **Overly specific paths** - Use generic paths like `path/to/nuttx`, not `/home/user/projects/my-custom-nuttx-fork`
5. **Outdated information** - Keep content aligned with current project practices
6. **Vague descriptions** - Be specific in skill descriptions
7. **Workflow summaries in descriptions** - The description should describe WHEN to use, not HOW it works (e.g., "Use when building with CMake" not "Build with CMake using Ninja backend")

### Skill Review Checklist

Before committing a new skill, verify:

- [ ] YAML frontmatter has valid `name` and `description`
- [ ] Directory name matches frontmatter `name` field
- [ ] **Skill description starts with "Use when..."** and focuses on triggering conditions
- [ ] **Description does NOT summarize the workflow or process** (only describes when to use)
- [ ] Main workflows are numbered sequentially
- [ ] Each workflow is complete and copy-pasteable
- [ ] Minimal descriptive text (focus on workflows)
- [ ] Troubleshooting section includes actionable commands
- [ ] "When to Use" section provides clear criteria
- [ ] Referenced skills exist
- [ ] File is 150-250 lines (unless domain requires more)

### Creating a New Skill

1. **Plan the skill** - Identify workflows and scope
2. **Create directory** - Follow naming convention
3. **Write SKILL.md** - Use the structure above
4. **Test workflows** - Verify commands work
5. **Review checklist** - Ensure quality standards
6. **Commit** - Follow project commit conventions


