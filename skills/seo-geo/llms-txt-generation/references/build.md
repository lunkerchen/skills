# 驗證（build 後）

```bash
ls .next/server/app/llms.txt.body  # Next.js build 產物，直接讀內容檢查
node -e "const f=require('fs').readFileSync('.next/server/app/llms.txt.body','utf8');console.log((f.match(/\/blog\//g)||[]).length)"
```
