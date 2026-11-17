# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within PlantGuard AI, please DO NOT open a public GitHub issue. Instead, report it privately to the maintainers at `security@plantguard-ai.org` (or directly via GitHub Security Advisories).

Please include:
1. Description of the vulnerability and attack vector.
2. Steps to reproduce or proof-of-concept payload.
3. Potential impact on backend services or user data.

Maintainers will acknowledge receipt within 48 hours and coordinate a coordinated disclosure timeline.

## Best Practices for Deployment
- Always deploy behind an HTTPS reverse proxy (e.g. Nginx, Caddy, Cloudflare).
- Configure restrictive CORS origins in `backend/main.py` rather than `*` in production.
- Use PostgreSQL with authenticated credentials rather than unencrypted database connections.
- Ensure strict file upload validation (enforced by default via file extension and header inspection).
