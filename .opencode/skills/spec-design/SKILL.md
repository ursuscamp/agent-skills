---
name: spec-design
description: Defines the format and structure for technical design documentation
---

## What I do

When you create or update a `design.md` file for a feature specification, follow this exact structure. This skill ensures designs are thorough, implementable, and consider cross-cutting concerns.

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

### 3. API Design

Table format for all endpoints:

| Method | Path | Request Body | Response | Description |
|--------|------|--------------|----------|-------------|
| POST | /api/users | `{ "name": "string" }` | `{ "id": "uuid" }` | Create a user |

Include:
- HTTP methods and paths
- Request/response schemas (JSON)
- Query parameters
- HTTP status codes
- Error responses

### 4. Data Models

#### Database Schema

Table format for tables/collections:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique identifier |
| name | VARCHAR(255) | NOT NULL | User's display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

#### Schema Changes

If modifying existing models:
- New fields added
- Fields modified (migration needed)
- Fields deprecated

### 5. Key Components

Describe each major component/module:

```markdown
### AuthService

**Responsibilities:**
- User authentication
- Token generation and validation
- Session management

**Public API:**
- `authenticate(credentials: Credentials): Promise<AuthToken>`
- `validateToken(token: string): Promise<User>`
- `revokeToken(token: string): Promise<void>`

**Dependencies:**
- UserRepository
- JWT library
```

### 6. User Interface

Describe UI/UX design:

#### Layout Structure
- Page sections
- Navigation flow
- Responsive breakpoints

#### User Flows
- Step-by-step interaction sequence
- User actions and system responses
- Error states and recovery

#### Visual Design (if applicable)
- Component library to use
- Styling approach
- Accessibility requirements

### 7. External Dependencies

| Dependency | Purpose | Version/Notes |
|------------|---------|---------------|
| Stripe API | Payment processing | v3 API |
| SendGrid | Email delivery | Transactional only |

Include:
- Third-party services
- External APIs
- Libraries/packages

### 8. Error Handling

| Error Code | Condition | Response | User Message |
|------------|-----------|----------|--------------|
| 400 | Invalid input | `{ "error": "VALIDATION_ERROR", "details": [...] }` | "Please check your input" |
| 401 | Unauthorized | `{ "error": "UNAUTHORIZED" }` | "Please log in" |
| 404 | Not found | `{ "error": "NOT_FOUND", "resource": "user" }` | "User not found" |
| 500 | Server error | `{ "error": "INTERNAL_ERROR" }` | "Something went wrong" |

Include:
- HTTP status codes
- Error response schemas
- Client-side error handling
- Retry logic

### 9. Security

| Concern | Approach |
|---------|----------|
| Authentication | JWT tokens with 1hr expiry |
| Authorization | Role-based: admin, user |
| Data at rest | AES-256 encryption |
| Data in transit | TLS 1.3 |
| Input validation | Zod schemas |
| Rate limiting | 100 req/min per user |

### 10. Configuration

Environment variables or config keys needed:

| Key | Type | Required | Default | Description |
|-----|------|----------|---------|-------------|
| STRIPE_API_KEY | string | yes | - | Stripe secret key |
| WEBHOOK_SECRET | string | yes | - | Webhook verification |

### 11. Trade-offs

Document architectural decisions and trade-offs:

```markdown
**Decision**: Use polling instead of WebSockets for real-time updates

**Reasoning**: 
- Team has limited WebSocket experience
- Lower traffic expected (< 100 updates/min)
- Simpler deployment (no sticky sessions)

**Impact**: 
- Max 5-second delay in updates
- Higher server load at scale
```

### 12. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-------------|
| Third-party API downtime | Medium | High | Implement circuit breaker, fallback to cached data |
| Database migration locks table | Low | High | Use online migration tool, schedule maintenance window |

## Quality Guidelines

1. **Be implementable** - A fellow developer should be able to build from this
2. **Cover edge cases** - Error states, race conditions, edge cases
3. **Be specific** - Use actual field names, paths, values
4. **Document rationale** - Don't just say what, say why
5. **Consider testing** - Include test strategy per component
