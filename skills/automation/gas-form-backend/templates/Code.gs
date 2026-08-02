/**
 * 批貨課程報名表單 — Google Apps Script 範本
 *
 * 三通道：① Google Sheets ② Email ③ LINE 客服群組
 *
 * 設定步驟：
 * 1. Google Drive 建試算表 → 擴充功能 → Apps Script → 貼入此檔
 * 2. 取代下方五個常數（SPREADSHEET_ID / NOTIFY_EMAIL / TURNSTILE_SECRET /
 *    LINE_CHANNEL_TOKEN / LINE_GROUP_ID）
 * 3. 跑 testPost 驗證寫入 → 部署 → 網頁應用程式 → 執行身份=自己、誰可以存取=所有人
 * 4. 部署網址貼回 index.html 表單的 fetch URL
 *
 * 試算表欄位順序（由 appendRow 決定）：
 *   時間戳記 | 姓名 | 手機 | Email | LINE ID | 報名班別 | 護理人員 | 備註
 */

const SPREADSHEET_ID  = 'YOUR_SPREADSHEET_ID_HERE';
const NOTIFY_EMAIL    = 'YOUR_EMAIL@EXAMPLE.COM';
const TURNSTILE_SECRET = 'YOUR_TURNSTILE_SECRET_KEY'; // 佔位符 = 驗證關閉
const LINE_CHANNEL_TOKEN = 'YOUR_LINE_CHANNEL_ACCESS_TOKEN'; // LINE Developers Messaging API long-lived token
const LINE_GROUP_ID      = 'YOUR_LINE_GROUP_ID';             // 客服群組 groupId（官方帳號須已在群組內）

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    // 驗證 Turnstile token（僅在已設定真實 secret 時啟用）
    if (TURNSTILE_SECRET !== 'YOUR_TURNSTILE_SECRET_KEY') {
      var token = data['cf-turnstile-response'] || '';
      if (!token) {
        return ContentService
          .createTextOutput(JSON.stringify({ success: false, error: 'missing token' }))
          .setMimeType(ContentService.MimeType.JSON);
      }
      var verifyUrl = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';
      var params = {
        method: 'post',
        payload: { secret: TURNSTILE_SECRET, response: token }
      };
      var result = UrlFetchApp.fetch(verifyUrl, params);
      var outcome = JSON.parse(result.getContentText());
      if (!outcome.success) {
        return ContentService
          .createTextOutput(JSON.stringify({ success: false, error: 'verify failed' }))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }

    // ① 寫入試算表（getSheets()[0] — 部署環境 getActiveSheet() 不可靠）
    const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheets()[0];
    const name  = data.name  || '';
    const phone = data.phone || '';
    const email = data.email || '';
    const line = data.line || '';
    const cls   = data.class || '';
    const nurse = data.nurse || '';
    const note  = data.note  || '';
    sheet.appendRow([new Date(), name, phone, email, line, cls, nurse, note]);

    // ② Email 通知
    const subject = '【新報名】' + cls + ' - ' + name;
    const body =
      '📋 新報名通知\n\n' +
      '姓名：' + name + '\n' +
      '手機：' + phone + '\n' +
      'Email：' + email + '\n' +
      'LINE：' + line + '\n' +
      '報名班別：' + cls + '\n' +
      '護理人員：' + nurse + '\n' +
      '備註：' + (note || '無') + '\n\n' +
      '時間：' + new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' });
    MailApp.sendEmail(NOTIFY_EMAIL, subject, body);

    // ③ LINE 群組推送（失敗不擋報名）
    sendLineNotify(subject, body);

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 推送 LINE 訊息到客服群組。
 * muteHttpExceptions + 只 log 不 throw — LINE 掛掉不能擋報名（主通道是 Sheets）。
 */
function sendLineNotify(subject, body) {
  if (LINE_CHANNEL_TOKEN.indexOf('YOUR_LINE') !== -1 || LINE_GROUP_ID.indexOf('YOUR_LINE') !== -1) {
    console.log('LINE notify skipped: token/groupId 未設定');
    return;
  }
  var message = '🔔 ' + subject + '\n' + body + '\n（由網站表單自動推送）';
  var params = {
    method: 'post',
    headers: {
      'Authorization': 'Bearer ' + LINE_CHANNEL_TOKEN,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({
      to: LINE_GROUP_ID,
      messages: [{ type: 'text', text: message }]
    }),
    muteHttpExceptions: true
  };
  var res = UrlFetchApp.fetch('https://api.line.me/v2/bot/message/push', params);
  var code = res.getResponseCode();
  if (code >= 400) {
    console.log('LINE push failed: HTTP ' + code + ' ' + res.getContentText());
  }
}

// ═══════════════════════════════════════════════
// 測試函式 — 在 Apps Script 編輯器直接執行（不需部署）
// ═══════════════════════════════════════════════

/** 正常送出（Turnstile 驗證已關閉時） */
function testPost() {
  const mock = {
    postData: {
      contents: JSON.stringify({
        name: '測試姓名', phone: '0912345678', email: 'test@example.com',
        class: '9月班', nurse: '否', note: '測試送出'
      })
    }
  };
  const result = doPost(mock);
  console.log('testPost →', result.getContent());
}

/** LINE 推送測試 — 需先設定 LINE_CHANNEL_TOKEN 與 LINE_GROUP_ID */
function testLineNotify() {
  if (LINE_CHANNEL_TOKEN.indexOf('YOUR_LINE') !== -1 || LINE_GROUP_ID.indexOf('YOUR_LINE') !== -1) {
    console.log('testLineNotify → SKIP: 請先設定 token/groupId');
    return;
  }
  sendLineNotify('【測試】網站', '姓名：測試\n手機：0912345678\n班別：9月班');
  console.log('testLineNotify → 已送出，請檢查客服群組');
}

/**
 * 取得群組 groupId 輔助函式。
 * 流程：部署為網頁應用程式 → URL 填 LINE Developers Webhook → 群組發訊息
 *       → 執行記錄印出 GROUP_ID → 填入 LINE_GROUP_ID
 */
function doPostWebhook(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    console.log('WEBHOOK_RAW →', e.postData.contents);
    if (body.events && body.events.length > 0) {
      const event = body.events[0];
      if (event.source && event.source.groupId) {
        console.log('GROUP_ID →', event.source.groupId);
        return ContentService
          .createTextOutput(JSON.stringify({ groupId: event.source.groupId }))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }
    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
