import { buildServer } from './server.js';

const PORT = Number(process.env.PORT || 5000);
const HOST = process.env.HOST || '0.0.0.0';

async function start() {
  const server = await buildServer();
  try {
    await server.listen({ port: PORT, host: HOST });
    console.log(`\n🚀 Upward Developer Documentation Portal is running!`);
    console.log(`   - Main Portal (All Services):  http://127.0.0.1:${PORT}/`);
    console.log(`   - BFF Reference:               http://127.0.0.1:${PORT}/bff/`);
    console.log(`   - Uptime Reference:            http://127.0.0.1:${PORT}/uptime/`);
    console.log(`   - Identify Reference:          http://127.0.0.1:${PORT}/identify/`);
    console.log(`   - Combined JSON Spec:          http://127.0.0.1:${PORT}/specs/combined.json\n`);
  } catch (err) {
    server.log.error(err);
    process.exit(1);
  }
}

start();
