# GSC OAuth and Loopback Auth Flow

## Local Re-Auth Workflow
`$HERMES_HOME/google_client_secret.json` is an installed-app client with redirect `http://localhost`.

1. Run a local HTTP listener on `http://localhost:8087`.
2. Open OAuth authorization URL with requested scopes (`webmasters` or `webmasters.readonly`).
3. Exchange authorization code at `https://oauth2.googleapis.com/token`.
4. Update `$HERMES_HOME/google_token.json` or project-specific token file.

## Common OAuth Pitfalls
- **Redirect URI mismatch**: Token exchange `redirect_uri` must strictly equal the exact request URI `http://localhost:8087`.
- **API Disabled (403)**: If GCP project never enabled GSC API, visit `https://console.developers.google.com/apis/api/searchconsole.googleapis.com/overview` to enable.
- **Scope Insufficient (401)**: Verify token file `scopes` array includes `https://www.googleapis.com/auth/webmasters` before calling endpoints.
