const { spawn } = require('child_process');
const fs = require('fs');

async function run() {
  const chrome = spawn('/etc/profiles/per-user/zerok/bin/chromium', [
    '--headless=new',
    '--remote-debugging-port=9223',
    '--disable-gpu',
    '--window-size=1400,1800',
    'http://127.0.0.1:3000/docs/'
  ]);

  await new Promise(r => setTimeout(r, 2500));

  try {
    const listRes = await fetch('http://127.0.0.1:9223/json');
    const tabs = await listRes.json();
    const pageTab = tabs.find(t => t.type === 'page');
    if (!pageTab) throw new Error('No page tab found');

    const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
    await new Promise(res => ws.onopen = res);

    let id = 1;
    function send(method, params = {}) {
      return new Promise((resolve) => {
        const curId = id++;
        const handler = (evt) => {
          const msg = JSON.parse(evt.data);
          if (msg.id === curId) {
            ws.removeEventListener('message', handler);
            resolve(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });
    }

    await send('Runtime.enable');
    await send('Page.enable');

    // Wait for swagger to render
    await new Promise(r => setTimeout(r, 2000));

    // Expand all endpoints
    await send('Runtime.evaluate', {
      expression: `
        document.querySelectorAll('.opblock-summary').forEach(el => el.click());
      `
    });

    await new Promise(r => setTimeout(r, 1500));

    // Capture screenshot of expanded operations
    const { data: b64Expanded } = await send('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: true
    });

    fs.writeFileSync('/home/zerok/projects/upward/screenshots/swagger_expanded.png', Buffer.from(b64Expanded, 'base64'));
    console.log('Saved swagger_expanded.png successfully!');

    ws.close();
  } finally {
    chrome.kill();
  }
}

run().catch(console.error);
