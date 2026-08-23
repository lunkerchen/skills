---
name: gmail-inbox-organizer
description: Automated Gmail inbox organization and label-based triage agent. Runs as a cron job to scan the inbox, classify emails by sender/subject patterns into category labels, apply labels, and optionally archive promotions. Uses direct gws CLI. Skip messages already bearing a target label to avoid redundant API calls.
version: 2.0.0
author: Nous Research
license: MIT
required_credential_files:
 - path: google_token.json
   description: Google OAuth2 token (created by google-workspace setup)
 - path: google_client_secret.json
   description: Google OAuth2 client credentials
metadata:
  hermes:
    tags: [Gmail, email, triage, organization, labels, automation, cron]
    homepage: https://github.com/NousResearch/hermes-agent
related_skills: [google-workspace, himalaya]
---

# Gmail Inbox Organizer

Automated daily inbox triage — fetch all inbox messages (read + unread), classify by sender/subject into category labels, apply labels, skip already-labeled messages.

## Architecture

```
gws_bridge.py   →  gws CLI (gmail +triage --labels)
google_api.py   →  gws CLI (gmail modify --add-labels)
```

## Prerequisites

- `google-workspace` skill must be set up (OAuth2 token exists at `$HERMES_HOME/google_token.json`)
- `gws` binary installed and in PATH
- Five category labels pre-created in Gmail:
  - 【重要/安全】 (Label_44)
  - 【帳單/金融】 (Label_45)
  - 【購物/訂單】 (Label_46)
  - 【資訊/推廣】 (Label_47)
  - 【其他/職涯】 (Label_48)

## Trigger

- **Cron job**: "organize inbox", "triage gmail", "label inbox emails"
- **Recurring**: Daily automated inbox cleanup
- **One-shot**: "organize my inbox"

## Classification Rules

Emails are classified by sender email domain + subject keyword matching.
**Classification order matters** — check more specific categories first.

### Check order (domain-based first, then keyword-based):

Order matters because broad keywords (`alert`, `交易`, `job`) can collide across categories.
**Two-pass principle:** classify by sender domain first, then by subject keywords.

#### Pass 1: Domain-level shortcuts

| Sender hint | Label |
|---|---|
| `jobalert.*indeed` | 【其他/職涯】 |
| `promo.*bitget`, `promo.*binance`, `promo.*okx` | 【資訊/推廣】 |
| `no-reply@accounts.google.com` | 【重要/安全】 (if security-related subject) |
| `noreply@tax.*`, `invoice*` | 【帳單/金融】 |

#### Pass 2: Keyword matching (in order)

1. **【其他/職涯】** (Label_48): Check FIRST to catch `jobalert`, `indeed`, `linkedin` before generic words like `alert` trigger security. Keywords: `應徵`, `面試`, `合作`, `工作`, `職缺`, `滾石`, `攝影`, `hire`, `job`, `career`, `出版授權`, `rock mobile`, `indeed`, `jobalert`, `linkedin`, `搜尋`

2. **【重要/安全】** (Label_44): `security`, `verify`, `login`, `password`, `驗證`, `安全`, `帳戶異常`, `認證`, `實名認證`, `suspicious`, `sign-in`, `authenticator`, `生物辨識`, `登入成功`, `登入失敗`, `login attempt`  
   ⚠️ Do NOT use `alert` as a standalone keyword — it triggers false positives on `jobalert`, `dealalert`, `pricealert`. Use `安全性`, `安全快訊`, `security alert` instead, or require word-boundary matching.

3. **【帳單/金融】** (Label_45): `銀行`, `帳單`, `對帳單`, `提領`, `匯款`, `交易`, `金融`, `發票`, `invoice`, `payment`, `receipt`, `繳費`, `subscription`, `續約`, `電子發票`, `cht.com.tw`, `tax`, `付款`, `billing`, `分潤`, `專戶`  
   ⚠️ `交易` is broad — also appears in crypto exchange promotional emails (`AI 交易之路`). If sender domain is `promo.*` or subject contains `playbook`, `getagent`, `策略`, classify as 【資訊/推廣】 instead.

4. **【資訊/推廣】** (Label_47): Check BEFORE shopping — a coupon from a shopping platform is still a promotion. Keywords: `newsletter`, `電子報`, `促銷`, `promo`, `推廣`, `推薦`, `日報`, `週報`, `canva`, `tiktok`, `永豐金`, `庫存日報`, `誠品`, `市集`, `insta360`, `dji`, `測驗`, `mbti`, `perplexity`, `supabase`, `adobe`, `noreply`, `no_reply`, `no-reply`, `donotreply`, `catchplay`, `穿搭`, `ranking`, `ランキング`, `trial`, `tradingview`, `bitget`, `getagent`, `travelodge`, `firecrawl`, `genius bar`, `vibe`, `deprecat`, `playbook`, `會員日`, `限時`, `優惠`, `coupon`, `補貨`

5. **【購物/訂單】** (Label_46): Actual order confirmations and shipping notices only — NOT coupons. Keywords: `pchome`, `蝦皮`, `shopee`, `露天`, `訂單`, `order`, `shipping`, `出貨`, `付款`, `p幣`, `購物`, `coupang`, `酷澎`, `momo購物`, `到貨通知`

**Default:** Unclassifiable → 【資訊/推廣】 (Label_47)

## Step-by-Step Workflow

### Step 1: Check gws CLI and labels

```bash
which gws  # should be /opt/homebrew/bin/gws
gws --version

# List labels to get name→ID mapping
gws gmail users labels list --params '{"userId": "me"}'
```

**Pitfall:** gws prints `Using keyring backend: keyring` to stdout before every JSON response. Strip this line before `json.loads()`.

### Step 2: Search inbox messages

```bash
gws gmail users messages list \
  --params '{"userId": "me", "maxResults": 50, "q": "in:inbox"}'
```

### Step 3: Read message metadata (headers only — cheap)

```bash
gws gmail users messages get \
  --params '{"userId": "me", "id": "MESSAGE_ID", "format": "metadata",
             "metadataHeaders": ["From", "Subject", "To", "Date"]}'
```

Key fields from response:
- `payload.headers[]` — array of `{name, value}` objects
- `snippet` — text preview
- `labelIds` — current labels (e.g. `["INBOX", "UNREAD", "CATEGORY_PROMOTIONS"]`)

### Step 4: Check existing labels

```python
our_labels = {"Label_44", "Label_45", "Label_46", "Label_47", "Label_48"}
label_ids = msg_data.get("labelIds", [])
has_label = any(lid in label_ids for lid in our_labels)
```

### Step 5: Classify and apply label

```python
# See Classification Rules above
# Match by sender domain + subject keywords
```python
GWS = "/opt/homebrew/bin/gws"
actions = {"addLabelIds": ["Label_47"]}  # or appropriate label
if archive:
    actions["removeLabelIds"] = ["INBOX"]

subprocess.run([GWS, "gmail", "users", "messages", "modify",
    "--params", json.dumps({"userId": "me", "id": msg_id}),
    "--json", json.dumps(actions)])
```
- The `--json` flag sends the body as-is (the POST body with `addLabelIds`/`removeLabelIds`).
- The `--params` flag provides URL parameters (`userId`, `id`).
- Returns HTTP 202 with no body on success.

**Restore from archive:** To bring an archived message back to inbox after reclassifying:
```python
{"addLabelIds": ["INBOX", "Label_44"], "removeLabelIds": ["Label_47"]}
```
This works because INBOX is a label in Gmail's internal model. Adding it "un-archives" the message.

**Batch classification pattern:** For speed, batch-fetch all message metadata first, classify in-memory, then apply labels in a single loop. This avoids N+1 round-trips and lets you verify the classification before committing. Write the intermediate data to `/tmp/gmail_inbox.json` for inspection.

### Step 6: Archive decisions

Archive (remove INBOX) for:
- Pure promotional emails (coupons, deals, discounts)
- Newsletters and digests
- Social notifications (TikTok, Instagram, etc.)
- Tool updates (newsletters from saas tools)
- Read-and-dismiss content

Keep in inbox for:
- Security alerts and verification emails
- Bills, invoices, financial statements
- Active job/collaboration threads (need reply/tracking)
- Government/authority notifications
- Account-related system notifications
- Any email with financial or security implications

**Default when uncertain:** keep in inbox.

## Pitfalls

1. **`gws` stdout prefix**: `gws` always prints `Using keyring backend: keyring` before JSON output. Strip it before parsing.

2. **Classification order**: Check 【資訊/推廣】 BEFORE 【購物/訂單】 for emails from shopping platforms (Coupang, PChome, etc). A promotional coupon email (subject: "限領$50", "限時特價") is 【資訊/推廣】, not 【購物/訂單】. Only actual order confirmations and shipping notices get 【購物/訂單】.

3. **Rate limits**: Gmail API quota is ~250 requests per second for reads, ~25/s for writes. The `gws` CLI handles retries on 429s. No need to add artificial delays.

4. **Already-labeled check**: Always check `labelIds` before applying. This avoids redundant API calls and prevents errors.

5. **`from` field format**: In `gws` JSON output, headers are arrays of `{name, value}` objects. Parse with: `headers = {h["name"].lower(): h["value"] for h in msg_data["payload"]["headers"]}`

6. **Label IDs are stable**: Use `Label_44`, `Label_45`, etc. Their display names can change but IDs are permanent.

7. **`resultSizeEstimate` lag**: The Gmail API estimate may not reflect recent modifications. Re-query for accurate counts.

8. **Suspicious senders**: If a sender domain doesn't match the claimed brand (e.g., `h.veen@chello.nl` claiming to be momo), treat with caution. Label conservatively and keep in inbox.

9. **`gws` binary path**: `/opt/homebrew/bin/gws` on Apple Silicon (Homebrew-installed). Verify path with `which gws`.

10. **Uncertainty rule**: If unsure whether to archive, **keep in inbox**. False positives (missed important email) are worse than a slightly cluttered inbox.

11. **`--json` vs `--params` mix-up**: The modify endpoint uses `--params` for URL params (`userId`, `id`) and `--json` for the POST body (`addLabelIds`, `removeLabelIds`). Swapping them results in 400 errors.

12. **Post-classification verification**: After batch-labelling, spot-check 2-3 messages per label to confirm correctness. Query with: `gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID", "format": "metadata", "metadataHeaders": ["From", "Subject"]}'` and inspect the `labelIds` field.

## Output Summary

Provide a final count per category:

| Category | New Labels | Archived |
|---|---|---|
| 【重要/安全】 | N | N |
| 【帳單/金融】 | N | N |
| 【購物/訂單】 | N | N |
| 【資訊/推廣】 | N | N |
| 【其他/職涯】 | N | N |
| **Total** | **N** | **N** |

Also report:
- Scanned: total inbox messages
- Already labeled: messages with existing labels (skipped)
- Newly labeled count per category
- Archived count per category
- Remaining inbox count

## Reference Files

- `references/classification-pipeline.py` — Standalone, copy-pasteable Python script that implements the full classification pipeline: batch-fetch inbox → domain/keyword two-pass classify → label → archive → verify. Contains all pitfalls (alert collision, 交易 collision, restore-from-archive) baked into the code.