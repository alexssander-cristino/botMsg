(() => {
  const button = document.getElementById('connect-wa');
  const title = document.getElementById('wa-title');
  const message = document.getElementById('wa-message');
  if (button) button.addEventListener('click', async () => {
    button.disabled = true; button.textContent = 'Abrindo…';
    try { await fetch('/api/whatsapp/connect', {method:'POST'}); }
    catch (e) { if (message) message.textContent = 'Não foi possível iniciar o navegador.'; }
    setTimeout(() => { button.disabled = false; button.textContent = 'Conectar'; }, 1500);
  });
  async function refresh() {
    try {
      const r = await fetch('/api/status'); const data = await r.json(); const s = data.whatsapp;
      if (title) title.textContent = s.connected ? 'WhatsApp conectado' : s.busy ? 'Conectando WhatsApp' : 'WhatsApp desconectado';
      if (message) message.textContent = s.message || '';
      const dot = document.querySelector('.status-dot');
      if (dot) dot.className = 'status-dot' + (s.connected ? ' online' : s.busy ? ' busy' : '');
    } catch (_) {}
  }
  refresh(); setInterval(refresh, 2500);
})();
