#### ICEX_MJ01: Founding the Ministry

- **Date:** 2026-03-03
- **Team Members Present:** `@adolata`, `@lvatista`, `@jampete`, `@bl35`
- **Roles:**
  - Repo Admin: `@jampete`
  - Process Lead: `@adolata`
  - Dev Lead: `@lvatista`
  - QA Sentinel: `@bl35`
- **Summary of Work:** Established the MoJ Flask skeleton with GET /jokes and POST /jokes
  routes, wrote the first pytest test using GIVEN/WHEN/THEN format, and set up the
  Engineering Log repos for all team members.

- **Planted Problem:**
  - **What was the problem?** There was an import error while importing test module.
  - **How did the team identify it?** We ran pytest tests/ -v we found an import module error, no module named "app" and an issue from the command"from app import create app"
  - **How was it resolved?** We needed to add a -m before the pytest, so the final command should have been (depending on version) python3 -m pytest tests/ -v whcih runs the python test through the python module interface, which handles path resolution.

- **Forward hook:** Next session (ICEX_MJ02), your team's runners will have different
  operating systems. Before class, make sure every team member's self-hosted runner
  is installed and shows as **Idle** in the repo's runner list.

---

# ICEX_MJ02: The Silliness Detector

- **Date:** 2026-03-05
- **Team Members Present:** `@lvatista`, `@bl35`, `@crmoll`
- **Roles:**
  - Repo Admin: `@crmoll`
  - Process Lead: `@crmoll`
  - Dev Lead: `@bl35`
  - QA Sentinel: `@lvatista`
- **OS Inventory:**
  - `@crmoll` — [macOS Tahoe + 26.0.1]
  - `@lvatista` — [macOS Tahoe + 20.3]
  - `@bl35` — [Windows 11 + 25H2]
- **Runner that picked up the first push:** `@bl35` (Windows 11)
- **Summary of Work:** Configured self-hosted runners on all team members' laptops,
  wired up the GitHub Actions CI workflow, diagnosed and fixed the heterogeneous
  environment problem.

- **Planted Problem:**
  - **What was the problem?** The workflow failed with "Exit Code 127" (Command not found) and "Permission Denied" errors on macOS, while passing on Windows.
  - **Which runners failed / which passed?** Windows 11 passed; macOS (14.x) failed initially.
  - **Diagnostic process:** Checked job logs; identified that `pip` wasn't in the Mac runner's path and the `setup-python` action was attempting to write to the unauthorized `/Users/runner` directory.
  - **Fix applied:** Added `actions/setup-python@v5` with `python-version: "3.12"` to the `ci.yml` to make the environment explicit and standardized across all OS types. Created the `/Users/runner/hostedtoolcache` directory locally on the Mac to bypass the permission bug.

- **Forward hook:** Your CI pipeline now runs tests on every push. Next session
  (ICEX_MJ03), your data moves out of a Python list and into a real database.
  Think about what your CI pipeline will need to know about the database
  before the tests can run against it

---

# ICEX_MJ03: The Official Ledgers

- **Date:** 2026-03-10
- **Team Members Present:** `@lvatista`, `@bl35`, `@adolata`, `@crmoll`
- **Roles:**
  - Repo Admin: `@lvatista`
  - Process Lead: `@bl35`
  - Dev Lead: `@adolata`
  - QA Sentinel: `@crmoll`
- **Summary of Work:** Defined User and Joke SQLAlchemy models, wired the App Factory
  pattern with Flask-Migrate, initialized the database, and documented schema decisions
  including deliberate data capture choices for v1.

## Planted Problem

- **What was the problem?**
  We cannot import name 'db' from partially initialized module 'app' (most likely due to a circular import).
  This was the error I was getting when running flask db init
- **How did the team identify it?**
  We ran pytest tests/test_db_init.py, traced the import chain, and found a circular dependency between app/models.py and app/init.py.
- **How was it resolved?**
  We moved db = SQLAlchemy() into app/models.py, removed from app import db, and kept app/init.py importing db from app.models.

## Forward Hook

Your schema is the foundation every future ICEX builds on. Next week (ICEX_MJ04),
you will write tests that verify this schema behaves correctly under valid input,
boundary conditions, and invalid input — at all three levels of the test taxonomy.
The decisions you documented today in `docs/schema.md` are the behaviors you will
be testing tomorrow.

# ICEX_MJ04: Upgrading the Detector

- **Date:** 2026-03-12
- **Team Members Present:** `@adolata`, `@bl35`, `@crmoll`, `@jampete`
- **Roles:**
  - Repo Admin: `@crmoll`
  - Process Lead: `@adolata`
  - Dev Lead: `@bl35`
  - QA Sentinel: `@jampete`
- **Summary of Work:** Added a parallel flake8 linting CI job; wrote a
  three-level test suite for POST /jokes using GIVEN/WHEN/THEN format;
  ran pytest --cov and observed coverage output.

## Planted Problem

- **What was the problem?**
  No Planted Problem Today
- **How did the team identify it?**
  N/A
- **How was it resolved?**
  N/A

## Coverage Output

========================================== tests coverage ===========================================
\_ coverage: platform win32, python 3.12.10-final-0 \_\_

## Name Stmts Miss Cover Missing

app**init**.py 11 0 100%
app\models.py 19 2 89% 15, 26
app\routes\jokes.py 14 0 100%

---

TOTAL 44 2 95%

## Individual Extension Route Assignments

| Team Member | Claimed Route / Function                                                        |
| ----------- | ------------------------------------------------------------------------------- |
| `@crmoll`   | def test_submit_joke_valid(client):                                             |
| `@adolata`  | test_submit_joke_max_length(client)def test_submit_joke_whitespace_only(client) |
| `@jampete`  | def test_submit_joke_empty_text(client)                                         |
| `@bl35`     | def test_submit_joke_over_max_length(client)                                    |

## Forward Hook

Your test suite now specifies what POST /jokes should do — at every level.
Next week (Cycle 1 Close), your team will assess the health of the full
test suite across all routes. The gap between what you tested today and
what the full app does is the gap you will document in the Test Health block.
Start thinking now: which routes have no tests at all?

# Cycle 1 Close — moj-c1-v1.0

- **Date:** 2026-03-23
- **Team Members:** `@crmoll`, `@adolata`, `@bl35`, `@jampete`, `@lvatista`
- **Summary:** Cycle 1 delivered the Ministry of Jokes foundation: repository setup, a green CI pipeline with automated testing and linting, a working Flask application, and the first database-backed schema and behavioral tests. The team is carrying a stronger workflow into Cycle 2, especially around testing discipline, release discipline, and cleaner branch/CI coordination.
- **Complexity Horizon:** The biggest gap between our MVP and the Ministry Vision is that our current app supports a small local workflow, while the full vision requires scalable user-facing features, richer moderation/governance, and broader operational support.

# ICEX_MJ05: Joke-Teller Licenses

**Date:** 2026-03-24
**Team Members Present:** `@lvatista`, `@bl35`, `@adolata`, `@crmoll`, '@jampete'
**Roles:**

- Repo Admin: `@bl35`
- Process Lead: `@lvatista`
- Dev Lead: `@adolata` & '@crmoll'
- QA Sentinel: `@jampete`
  **Summary:**
  Implemented user authentication and authorization using Flask-Login; added registration, login, and logout routes; secured the Admin user list with role-based access control and verified security behaviors with a three-level test suite.

## Planted Problem

- **What was the problem?**
  - The /admin/users route was missing @login_required, which allowed unauthenticated users to trigger a role-check error.
- **How did the team identify it?**
  - The QA sentinel found it in the error case, which tested for unauthorized access to GET /admin/users. This failed because it did not return 401 unauthorized.
- **How was it resolved?**
  - @login_required was added to the list_users function in auth.py to ensure the session is validated before checking roles.

**Forward hook:**

- in ICEX 6 we need to harden every route that we wrote today to ensure they are not open to any attackers.

# ICEX_MJ06: Forging Unforgeable Licenses

- **Date:** 2026-03-26
- **Team Members Present:** `@jampete`, `@adolata`, `@lvatista`, `@bl35`, `@crmoll`
- **Roles:**
  - Repo Admin: `@adolata`
  - Process Lead: `@jampete`
  - Dev Lead: `@bl35` & `@lvatista`
  - QA Sentinel: `@crmoll`
- **Summary of Work:** Configured and fixed CI security scanning and conducted a STRIDE analysis on /login.

### Planted Problem

- **What was the bug?** The CI never installs the project’s dependencies first.
- **How did the team identify it?** Dev Lead noticed CI reported no vulnerabilities because it never installed dependencies and suppressed failures.
- **How was it resolved?** Add a step to install requirements.txt before running the audit.

- **Forward Hook:** Next time, MoJ gets an opinion system. ICEX 7 adds three-axis
  attributed ratings — funniness, appropriateness, and originality. Every threat in
  your STRIDE table applies to the rating endpoints too. The security issues you
  opened today are the backlog you carry into feature development.

# ICEX 7: The Department of Conditions and Alarm

- **Date:** 2026-03-21
- **Team Members Present:** `@crmoll`, `@bl35`, `@lvatista`, `@adolata`, `@jampete`
- **Roles:**
  - Repo Admin: `@lvatista`
  - Process Lead: `@crmoll`
  - Dev Lead: `@bl35`, `@jampete`
  - QA Sentinel: `@adolata`
- **Summary of Work:** We created the ratings route to attatch ratings to jokes submitted by users. Since ratings pertains to both users and jokes, we will abstract to its own route.

### Planted Problem (either one)

- **What was the bug?** [Describe the omission in the starter model]

* UniqueConstraint was missing from the Rating model — no database-level enforcement prevented a user from rating the same joke twice.

- **What was the consequence?** [What behavior did tests reveal without the fix?]

* Without the constraint, a second POST to/jokes/<id>/ratings by the same user would succeed and create a duplicate rating instead of returning 409 Conflict.

- **How was it resolved?** [What was added and why does it matter?]

* Added **table_args** with a UniqueConstraint on (user_id, joke_id), ensuring the database rejects duplicate ratings even if the application-layer check is bypassed.

### Planted Problem 2 (brief descr)

- The starter rating.py used ForeignKey('users.id')
  and ForeignKey('jokes.id'), but the actual project tables are named'user' and 'joke' (singular), as defined in app/models.py.

### Security Carry-Forward

- **STRIDE threat 1 from ICEX 6 that applies to ratings:**

* Denial of Service: Without any current rate limiting, attackers can flood our `POST /ratings` endpoint causing our API to become overwhelmed and either slow down our webapp or shut down functionality entirely.

- **STRIDE threat 2 from ICEX 6 that applies to ratings:** [Threat name + 1-2 sentence explanation]

* Repudiation: The MoJ mvp still has insufficient logging, so there is no audit trail for updating or creating new ratings. This would prevent us from finding out which users may be acting maliciously.

- **Evidence & Reflection:** The POST endpoint is non-idempotent and the PUT endpoint is idempotent. In one sentence: what would break in MoJ's user experience if both were non-idempotent (both POST)?
  If both were non-idempotent, every time a joke is rated a new rating object is created, which would result in duplicate records and likely slow down the querying of jokes.

# ICEX_MJ08: Ministry Minutes

**Date:** 2026-04-02
**Team Members Present:** `@lvatista`, `@bl35`, `@adolata`, `@crmoll`, '@jampete'
**Roles:**

- Repo Admin: `@jampete`
- Process Lead: `@lvatista`
- Dev Lead: `@adolata` & '@crmoll'
- QA Sentinel: `@bl35`
  **Summary:**
- Implemented structured JSON logging across the application and resolved a formatting bug to ensure an immutable audit trail.

### Spec → Implementation Map

| Team Best Event                 | Category    | Implemented? | Notes |
| ------------------------------- | ----------- | ------------ | ----- |
| 1. Failed login attempt         | Auth        | ✅           |       |
| 2. Successful login             | Auth        | ✅           |       |
| 3. Logout                       | Auth        | ✅           |
| 4. Permission denied            | Error       | ⏳           |       |
| 5. Joke submitted               | Content     | ✅           |       |
| 6. Joke submission rejected     | Error       | ✅           |       |
| 7. Application exception        | Error       | ⏳           |       |
| 8. Database query failure       | Error       | ⏳           |       |
| 9. Admin viewing private data   | Interaction | ⏳           |       |
| 10. User role change            | Auth        | ⏳           |       |
| 11. Account deletion            | Interaction | ⏳           |       |
| 12. API request received        | Operational | ⏳           |       |
| 13. API response time           | Operational | ⏳           |       |
| 14. Session start/end           | Auth        | ⏳           |       |
| 15. Failed joke submission      | Error       | ✅           |       |
| 16. Rate limit block            | Auth        | ⏳           |       |
| 17. Database connection health  | Operational | ⏳           |       |
| 18. Service startup/shutdown    | Operational | ⏳           |       |
| 19. Session expired             | Auth        | ⏳           |       |
| 20. Terms of service acceptance | Interaction | ⏳           |       |
| Rating Created                  | Interaction | ✅           |       |

## Planted Problem

- **What was the problem?**

* The EXTRA_FIELDS tuple hardcoded only ("event", "user_id"), so any extra fields passed beyond those two — such as joke_id, status_code, funniness, appropriateness, and originality — were silently dropped from the JSON log output.

- **How did the team identify it?**

* We checked if all of the required fields were are present based on the hint that the assignment provided us, and found that they are clearly not.

- **How was it resolved?**

* Replaced EXTRA_FIELDS with a RESERVED_FIELDS set containing Python's internal logging attributes, then iterated over all fields in record.dict and included any field not in the reserved set — so all extra fields passed via extra={} appear in the JSON output automatically.

- **Evidence & Reflection:** Your JSONFormatter now emits structured JSON for every significant event. In one sentence: if MoJ were operating in production and a user claimed "I never submitted that joke," which specific log fields would you use to prove or disprove the claim?
  - **Answer:** We would query the logs for the `joke_created` event matching the `joke_id`, and verify the `user_id`, `timestamp`, and `source_ip` to determine if the action originated from their authenticated session.

# ICEX 9: The Great Joke-O-Meter

- **Date:** 2026-04-07
- **Team Members Present:** `@adolata`, `@bl35`, `@jampete`, `@lvatista`
- **Roles:**
  - Repo Admin: `@bl35`
  - Process Lead: `@adolata`
  - Dev Lead: `@lvatista`
  - QA Sentinel: `@jampete`
- **Summary of Work:** The team implemented the first versioned API endpoint for the Ministry of Jokes application. We created the endpoint `GET /api/v1/jokes/count`, added tests verifying the response structure and behavior, documented the API contract, and integrated structured logging for the endpoint.

### API Contract Reflection

- **Contract completeness:** Yes. A developer who has never seen the Flask source code could build a working `fetch()` request using the information in `docs/api.md`. The contract specifies the endpoint URL, HTTP method, authentication requirements, and the exact JSON structure returned by the API. The only additional information a developer might need is the production base URL of the API server, since the document currently references a local development URL.

- **Pagination question:** If a client consumes `GET /api/v1/jokes` when there are 10,000 jokes and no pagination, the server would attempt to return the entire dataset in one response. This could cause slow response times, increased memory usage, and poor performance for both the server and the client application. The count endpoint enables pagination by allowing the client to first request the total number of jokes and then calculate how many pages of results exist. The frontend can then request jokes in smaller page-sized batches instead of loading the entire dataset at once.

# ICEX 10: The Display Terminal
* **Date:** 2026-04-09
* **Team Members Present:** `@adolata`, `@lvatista`, `@jampete`, `@crmoll`
* **Roles:**
    * Repo Admin: `@jampete`
    * Process Lead: `@crmoll`
    * Dev Lead: `@adolata`
    * QA Sentinel: `@lvatista`
* **Summary of Work:** We created a simple react front end page for our app with hardcoded values that will later be changed to fetch jokes from the DB. 

### Timing Report
* **Start time:** 3:00pm 
* **End time:** 3:31pm
* **Total elapsed:** 31
* **Biggest time sink:** Getting the server up and running took the longest time. 
* **Comfort level with React after this ICEX:** 3/5. It's new to most of us on the team, but so far it seemed pretty straight forward. 

### Component Tree
<App> — owns JOKES data and showJokes state
  ├── <JokeCount count={3} /> — pure display component (receives count via props)
  ├── <button> — triggers setShowJokes to toggle visibility
  └── <JokeList jokes={[...]} /> — receives jokes via props and renders them using .map()
        ├── <li key={1}> Why did the chicken cross the road? — alice </li>
        ├── <li key={2}> A priest and a rabbi walk into a bar... — bob </li>
        └── <li key={3}> Why do programmers prefer dark mode? — carol </li>

### Reflection
* **Props vs. state:** In your own words, what is the difference between a prop and a state variable? Which component in this ICEX owns state? Which components only receive props?
- A prop variable is passed as a parameter to a react component, while a state variable is changed via a setter and persists after a function is ran. So a prop variable is immutable and a state variable is muutable.
- The App component owns state. JokeList and JokeCount only recieve props. 
* **The seam:** The `JOKES` array at the top of `App.jsx` is hardcoded. Next week, `fetch()` will replace it with data from the Flask API. 
Which files would need to change? Which files would stay exactly the same? What does that tell you about how this code is organized?
- The app.jsx file will need to change. JokeList and JokeCount are set up to recieve prop variables and carry out their respective functions, so they don't need to change. But app.jsx will need to fetch the data from the flask API in order to pass the jokes to the other components. This shows that the code is organized by top-down relationships where App is the highest level. App will get the data to send to other components. 

