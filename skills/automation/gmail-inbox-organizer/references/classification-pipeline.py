#!/usr/bin/env python3
"""
Gmail inbox classifier — batch-scan, classify, label, archive.
Reproduce from scratch: run label creation first, then this script.

Two-pass classification:
  Pass 1: sender-domain shortcuts (e.g. jobalert.*indeed → career)
  Pass 2: keyword matching in priority order

Usage:
  python3 classification-pipeline.py

Requires:
  - gws CLI installed (brew install gws) and authenticated
  - Five labels pre-created (see label-setup.py or create manually via Gmail)
"""

import subprocess, json, sys, re

GWS = "gws"

# ── helpers ──────────────────────────────────────────────────────────

def gws(*args):
    """Call gws CLI, strip keyring header, return parsed JSON."""
    result = subprocess.run([GWS] + list(args), capture_output=True, text=True)
    out = result.stdout
    if out.startswith("Using keyring backend:"):
        out = out[out.index("\n") + 1:]
    return json.loads(out) if out.strip() else {}


def kv_headers(payload):
    """Return {name.lower(): value} from payload.headers[]."""
    return {h["name"].lower(): h["value"]
            for h in payload.get("headers", [])}


# ── classification ───────────────────────────────────────────────────

def classify(sender: str, subject: str) -> tuple:
    """
    Return (label_id, label_name) for one email.
    Two-pass: domain shortcuts → keyword matching.
    """
    s = f"{sender} {subject}".lower()

    # ── Pass 1: domain shortcuts ──────────────────────────────────
    # jobalert.*indeed → career (pre-empts `alert` keyword collision)
    if "jobalert" in s and "indeed" in s:
        return "Label_48", "【其他/職涯】"

    # Promo subdomain from crypto/exchanges → promo (pre-empts `交易`)
    if re.search(r'promo\..*bitget|promo\..*okx|promo\..*binance', s):
        return "Label_47", "【資訊/推廣】"

    # Google account security
    if "no-reply@accounts.google.com" in s:
        return "Label_44", "【重要/安全】"

    # Tax/invoice
    if "noreply@tax." in s or "invoice" in s and "strip" not in s:
        return "Label_45", "【帳單/金融】"

    # ── Pass 2: keyword matching (priority order) ────────────────

    # 1. 其他/職涯
    career_terms = [
        "應徵", "面試", "合作", "工作", "職缺", "滾石", "攝影",
        "hire", "job", "career", "出版授權", "rock mobile",
        "indeed", "jobalert", "linkedin", "搜尋",
    ]
    if any(k in s for k in career_terms):
        return "Label_48", "【其他/職涯】"

    # 2. 重要/安全  —  no bare `alert` here, too many false positives
    security_terms = [
        "security", "verify", "login", "password",
        "驗證", "安全", "帳戶異常", "認證", "實名認證",
        "suspicious", "sign-in", "authenticator",
        "生物辨識", "登入成功", "登入失敗", "login attempt",
        "安全性快訊", "帳戶設定",
    ]
    if any(k in s for k in security_terms):
        return "Label_44", "【重要/安全】"

    # 3. 帳單/金融
    finance_terms = [
        "銀行", "帳單", "對帳單", "提領", "匯款",
        "金融", "發票", "invoice", "payment", "receipt",
        "繳費", "subscription", "續約", "電子發票",
        "cht.com.tw", "tax", "付款", "billing", "分潤", "專戶",
    ]
    if any(k in s for k in finance_terms):
        # But check: if it's a crypto exchange promo with "交易",
        # reclassify to promo
        if "promo" in s or "playbook" in s or "getagent" in s:
            return "Label_47", "【資訊/推廣】"
        return "Label_45", "【帳單/金融】"

    # 4. 資訊/推廣 (checked before shopping for coupon emails)
    promo_terms = [
        "newsletter", "電子報", "促銷", "promo", "推廣", "推薦",
        "日報", "週報", "canva", "tiktok", "永豐金", "庫存日報",
        "誠品", "市集", "insta360", "dji", "測驗", "mbti",
        "perplexity", "supabase", "adobe",
        "noreply", "no_reply", "no-reply", "donotreply",
        "catchplay", "穿搭", "ranking", "ランキング",
        "trial", "tradingview", "bitget", "getagent",
        "travelodge", "firecrawl", "genius bar",
        "vibe", "deprecat", "playbook",
        "會員日", "限時", "優惠", "coupon", "補貨",
    ]
    if any(k in s for k in promo_terms):
        return "Label_47", "【資訊/推廣】"

    # 5. 購物/訂單 — only real order/shipping, not coupons
    shopping_terms = [
        "pchome", "蝦皮", "shopee", "露天", "訂單", "order",
        "shipping", "出貨", "付款", "p幣", "購物",
        "coupang", "酷澎", "momo購物", "到貨通知",
    ]
    if any(k in s for k in shopping_terms):
        return "Label_46", "【購物/訂單】"

    # Default: promo
    return "Label_47", "【資訊/推廣】"


def should_archive(label_id: str, sender: str, subject: str) -> bool:
    """
    Archive (remove INBOX) for pure promotions/newsletters/social.
    Keep in inbox for security, financial, orders, career threads.
    """
    if label_id in ("Label_44", "Label_46", "Label_48"):
        return False
    if label_id == "Label_45":
        return False   # keep invoices and bills in inbox
    # Label_47 — archive most, but not receipts or confirmations
    s = f"{sender} {subject}".lower()
    keep_terms = ["receipt", "invoice", "發票", "subscription", "confirm"]
    if any(k in s for k in keep_terms):
        return False
    return True


# ── main pipeline ────────────────────────────────────────────────────

def main():
    # Step 1: scan inbox
    data = gws("gmail", "users", "messages", "list",
               "--params", json.dumps({"userId": "me", "maxResults": 200,
                                        "q": "in:inbox"}))
    msgs = data.get("messages", [])
    print(f"\n📬 Inbox: {len(msgs)} messages to classify")

    our_labels = {"Label_44", "Label_45", "Label_46", "Label_47", "Label_48"}
    classified = []
    skipped = 0
    errors = 0

    # Step 2: batch-fetch metadata
    for msg in msgs:
        detail = gws("gmail", "users", "messages", "get",
                     "--params", json.dumps({
                         "userId": "me", "id": msg["id"],
                         "format": "metadata",
                         "metadataHeaders": ["From", "Subject", "Date"],
                     }))
        headers = kv_headers(detail.get("payload", {}))
        existing = set(detail.get("labelIds", []))
        if any(l in existing for l in our_labels):
            skipped += 1
            continue

        classified.append({
            "id": msg["id"],
            "from": headers.get("from", ""),
            "subject": headers.get("subject", ""),
            "existing_labels": list(existing),
        })

    print(f"⏭️  Already labeled: {skipped}")
    print(f"🔍 To classify: {len(classified)}\n")

    # Step 3: classify + apply
    stats = {}
    archived = 0
    applied = 0

    for m in classified:
        label_id, label_name = classify(m["from"], m["subject"])
        archive = should_archive(label_id, m["from"], m["subject"])

        actions = {"addLabelIds": [label_id]}
        if archive:
            actions["removeLabelIds"] = ["INBOX"]

        try:
            gws("gmail", "users", "messages", "modify",
                "--params", json.dumps({"userId": "me", "id": m["id"]}),
                "--json", json.dumps(actions))
            stats[label_id] = stats.get(label_id, 0) + 1
            applied += 1
            if archive:
                archived += 1
            icon = "📁" if archive else "📥"
            print(f"  {icon} {label_name:<12} {m['subject'][:55]}")
        except Exception as e:
            errors += 1
            print(f"  ✗ {m['id']}: {e}")

    # Step 4: summary
    name_map = {
        "Label_44": "【重要/安全】", "Label_45": "【帳單/金融】",
        "Label_46": "【購物/訂單】", "Label_47": "【資訊/推廣】",
        "Label_48": "【其他/職涯】",
    }
    print(f"\n{'='*50}")
    print(f"Applied: {applied} | Archived: {archived} | Errors: {errors}")
    for lid, name in name_map.items():
        print(f"  {name}: {stats.get(lid, 0)}")

    # Step 5: verify final inbox count
    final = gws("gmail", "users", "messages", "list",
                "--params", json.dumps({"userId": "me", "maxResults": 1,
                                         "q": "in:inbox"}))
    print(f"Inbox remaining: {final.get('resultSizeEstimate', '?')}")


if __name__ == "__main__":
    main()
