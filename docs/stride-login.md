# STRIDE Analysis: POST /login

| Threat | Attack Scenario | Current Mitigation | Gap? | OWASP Category |
|--------|----------------|-------------------|------|----------------|
| S — Spoofing | An attacker repeatedly submits guessed username/password combinations to try to log in as another user. | The endpoint checks submitted credentials against stored user credentials before creating a session. | Yes | A07 Auth Failures |
| T — Tampering | An attacker sends malformed JSON, missing fields, or wrong data types to interfere with login processing or trigger unintended behavior. | Basic request parsing exists, but strict validation of required fields and types may be limited. | Yes | A03 Injection |
| R — Repudiation | A user can deny making repeated login attempts because authentication attempts are not explicitly logged in a structured audit trail. | Default app/server logs may exist, but there is no clear login-specific audit logging. | Yes | Outside OWASP selection |
| I — Info Disclosure | The endpoint may reveal whether a username exists or expose internal details through detailed login error responses. | The app returns failure responses, but the messages may not be fully generic or hardened. | Yes | A07 Auth Failures |
| D — Denial of Service | An attacker floods POST /login with repeated requests, consuming resources and enabling brute-force attempts. | No dedicated rate limiting or throttling is present on the login endpoint. | Yes | Outside OWASP selection |
| E — Elevation of Privilege | An attacker abuses weaknesses in authentication/session handling to gain access as another user or reach privileged functionality after login. | Authentication is required and role checks exist after login, but the login boundary itself may still be weak. | Yes | A01 Broken Access Control |
