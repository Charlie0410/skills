---
name: send-completion-reminder
description: Send a reminder email with `C:\Program Files\self\send_reminder.exe` after Codex finishes the user's requested work while otherwise following the existing instructions normally. Use when the user wants the task to proceed without intervention, changes to the workflow, or extra reminder-specific coordination, and only wants an email sent at the end.
---

# Purpose

Complete the user's task under the active system, developer, repository, and user instructions as usual. Treat the reminder as a final post-task step only.

## Workflow

1. Execute the requested work normally.
2. Do not change the planning process, tool usage, validation flow, or response style because this skill is active.
3. Do not interrupt the task just to acknowledge, announce, or coordinate the reminder.
4. When the task work is finished and immediately before the final user-facing response, run:

```powershell
& 'C:\Program Files\self\send_reminder.exe' --subject "<subject>" --body "<body>"
```

5. Send the reminder exactly once for the completed task.

## Reminder Content

Write a short subject and body that match the actual outcome.

Guidelines:

1. Keep the subject concise and status-oriented.
2. Summarize what was completed in the body.
3. Mention any important limitation, blocker, or unfinished portion when relevant.
4. Include enough context for the email to be useful on its own.

## Constraints

1. Do not interfere with the main instructions.
2. Do not add reminder-specific confirmation steps unless a higher-priority instruction requires them.
3. Do not send the reminder before the task is actually finished.
4. Do not claim success, completion, or file changes that did not happen.
5. Use the exact executable path `C:\Program Files\self\send_reminder.exe`.

## Failure Handling

1. If the reminder command fails, do not retry in a loop.
2. Still provide the normal final response for the task.
3. Note the reminder failure briefly in the final response if the email could not be sent.
