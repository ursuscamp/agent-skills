---
name: spec-design
description: Defines the format and structure for technical design documentation
---

## What I do

When you create or update a `design.md` file for a feature specification, follow this exact structure. This skill ensures designs are thorough, implementable, and consider cross-cutting concerns. Adapt the terminology to fit your project type (API, CLI, library, embedded system, etc.).

## Required Sections

Every `design.md` MUST include these sections in order:

### 1. Title

```markdown
# [Feature Name] - Technical Design
```

### 2. Architecture Overview

High-level description of how this feature fits into the system. Include:
- Component diagram description (if applicable)
- Data flow summary
- Key architectural decisions
- How this feature interacts with existing system parts

### 3. Interface Design

Document how this feature exposes its functionality. **Keep interfaces shallow** - describe what the interface does, not how it does it. No implementation details.

| Interface | Input | Output | Description |
|-----------|-------|--------|-------------|
| createUser | `{ name, email }` | `{ id, created }` | Creates a new user |
| deleteUser | `id: UUID` | `{ success }` | Deletes a user by ID |

Include:
- Function/method signatures only (no bodies)
- Command syntax (for CLI tools)
- Protocol messages (for IPC/networking)
- Request/response formats
- Parameter types and constraints

### 4. Data Models

Document the data structures this feature uses:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| name | String | NOT NULL, max 255 | Display name |
| createdAt | DateTime | NOT NULL | Creation timestamp |

Apply this to:
- Database schemas
- Configuration files
- Message formats
- Structs/classes
- File formats

#### Schema Changes

If modifying existing models:
- New fields added
- Fields modified (migration/conversion needed)
- Fields deprecated

### 5. Key Components

Describe each major component/module. **Keep descriptions shallow** - focus on responsibilities and interface signatures, not implementations. For complex algorithms, use pseudo-code.

```markdown
### UserService

**Responsibilities:**
- User lifecycle management
- User data validation
- Event publishing on user actions

**Public API:**
- `create(input: CreateUserInput): Promise<User>`
- `findById(id: string): Promise<User | null>`
- `delete(id: string): Promise<void>`

**Algorithm Example (if complex):**
\`\`\`
function calculatePriority(user):
  baseScore = user.reputation * 0.5
  recencyBonus = now() - user.lastActive < 7 days ? 10 : 0
  return baseScore + recencyBonus
\`\`\`

**Dependencies:**
- UserRepository
- EventBus
- Validator
```

### 6. User Interaction

Describe how users interact with this feature:

#### Invocation Patterns
- Direct function call
- Command-line command
- API/RPC call
- Message/event consumption
- UI interaction

#### Flows
- Step-by-step interaction sequence
- Input sources and destinations
- Error states and recovery paths

#### Input/Output Examples
\`\`\`markdown
# CLI example
$ myapp user create --name "John" --email "john@example.com"
Created user: 550e8400-e29b-41d4-a716-446655440000

# API example
$ curl -X POST /users -d '{"name": "John"}'
{"id": "550e8400-e29b-41d4-a716-446655440000"}
\`\`\`
```

### 7. External Dependencies

| Dependency | Purpose | Version/Notes |
|------------|---------|---------------|
| database | Persistent storage | PostgreSQL 14+ |
| cache | Fast access storage | Redis 6+ |
| logger | Structured logging | Winston |
| auth-provider | Authentication | OAuth 2.0 |

Include:
- External services
- Libraries/packages
- System resources (filesystem, network, etc.)

### 8. Error Handling

| Error Code | Condition | Error Data | Recovery |
|------------|-----------|------------|----------|
| INVALID_INPUT | Input validation fails | `{ field, message }` | Show error, request valid input |
| NOT_FOUND | Resource doesn't exist | `{ resource, id }` | Return empty, prompt to create |
| CONFLICT | Resource already exists | `{ resource, identifier }` | Offer to update existing |
| UNAUTHORIZED | Missing permissions | `{ action }` | Redirect to auth |
| UNAVAILABLE | Service unavailable | `{ service }` | Retry with backoff |

Include:
- Error types and codes
- Error payloads
- Recovery strategies
- Logging requirements

### 9. Security

| Concern | Approach |
|---------|----------|
| Authentication | Verify caller identity |
| Authorization | Check permissions before action |
| Input Sanitization | Validate and sanitize all inputs |
| Secrets | Never log sensitive data |
| Access Control | Principle of least privilege |

Tailor to your system:
- For APIs: token-based auth, rate limiting
- For libraries: input validation, safe defaults
- For CLI: secure storage for credentials
- For systems: resource limits, isolation

### 10. Configuration

Configuration options this feature needs:

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| timeout | number | no | 5000 | Operation timeout in ms |
| maxRetries | number | no | 3 | Maximum retry attempts |
| connectionString | string | yes | - | Database connection |

Include:
- Environment variables
- Config file options
- Runtime flags
- Secrets management approach

### 11. Component Interactions

How components communicate:

```markdown
# Synchronous (function calls)
UserController → UserService → UserRepository → Database

# Asynchronous (events/messages)
UserService → EventBus → NotificationService → EmailProvider
```

Include:
- Call flow diagrams (text-based)
- Message formats for async communication
- Protocol choices (REST, gRPC, message queue, events)
- Timeout and retry expectations

### 12. Platform Considerations

If this feature runs on multiple platforms:

| Platform | Consideration | Approach |
|----------|---------------|----------|
| Linux | File paths | Use XDG dirs |
| macOS | File paths | Use ~/Library |
| Windows | File paths | Use AppData |

- Path conventions
- Platform-specific dependencies
- Conditional code paths

### 13. Trade-offs

Document architectural decisions and trade-offs:

```markdown
**Decision**: Use synchronous processing over async

**Reasoning**: 
- Simpler to reason about and debug
- Lower latency for user-facing operations
- Team has less experience with async patterns

**Impact**: 
- May struggle with high-throughput scenarios
- Can scale vertically before needing horizontal scaling
```

### 14. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-------------|
| External service failure | Medium | High | Circuit breaker, fallback to cached/default |
| Data migration complexity | Low | High | Automated migration scripts, rollback plan |
| Performance at scale | Medium | Medium | Load testing, monitoring, capacity planning |

## Quality Guidelines

1. **Be implementable** - A fellow developer should be able to build from this
2. **Cover edge cases** - Error states, race conditions, boundary conditions
3. **Be specific** - Use actual field names, types, values
4. **Document rationale** - Don't just say what, say why
5. **Consider testing** - Include test strategy per component
6. **Adapt to context** - Use appropriate terminology for your project type
7. **Keep it shallow** - Describe interfaces, not implementations. Use pseudo-code for complex algorithms. A design doc should tell a developer *what* to build, not *how* to build it.
