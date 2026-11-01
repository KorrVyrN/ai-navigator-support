# Security policy

## Implemented controls

- The analysis endpoint requires a separately generated server-side Bearer token (minimum 32 characters; use `secrets.token_urlsafe(32)`).
- Missing configuration and example credentials prevent API startup. Health and documentation routes are public.
- GigaChat authorization credentials are exchanged for a short-lived OAuth token. Tokens are cached only in process memory, refreshed before expiry, and retried once on 401.
- Provider errors are mapped to generic responses; credentials, request bodies and provider response bodies are not logged by application code.
- HTTPS certificate verification is always enabled. A trusted PEM CA bundle can be configured without disabling verification.
- `.env` is excluded from Git and the Docker build context. Docker runs as an unprivileged user.

## Deployment responsibilities and limitations

Use HTTPS and rate limiting at the reverse proxy. Restrict access to secrets; do not embed the shared service token into public browser code. Rotate credentials by replacing the environment values and restarting every process. This MVP has no individual users, roles, refresh tokens, revocation database or audit trail.

Regex anonymization is partial: names, addresses, passwords and other sensitive data can remain. It is not a guarantee of compliance with ФЗ-152. Use synthetic or reviewed inputs until a suitable privacy review is complete. Model responses are untrusted recommendations requiring human review.

`/health` is a process liveness endpoint, not a provider readiness test. Startup validates configuration without making paid/provider requests.

## Reporting

Do not publish live credentials or personal data in issues. Use GitHub private vulnerability reporting when enabled; otherwise contact the repository owner privately. Never include secrets in reproduction steps.

## Validation

CI runs lint and tests on Python 3.10–3.12. OAuth and API tests use synthetic credentials and mocked HTTP responses. A successful test run does not certify deployment security or legal compliance.
