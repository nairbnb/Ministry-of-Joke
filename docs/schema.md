# MoJ Schema Decisions — ICEX_MJ03

## Models

### User

| Field         | Type         | Nullable | Notes                  |
| ------------- | ------------ | -------- | ---------------------- |
| id            | Integer      | False    | Primary Key            |
| username      | String(80)   | False    | Unique identifier      |
| password_hash | String(256)  | False    | Hashed password        |
| jokes         | Relationship | True     | Backref to Joke author |

### Joke

| Field        | Type        | Nullable | Notes                        |
| ------------ | ----------- | -------- | ---------------------------- |
| id           | Integer     | False    | Primary Key                  |
| text         | String(500) | False    | Joke content                 |
| submitted_by | Integer     | False    | Foreign Key to user.id       |
| created_at   | DateTime    | False    | Timestamp (default: UTC now) |

## Data Capture Decisions

### Fields captured in v1 that are not displayed in v1

For each field below, explain: (1) what it enables, (2) why it cannot be reconstructed later.

- `submitted_by`:  
  Enables user attribution and future per-user analytics, leaderboards, and moderation workflows.
  Cannot be reconstructed after insertion — once a joke is stored without a user link,
  the association is permanently lost. The capture cost is minimal (one FK column).
  This is a deliberate MVP exception: MVP governs what features we build,
  not what data we can never recover.
- `created_at`:
  Enables chronological sorting, audit trails, and future trending analysis.
  Cannot be reconstructed from any other data source — system timestamps are only accurate at insertion time.
  Like submitted_by, this is a foundational field that must exist from v1
  to support any future timeline-based features.

## Deferred Fields

Fields explicitly excluded from v1 with a known migration path:

- `quality_score`: deferred to Cycle 3 (Ollama integration). Will be added via `flask db migrate`.
