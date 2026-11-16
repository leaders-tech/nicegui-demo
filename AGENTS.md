# Counter teaching app

This repository is a minimal deployable teaching example for school students.
All comments, documentation and user-facing text must be in simple English.

- One process: `main.py` holds the page and the HTTP routes; all SQL is in `db.py`.
- Use NiceGUI the standard way: event handlers call Python code directly.
  NiceGUI's `app` is FastAPI, so extra HTTP routes go on it, never in a second server.
- The counter is shared by all visitors, and stored in SQLite, never session state.
  Open pages follow it through a bound label, without reloads.
- Keep runtime data out of Git. Preserve existing database values on startup.
- Add dependencies with `uv add` or `uv add --dev`, and commit `uv.lock`.
- Before pushing, run `make test` and check the real UI, console and network in a browser.
- Tests include SQLite persistence, concurrent increments and a real browser flow.
- Keep Compose platform-safe: `expose`, no `ports`, no Compose `user`, no external volumes.
- Runtime images must use a non-root Dockerfile `USER` and listen on `0.0.0.0`.
- Keep non-secret deployment defaults in `.docker.env`; secrets belong in the platform UI.
- Read https://deploy.tlfedu.tech/guides/docker/agents.md before changing deployment files.
- Keep short source headers explaining purpose, when to edit, and when to copy.
