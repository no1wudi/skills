# Skills

Skills are directories containing domain-specific knowledge and guides for performing particular tasks. Each skill is organized as a directory with a `SKILL.md` file containing YAML frontmatter for OpenCode skill discovery.

## Directory Structure

```
skills/
├── general-creating-agents-files/
│   └── SKILL.md
├── general-creating-skills/
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
- `{domain}`: Technology domain prefix (e.g., `nuttx`, `wamr`, or `general` for general-purpose skills)
- `{descriptive-name}`: Hyphenated description of the skill's purpose
- Example: `skills/nuttx-creating-sensor-drivers/SKILL.md`
