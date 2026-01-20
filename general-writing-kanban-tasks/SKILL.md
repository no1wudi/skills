---
name: general-writing-kanban-tasks
description: Creates clear kanban task titles and descriptions that include environment setup, problem/symptoms, goal/definition of done, affected scope, verification plan (with a discovery step if commands are unknown), and a completion report to paste back into the task. Use when creating or updating kanban tasks for engineering work.
---

# Writing Kanban Tasks

This skill standardizes kanban task content so tasks are executable, scoped, and verifiable.

## Core Rules

1. **Actionable**: Every task must have a clear definition of done and a verification plan.
2. **Dependency-light**: Prefer tasks that can proceed independently (no reliance on other tasks).
3. **Split when needed**: If work naturally depends on something else, recommend follow-up tasks that are each independently actionable.
4. **Facts vs guesses**: Keep observed behavior separate from hypotheses.
5. **Close the loop**: Before finishing work, fill in the task's completion summary block.

## 1. Create a Task (Workflow)

### Step 1: Write a Good Title

Use: `verb + object + qualifier`.

Good:
- Fix `<component>` crash when `<condition>`
- Add `<feature>` to `<area>` behind `<flag>`
- Investigate `<symptom>` in `<service>`

Avoid:
- "Update stuff"
- "Investigate issue" (missing symptom/area)

### Step 2: Fill in the Description Template

Paste this into the kanban task description and fill in what you know.

```text
Context / Env Setup
- Repo/workdir:
- Branch/revision:
- Tooling/runtime:
- Config/flags:
- Constraints: (no network, read-only, etc.)

Inputs Required (So Work Can Start)
- Logs/errors:
- Repro steps / sample input:
- Access/credentials needed: (names only)
- Where to find config/flags:

Problem / Symptom
- Observed:
- Expected:
- Evidence: (exact error text, logs, links, screenshots, file paths)

Goal (Definition of Done)
- Must:
  - <measurable outcome>
  - <measurable outcome>
- Non-goals:
  - <explicitly out of scope>

Affected Range (Scope)
- In scope: (dirs/modules/interfaces)
- Out of scope: (areas to avoid)
- Risk/impact notes: (compat/perf/security/data migrations)

Prereqs (Dependency-Light)
- Assumes: (stable, already-existing things)
- Hard dependencies: NONE intended
- If a hard dependency is discovered:
  - Propose follow-up tasks (see format below)
  - Continue with any independent work in this task

Verification Plan
- If commands are unknown, discovery step:
  - Identify canonical commands for: build, lint/format, test
  - Record them here once found
- Checks to run:
  - <command> (expected: <result>)
  - <command> (expected: <result>)
- Manual validation steps (if applicable):
  1) <step>
  2) <step>

Completion Summary (Fill this in before finishing)
- Outcome: Fixed | Root cause found (fix pending) | Not reproduced | Needs info
- Repro steps: (final minimal repro, or "not found")
- Root cause: (if known)
- Narrowed scope: (files/modules/conditions)
- Hypotheses (ranked): (if root cause not proven)
- What changed: (fixes and/or debug instrumentation)
- Verification results: (commands + results, or "not run" + why)
- Follow-ups/risks: (concrete next steps)
```

### Step 3: If the Task Is Too Big, Split It

Default target size: medium (about 1-3 days). If it exceeds that, split into multiple tasks where each task is independently actionable and has its own DoD + verification.

When you create multiple kanban tasks from one complex effort, number them in the task titles so the set is easy to track.

Title format:
- `Task <i>/<n>: <short specific title>`

Example:
- `Task 1/3: Add parser for <format>`
- `Task 2/3: Wire parser into <pipeline>`
- `Task 3/3: Add tests and verification docs`

Use this follow-up proposal format inside the current task:

```text
Follow-up Task Proposals
1) Title: Task 1/<n>: ...
   Goal/DoD: ...
   Scope: ...
   Verify: ...
2) Title: Task 2/<n>: ...
   Goal/DoD: ...
   Scope: ...
   Verify: ...
```

## 2. Systematic Discovery (When the Problem Is Unknown)

Use this workflow when you have symptoms but no confirmed root cause.

The agent is allowed to run commands and make small, scoped debug/instrumentation patches when needed. Keep discovery changes tight and reversible.

### Discovery Protocol

1) Restate the symptom precisely
- What fails, where, how often, under what conditions
- Define what a "successful investigation" returns (even if not fixing)

2) Reproduce (or confirm non-repro)
- Attempt reproduction with provided steps
- If no repro exists, construct minimal repro steps
- Record exact commands, inputs, env, and observed output

3) Minimize and isolate
- Reduce to smallest failing case (input/config/flag)
- Narrow to subsystem/module/file range
- If feasible, narrow to a regression window (last-known-good)

4) Instrument and observe
- Add temporary logging/assertions/metrics to confirm code paths and invariants
- Prefer feature-flagged or clearly removable instrumentation
- Avoid refactors during discovery

5) Form hypotheses and test them
- Maintain top 2-3 hypotheses, each with evidence and a falsification test
- Run the smallest experiment that discriminates between hypotheses

6) Converge on an outcome
- If root cause found: propose fix approach + verification plan
- If root cause not found: publish a reliable repro (or explicit non-repro), narrowed scope, ranked hypotheses, and next steps

## 3. Verification Guidance (Generic)

Prefer a verification plan that is executable by any assignee.

- If commands are known, include them with expected outcomes.
- If commands are unknown, include a discovery step that results in recording:
  - build command
  - test command(s)
  - lint/format command (if applicable)
- If verification cannot be run in the current environment, include a manual plan and what outputs/logs to capture.

## When to Use This Skill

- Creating a new kanban task that must be actionable without extra context.
- Turning a vague request into a scoped task with DoD + verification.
- Writing investigation tasks where the root cause is not yet known.

## Quick Checklist

- [ ] Title is specific and scoped
- [ ] Context/Env includes constraints and required inputs
- [ ] Goal contains measurable DoD and explicit non-goals
- [ ] Scope lists in-scope and out-of-scope areas
- [ ] Verification plan exists (or includes discovery step)
- [ ] Task is dependency-light; otherwise includes follow-up task proposals
- [ ] Completion summary block is present and filled at finish
