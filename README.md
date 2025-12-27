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
   description: Create uORB-based sensor drivers in NuttX with publish/subscribe pattern, character device creation, and standardized data structures.
   ---
   ```

4. **Use the skill tool** - Load skills dynamically using the skill tool:
   ```bash
   skill nuttx-creating-sensor-drivers
   ```

The domain-prefixed naming and descriptive skill names make it straightforward to locate the right guide for your specific task.


