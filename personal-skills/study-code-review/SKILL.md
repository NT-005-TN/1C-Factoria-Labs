---
name: study-code-review
description: Review study code for correctness, tests, maintainability, and common security risks without rewriting the project unless requested.
---

# Study Code Review

Review the code against the assignment rather than an imagined production system.

1. Read the task, expected inputs and outputs, and existing tests.
2. Reproduce the build or test result when the environment permits.
3. Prioritize findings that cause wrong output, crashes, data loss, insecure input handling, or missing requirements.
4. Check boundaries, empty inputs, invalid data, duplicate operations, and state changes.
5. Verify that tests assert behavior rather than implementation details.
6. Give each finding a precise file and line, consequence, and practical correction.
7. Separate confirmed defects from suggestions and questions.

Do not edit the code during a review unless the user also asks for fixes.
