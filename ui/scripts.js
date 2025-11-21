//AI分析返回
(
  async function loadAIResults()
  {
    const listEl = document.getElementById('item-list');
    const timeEl = document.getElementById('update-time');

    // safety: ensure elements exist
    if (!listEl || !timeEl)
    {
      console.error('Missing DOM elements: ensure #item-list and #update-time exist in HTML.');
      return;
    }

    // helper to render data
    function render(data)
    {
      listEl.innerHTML = ''; // clear
      if (!Array.isArray(data.items) || data.items.length === 0)
      {
        listEl.innerHTML = '<li style="color:#6b7280;">No items detected</li>';
      }
      else
      {
        data.items.forEach(item => {
          const li = document.createElement('li');
          li.innerHTML = `
            <span class="item-name">${escapeHtml(item.name)}</span>
            <span class="item-time">${escapeHtml(item.stored_for)}</span>
          `;
          li.className = 'ai-item';
          listEl.appendChild(li);
        });
      }
      timeEl.textContent = 'Last updated: ' + (data.last_updated || '—');
    }

    // simple html-escape to avoid injection when using fallback or dynamic text
    function escapeHtml(str)
    {
      return String(str || '').replace(/[&<>"']/g, function(m) {
        return ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[m];
      });
    }

    // Try fetch first
    try
    {
      const res = await fetch('analysis.json', { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP status ' + res.status);
      const data = await res.json();
      console.log('Loaded analysis.json successfully', data);
      render(data);
      return;
    }
    catch (err)
    {
      console.warn('Failed to load analysis.json via fetch:', err.message);
      console.warn('Falling back to built-in sample data. If you are opening the file via file:// in Chrome, use Live Server or python -m http.server to serve files over http://localhost.');
      // AI 默认测试数据
      const fallback =
      {
        last_updated: 'default-update-time',
        items: [
          { name: 'default-item1', stored_for: 'default-day1' },
          { name: 'default-item2', stored_for: 'default-day2' },
          { name: 'default-item3', stored_for: 'default-day3' }
        ]
      };
      render(fallback);
    }

    
  }
)();

//冰箱数据返回
(
  async function loadFridgeOverview()
  {
    const doorEl = document.getElementById('door-status');
    const sensorEl = document.getElementById('sensor-status');
    const powerEl = document.getElementById('power-status');
    const freeSpaceEl = document.getElementById('free-space');
    const updateEl = document.getElementById('overview-update-time');

    if (!doorEl || !sensorEl || !powerEl || !freeSpaceEl || !updateEl) return;

    try
    {
      const res = await fetch('fridge.json', { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP status ' + res.status);
      const data = await res.json();

      doorEl.textContent = data.door || '—';
      sensorEl.textContent = data.sensor || 'Offline';
      powerEl.textContent = data.power || 'Offline';
      freeSpaceEl.textContent = data.free_space != null ? data.free_space : '—';
      updateEl.textContent = 'Last updated: ' + (data.last_updated || '—');
    }
    catch (err)
    {
      console.warn('Failed to load fridge_overview.json, using fallback', err);
      //冰箱默认数据
      doorEl.textContent = 'default-door-state';
      sensorEl.textContent = 'default-sensor-state';
      powerEl.textContent = 'default-power-state';
      freeSpaceEl.textContent = 0;
      updateEl.textContent = 'default-update-time';
    }
  }
)();

//视频
(
  async function loadVideoTimeline()
  {
    const container = document.getElementById('timeline-container');
    if (!container) return console.error('Missing #timeline-container');

    // helper: escape HTML
    function escapeHtml(str)
    {
      return String(str || '').replace(/[&<>"']/g, m => ({
        '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[m]);
    }

    try
    {
      const res = await fetch('videos.json', { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP status ' + res.status);
      const data = await res.json();

      container.innerHTML = ''; // 清空

      data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'timeline-item';
        div.innerHTML = `
        <span>${escapeHtml(item.time)}</span>
        <img class="thumbnail" src="${escapeHtml(item.thumb)}" data-video="${escapeHtml(item.video)}">
        `;
        container.appendChild(div);
      });

      // 点击缩略图播放视频
      container.querySelectorAll('img.thumbnail').forEach(img => {
        img.addEventListener('click', () => {
          const videoSrc = img.dataset.video;
          const videoWindow = window.open('', '_blank', 'width=640,height=480');
          videoWindow.document.write(`
            <video controls autoplay style="width:100%;height:auto;">
            <source src="${videoSrc}" type="video/mp4">
            Your browser does not support the video tag.
            </video>
          `);
        });
      });
    }
    catch (err)
    {
      console.warn('Failed to load videos.json, using fallback data', err);
      // 视频默认测试数据
      const fallback = [
        { time: 'default-update-date1', video: 'videos/video1.mp4', thumb: 'videos/thumb1.jpg' },
        { time: 'default-update-date2', video: 'videos/video2.mp4', thumb: 'videos/thumb2.jpg' }
      ];
      fallback.forEach(item => {
        const div = document.createElement('div');
        div.className = 'timeline-item';
        div.innerHTML = `
          <span>${escapeHtml(item.time)}</span>
          <img class="thumbnail" src="${escapeHtml(item.thumb)}" data-video="${escapeHtml(item.video)}" alt="Fridge event">
        `;
        container.appendChild(div);
      });
    }
  }
)();