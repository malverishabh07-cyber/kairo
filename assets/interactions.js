/**
 * Kairo — Interactive JavaScript Physics & Cursor Engine
 * Two-layer trailing cursor ring + lagging orb, magnetic button hover, and keyboard shortcuts.
 */
(function () {
  'use strict';

  // Check if touch or reduced motion
  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const isReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Two-Layer Spring Trailing Custom Cursor
  if (!isTouch && !isReducedMotion) {
    let ring = document.getElementById('kairo-cursor-ring');
    let dot = document.getElementById('kairo-cursor-dot');

    if (!ring) {
      ring = document.createElement('div');
      ring.id = 'kairo-cursor-ring';
      document.body.appendChild(ring);
    }
    if (!dot) {
      dot = document.createElement('div');
      dot.id = 'kairo-cursor-dot';
      document.body.appendChild(dot);
    }

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let ringX = mouseX, ringY = mouseY;
    let dotX = mouseX, dotY = mouseY;
    let isVisible = false;

    // Track mouse coordinates
    document.addEventListener('mousemove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isVisible) {
        ring.style.opacity = '1';
        dot.style.opacity = '1';
        isVisible = true;
      }
    });

    document.addEventListener('mouseleave', function () {
      if (ring) ring.style.opacity = '0';
      if (dot) dot.style.opacity = '0';
      isVisible = false;
    });

    document.addEventListener('mousedown', function () {
      if (ring) ring.classList.add('cursor-active');
    });

    document.addEventListener('mouseup', function () {
      if (ring) ring.classList.remove('cursor-active');
    });

    // Spring/Inertial Physics Loop
    function renderCursor() {
      // Ring follows pointer with spring easing (0.16)
      ringX += (mouseX - ringX) * 0.16;
      ringY += (mouseY - ringY) * 0.16;

      // Small orb is offset near ring's edge (12px offset) and lags further (0.09)
      const targetDotX = mouseX + 11;
      const targetDotY = mouseY + 11;
      dotX += (targetDotX - dotX) * 0.09;
      dotY += (targetDotY - dotY) * 0.09;

      if (ring) {
        ring.style.left = ringX + 'px';
        ring.style.top = ringY + 'px';
      }
      if (dot) {
        dot.style.left = dotX + 'px';
        dot.style.top = dotY + 'px';
      }

      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Hover detection for buttons, cards, links, tabs
    document.addEventListener('mouseover', function (e) {
      const target = e.target.closest(
        'button, .stButton > button, .stDownloadButton > button, .glass-card, .metric-card, ' +
        'a, [role="button"], [role="tab"], input, textarea, select, .timer-ctrl-btn, .timer-play-btn, .timer-mode-pill, .floating-ai-launcher'
      );
      if (target && ring) {
        ring.classList.add('cursor-hover');
      }
    });

    document.addEventListener('mouseout', function (e) {
      const target = e.target.closest(
        'button, .stButton > button, .stDownloadButton > button, .glass-card, .metric-card, ' +
        'a, [role="button"], [role="tab"], input, textarea, select, .timer-ctrl-btn, .timer-play-btn, .timer-mode-pill, .floating-ai-launcher'
      );
      if (target && ring) {
        ring.classList.remove('cursor-hover');
      }
    });
  }

  // 2. Magnetic Pull on Primary Interactive Elements
  if (!isTouch && !isReducedMotion) {
    document.addEventListener('mousemove', function (e) {
      const magneticElements = document.querySelectorAll(
        '.stButton > button, .timer-play-btn, .timer-ctrl-btn, .floating-ai-launcher'
      );

      magneticElements.forEach(function (el) {
        const rect = el.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const dist = Math.hypot(e.clientX - centerX, e.clientY - centerY);
        const radius = 65; // Magnetic detection radius

        if (dist < radius) {
          const pullFactor = (radius - dist) / radius;
          const pullX = (e.clientX - centerX) * pullFactor * 0.35;
          const pullY = (e.clientY - centerY) * pullFactor * 0.35;
          el.style.transform = `translate(${pullX}px, ${pullY}px) scale(1.04)`;
        } else {
          if (el.style.transform && el.style.transform.includes('translate')) {
            el.style.transform = '';
          }
        }
      });
    });
  }

  // 3. Ripple Feedback on Click
  document.addEventListener('click', function (e) {
    const target = e.target.closest('.stButton > button, .glass-card, .metric-card, .timer-ctrl-btn');
    if (!target) return;

    const rect = target.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple-effect';
    ripple.style.left = (e.clientX - rect.left) + 'px';
    ripple.style.top = (e.clientY - rect.top) + 'px';

    target.appendChild(ripple);\n    setTimeout(function () {\n      ripple.remove();\n    }, 600);\n  });\n\n  // 4. Keyboard Shortcuts: Space to Start/Pause, R to Reset\n  document.addEventListener('keydown', function (e) {\n    // Ignore if typing in input or textarea\n    const activeEl = document.activeElement;\n    if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA')) {\n      return;\n    }\n\n    if (e.code === 'Space') {\n      const playBtn = document.querySelector('.timer-play-btn, button[data-testid=\"timer-play-trigger\"]');\n      if (playBtn) {\n        e.preventDefault();\n        playBtn.click();\n      }\n    } else if (e.code === 'KeyR') {\n      const resetBtn = document.querySelector('.timer-reset-btn, button[data-testid=\"timer-reset-trigger\"]');\n      if (resetBtn) {\n        e.preventDefault();\n        resetBtn.click();\n      }\n    }\n  });\n\n})();\n