---
name: study-skill-builder
description: Create or improve a reusable Codex skill for a repeated study or personal workflow, with focused triggers, instructions, and validation.
---

# Study Skill Builder

Create a skill only when a repeated workflow benefits from reusable non-obvious guidance.

1. Collect two or three realistic requests that should trigger the skill.
2. Define the outcome, boundaries, required inputs, and actions that still need user authorization.
3. Choose a lowercase hyphenated name under 64 characters.
4. Create a folder with a required `SKILL.md` containing YAML `name` and `description`.
5. Make the description specific enough to distinguish the skill from similar workflows.
6. Keep essential routing and constraints in `SKILL.md`; move substantial conditional details to `references/`.
7. Add scripts only when deterministic repetition is valuable, and test every script.
8. Remove placeholders, validate the frontmatter, and test the skill on a realistic request.
9. Revise rules only from observed failures, not hypothetical edge cases.

Do not copy proprietary or private skills into a public repository. Write original
instructions and exclude tokens, internal URLs, personal data, and environment-specific secrets.
