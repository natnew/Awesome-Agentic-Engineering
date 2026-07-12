# Skill: ask-user

## Metadata

| Field       | Value                                                                 |
| :---------- | :-------------------------------------------------------------------- |
| **Name**    | ask-user                                                              |
| **Version** | 1.0.0                                                                 |
| **Status**  | stable                                                                |
| **Author**  | natnew                                                                |
| **Last reviewed** | July 2026                                                      |

---

## Description

Reusable pattern for presenting the user with explicit choices and gating
execution until they respond. Used by other skills when a decision point
requires human input before proceeding. Platform-agnostic — works on
Telegram (inline buttons), Discord, CLI, or any agent with a message tool.

---

## Triggers

This skill activates when any of the following conditions are true:

- Another skill reaches a decision point that requires human confirmation
  before a potentially irreversible or high-impact action.
- The calling skill cannot safely choose a default without knowing the
  user's intent (e.g. overwrite vs. skip, approve vs. reject, branch name
  selection).
- An upstream workflow passes `require_human_gate: true` in its context.
- The agent detects ambiguity in the user's original request that cannot
  be resolved from prior conversation context.
- A destructive operation is about to be performed and no prior explicit
  consent has been recorded in the current session.

---

## Priority Fields and Contract

| Priority | Field             | Type      | Required | Description                                               |
| :------- | :---------------- | :-------- | :------- | :-------------------------------------------------------- |
| P0       | `prompt`          | `string`  | Yes      | The question text presented to the user.                  |
| P0       | `choices`         | `array`   | Yes      | Ordered list of `{ label, value, description? }` objects. |
| P0       | `caller_skill`    | `string`  | Yes      | Name of the skill that invoked ask-user.                  |
| P1       | `default`         | `string`  | No       | The `value` to use if the user does not respond.          |
| P1       | `timeout_seconds` | `integer` | No       | Seconds before `default` is applied. `0` = no timeout.   |
| P1       | `allow_freetext`  | `boolean` | No       | Whether to accept an answer outside the listed choices.   |
| P2       | `destructive`     | `boolean` | No       | Flags the decision as destructive; adds a warning prefix. |
| P2       | `context_snippet` | `string`  | No       | Optional context shown below the prompt.                  |

**Return contract** — the skill resolves with:

```json
{
  "selected_value": "<value from choices or freetext>",
  "selected_label": "<display label>",
  "source": "user | default | timeout",
  "elapsed_seconds": 12
}
```

Callers must not proceed if `selected_value` is `null` and no `default`
was supplied.

---

## What This Is

ask-user is a **synchronous human-in-the-loop gate**. It pauses agent
execution, surfaces a structured choice to the user on whatever channel
the agent runs on, and waits for a response before returning control to
the caller.

It is not a free-form conversation starter. It is not a polling loop. It
is a single, bounded decision point with a fixed set of expected outcomes.

The skill owns only the presentation and response-handling logic. Business
logic (what to do with the answer) remains with the calling skill.

---

## When to Use

- Before deleting, overwriting, or publishing content that cannot be
  easily undone.
- When a workflow branches on a user preference that cannot be inferred
  from prior messages (e.g. "merge now or open a draft PR?").
- When two or more downstream actions are mutually exclusive and roughly
  equally plausible.
- When another skill's contract requires explicit opt-in (e.g. a skill
  that sends an email or posts to a channel).
- When the agent must record a human decision as an audit trail entry.

---

## When Not to Use

- When the answer can be inferred with high confidence from recent
  context — prefer silent inference and log the assumption.
- When the call would interrupt a fully automated, scheduled, or headless
  pipeline where no human is present. Supply a `default` and set
  `timeout_seconds` instead, or skip the gate entirely.
- When you only need the user's attention or confirmation of a
  non-consequential action. Use a status message instead.
- When choices exceed seven items. Split into sub-questions or use a
  different interaction pattern.
- When the operation is idempotent and can be retried safely without user
  involvement.
- As a substitute for proper error handling or missing logic.

---

## How to Present Choices

1. **One question per invocation.** Never combine two decision points into
   a single ask-user call.
2. **Label each choice with a short, action-oriented phrase** (≤ 6 words).
   Avoid vague labels like "OK" or "Yes".
3. **Provide a `description`** for any choice where the consequence is not
   obvious from the label alone.
4. **Order choices logically**: safe/default first, destructive last.
5. **Mark the default** visually (e.g. `[default]` suffix) when one exists.
6. **Flag destructive choices** with a ⚠️ prefix in the label.

### Platform rendering

| Platform          | Rendering mechanism               | Notes                                   |
| :---------------- | :-------------------------------- | :-------------------------------------- |
| Telegram          | `InlineKeyboardMarkup` buttons    | Labels ≤ 64 chars; no `description`     |
| Discord           | Interaction components (buttons)  | Max 5 buttons per row; use embeds       |
| CLI               | Numbered list + `stdin` prompt    | Full `description` shown                |
| Agent message API | Formatted list in message body    | Use numbered options if no button API   |
| GitHub PR comment | Checkbox list or reply instruction| User replies with option number or text |

---

## Constraints

- **Maximum choices per call:** 7.
- **Maximum prompt length:** 280 characters.
- **Maximum label length:** 64 characters.
- **Maximum description length per choice:** 120 characters.
- **Nesting depth:** ask-user must not invoke ask-user recursively.
- **Side effects:** ask-user must not write to state, call external APIs,
  or perform file I/O. It is a pure presentation-and-wait pattern.
- **Concurrency:** only one ask-user gate may be active per conversation
  session at a time. Queue additional gates if needed.

---

## How to Gate

The gate mechanism pauses the calling skill's execution context until
`ask-user` resolves. Implementation varies by runtime:

### Async / event-driven runtimes

```
caller_skill:
  1. Build the ask-user input payload.
  2. Call await ask_user(payload) — suspends the coroutine.
  3. ask-user posts the prompt and registers a callback/handler.
  4. On user response, the handler validates and resolves the awaitable.
  5. Caller resumes with the resolved value.
```

### Stateless / webhook runtimes

```
caller_skill:
  1. Build the ask-user input payload.
  2. Persist current execution state to a state store with a unique gate_id.
  3. Trigger ask-user with gate_id.
  4. ask-user posts the prompt and tags the message with gate_id.
  5. User responds; webhook handler routes the response to the gate_id.
  6. ask-user writes the resolved value to the state store.
  7. Caller workflow re-invokes from the persisted checkpoint.
```

In both cases, the caller must treat a `null` response (no default,
timeout elapsed, or user dismissed) as an abort signal and surface a
clear explanation to the user.

---

## How to Handle the Response

1. **Validate the response** against the `choices` array. Reject any value
   not in `choices` unless `allow_freetext: true`.
2. **Normalise case and whitespace** before comparison.
3. **Log the decision** — record `selected_value`, `source`, `caller_skill`,
   and `elapsed_seconds` to the session audit trail.
4. **Return the resolved struct** to the calling skill without further
   interpretation.
5. **On timeout with a default**: apply the default, set `source: timeout`,
   and notify the user that the default was applied.
6. **On timeout without a default**: abort the calling operation, set
   `source: timeout`, `selected_value: null`, and return a human-readable
   abort message.
7. **On invalid freetext** (when `allow_freetext: false`): re-present the
   choices once. If the user responds with invalid input a second time,
   abort and return `null`.

---

## Formatting Guidelines

- Begin the prompt with a capitalised sentence ending in `?`.
- Do not use markdown inside button labels on Telegram or Discord;
  use plain text only.
- In CLI and message-body contexts, wrap the prompt in a visual
  delimiter (e.g. a horizontal rule or `---`) to separate it from
  prior output.
- Number options starting from `1` in text-only contexts.
- Always include a "Cancel / do nothing" choice unless the operation
  is irreversible and cancellation has already occurred upstream.
- For destructive gates, prepend the prompt with:
  `⚠️ This action cannot be undone. Please confirm.`

---

## Examples

### Example 1 — Overwrite confirmation (CLI)

**Input payload**

```json
{
  "prompt": "A file named report.md already exists. What should I do?",
  "choices": [
    { "label": "Skip (keep existing)", "value": "skip" },
    { "label": "Overwrite", "value": "overwrite", "description": "Replaces the existing file permanently." },
    { "label": "Rename new file", "value": "rename" },
    { "label": "Cancel", "value": "cancel" }
  ],
  "caller_skill": "file-writer",
  "default": "skip",
  "timeout_seconds": 60,
  "destructive": true
}
```

**Rendered output (CLI)**

```
---
⚠️ This action cannot be undone. Please confirm.
A file named report.md already exists. What should I do?

  1. Skip (keep existing) [default]
  2. ⚠️ Overwrite — Replaces the existing file permanently.
  3. Rename new file
  4. Cancel

Enter a number (1–4), or press Enter to accept the default:
---
```

**Resolved return value**

```json
{
  "selected_value": "skip",
  "selected_label": "Skip (keep existing)",
  "source": "user",
  "elapsed_seconds": 8
}
```

---

### Example 2 — PR action gate (GitHub PR comment)

**Input payload**

```json
{
  "prompt": "Review complete. How should I proceed?",
  "choices": [
    { "label": "Approve and merge", "value": "merge" },
    { "label": "Request changes", "value": "request_changes" },
    { "label": "Leave as draft", "value": "draft" },
    { "label": "Do nothing", "value": "noop" }
  ],
  "caller_skill": "pr-review",
  "default": "noop",
  "timeout_seconds": 0
}
```

**Rendered output (PR comment)**

```
Review complete. How should I proceed?

1. Approve and merge
2. Request changes
3. Leave as draft
4. Do nothing [default]

Reply with the number of your choice.
```

---

### Example 3 — Telegram inline buttons

**Input payload**

```json
{
  "prompt": "Send the weekly digest now?",
  "choices": [
    { "label": "Send now", "value": "send" },
    { "label": "Schedule for tomorrow", "value": "schedule" },
    { "label": "Cancel", "value": "cancel" }
  ],
  "caller_skill": "digest-sender",
  "destructive": false,
  "timeout_seconds": 300,
  "default": "cancel"
}
```

**Rendered output (Telegram)**

```
Send the weekly digest now?

[ Send now ] [ Schedule for tomorrow ] [ Cancel ]
```

---

## Destructive Commands

When `destructive: true` is set, ask-user applies the following additional
safeguards:

1. Prepend the visual warning prefix to the prompt regardless of platform.
2. If a destructive choice is present, move it to the last position in the
   rendered list.
3. Do not set a `default` to a destructive choice value. If the caller
   attempts this, ask-user must override `default` to `"cancel"` and log
   a warning.
4. Require the user to confirm a second time if the first response selects
   a destructive value and `timeout_seconds > 0`. The second confirmation
   uses a minimal yes/no prompt:
   - "Are you sure? This cannot be undone. (yes / cancel)"
5. Record both confirmations in the audit trail.

---

## Integration with Other Skills

ask-user is designed to be composed into larger skills and workflows.
Calling conventions:

### Invoking ask-user from another skill

```yaml
# Skill manifest excerpt
dependencies:
  - ask-user@^1.0.0

steps:
  - name: Gate on deployment target
    skill: ask-user
    input:
      prompt: "Which environment should I deploy to?"
      choices:
        - { label: "Staging", value: "staging" }
        - { label: "Production", value: "production" }
        - { label: "Cancel", value: "cancel" }
      caller_skill: "{{ skill.name }}"
      default: "cancel"
      destructive: false
    output_binding: deployment_gate
```

### Consuming the result

```yaml
  - name: Deploy
    condition: "{{ deployment_gate.selected_value != 'cancel' }}"
    skill: deploy
    input:
      target: "{{ deployment_gate.selected_value }}"
```

### Skills that commonly integrate ask-user

| Skill              | Typical gate                                       |
| :----------------- | :------------------------------------------------- |
| `file-writer`      | Overwrite / skip / rename on conflict              |
| `pr-review`        | Approve / request changes / leave draft            |
| `digest-sender`    | Send now / schedule / cancel                       |
| `entry-draft`      | Publish to README / save draft / discard           |
| `repo-agent`       | Triage action: label / close / request changes     |
| `deploy`           | Environment selection before irreversible push     |

---

## Anti-Patterns

| Anti-pattern                              | Why it fails                                                                           |
| :---------------------------------------- | :------------------------------------------------------------------------------------- |
| Using ask-user for informational messages | Creates unnecessary friction; use a status/log message instead.                        |
| Nesting ask-user inside ask-user          | Creates confusing UX and breaks the single-gate-per-session constraint.                |
| Setting a destructive action as `default` | Risk of unintended data loss on timeout or accidental Enter press.                     |
| Offering more than 7 choices              | Cognitive overload; split into sub-questions or use a hierarchical selection pattern.  |
| Re-using ask-user as a conversation loop  | ask-user is a gate, not a dialogue manager; use a dedicated conversation skill.        |
| Omitting a cancel option                  | Traps the user; always provide an escape unless cancellation is impossible at this point. |
| Presenting technical jargon in labels     | Users should not need to understand internals to make a decision.                      |
| Calling ask-user in headless pipelines    | Blocks execution indefinitely with no one present; always supply `default` + timeout.  |
| Silently applying a default without notice| Surprising and untrustworthy; always notify the user when a default is applied.        |
| Interpreting the answer inside ask-user   | Business logic belongs in the calling skill, not the gate.                             |

---

## Output Format

All responses from ask-user conform to the following JSON schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AskUserResponse",
  "type": "object",
  "required": ["selected_value", "selected_label", "source", "elapsed_seconds"],
  "properties": {
    "selected_value": {
      "type": ["string", "null"],
      "description": "The `value` from the chosen option, or null if aborted."
    },
    "selected_label": {
      "type": ["string", "null"],
      "description": "The human-readable label of the chosen option."
    },
    "source": {
      "type": "string",
      "enum": ["user", "default", "timeout"],
      "description": "How the value was determined."
    },
    "elapsed_seconds": {
      "type": "integer",
      "minimum": 0,
      "description": "Seconds between prompt display and response resolution."
    },
    "audit_id": {
      "type": ["string", "null"],
      "description": "Opaque ID of the audit trail entry, if logging is active."
    }
  },
  "additionalProperties": false
}
```

Callers receive this object and must not rely on any additional fields
beyond those defined above.
