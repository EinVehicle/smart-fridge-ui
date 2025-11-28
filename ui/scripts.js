// ================= AI 分析结果 =================
(async function loadAIResults() {
  const listEl = document.getElementById('item-list');
  const timeEl = document.getElementById('update-time');

  if (!listEl || !timeEl) return;

  function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, m => ({
      '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
    })[m]);
  }

  function render(data) {
    listEl.innerHTML = '';
    if (!Array.isArray(data.items) || data.items.length === 0) {
      listEl.innerHTML = '<li style="color:#6b7280;">No items detected</li>';
    } else {
      data.items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'ai-item';
        li.innerHTML = `
          <span class="item-name">${escapeHtml(item.item_name)}</span>
          <span class="item-time">${escapeHtml(item.timestamp || '—')}</span>
        `;
        listEl.appendChild(li);
      });
    }
    timeEl.textContent = 'Last updated: ' + (data.items[0]?.timestamp || '—');
  }

  try {
    const res = await fetch('/api/analysis', { cache: 'no-store' });
    if (!res.ok) throw new Error('Bad status ' + res.status);
    const data = await res.json();
    render(data);
  } catch (err) {
    console.warn('API /api/analysis failed:', err);
    render({
      items: [
        { item_name: 'fallback-item1', timestamp: '1 day' },
        { item_name: 'fallback-item2', timestamp: '2 days' }
      ]
    });
  }
})();

// ================= 冰箱总览 =================
(async function loadFridgeOverview() {
  const doorEl = document.getElementById('door-status');
  const sensorEl = document.getElementById('sensor-status');
  const powerEl = document.getElementById('power-status');
  const freeSpaceEl = document.getElementById('free-space');
  const updateEl = document.getElementById('overview-update-time');
  if (!doorEl || !sensorEl || !powerEl || !freeSpaceEl || !updateEl) return;

  try {
    const res = await fetch('/api/overview', { cache: 'no-store' });
    if (!res.ok) throw new Error('Bad status ' + res.status);
    const data = await res.json();

    doorEl.textContent = data.door ?? '—';
    sensorEl.textContent = data.sensor ?? 'Offline';
    powerEl.textContent = data.power ?? 'Offline';
    freeSpaceEl.textContent = data.free_space ?? '—';
    updateEl.textContent = 'Last updated: ' + (data.last_updated || '—');
  } catch (err) {
    console.warn('API /api/overview failed:', err);
    doorEl.textContent = 'fallback-door';
    sensorEl.textContent = 'fallback-sensor';
    powerEl.textContent = 'fallback-power';
    freeSpaceEl.textContent = '—';
    updateEl.textContent = 'fallback-update';
  }
})();

// ================= 视频时间线 =================
(async function loadVideoTimeline() {
  const container = document.getElementById('timeline-container');
  if (!container) return;

  function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, m => ({
      '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
    })[m]);
  }

  try {
    const res = await fetch('/api/videos', { cache: 'no-store' });
    if (!res.ok) throw new Error('Bad status ' + res.status);
    const data = await res.json();

    container.innerHTML = '';
    data.forEach(item => {
      const div = document.createElement('div');
      div.className = 'timeline-item';
      div.innerHTML = `
        <span>${escapeHtml(item.time || '—')}</span>
        <img class="thumbnail" src="${escapeHtml(item.thumb)}" data-video="${escapeHtml(item.video)}">
      `;
      container.appendChild(div);
    });

    container.querySelectorAll('img.thumbnail').forEach(img => {
      img.addEventListener('click', () => {
        const url = img.dataset.video;
        const win = window.open('', '_blank', 'width=640,height=480');
        win.document.write(`
          <video controls autoplay style="width:100%;height:auto;">
            <source src="${url}" type="video/mp4">
          </video>
        `);
      });
    });
  } catch (err) {
    console.warn('API /api/videos failed:', err);
    const fallback = [
      { time: 'fallback1', video: '/static/videos/video1.mp4', thumb: '/static/thumbs/thumb1.jpg' },
      { time: 'fallback2', video: '/static/videos/video2.mp4', thumb: '/static/thumbs/thumb2.jpg' },
    ];
    fallback.forEach(item => {
      const div = document.createElement('div');
      div.className = 'timeline-item';
      div.innerHTML = `
        <span>${escapeHtml(item.time)}</span>
        <img class="thumbnail" src="${escapeHtml(item.thumb)}" data-video="${escapeHtml(item.video)}">
      `;
      container.appendChild(div);
    });
  }
})();
