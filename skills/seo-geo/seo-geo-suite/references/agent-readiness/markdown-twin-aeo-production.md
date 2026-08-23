# 驗證迴圈（production）

```bash
curl -s -A "GPTBot/1.0" https://site/about | head -c 200          # AI UA → markdown
curl -s https://site/about.md | head -c 200                        # .md URL → markdown
curl -s -H "Accept: text/markdown" https://site/ | head -c 200     # Accept → markdown
curl -sI https://site/about | grep -i ^link                        # HTML 帶 Link alternate
curl -s -o /dev/null -w "%{http_code}" -A "GPTBot/1.0" https://site/random-missing  # 404 非 500
curl -s -o /dev/null -w "%{http_code}" https://site/random-missing # 一般請求也 404
npx -y @vercel/agent-readability audit https://site                # 重跑 → 目標 85+
```
