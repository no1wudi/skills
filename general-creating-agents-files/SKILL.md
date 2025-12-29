---
name: general-creating-agents-files
description: Use when establishing project-specific guidelines for AI assistants, defining command patterns, documenting critical rules, or creating documentation to ensure consistent agent behavior across a codebase.
---

# Creating AGENTS.md Files

This guide provides instructions for creating AGENTS.md files that provide effective agent instructions.

## Purpose

AGENTS.md files contain instructions for AI assistants working in specific domains or subdomains. These files define project context, command patterns, and critical rules that guide behavior when performing tasks.

## File Structure

A well-structured AGENTS.md file contains the following standard sections:

### 1. Domain Header

A clear heading that identifies the domain:

```markdown
# Agent Guidelines for <Domain Name>
```

**Examples**:
- `# Agent Guidelines for NuttX Codebase`
- `# Agent Guidelines for WAMR Applications`

### 1. Project Overview

A brief introduction explaining what the project is and any critical constraints:

```markdown
## Project Overview
This is a <brief description>. All code changes must be built and tested by the user manually - never attempt to run or test code automatically.
```

**Purpose**: Sets context and immediately establishes critical constraints.

**Example from main AGENTS.md**:
```markdown
## Project Overview
This is a NuttX embedded project. All code changes must be built and tested by the user manually - never attempt to run or test code automatically.
```

### 2. Project Layout

A structured list of directories and their purposes:

```markdown
## Project Layout

- `directory1` - Description of this directory
- `directory2` - Description of this directory
  - `subdirectory` - Description of this subdirectory
- `directory3` - Description of this directory
```

**Purpose**: Helps agents understand the codebase structure and quickly locate relevant files.

**Example from main AGENTS.md**:
```markdown
## Project Layout

- `nuttx` - Core NuttX RTOS source code including kernel, drivers, and architecture-specific implementations
- `nuttx-apps` - Application code and examples for NuttX, including system applications and user programs
- `boards` - Contains your custom BSP (Board Support Package) with board-specific configurations, hardware abstraction layers
- `skills` - Skill modules with guidance for specialized tasks
- `reference` - READ ONLY, reference materials and guides for specialized tasks
```

### 3. Essential Commands

Commands that agents will frequently use, organized by category:

```markdown
## Essential Commands

### Category Name
- `command` - Description of what the command does
- `command` - Description of what the command does

### Another Category
- `command` - Description of what the command does
```

**Purpose**: Provides quick reference for common commands, reducing the need to search through documentation.

**Common categories**:
- Build System
- Code Quality
- Git Usage
- Command Execution
- Testing
- Debugging

**Example from main AGENTS.md**:
```markdown
## Essential Commands

### Build System
- `make -C nuttx -j32` - Build the current project
- `kconfig-tweak --file nuttx/.config --enable CONFIG_<OPTION>` - Enable features
- `kconfig-tweak --file nuttx/.config --disable CONFIG_<OPTION>` - Disable features
- `kconfig-tweak --file nuttx/.config --set-str CONFIG_<OPTION> "<value>"` - Set string values
- `make -C nuttx olddefconfig` - Update configuration and validate changes

### Code Quality
- `nuttx/tools/checkpatch.sh -f <file>` - Style check files under nuttx and nuttx-apps directories
  - **Note**: Skip checkpatch for files under `nuttx-apps/external/*` - these are third-party codebases that follow their own coding style conventions
```

#### Command Documentation Guidelines

When documenting commands:

1. **Use backticks for inline commands**: `make -C nuttx -j32`
2. **Provide clear, concise descriptions**: "Build the current project" (not "This command builds the current project")
3. **Include placeholders in angle brackets**: `CONFIG_<OPTION>`, `<file>`
4. **Add notes for important exceptions or caveats**
5. **Organize commands logically** (e.g., by function, by workflow)

### 4. Critical Rules

The most important rules that agents must follow:

```markdown
## Critical Rules
1. **Rule description**
2. **Another rule description**
3. **Yet another rule description**
```

**Purpose**: Emphasizes rules that must never be violated. These typically represent fundamental constraints or safety requirements.

**Example from main AGENTS.md**:
```markdown
## Critical Rules
1. **NEVER test or run code** - This is embedded firmware that must be burned to hardware
2. **Follow existing code patterns** when making changes
3. **Check style** with checkpatch.sh before completing tasks
```

## Writing Guidelines

### Clear, Unambiguous Instructions

The most important quality of an AGENTS.md file is clarity. Instructions must be unambiguous to ensure agents behave correctly.

#### Be Specific

**Good**: "Always use the `workdir` parameter in bash commands instead of using `cd` commands."

**Bad**: "Try to use workdir when possible."

#### Use Concrete Examples

When explaining concepts, provide specific examples:

**Good**:
```markdown
**Examples**:
```bash
# Good: Use workdir parameter
<tool workdir="nuttx" command="make -j32" />

# Bad: Avoid cd chains
<tool command="cd nuttx && make -j32" />
```
```

**Bad**: "For example, you could use workdir='nuttx' when running commands."

#### Avoid Ambiguous Language

Avoid words like:
- "Try to" → Use "Always" or "Must"
- "If possible" → Specify the condition explicitly
- "Usually" → Define when the rule applies
- "Sometimes" → Specify the exact conditions

**Good**: "All git commands must specify the correct working directory."

**Bad**: "Usually you want to specify the working directory for git commands."

#### Define Command Syntax Clearly

When documenting tool invocations, show the exact format:

```markdown
<tool workdir="directory" command="command" />
```

For bash commands:
```markdown
<tool command="your command here" />
```

For file operations:
```markdown
<tool file="path/to/file" />
```

#### Explain Why, Not Just What

Provide context for rules and commands:

**Good**:
```markdown
The current working directory is **not** a git repository.
```

**Better**:
```markdown
The current working directory is **not** a git repository. Always use the `workdir` parameter to specify which repository to operate in.
```

### Formatting Best Practices

1. **Use consistent heading levels**: H1 for title, H2 for main sections, H3 for subsections
2. **Use lists for command documentation**: Clear, scannable format
3. **Use code blocks for commands**: Backticks preserve formatting
4. **Use bold for emphasis**: `**NEVER**`, `**ALWAYS**`, `**Important**`
5. **Keep descriptions concise**: One-line descriptions for commands when possible

## Domain-Specific Customization

### When to Customize

Customize the AGENTS.md structure based on:

1. **Project type**: Embedded systems, web applications, data pipelines - each has different constraints
2. **Build system**: Make, CMake, Gradle, npm - different command patterns
3. **Development workflow**: Git, multiple repositories, monorepo - different repository handling
4. **Safety requirements**: Production code, firmware, security-critical systems - different rules

### Common Customizations

#### Embedded Systems Projects

Typical additions:
- Hardware-specific constraints
- Flashing/burning commands
- Hardware testing procedures
- Power management rules

#### Web Applications

Typical additions:
- Development server commands
- Database migration commands
- Deployment procedures
- API testing guidelines

#### Data Pipelines

Typical additions:
- Data validation rules
- Pipeline execution commands
- Monitoring and alerting
- Rollback procedures

#### Multi-Repository Projects

Typical additions:
- Clear mapping of repositories to functions
- Inter-repository dependency rules
- Coordinated change procedures

**Example from main AGENTS.md (multi-repository)**:
```markdown
### Git Usage

The project consists of multiple separate git repositories. **Always specify the correct working directory for bash tool** when running git commands.

The following directories are individual git repositories:
- `nuttx`
- `nuttx-apps`
- `boards`
- `skills`

Note: `reference` is read-only and not a git repository.

The current working directory is **not** a git repository.
```

### Subdomain AGENTS.md Files

For large domains, create subdomain-specific AGENTS.md files:

```
domain/
├── AGENTS.md          # Domain-level guidelines
└── subdomain/
    └── AGENTS.md      # Subdomain-specific extensions
```

Subdomain AGENTS.md should:
1. Reference the parent domain AGENTS.md for general rules
2. Add subdomain-specific commands and rules
3. Override parent rules if necessary (with explanation)
4. Focus on the specific subdomain context

## Validation Checklist

Before finalizing an AGENTS.md file, verify:

1. **Completeness**: Are all relevant sections present?
2. **Clarity**: Are instructions unambiguous?
3. **Accuracy**: Are commands correct and tested?
4. **Examples**: Are there concrete examples for complex concepts?
5. **Consistency**: Is formatting consistent throughout?
6. **Relevance**: Does it match the actual project structure and workflow?
7. **Criticality**: Are the most important rules emphasized?

## Reference Examples

### Minimal AGENTS.md Template

```markdown
# Agent Guidelines for <Domain Name>

## Project Overview
<One or two sentences describing the project and key constraints>

## Project Layout

- `directory1` - Description
- `directory2` - Description
- `directory3` - Description

## Essential Commands

### Build System
- `command` - Description

### Code Quality
- `command` - Description

## Critical Rules
1. **Rule 1** - Explanation
2. **Rule 2** - Explanation
3. **Rule 3** - Explanation
```

For a complete example, see the main `AGENTS.md` file at the root of this project.
