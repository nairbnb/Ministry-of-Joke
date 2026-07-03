# MoJ Schema Decisions — ICEX_MJ03

## Models

### User
| Field | Type | Nullable | Notes |
|---|---|---|---|
| `id` | Integer | No | Primary key, auto-increment. Identifies each user row. |
| `username` | String(80) | No | Unique login name (`unique=True`). Human-readable identifier. |
| `password_hash` | String(256) | No | Stores the hashed password only — never plaintext. Excluded from `__repr__` to avoid leaking it into logs. |
| `jokes` | relationship → Joke | — | ORM relationship, not a stored column. One-to-many; `backref='author'` exposes `joke.author`. |

### Joke
| Field | Type | Nullable | Notes |
|---|---|---|---|
| `id` | Integer | No | Primary key, auto-increment. Identifies each joke row. |
| `text` | String(500) | No | The joke body. Capped at 500 characters. |
| `submitted_by` | Integer (FK → `user.id`) | No | Foreign key to the authoring user. Establishes the User→Joke one-to-many link. |
| `created_at` | DateTime | No | UTC creation timestamp. Defaults to `datetime.utcnow` on insert — no client input required. |

## Data Capture Decisions

### Fields captured in v1 that are not displayed in v1
For each field below, explain: (1) what it enables, (2) why it cannot be reconstructed later.

- `submitted_by`: `submitted_by: We store the author link even though v1 never shows who wrote a joke. If we skip it, the link between a joke and its author is lost forever — there is no other source to rebuild it from. The cost is tiny: one column and one foreign key. It enables future features like attribution, leaderboards, or per-user stats, all of which need this link to exist from the very first joke. MVP (Minimum Viable Product) limits the features we build, not the data we can never get back.
- `created_at`: `We store the creation time even though v1 never displays it. The moment a joke is inserted is the only time we can know its true creation time — miss it, and it's gone for good. The cost is just one DateTime column that fills itself automatically (datetime.utcnow), so the client sends nothing extra. It enables future features like newest-first ordering, time-based feeds, or analytics — and these need every row to have a timestamp. If we add the column later, only new jokes get dated and every older joke stays blank forever. Same rule as above: MVP limits features, not unrecoverable data.

## Deferred Fields
Fields explicitly excluded from v1 with a known migration path:

- `quality_score`: Postponed to Cycle 3 (Ollama integration). Nothing in v1 creates or uses a quality score, so adding it now would just leave an empty, unused column. Unlike the two fields above, a score can be recomputed anytime later from the joke's text, so waiting costs us nothing. We'll add it safely to existing rows with flask db migrate -m "add quality_score" then flask db upgrade.