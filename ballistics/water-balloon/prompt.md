# Benchmark Specification: Ballistics Water Balloon Slow-Motion Simulation

Generate a complete, single-file `index.html` application containing a physics-based simulation of a projectile penetrating a suspended water balloon observed in 15,000+ FPS slow-motion. Write the completed deliverable directly to `./index.html` in the current working directory, and do not leave auxiliary files in the working directory.

### Mandatory Architecture & Constraints (Universal Standard)
- **Format & Target File:** Exactly one single `.html` file written to `./index.html` containing all HTML, CSS inside `<style>`, and JavaScript inside `<script>`.
- **Permitted External Resource (Single Exception Only):**
  Exactly one external network resource is permitted—the pinned Three.js `r128` global UMD script:
  `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>`
  Do NOT load any other external scripts, `<script type="importmap">`, `esm.sh`, 3D models (`.gltf`, `.glb`, `.obj`), textures/images, HDR/EXR environment maps, web fonts (`@import` or `<link>`), audio files, or CSS files. Do NOT make any `fetch()`, `XMLHttpRequest`, `WebSocket`, or external `THREE.TextureLoader` requests at runtime.
  All procedural textures, sprites, materials, and geometry must be generated dynamically in memory (keep any 2D helper canvases detached in memory; never append helper canvases to the DOM). Because this is the `r128` global UMD build, configure color output with `renderer.outputEncoding = THREE.sRGBEncoding;` (do NOT reference `THREE.SRGBColorSpace`).
- **Deterministic Replay & Frame-Exact Scrubbing (Seed `42`):**
  Implement a deterministic seeded pseudo-random number generator (e.g. Mulberry32 or sfc32 initialized with fixed seed `42`) for all procedural geometry, particle initial states, and physics perturbations. Never call `Math.random()`.
  Simulation state at any logical time `simTime` in `[0, 8.000]` MUST be evaluated deterministically—either via a pure analytical/parametric function `renderAt(simTime)` OR by precomputing/checkpointing fixed `1 / 240` s physics substeps from `simTime = 0` (resetting the PRNG to seed `42` at `simTime = 0` and interpolating fractional remainder)—so that forward playback, backward scrubbing, repeated resets, and 60Hz vs. 120Hz displays produce identical visual states at any given `simTime`. Drive all visual/shader animations from `simTime`, never from frame counters or `Date.now()`.
- **Local Execution:** Opening `./index.html` directly via `file://` in a desktop browser (with internet access for the single pinned Three.js CDN tag) must run cleanly with zero CORS or module errors.

---

### 1. Scene Composition & Camera
- **Backdrop & Stage Canvas:** Mount WebGL strictly onto the canonical `<canvas id="stage"></canvas>` element using `new THREE.WebGLRenderer({ canvas: document.getElementById('stage'), antialias: true, alpha: true })` over the CSS studio radial gradient (`#161922` center fading to `#090a0f` at edges).
- **Renderer DPR & Resize:** Set `renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));` and `renderer.setSize(window.innerWidth, window.innerHeight, false);`. Update camera projection and renderer size cleanly on `window` `resize`.
- **Camera:** Fixed orthographic or narrow perspective camera (85mm equivalent, FOV ≈ 35°), locked along the Z-axis perpendicular to the horizontal flight path (pure lateral cross-section).
- **Subject / Centerpiece (Suspended Water Balloon):**
  - Placed dead center of the screen, suspended from an off-screen tether above.
  - Geometry: Procedural teardrop silhouette reflecting hydrostatic bottom sag (wider bottom, tapering upper neck).
  - Material: Deep crimson red (`#e61c24`), semi-translucent elastic latex using high specular gloss, subtle subsurface transmission, and Fresnel edge highlights.
- **Lighting:** Three-point studio lighting with strong dual rim-lights (cool white and subtle cyan/magenta tint) positioned to illuminate water droplet refraction and edge boundaries.

---

### 2. Physical Phenomena & Dynamic Phases
Simulate the sequential physical phases across the exact active simulation timeline from `simTime = 0.000` s to `simTime = 8.000` s:
1. **Approach (`simTime = 0.000s – 1.000s`):** Conical copper/brass bullet enters horizontally from off-screen right (`+X -> -X`) at high velocity toward the primed balloon.
2. **Elastic Contact & Burst (`simTime = 1.000s – 1.600s`):** Puncture of right latex boundary, elastic indentation, followed by rapid skin tear contracting toward tether and base 3–5× faster than fluid movement.
3. **Inertial Stasis (`simTime = 1.600s – 2.400s`):** Free-standing water mass retains the teardrop balloon shape for a fraction of a second after latex retraction.
4. **Cavitation Tunnel & Wake (`simTime = 2.400s – 3.800s`):** High-speed bullet core creates a low-pressure vapor tunnel; backward cavitation splash vents from right entry hole.
5. **Exit Puncture & Forward Cone (`simTime = 3.800s – 5.000s`):** Bullet emerges from left boundary, projecting a high-velocity forward conical plume of mist and micro-droplets.
6. **Fluid Disintegration & Splashdown (`simTime = 5.000s – 8.000s`):** Rayleigh-Taylor and Plateau-Rayleigh breakup into cascading droplets and fluid sheets falling under gravity.

---

### 3. Timeline, State Machine & Playback Controls
Define total active duration `const DURATION = 8.000;` (in seconds) and implement the following exact 5-state playback state machine (`COUNTDOWN`, `PLAYING`, `PAUSED`, `REFIRE_HOLD`, `ENDED`):

1. **Initial Launch (`COUNTDOWN` State — Exactly 3.000s Wall-Clock):**
   - Start `COUNTDOWN` on the first `requestAnimationFrame` callback after the initial resting scene (`simTime = 0.000`) has rendered (`countdownElapsed = 0`).
   - While `0.000 <= countdownElapsed < 3.000` (measured in real wall-clock seconds, **unaffected** by the speed selector):
     - `0.000 <= countdownElapsed < 1.000`: `#countdown` is visible (`display: block`) with text `"3"`.
     - `1.000 <= countdownElapsed < 2.000`: `#countdown` is visible with text `"2"`.
     - `2.000 <= countdownElapsed < 3.000`: `#countdown` is visible with text `"1"`.
     - `simTime` remains `0.000` and `#scrubber.value` remains `"0"`.
   - At `countdownElapsed >= 3.000`: immediately hide `#countdown` (`display: none` and text `""`), transition to `PLAYING`, and advance `simTime` from `0.000` at rate `dt * playbackSpeed`.
2. **Active Playback (`PLAYING` State) & Endpoint Hold (`ENDED` State):**
   - During `PLAYING`, advance `simTime = Math.min(DURATION, simTime + dt * playbackSpeed)` each frame (clamping per-frame wall `dt` to `<= 0.1` s so background tab switches do not jump the simulation), update `#scrubber.value = simTime.toFixed(3)`, and render `simTime`.
   - When `simTime >= DURATION`, clamp `simTime = DURATION`, set `#scrubber.value = DURATION.toFixed(3)`, render the final state, and transition to `ENDED` (holding the final frame cleanly; `#icon-pause` hides, `#icon-play` shows, and `#btn-toggle` sets `aria-label="Play"`).
3. **Play / Pause Toggle (`#btn-toggle`):**
   - If clicked during `PLAYING`: transition to `PAUSED` (freeze `simTime`, show `#icon-play`, hide `#icon-pause`, set `aria-label="Play"`).
   - If clicked during `COUNTDOWN` or `REFIRE_HOLD`: cancel the countdown/hold immediately, hide `#countdown` (`display: none`), keep `simTime = 0.000`, and transition to `PAUSED`.
   - If clicked during `PAUSED`: transition to `PLAYING` from current `simTime` (show `#icon-pause`, hide `#icon-play`, set `aria-label="Pause"`).
   - If clicked during `ENDED`: reset `simTime = 0.000` and transition immediately to `PLAYING` (with `#countdown` hidden).
4. **Speed Selector Pills (`.speed-pill`):**
   - Clicking a pill sets `playbackSpeed` (`0.25`, `0.5`, `1.0`, or `2.0`), moves `.is-active` and `aria-checked="true"` exclusively to that pill (setting `aria-checked="false"` on the other three), and persists `playbackSpeed` across `Re-fire` and scrubbing.
5. **Scrubbing Slider (`#scrubber`):**
   - Any `input` event on `#scrubber` immediately cancels `COUNTDOWN` or `REFIRE_HOLD` (hiding `#countdown` via `display: none`), sets `simTime = parseFloat(scrubber.value)`, renders `simTime` deterministically, and transitions to `PAUSED` while the user scrubs (or remains `PAUSED` until `#btn-toggle` or `#btn-refire` is pressed).
6. **Silent Re-Fire (`#btn-refire` -> `REFIRE_HOLD` State):**
   - Clicking `#btn-refire` from ANY state cancels any active timers, hides `#countdown` (`display: none`, text `""`), resets `simTime = 0.000` and `#scrubber.value = "0"`, renders the exact initial resting state immediately, shows `#icon-pause` (`aria-label="Pause"`), and enters `REFIRE_HOLD` (`holdElapsed = 0`).
   - `#countdown` MUST remain completely hidden throughout `REFIRE_HOLD`. After **1.000 second** of wall-clock hold (`holdElapsed >= 1.000`, unaffected by `playbackSpeed`), transition automatically to `PLAYING`.

---

### 4. Canonical Minimalist Bottom Dock (UI) & Clean Viewport Contract
To guarantee pixel-accurate alignment in side-by-side multi-model video compositing at `1920x1080`, use the **exact** DOM structure, IDs, attributes, and CSS rules below without adding extra elements, labels, readouts, or wrappers:

#### Canonical `<body>` Markup:
```html
<canvas id="stage"></canvas>
<div id="countdown" aria-hidden="true">3</div>

<div id="dock" role="toolbar" aria-label="Simulation Controls">
  <button id="btn-refire" type="button" aria-label="Re-fire" title="Re-fire">
    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.19"/>
    </svg>
    <span>Re-fire</span>
  </button>
  <span class="dock-sep" aria-hidden="true"></span>
  <button id="btn-toggle" type="button" aria-label="Pause" title="Play / Pause">
    <svg id="icon-pause" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true">
      <rect x="6" y="4" width="4" height="16" rx="1"/>
      <rect x="14" y="4" width="4" height="16" rx="1"/>
    </svg>
    <svg id="icon-play" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true" style="display:none;">
      <path d="M8 5v14l11-7z"/>
    </svg>
  </button>
  <span class="dock-sep" aria-hidden="true"></span>
  <div id="speed-group" role="radiogroup" aria-label="Playback Speed">
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="0.25">0.25×</button>
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="0.5">0.5×</button>
    <button class="speed-pill is-active" type="button" role="radio" aria-checked="true" data-speed="1.0">1.0×</button>
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="2.0">2.0×</button>
  </div>
  <span class="dock-sep" aria-hidden="true"></span>
  <input id="scrubber" type="range" min="0" max="8.000" step="0.001" value="0" aria-label="Timeline Scrubber">
</div>
```

#### Mandatory CSS Rules (include verbatim inside `<style>`; do not override these geometry properties):
```css
*, *::before, *::after {
  box-sizing: border-box;
}
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: radial-gradient(circle at center, #161922 0%, #090a0f 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -webkit-user-select: none;
  user-select: none;
}
#stage {
  display: block;
  width: 100vw;
  height: 100vh;
}

#countdown {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 50;
  pointer-events: none;
  font-size: 96px;
  font-weight: 700;
  line-height: 1;
  color: rgba(255, 255, 255, 0.35);
  font-variant-numeric: tabular-nums;
}

#dock {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 536px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 0 14px;
  background: rgba(15, 17, 23, 0.78);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

#dock button {
  font-family: inherit;
  line-height: 1;
  margin: 0;
  flex-shrink: 0;
  white-space: nowrap;
  appearance: none;
  -webkit-appearance: none;
}

.dock-sep {
  width: 1px;
  height: 18px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.12);
}

#btn-refire {
  width: 78px;
  height: 28px;
  padding: 0 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}
#btn-refire:hover {
  background: rgba(255, 255, 255, 0.16);
}

#btn-toggle {
  width: 28px;
  height: 28px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  color: #ffffff;
  cursor: pointer;
}
#btn-toggle:hover {
  background: rgba(255, 255, 255, 0.16);
}

#speed-group {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}
.speed-pill {
  width: 42px;
  height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 9999px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
}
.speed-pill:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}
.speed-pill.is-active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.2);
}

#scrubber {
  width: 157px;
  height: 4px;
  margin: 0;
  padding: 0;
  flex-shrink: 0;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.22);
  border-radius: 9999px;
  outline: none;
  cursor: pointer;
}
#scrubber::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ffffff;
  border: none;
  cursor: pointer;
}
#scrubber::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ffffff;
  border: none;
  cursor: pointer;
}
```

- **Unobstructed Viewport (Strict):** Do NOT render any other DOM elements, visible text, titles, headings, watermarks, phase labels, FPS counters, HUD readouts, or 2D canvas text overlays anywhere on screen outside of `#countdown` and `#dock`. Note that `#dock` and `#countdown` use translucent studio styling so their geometry, positions, and control widths are pixel-locked across models while subtly blending over each model's rendered scene.

---

### 5. Implementation Strategy Tips (Three.js)
- **Fluid & Splatter Engine:** Use `THREE.InstancedMesh` or a point particle system (2,000 to 6,000 particles) with a custom particle sprite generated dynamically via a 2D offscreen canvas (smooth radial drop with specular hot-spot; keep canvas detached in memory).
- **Membrane Retraction:** Either implement dynamic vertex displacement with an alpha/discard threshold radiating from the impact coordinates, or dual shrinking hemispherical geometry morphing back along the pole axis.
