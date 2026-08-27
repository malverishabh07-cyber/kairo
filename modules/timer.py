"""
Kairo — Focus Timer Module
Features a circular glowing SVG progress ring, real-time tick countdown,
ambient focus soundscapes, streak/XP rewards, and keyboard shortcuts.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.storage_helper import complete_focus_session, save_user_data

def render_timer():
    # Header Banner
    st.markdown(
        """
        <div class="kairo-header page-enter">
            <div>
                <h1 class="kairo-title">⏱️ Focus Timer</h1>
                <p class="kairo-tagline">Enter flow state · <b>Space</b> to start/pause · <b>R</b> to reset</p>
            </div>
            <div style="text-align: right;">
                <span style="background: rgba(var(--accent-rgb), 0.15); color: var(--primary-accent); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(var(--accent-rgb), 0.3);">
                    🧠 Deep Flow Protocol
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Session stats
    streak = st.session_state.get("study_streak", 12)
    xp = st.session_state.get("user_xp", 1450)
    sessions_done = st.session_state.get("focus_sessions_completed", 16)
    theme = st.session_state.get("theme_preset", "cyan_violet")

    # Mode Selector Tabs
    mode_cols = st.columns([1, 1, 1, 1])
    if "timer_mode" not in st.session_state:
        st.session_state["timer_mode"] = "Focus (25m)"

    modes = ["Focus (25m)", "Short Break (5m)", "Long Break (15m)", "Custom (50m)"]
    for i, m in enumerate(modes):
        with mode_cols[i]:
            is_active = (st.session_state["timer_mode"] == m)
            btn_style = "primary" if is_active else "secondary"
            if st.button(m, key=f"mode_btn_{i}", use_container_width=True, type=btn_style):
                st.session_state["timer_mode"] = m
                st.rerun()

    current_mode = st.session_state["timer_mode"]
    if "25m" in current_mode:
        duration_sec = 25 * 60
        mode_title = "FOCUS"
    elif "5m" in current_mode:
        duration_sec = 5 * 60
        mode_title = "SHORT BREAK"
    elif "15m" in current_mode:
        duration_sec = 15 * 60
        mode_title = "LONG BREAK"
    else:
        duration_sec = 50 * 60
        mode_title = "DEEP FOCUS"

    # Sound options
    sound_choice = st.session_state.get("ambient_sound", "lofi")
    sound_enabled = st.session_state.get("ambient_sound_enabled", True)

    # Primary colors mapped from theme
    color_map = {
        "cyan_violet": ("#00f2fe", "#7f00ff", "0, 242, 254"),
        "emerald_amber": ("#10b981", "#f59e0b", "16, 185, 129"),
        "rose_indigo": ("#f43f5e", "#6366f1", "244, 63, 94"),
        "amber_slate": ("#f59e0b", "#94a3b8", "245, 158, 11"),
    }
    primary_color, sec_color, rgb_str = color_map.get(theme, ("#00f2fe", "#7f00ff", "0, 242, 254"))

    # Render Interactive Real-Time JavaScript Circular Timer Component
    timer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
      <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }}
        body {{
          background: transparent;
          color: #f8fafc;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          overflow: hidden;
        }}
        .timer-card {{
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          width: 100%;
          padding: 10px 0;
        }}
        .timer-wrap {{
          position: relative;
          width: 290px;
          height: 290px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 1.5rem;
        }}
        .timer-svg {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          transform: rotate(-90deg);
        }}
        .circle-bg {{
          fill: none;
          stroke: rgba(255, 255, 255, 0.06);
          stroke-width: 10;
        }}
        .circle-progress {{
          fill: none;
          stroke: url(#timerGrad);
          stroke-width: 10;
          stroke-linecap: round;
          stroke-dasharray: 816.8;
          stroke-dashoffset: 0;
          filter: drop-shadow(0 0 14px rgba({rgb_str}, 0.65));
          transition: stroke-dashoffset 0.8s linear;
        }}
        .timer-info {{
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          z-index: 5;
        }}
        .timer-time {{
          font-size: 4.4rem;
          font-weight: 900;
          letter-spacing: -0.03em;
          color: #ffffff;
          text-shadow: 0 0 24px rgba({rgb_str}, 0.5);
          line-height: 1;
        }}
        .timer-status {{
          font-size: 0.9rem;
          font-weight: 700;
          letter-spacing: 0.18em;
          text-transform: uppercase;
          color: #94a3b8;
          margin-top: 0.6rem;
        }}
        .controls-row {{
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1.4rem;
          margin-bottom: 0.5rem;
        }}
        .btn {{
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
        }}
        .btn:hover {{
          transform: scale(1.12);
        }}
        .btn:active {{
          transform: scale(0.95);
        }}
        .btn-side {{
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background: rgba(22, 31, 51, 0.85);
          border: 1px solid rgba({rgb_str}, 0.3);
          color: #f8fafc;
          font-size: 1.25rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        .btn-side:hover {{
          border-color: {primary_color};
          box-shadow: 0 0 18px rgba({rgb_str}, 0.4);
          color: {primary_color};
        }}
        .btn-main {{
          width: 72px;
          height: 72px;
          border-radius: 50%;
          background: linear-gradient(135deg, {primary_color} 0%, {sec_color} 100%);
          color: #ffffff;
          font-size: 1.8rem;
          box-shadow: 0 6px 28px rgba({rgb_str}, 0.45);
        }}
        .btn-main:hover {{
          box-shadow: 0 8px 38px rgba({rgb_str}, 0.7);
        }}
        .celebrate-pulse {{
          animation: popScale 0.6s ease-out;
        }}
        @keyframes popScale {{
          0% {{ transform: scale(0.9); }}
          50% {{ transform: scale(1.08); }}
          100% {{ transform: scale(1); }}
        }}
      </style>
    </head>
    <body>
      <div class="timer-card">
        <div class="timer-wrap" id="timerWrap">
          <svg class="timer-svg" viewBox="0 0 280 280">
            <defs>
              <linearGradient id="timerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{primary_color}" />
                <stop offset="100%" stop-color="{sec_color}" />
              </linearGradient>
            </defs>
            <circle class="circle-bg" cx="140" cy="140" r="130" />
            <circle class="circle-progress" id="progressRing" cx="140" cy="140" r="130" />
          </svg>
          <div class="timer-info">
            <div class="timer-time" id="timeDisplay">25:00</div>
            <div class="timer-status" id="statusLabel">{mode_title}</div>
          </div>
        </div>

        <div class="controls-row">
          <button class="btn btn-side" id="resetBtn" title="Reset (R)">🔄</button>
          <button class="btn btn-main" id="playBtn" title="Start/Pause (Space)">▶</button>
          <button class="btn btn-side" id="soundBtn" title="Soundscape">{'🔊' if sound_enabled else '🔇'}</button>
        </div>
      </div>

      <script>
        const TOTAL_SECONDS = {duration_sec};
        let remainingSeconds = TOTAL_SECONDS;
        let isRunning = false;
        let timerInterval = null;
        const CIRCUMFERENCE = 2 * Math.PI * 130;

        const timeDisplay = document.getElementById('timeDisplay');
        const progressRing = document.getElementById('progressRing');
        const playBtn = document.getElementById('playBtn');
        const resetBtn = document.getElementById('resetBtn');
        const soundBtn = document.getElementById('soundBtn');
        const timerWrap = document.getElementById('timerWrap');

        let audioCtx = null;
        let noiseNode = null;
        let gainNode = null;
        let soundActive = {'true' if sound_enabled else 'false'};

        function initAudio() {
          if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          }
        }

        function playChime() {
          try {
            initAudio();
            const osc = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880.00, audioCtx.currentTime + 0.3);
            g.gain.setValueAtTime(0.3, audioCtx.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            osc.connect(g);
            g.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 1.2);
          } catch(e) {}
        }

        function startAmbientNoise() {
          if (!soundActive) return;
          try {
            initAudio();
            if (audioCtx.state === 'suspended') {
              audioCtx.resume();
            }
            const bufferSize = audioCtx.sampleRate * 2;
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            let lastOut = 0.0;
            for (let i = 0; i < bufferSize; i++) {
              const white = Math.random() * 2 - 1;
              data[i] = (lastOut + (0.02 * white)) / 1.02;
              lastOut = data[i];
              data[i] *= 3.5;
            }
            noiseNode = audioCtx.createBufferSource();
            noiseNode.buffer = buffer;
            noiseNode.loop = true;

            const filter = audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(400, audioCtx.currentTime);

            gainNode = audioCtx.createGain();
            gainNode.gain.setValueAtTime(0.06, audioCtx.currentTime);

            noiseNode.connect(filter);
            filter.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            noiseNode.start(0);
          } catch(e) {}
        }

        function stopAmbientNoise() {
          if (noiseNode) {
            try { noiseNode.stop(); noiseNode.disconnect(); } catch(e) {}
            noiseNode = null;
          }
        }

        function updateDisplay() {
          const mins = Math.floor(remainingSeconds / 60);
          const secs = remainingSeconds % 60;
          timeDisplay.textContent = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;

          const progressRatio = remainingSeconds / TOTAL_SECONDS;
          const offset = CIRCUMFERENCE * (1 - progressRatio);
          progressRing.style.strokeDashoffset = offset;
        }

        function toggleTimer() {
          if (isRunning) {
            clearInterval(timerInterval);
            isRunning = false;
            playBtn.textContent = '▶';
            stopAmbientNoise();
          } else {
            isRunning = true;
            playBtn.textContent = '⏸';
            startAmbientNoise();
            timerInterval = setInterval(() => {
              if (remainingSeconds > 0) {
                remainingSeconds--;
                updateDisplay();
              } else {
                clearInterval(timerInterval);
                isRunning = false;
                playBtn.textContent = '▶';
                stopAmbientNoise();
                playChime();
                timerWrap.classList.add('celebrate-pulse');
                setTimeout(() => timerWrap.classList.remove('celebrate-pulse'), 1200);
              }
            }, 1000);
          }
        }

        function resetTimer() {
          clearInterval(timerInterval);
          isRunning = false;
          playBtn.textContent = '▶';
          remainingSeconds = TOTAL_SECONDS;
          stopAmbientNoise();
          updateDisplay();
        }

        playBtn.addEventListener('click', toggleTimer);
        resetBtn.addEventListener('click', resetTimer);

        soundBtn.addEventListener('click', () => {
          soundActive = !soundActive;
          soundBtn.textContent = soundActive ? '🔊' : '🔇';
          if (isRunning) {
            if (soundActive) startAmbientNoise();
            else stopAmbientNoise();
          }
        });

        window.addEventListener('keydown', (e) => {
          if (e.code === 'Space') {
            e.preventDefault();
            toggleTimer();
          } else if (e.code === 'KeyR') {
            e.preventDefault();
            resetTimer();
          }
        });

        updateDisplay();
      </script>
    </body>
    </html>
    """

    components.html(timer_html, height=430)

    # Sync Focus Session Completion to Shared Profile
    col_claim1, col_claim2 = st.columns([2, 1])
    with col_claim1:
        st.markdown(
            f"""
            <div style="background: rgba(22, 31, 51, 0.6); border: 1px solid var(--border-glass); border-radius: 12px; padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="font-weight: 700; color: var(--primary-accent);">🏆 Session Rewards</span>
                    <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 2px;">Completed your 25m focus block? Record it to claim XP and sync with Analytics!</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_claim2:
        if st.button("🎉 Complete & Claim +50 XP", use_container_width=True):
            complete_focus_session(25.0)
            st.success("🔥 +50 XP earned! Study streak & analytics updated!")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Three Stat Cards (Streak / XP / Ambient Audio)
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div style="font-size: 2.2rem; color: var(--color-streak);" class="flame-icon">🔥</div>
                <div class="metric-val" style="color: var(--color-streak); background: none; -webkit-text-fill-color: var(--color-streak);">{streak} Days</div>
                <div class="metric-lbl">Daily Focus Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s2:
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div style="font-size: 2.2rem; color: var(--color-xp);">⚡</div>
                <div class="metric-val" style="color: var(--color-xp); background: none; -webkit-text-fill-color: var(--color-xp);">{xp:,} XP</div>
                <div class="metric-lbl">Total Flow XP</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s3:
        status_text = "On (Lo-Fi Ambient)" if sound_enabled else "Muted"
        st.markdown(
            f"""
            <div class="metric-card stagger-item">
                <div style="font-size: 2.2rem; color: var(--color-ambient);">🎵</div>
                <div class="metric-val" style="color: var(--color-ambient); background: none; -webkit-text-fill-color: var(--color-ambient); font-size: 1.6rem;">{status_text}</div>
                <div class="metric-lbl">Focus Soundscape</div>
            </div>
            """,
            unsafe_allow_html=True
        )
