// ══════════════════ HERO STATE MACHINE ══════════════════
// Phase A: Animation plays, dangers appear. Body is scroll-locked.
// Phase B: User scroll/wheel/touch/key triggers crossfade — animation fades, text appears.
//          Body remains locked until Phase B transition completes.
// Phase C: Scroll unlocked, normal page navigation.

const heroPhase = { current: 'waiting' }; // waiting → animating → dangers → phaseB → done
const threeContainer = document.getElementById('three-container');
const rippleLabels = document.getElementById('ripple-labels');
const labels = document.querySelectorAll('.ripple-label');
const phaseAHint = document.getElementById('phase-a-hint');
const heroText = document.getElementById('hero-text');
const mainNav = document.getElementById('main-nav');

function showDangers() {
  heroPhase.current = 'dangers';
  // Show center label first
  const centerLabel = document.querySelector('.rl-center');
  if (centerLabel) centerLabel.classList.add('show');
  // Shuffle surrounding labels and stagger randomly
  const dangerLabels = Array.from(document.querySelectorAll('.ripple-label:not(.rl-center)'));
  const shuffled = dangerLabels.sort(() => Math.random() - 0.5);
  shuffled.forEach((l, i) => setTimeout(() => l.classList.add('show'), 350 + i * 260));
  // Show scroll hint after all labels appear
  setTimeout(() => {
    phaseAHint.classList.add('show');
    heroPhase.current = 'ready';
  }, 350 + shuffled.length * 260 + 500);
}

function triggerPhaseB() {
  if (heroPhase.current !== 'ready') return;
  heroPhase.current = 'phaseB';

  // Fade out animation + dangers
  threeContainer.classList.add('faded');
  rippleLabels.classList.add('faded');
  phaseAHint.classList.remove('show');

  // Fade in text
  setTimeout(() => {
    heroText.classList.add('show');
  }, 400);

  // Unlock scroll after text is visible
  setTimeout(() => {
    heroPhase.current = 'done';
    document.body.classList.remove('hero-locked');
    mainNav.classList.remove('nav-hidden');
  }, 1600);
}

// Listen for scroll intent (wheel, touch, keyboard)
let touchStartY = 0;

window.addEventListener('wheel', (e) => {
  if (heroPhase.current === 'ready' && e.deltaY > 0) {
    e.preventDefault();
    triggerPhaseB();
  }
}, { passive: false });

window.addEventListener('touchstart', (e) => {
  touchStartY = e.touches[0].clientY;
}, { passive: true });

window.addEventListener('touchmove', (e) => {
  if (heroPhase.current === 'ready') {
    const deltaY = touchStartY - e.touches[0].clientY;
    if (deltaY > 30) {
      e.preventDefault();
      triggerPhaseB();
    }
  }
}, { passive: false });

window.addEventListener('keydown', (e) => {
  if (heroPhase.current === 'ready' &&
      (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown')) {
    e.preventDefault();
    triggerPhaseB();
  }
});

// Second scroll from Phase B text → continue to page
window.addEventListener('wheel', (e) => {
  if (heroPhase.current === 'done' && window.scrollY === 0 && e.deltaY > 0) {
    // Normal scroll takes over — no intervention needed
  }
});


// ══════════════════ THREE.JS — PURPLE DROPLET & RIPPLE ══════════════════

(function() {
  const container = document.getElementById('three-container');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.set(0, 6, 8);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  const waterGeo = new THREE.PlaneGeometry(20, 20, 200, 200);
  waterGeo.rotateX(-Math.PI / 2);

  const poisonPurple = new THREE.Color(0x6D28D9);
  const purpleGlow = new THREE.Color(0x2E1165);

  const waterMat = new THREE.ShaderMaterial({
    transparent: true,
    uniforms: {
      uTime: { value: 0 },
      uDropTime: { value: -1.0 },
      uRippleStrength: { value: 0.0 },
      uColor: { value: new THREE.Color(0x080808) },
      uHighlight: { value: new THREE.Color(0x141422) },
      uPoisonTint: { value: poisonPurple },
    },
    vertexShader: `
      uniform float uTime;
      uniform float uDropTime;
      uniform float uRippleStrength;
      varying vec2 vUv;
      varying float vElevation;

      void main() {
        vUv = uv;
        vec3 pos = position;

        if (uDropTime > 0.0) {
          float t = uTime - uDropTime;
          if (t > 0.0) {
            float dist = length(pos.xz);
            float rippleSpeed = 3.0;
            float rippleFront = t * rippleSpeed;
            float rippleWidth = 1.4 + t * 0.5;
            float ripple = sin((dist - rippleFront) * 3.5) *
                           exp(-pow(dist - rippleFront, 2.0) / rippleWidth) *
                           uRippleStrength * exp(-t * 0.3);
            float ripple2Front = t * rippleSpeed * 0.55;
            float ripple2 = sin((dist - ripple2Front) * 5.5) *
                            exp(-pow(dist - ripple2Front, 2.0) / (rippleWidth * 0.4)) *
                            uRippleStrength * 0.35 * exp(-t * 0.45);
            pos.y += ripple + ripple2;
            vElevation = ripple + ripple2;
          } else { vElevation = 0.0; }
        } else {
          pos.y += sin(pos.x * 0.7 + uTime * 0.25) * 0.012 +
                   sin(pos.z * 0.5 + uTime * 0.18) * 0.008;
          vElevation = 0.0;
        }
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `,
    fragmentShader: `
      uniform float uTime;
      uniform float uDropTime;
      uniform vec3 uColor;
      uniform vec3 uHighlight;
      uniform vec3 uPoisonTint;
      varying vec2 vUv;
      varying float vElevation;

      void main() {
        vec3 base = uColor;
        float gridX = smoothstep(0.48, 0.5, fract(vUv.x * 35.0)) * 0.025;
        float gridZ = smoothstep(0.48, 0.5, fract(vUv.y * 35.0)) * 0.025;
        base += (gridX + gridZ) * uHighlight;

        if (uDropTime > 0.0) {
          float t = uTime - uDropTime;
          float elevAbs = abs(vElevation);
          base = mix(base, uPoisonTint, elevAbs * 2.5 * smoothstep(0.0, 2.5, t));
          base += uHighlight * elevAbs * 3.5;
        }

        float edgeFade = 1.0 - smoothstep(0.3, 0.5, max(abs(vUv.x - 0.5), abs(vUv.y - 0.5)));
        gl_FragColor = vec4(base, edgeFade * 0.85);
      }
    `
  });

  const water = new THREE.Mesh(waterGeo, waterMat);
  scene.add(water);

  // Droplet — starts as sphere, deforms to teardrop during fall
  const dropGeo = new THREE.SphereGeometry(0.13, 24, 24);
  const dropMat = new THREE.MeshBasicMaterial({
    color: 0x6D28D9, transparent: true, opacity: 0.92
  });
  const droplet = new THREE.Mesh(dropGeo, dropMat);
  droplet.position.set(0, 5, 0);
  droplet.visible = false;
  scene.add(droplet);

  // Store original vertex positions for teardrop deformation
  const dropOrigPositions = dropGeo.attributes.position.array.slice();

  function deformToTeardrop(progress) {
    // progress: 0 = sphere, 1 = full teardrop
    const positions = dropGeo.attributes.position.array;
    for (let i = 0; i < positions.length; i += 3) {
      const ox = dropOrigPositions[i];
      const oy = dropOrigPositions[i + 1];
      const oz = dropOrigPositions[i + 2];

      // Stretch vertices above center upward, taper them inward
      if (oy > 0) {
        const t = oy / 0.13; // normalize to 0..1 based on radius
        const stretch = 1 + progress * t * 1.8; // elongate top
        const taper = 1 - progress * t * 0.6; // narrow top
        positions[i] = ox * taper;
        positions[i + 1] = oy * stretch;
        positions[i + 2] = oz * taper;
      } else {
        // Bottom half — slight squash for weight
        const t = Math.abs(oy) / 0.13;
        const squash = 1 - progress * t * 0.15;
        const bulge = 1 + progress * t * 0.2;
        positions[i] = ox * bulge;
        positions[i + 1] = oy * squash;
        positions[i + 2] = oz * bulge;
      }
    }
    dropGeo.attributes.position.needsUpdate = true;
  }

  let dropStarted = false;
  let dropHit = false;
  const dropDelay = 0.8;
  const dropSpeed = 4.8;
  const clock = new THREE.Clock();
  let lastTime = 0;
  const dropStartY = 5;

  heroPhase.current = 'waiting';

  function animate() {
    requestAnimationFrame(animate);
    const elapsed = clock.getElapsedTime();
    const delta = elapsed - lastTime;
    lastTime = elapsed;
    waterMat.uniforms.uTime.value = elapsed;

    if (elapsed > dropDelay && !dropHit) {
      if (!dropStarted) {
        droplet.visible = true;
        dropStarted = true;
        heroPhase.current = 'animating';
      }
      droplet.position.y -= dropSpeed * Math.max(delta, 0.001);

      // Deform from sphere to teardrop as it falls
      const fallProgress = Math.min(1, (dropStartY - droplet.position.y) / dropStartY);
      deformToTeardrop(fallProgress * 0.85);

      if (droplet.position.y <= 0.05) {
        droplet.visible = false;
        dropHit = true;
        waterMat.uniforms.uDropTime.value = elapsed;
        waterMat.uniforms.uRippleStrength.value = 0.4;
        setTimeout(showDangers, 600);
      }
    }

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
})();


// ══════════════════ DARK→LIGHT TRANSITION ══════════════════

const shiftLeftSection = document.getElementById('shift-left');

const transitionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.intersectionRatio > 0.35) {
      shiftLeftSection.classList.add('transitioned');
      mainNav.classList.add('nav-light');
    } else if (entry.intersectionRatio < 0.1) {
      shiftLeftSection.classList.remove('transitioned');
      mainNav.classList.remove('nav-light');
    }
  });
}, { threshold: [0, 0.1, 0.2, 0.35, 0.5] });
transitionObserver.observe(shiftLeftSection);

// Back to dark for alignment
const alignmentSection = document.getElementById('alignment');
const darkNavObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && entry.intersectionRatio > 0.2) {
      mainNav.classList.remove('nav-light');
    }
  });
}, { threshold: [0.2] });
darkNavObserver.observe(alignmentSection);


// ══════════════════ REVEAL ON SCROLL ══════════════════

const revealElements = document.querySelectorAll('.reveal-hp');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
revealElements.forEach(el => revealObserver.observe(el));

const philStatements = document.querySelectorAll('.phil-statement');
const philObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const idx = Array.from(philStatements).indexOf(entry.target);
      setTimeout(() => entry.target.classList.add('visible'), idx * 200);
      philObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });
philStatements.forEach(el => philObserver.observe(el));
