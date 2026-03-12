---
name: bug-report
description: Defines the format and structure for bug report documentation
---

## What I do

When you create or update a `bug-report.md` file, follow this exact structure. This skill ensures bug reports are complete, reproducible, and provide enough context to implement a fix.

## Required Sections

Every `bug-report.md` MUST include these sections in order:

### 1. Title

```markdown
# [Bug ID]: [Brief description of the bug]
```

### 2. Summary

2-3 sentence overview of the bug - what it is and why it matters.

### 3. Severity

Choose one with justification:

| Level | Criteria |
|-------|----------|
| Critical | Data loss, security breach, entire app unusable |
| High | Major feature broken, workaround difficult |
| Medium | Feature impaired, workaround exists |
| Low | Minor issue, cosmetic, easy workaround |

Format:
```markdown
## Severity: [Level]

- Justification and impact
- Number of users affected (if known)
- Workaround available (if any)
```

### 4. Environment

Document where the bug occurs:

| Field | Value |
|-------|-------|
| App Version | |
| OS | |
| Browser / Device | |
| Backend Version | |
| Database | |

### 5. Reproduction Steps

Numbered, step-by-step instructions to reproduce the bug. Must be reproducible.

Format:
```markdown
## Reproduction Steps

1. [First step]
2. [Second step]
3. [Third step]
```

### 6. Expected Behavior

What should happen after the reproduction steps.

### 7. Actual Behavior

What actually happens - be specific about error messages, UI state, etc.

### 8. Impact

- User impact (frustration, blocked work, data issues)
- Frequency (every time? intermittent? rare?)
- Business impact if unfixed

### 9. Root Cause

Investigation findings:
- What is causing the bug
- Code location(s) if identified
- Why it's happening

Format:
```markdown
## Root Cause

[Description of the root cause]

Location: `path/to/file:line-number`
```

### 10. Solution Approach

How to fix it:
- Option considered
- Chosen approach and reasoning
- Alternative approaches that were rejected (and why)

```markdown
## Solution Approach

**Chosen**: [Brief description]

**Reasoning**: 
- [Reason 1]
- [Reason 2]

**Rejected alternatives**:
- [Alternative 1]: Rejected because [reason]
```

### 11. Code Changes

Specific files and changes needed:

| File | Change | Description |
|------|--------|-------------|
| `src/auth.ts` | Modify | Update token validation logic |
| `src/utils.ts` | Add | New helper function |

### 12. Edge Cases

What else might be affected, other scenarios to test:
- What happens with invalid input?
- Are there related features that might break?
- What about edge cases (empty data, max values, etc.)?

## Quality Guidelines

1. **Be reproducible** - Someone else should be able to follow your steps and see the bug
2. **Be specific** - Include exact error messages, line numbers, values
3. **Document investigation** - What did you try? What did you find?
4. **Consider testability** - How will you verify the fix works?

## Example

```markdown
# BUG-001: Login button does nothing on mobile

## Summary
Clicking the login button has no effect on mobile devices due to missing touch event handler, preventing ~15% of users from logging in on mobile.

## Severity: Medium

- Affects ~15% of users (mobile traffic)
- Workaround: use desktop browser
- Not a security issue

## Environment

| Field | Value |
|-------|-------|
| App Version | 2.1.0 |
| iOS | 16.x |
| Android | 12 |
| Browser | Safari, Chrome |

## Reproduction Steps

1. Open app on mobile device (iOS or Android)
2. Navigate to login page
3. Tap the login button
4. Observe: nothing happens
5. Expected: login form should appear

## Expected Behavior
Login button tap should open the login form on all devices.

## Actual Behavior
On mobile devices, tapping the login button does nothing. No error, no form appears.

## Impact
- ~15% of users cannot log in on mobile
- Users must switch to desktop to use the app
- Negative reviews on app stores

## Root Cause

The LoginButton component only binds `onClick` events, not touch events. Mobile browsers handle taps differently - they may fire touch events or delayed click events, and our tap handler is missing.

Location: `src/components/LoginButton.tsx:23`

## Solution Approach

**Chosen**: Add `onTouchEnd` handler that calls the same handler as `onClick`

**Reasoning**: 
- Simplest fix with minimal code changes
- Maintains existing behavior for desktop
- No breaking changes

**Rejected alternatives**:
- Replace onClick with onPointerUp: Would require testing all click behaviors, higher risk

## Code Changes

| File | Change | Description |
|------|--------|-------------|
| `src/components/LoginButton.tsx` | Modify | Add onTouchEnd handler |

## Edge Cases
- Verify double-tap prevention still works (no double submission)
- Test on tablet devices
- Verify desktop click behavior unchanged
- Test with assistive technologies (VoiceOver, TalkBack)
```
