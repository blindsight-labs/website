  // ── THEME TOGGLE ──
  const html = document.documentElement;
  document.getElementById('theme-toggle').addEventListener('click', () => {
    html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    initCanvas();
  });

  // ── TAB FLIPPER ──
  function switchTab(panel, btn) {
    document.querySelectorAll('.flipper-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.flipper-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('panel-' + panel).classList.add('active');
    btn.classList.add('active');
  }

  // ── CANVAS ──
  const canvas = document.getElementById('bg-canvas');
  const ctx = canvas.getContext('2d');
  let W, H, nodes, animId;

  function getNodeColor() {
    return html.getAttribute('data-theme') === 'dark' ? '197,197,197' : '60,60,60';
  }

  function initCanvas() {
    cancelAnimationFrame(animId);
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    const count = Math.max(20, Math.floor((W * H) / 26000));
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
      r: Math.random() * 1.8 + 0.8, pulse: Math.random() * Math.PI * 2,
    }));
    drawCanvas();
  }

  function drawCanvas() {
    ctx.clearRect(0, 0, W, H);
    const col = getNodeColor();
    const maxDist = 140;
    const scrollFrac = window.scrollY / (document.body.scrollHeight - window.innerHeight || 1);

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
        const d = Math.sqrt(dx*dx + dy*dy);
        if (d < maxDist) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(${col},${(1 - d/maxDist) * (0.08 + scrollFrac * 0.18)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }
    nodes.forEach(n => {
      n.pulse += 0.018;
      const glow = (0.25 + Math.sin(n.pulse) * 0.2) * (0.6 + scrollFrac * 0.7);
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r + scrollFrac, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${col},${glow})`;
      ctx.fill();
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
    });
    animId = requestAnimationFrame(drawCanvas);
  }

  window.addEventListener('resize', initCanvas);
  initCanvas();

  // ── DEPTH INDICATOR ──
  const dot = document.getElementById('depth-dot');
  const z1El = document.getElementById('zone-1');
  const z2El = document.getElementById('zone-2');
  const z3El = document.getElementById('zone-3');
  const zlabels = [document.getElementById('zlabel-1'), document.getElementById('zlabel-2'), document.getElementById('zlabel-3')];

  function updateDepth() {
    const sy = window.scrollY + window.innerHeight / 2;
    let zone = sy > z2El.offsetTop + z2El.offsetHeight ? 3 : sy > z1El.offsetTop + z1El.offsetHeight ? 2 : 1;
    dot.style.top = (zone === 1 ? 0 : zone === 2 ? 50 : 95) + '%';
    dot.className = 'depth-marker zone-' + zone;
    zlabels.forEach((l, i) => l.classList.toggle('active', i + 1 === zone));
  }

  window.addEventListener('scroll', updateDepth, { passive: true });
  window.addEventListener('scroll', () => {
    const f = window.scrollY / (document.body.scrollHeight - window.innerHeight || 1);
    canvas.style.opacity = Math.min(0.7, parseFloat(getComputedStyle(html).getPropertyValue('--canvas-op')) + f * 0.22);
  }, { passive: true });
  updateDepth();

  // ── REVEAL ──
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(r => observer.observe(r));

  // ── STAGGER BEATS ──
  const beats = document.querySelectorAll('.mechanism-beat');
  const beatObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        beats.forEach((b, i) => setTimeout(() => { b.style.opacity = '1'; b.style.transform = 'translateY(0)'; }, i * 100));
        beatObs.disconnect();
      }
    });
  }, { threshold: 0.15 });
  beats.forEach(b => { b.style.opacity = '0'; b.style.transform = 'translateY(16px)'; b.style.transition = 'opacity 0.5s ease, transform 0.5s ease'; });
  if (beats[0]) beatObs.observe(beats[0]);

  // ── GA EVENT TRACKING ──
  document.querySelectorAll('a[href*="tally.so"]').forEach(link => {
    link.addEventListener('click', () => {
      gtag('event', 'cta_click', {
        event_category: 'engagement',
        event_label: link.textContent.trim().replace(/\s+/g, ' ')
      });
    });
  });
