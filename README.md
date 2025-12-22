# Skills

Skills are directories containing domain-specific knowledge and guides for performing particular tasks. Each skill is organized by directory path and uses markdown files to describe detailed instructions and usage patterns.

## Directory Structure

```
skills/
├── nuttx/
│   ├── applications/
│   ├── drivers/
│   │   ├── sensors/
│   │   └── gpio-expanders/
│   └── boards/
└── wamr/
    └── compilation/
```

## Naming Conventions

All directories and files under `skills/` follow consistent naming rules:

### Directory Names
- Use **kebab-case** (lowercase letters with hyphens separating words)
- First-level directory: domain name (e.g., `nuttx`, `wamr`)
- Subdirectories: category or subcategory names (e.g., `applications`, `drivers`, `sensors`)

### File Names
- Use **kebab-case** with `.md` extension
- Descriptive and self-explanatory (e.g., `creating-applications.md`, `out-of-tree-board-creation.md`)
- Use action verbs when appropriate (e.g., `creating-`, `compiling-`)

### Path Structure Pattern
```
skills/{domain}/{category}/{subcategory}/{descriptive-name}.md
```
- `{domain}`: Top-level category (e.g., `nuttx`, `wamr`)
- `{category}`: Primary topic area (e.g., `applications`, `drivers`, `boards`, `compilation`)
- `{subcategory}`: Optional nested category for grouping (e.g., `sensors`, `gpio-expanders`)
- `{descriptive-name}.md`: Concise, hyphenated description of the guide's content

## How to Pick a Proper Skill File

To find the appropriate skill guide for your task:

1. **Identify the domain** - Determine which top-level domain your task belongs to (e.g., `nuttx` for RTOS-related tasks, `wamr` for WebAssembly-related tasks)

2. **Navigate the category hierarchy** - Browse through the domain subdirectories to find the relevant category:
   - `applications/` - For creating and managing NuttX applications
   - `drivers/` - For implementing hardware drivers (sensors, GPIO expanders, etc.)
   - `boards/` - For board creation, configuration, and defconfig management
   - `compilation/` - For compilation and optimization guides

3. **Read the descriptive filename** - Each skill file has a self-explanatory name that clearly indicates its purpose. For example:
   - `creating-sensor-drivers.md` - Guide for creating sensor drivers
   - `wamrc-aot-compilation.md` - Guide for AOT compilation with wamrc
   - `out-of-tree-board-creation.md` - Guide for creating custom boards

The hierarchical organization and descriptive naming make it straightforward to locate the right guide for your specific task.
