# Benchmark Specification: Storm Titan: Tethered Hunter vs. Lightning-Bound Boulder Golem

Generate a complete, single-file `index.html` application containing a physics-based simulation of a self-playing boss-fight slice from an original 3D action game: a small, agile hunter with a grappling tether fights a 40 m golem made of magnetized boulders held together by arcing lightning, on a wind-swept grass plateau in a rainstorm. Over a fixed 40-second fight the hunter tethers onto the Titan three times, breaks three glowing weak points, is knocked flying once and recovers, and brings the Titan down in a collapse of falling boulders. Write the completed deliverable directly to `./index.html` in the current working directory, and do not leave auxiliary files in the working directory.

### Mandatory Architecture & Constraints (Universal Standard)
- **Format & Target File:** Exactly one single `.html` file written to `./index.html` containing all HTML, CSS inside `<style>`, and JavaScript inside `<script>`.
- **Permitted External Resource (Single Exception Only):**
  Exactly one external network resource is permitted—the pinned Three.js `r128` global UMD script:
  `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>`
  Do NOT load any other external scripts, `<script type="importmap">`, `esm.sh`, 3D models (`.gltf`, `.glb`, `.obj`), textures/images, HDR/EXR environment maps, web fonts (`@import` or `<link>`), audio files, or CSS files. Do NOT make any `fetch()`, `XMLHttpRequest`, `WebSocket`, or external `THREE.TextureLoader` requests at runtime.
  All procedural textures, sprites, materials, and geometry must be generated dynamically in memory (keep any 2D helper canvases detached in memory; never append helper canvases to the DOM). Because this is the `r128` global UMD build, configure color output with `renderer.outputEncoding = THREE.sRGBEncoding;` (do NOT reference `THREE.SRGBColorSpace`).
- **Deterministic Replay & Frame-Exact Scrubbing (Seed `42`):**
  Implement a deterministic seeded pseudo-random number generator (e.g. Mulberry32 or sfc32 initialized with fixed seed `42`) for all procedural geometry, particle initial states, and physics perturbations. Never call `Math.random()`.
  Simulation state at any logical time `simTime` in `[0, 40]` MUST be evaluated deterministically—either via a pure analytical/parametric function `renderAt(simTime)` OR by precomputing/checkpointing fixed `1 / 240` s physics substeps from `simTime = 0` (resetting the PRNG to seed `42` at `simTime = 0` and interpolating fractional remainder)—so that forward playback, backward scrubbing, repeated resets, and 60Hz vs. 120Hz displays produce identical visual states at any given `simTime`. Drive all visual/shader animations from `simTime`, never from frame counters or `Date.now()`.
- **Local Execution:** Opening `./index.html` directly via `file://` in a desktop browser (with internet access for the single pinned Three.js CDN tag) must run cleanly with zero CORS or module errors.

---

### 1. Scene Composition & Camera
- **Backdrop & Stage Canvas:** Mount WebGL strictly onto the canonical `<canvas id="stage"></canvas>` element using `new THREE.WebGLRenderer({ canvas: document.getElementById('stage'), antialias: true, alpha: true })` over the CSS studio radial gradient (`#161922` center fading to `#090a0f` at edges).
- **Renderer DPR & Resize:** Set `renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));` and `renderer.setSize(window.innerWidth, window.innerHeight, false);`. Update camera projection and renderer size cleanly on `window` `resize`.
- **Camera:** One `THREE.PerspectiveCamera` (near `0.1`, far `2000`) whose position, look-at target and vertical FOV are a pure function of `simTime` following the exact shot schedule below. Shots change with hard cuts at the listed times. `H` is the hunter's chest position, `Hs` is `H` smoothed in closed form (the average of `H` evaluated at `simTime - k * 0.05` for `k = 0..7`, clamped at `0`; never a per-frame damped value), `TC` is the Titan's chest bone position, `MID = (H + TC) / 2`, and `vH` is the hunter's speed in m/s. The same schedule must keep the hunter and the Titan's upper body inside the frame at `16:9` and at portrait `1280×1340`.
  | Shot | `simTime` window | Camera position | Look-at target | Base FOV |
  | :--- | :--- | :--- | :--- | :--- |
  | 1. Establishing | `[0, 3)` | fixed `(-70, 6, 50)` | `MID` | 40° |
  | 2. Follow, first tether | `[3, 9)` | `Hs` + 9 m back along the horizontal direction from the Titan to the hunter + `(0, 3, 0)` | point 35% of the way from `Hs` to `TC` | 55° |
  | 3. Orbit | `[9, 16)` | on a circle of radius 55 m and height 12 m around the Titan's pelvis ground point, at angle `200° + 6° * (simTime - 9)` | `0.6 * TC + 0.4 * Hs` | 45° |
  | 4. Low wide, the sweep | `[16, 22.5)` | fixed `(-14, 1.5, -46)` | `MID` | 42° |
  | 5. Close chase | `[22.5, 29.5)` | `Hs` + 6 m behind the hunter's direction of travel + `(0, 2, 0)` | weak point `W3` | 60° |
  | 6. Wide, the collapse | `[29.5, 36)` | fixed `(-74, 25, -60)` | `(16, 14, 0)` | 38° |
  | 7. Aftermath pull-back | `[36, 40]` | `H + (-8 - 2 * (simTime - 36), 2 + 0.5 * (simTime - 36), 6)` | `H + (0, 1, 0)` | 35° |

  In shots 2 and 5 compose the frame so the hunter sits near the lower-left rule-of-thirds point and the targeted weak point near the upper-right one.
  **Camera feel (all closed-form in `simTime`, so scrubbing gives the identical frame):**
  - *Trauma shake:* each event in the event table (section 2) adds its listed trauma at its event time; trauma decays linearly at `0.8` per second and is clamped to `[0, 1]`. Shake offset is `trauma²` times smooth seeded noise of `simTime` (up to 0.6 m of translation and 2.5° of rotation at trauma `1`).
  - *FOV kick:* in shots 2 and 5, FOV = base + `min(12, 0.4 * vH)` degrees.
  - *Chromatic aberration:* a full-screen post pass splits the red and blue channels radially by up to 6 px, proportional to `trauma²`, visible only on the heaviest events.
- **Subject / Centerpiece:**
  - **Geometry & Placement:**
    - **World:** World units are metres, `+Y` is up. The plateau is a disc of radius 90 m centred on the origin with gentle procedural height variation (within ±0.6 m) and a cliff edge falling away into fog. Wind blows toward `+X` throughout.
    - **Titan (skeleton must be followed exactly):** A hierarchical skeleton of 14 bones posed entirely in code from `simTime` (no keyframe data files): pelvis (rest height 18 m), spine, chest, head, and for each side upper arm, forearm, fist, thigh, shin and foot. Standing height is about 40 m, shoulder width about 16 m, each arm about 17 m long and each leg about 18 m. Every bone carries a cluster of 6 to 12 irregular boulders (instanced, at least 120 boulders in total, 1 to 4 m across) that float a short distance off the bone, each drifting and slowly rotating around its own seeded offset. No boulder touches another: they are held together by lightning arcs (see Lighting). The Titan starts at pelvis ground point `(40, 0, 0)` facing `-X`.
    - **Weak points:** Three glowing cores, each a 1.2 m emissive sphere seated among the boulders: `W1` on the left knee, `W2` on the right shoulder, `W3` in the centre of the chest. A weak point glows amber while intact, flashes white when struck and goes dark when broken (after its last strike in the event table). `W3` is hidden behind chest boulders until the sky lightning strike at `simTime = 25.000` parts them.
    - **Hunter:** An original humanoid figure 1.8 m tall built from code-generated geometry (at least 12 separately posed parts: head, torso, pelvis, upper and lower arms, hands, upper and lower legs), with a short cloak, a wrist-mounted tether launcher and a glowing blade. It starts at `(-40, 0, 10)`. Use an invented design only: no characters, creatures, logos or names from any existing game or film.
    - **Grass:** An instanced field with a target of 100,000 blades covering the plateau, each blade a tapered, slightly curved strip 0.4 to 0.9 m tall with seeded position, height, lean and colour. Blade bending is computed in the vertex shader as a closed-form function of `simTime`: a travelling wind sway along `+X`, plus a radial push away from every footfall and shockwave ring in the event table (ring radius grows at 30 m/s from the event time and position; blades inside the ring's 4 m wide front are flattened outward and recover over 1.5 s).
    - **Rain:** A target of 20,000 instanced streaks falling at about 30° from vertical toward `+X`, positioned in closed form from `simTime` (seeded start position plus velocity times `simTime`, wrapped inside a volume that follows the camera), with small splash rings where they meet the ground near the camera.
    - **Tethers (real rope simulation):** Each of the three tethers is a Verlet chain of at least 24 points with distance constraints, gravity and wind, pinned at one end to its anchor bone on the Titan and at the other to the hunter's launcher, and colliding with capsules around the Titan's bones so the line visibly sags, whips and wraps around the limb. Step each rope at a fixed `1 / 240` s from its own fire time (re-simulating from the fire time when the scrubber moves backward), so its shape at any `simTime` is identical on every run. During the swing windows in the event table the rope is taut and the hunter moves on an arc at constant rope length around the anchor.
    - **Hunter ragdoll:** From the sweep hit at `simTime = 19.000` until `21.500` the hunter is a Verlet ragdoll of at least 11 point masses joined by stick constraints with ground collision, launched with initial velocity `(-14, 9, -6)` m/s and stepped at a fixed `1 / 240` s from the hit time. From `21.500` to `22.500` every body part is interpolated from its ragdoll pose to the animated get-up pose (a smooth blend, not a snap).
    - **Hit-stop:** Each strike in the event table freezes scene motion. Define `motionTime(simTime)`: it equals `simTime` except that it holds at the strike time for the listed hit-stop duration and then catches up linearly over the following `0.300` s. The Titan, hunter, ropes, boulders, grass and rain are evaluated at `motionTime`; camera shake, strike sparks, the HUD and audio use `simTime`.
  - **Materials:** Boulders are dark wet basalt with procedural cracks and veins of faint blue emissive ore that brighten near active lightning arcs. The hunter has matte cloth, worn leather and brushed-metal armour with one saturated accent colour so it stays readable against the grass at a distance. Grass is a two-tone green with a paler tip. **Wetness (must be visible):** a global `wetness` value rises linearly from `0` at `simTime = 0` to `1` at `simTime = 30` and stays there; boulder, hunter and ground materials move from roughness `0.9` to `0.35` and gain specular response in proportion to it, so surfaces visibly darken and pick up sharper lightning highlights as the fight goes on. Generate one storm environment map at startup with `THREE.PMREMGenerator` from an in-memory scene (dark cloud dome with a brighter horizon band) so wet surfaces have something to reflect.
- **Lighting:** A dark, overcast storm in late dusk. Set an opaque procedural sky as the scene background (layered grey-blue cloud with slow drift driven by `simTime`), covering the CSS gradient, with exponential fog that swallows the plateau edge. Keep ambient fill at or below intensity `0.25`; a single cool directional key light with shadows gives the Titan and hunter readable form, and use `renderer.toneMapping = THREE.ACESFilmicToneMapping`. **Binding lightning:** jagged blue-white arcs (at least 40 at a time) jump between neighbouring boulders and along each bone; each arc's path is regenerated from a seeded hash of `floor(simTime * 20)`, so the arcs flicker at 20 Hz yet are identical at any given `simTime`. Arcs light nearby boulders and grass. Arc brightness and count scale with a per-bone `charge` value: `1` normally, `1.6` during attacks, `0.4` during the stagger, and falling to `0` bone by bone during the collapse. **Sky lightning:** three strikes at `simTime = 8.200`, `25.000` (hits the Titan's head) and `33.000`, each a branching bolt visible for 0.25 s with a full-scene flash that decays over 0.4 s. Weak points, the hunter's blade, strike sparks and tether lines are emissive.

---

### 2. Physical Phenomena & Dynamic Phases
Simulate the sequential physical phases across the exact active simulation timeline from `simTime = 0.000` s to `simTime = 40` s:
**Standardized fight (must be followed exactly).** The event table fixes what happens and when; how the hunter moves between events is yours to design, provided it reaches each event on time and the motion reads as agile and continuous. All times are `simTime` in seconds. Trauma is the camera-shake value added (section 1). Boss health starts at `2000`.

| `simTime` | Event | Trauma | Notes |
| ---: | :--- | ---: | :--- |
| 1.000, 2.500, 4.000, 5.500 | Titan footfall (left, right, left, right) | 0.25 | Shockwave ring through the grass from the foot position |
| 3.000 | Tether 1 fired at the left shin | 0 | Line reaches the shin and attaches at `3.300` |
| 3.300 – 5.000 | Swing 1 | 0 | Hunter swings around the left leg; the line wraps at least one full turn |
| 5.000 | **Strike on `W1`**, damage `400` | 0.45 | Hit-stop `0.100` s. Stagger gauge to 50%. `W1` broken |
| 5.600 | Tether 1 released | 0 | Hunter drops to the grass and runs clear |
| 6.000 – 7.500 | Slam wind-up (right fist raised) | 0 | Titan stops walking at `6.000` with its pelvis over `(16, 0, 0)` |
| 7.500 | **Fist slam** on the hunter's position at `6.500` | 0.9 | Largest shockwave ring; dirt and torn grass thrown up; hunter is already clear |
| 8.200 | Sky lightning | 0.3 | Strikes the plateau edge |
| 9.000 | Tether 2 fired at the right forearm | 0 | Attaches at `9.300`; the fist stays planted until `10.500`, then the arm lifts the hunter with it |
| 12.000 | **Strike on `W2`**, damage `600` | 0.55 | Hit-stop `0.100` s. Stagger gauge to 100%: stagger begins. `W2` broken |
| 12.000 – 16.000 | **Stagger** | 0 | Titan reels; arcs dim; tether 2 released at `12.400`; hunter lands at `13.500` |
| 13.000 | Titan's left knee hits the ground | 0.7 | Shockwave ring from the knee |
| 15.000 – 16.000 | Titan rises | 0 | Stagger gauge drains to 0 by `16.000` |
| 17.000 – 18.500 | Sweep wind-up (left arm drawn back) | 0 | |
| 18.500 – 19.300 | Left-arm sweep, low across the ground | 0 | Flattens grass along its path |
| 19.000 | **Sweep hits the hunter** | 0.8 | Ragdoll begins (launch velocity in section 1) |
| 21.500 – 22.500 | Ragdoll-to-active blend | 0 | Hunter is back on its feet at `22.500` |
| 23.500 | Tether 3 fired at the chest | 0 | Attaches at `23.800` |
| 23.800 – 27.000 | Swing 3 and reel-in | 0 | Hunter swings up in front of the chest |
| 25.000 | Sky lightning hits the Titan's head | 0.5 | Chest boulders part; `W3` exposed and glowing |
| 27.000 | **Strike on `W3`**, damage `500` | 0.6 | Hit-stop `0.100` s. Stagger gauge to 50% |
| 29.500 | **Killing strike on `W3`**, damage `500` | 1.0 | Hit-stop `0.200` s. Boss health `0`. `W3` broken |
| 29.700 – 32.600 | **Collapse** | 0 | Bones lose charge in order: head `29.700`, arms `30.200`, chest `30.800`, spine `31.400`, pelvis `32.000`, legs `32.600` |
| 31.500 | Hunter lands | 0.2 | Drops on tether 3, rolls clear, standing by `33.000` |
| 33.000 | Sky lightning | 0.3 | Distant |

1. **Approach (`simTime = 0.000s – 3.000s`):** The Titan walks toward the hunter at 4 m/s with a slow, heavy gait: each foot plants with a visible weight shift, the pelvis sinks and rebounds, the torso counter-rotates and the arms swing late, as if every limb weighs hundreds of tonnes. The hunter sprints through the grass toward it. Rain and wind are already at full strength.
2. **First Tether & Knee Strike (`simTime = 3.000s – 6.000s`):** The hunter fires tether 1, swings around the left leg wrapping the line, and strikes `W1`. Every strike produces the hit-stop, a burst of at least 60 directional sparks thrown along the blade's direction of travel (ballistic, closed-form from the strike time), a white flash on the weak point and a floating damage number.
3. **Fist Slam (`simTime = 6.000s – 9.000s`):** The Titan plants its feet, raises its right fist and drives it into the ground. The shockwave ring races outward through the grass, clods of dirt and grass fly up on parabolic arcs, and the first sky lightning follows.
4. **Second Tether & Stagger (`simTime = 9.000s – 16.000s`):** The hunter tethers the planted forearm, is carried up as the arm lifts, and strikes `W2`. The stagger gauge fills and the Titan staggers: it lurches backward, its arcs dim, it drops onto its left knee, hangs there, then heaves itself upright.
5. **Sweep & Ragdoll (`simTime = 16.000s – 22.500s`):** The Titan draws back its left arm and sweeps it low across the plateau. The hunter is hit, goes limp and is thrown through the rain as a ragdoll, tumbles to rest in the grass, then pushes up and blends back to full control.
6. **Third Tether & Kill (`simTime = 22.500s – 29.500s`):** The hunter fires tether 3 and swings up toward the chest. Sky lightning strikes the Titan's head, the chest boulders part and `W3` is exposed. Two strikes on `W3` finish the fight.
7. **Collapse (`simTime = 29.500s – 36.000s`):** With the lightning that binds it failing bone by bone from the head down, the Titan comes apart. Each bone's boulders fall freely from their positions at that bone's release time (closed-form ballistic motion from the release time, coming to rest on the ground with at most one bounce), each ground impact raising dust and a small grass shockwave. The hunter rides tether 3 down, lands and rolls clear.
8. **Aftermath (`simTime = 36.000s – 40.000s`):** The boulders lie scattered and dark in the flattened grass, a few last arcs crawl over them and die, the rain keeps falling on fully wet stone, and the hunter stands over the remains.

---

### 3. Timeline, State Machine & Playback Controls
Define total active duration `const DURATION = 40;` (in seconds) and implement the following exact 5-state playback state machine (`COUNTDOWN`, `PLAYING`, `PAUSED`, `REFIRE_HOLD`, `ENDED`):

1. **Initial Launch (`COUNTDOWN` State — Exactly 3.000s Wall-Clock):**
   - Start `COUNTDOWN` on the first `requestAnimationFrame` callback after the initial resting scene (`simTime = 0.000`) has rendered (`countdownElapsed = 0`), advancing `countdownElapsed` by clamped wall `dt = Math.min(rawDt, 0.1)` each frame so cold-start shader compilation never skips `"3"`.
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
  <input id="scrubber" type="range" min="0" max="40" step="0.001" value="0" aria-label="Timeline Scrubber">
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

- **Unobstructed Viewport (Strict):** Do NOT render any other DOM elements, visible text, titles, headings, watermarks, phase labels, FPS counters, or 2D canvas text overlays anywhere on screen outside of `#countdown` and `#dock`. The only exception is the wordless HUD defined in section 5, which is drawn inside `#stage` by the WebGL renderer and adds nothing to the DOM. Note that `#dock` and `#countdown` use translucent studio styling so their geometry, positions, and control widths are pixel-locked across models while subtly blending over each model's rendered scene.

---

### 5. World-Anchored HUD (Drawn Inside the WebGL Canvas)
This benchmark has a HUD, and it is the one exception to the clean viewport contract in section 4: draw it **inside `#stage`** as a final orthographic pass of the same `THREE.WebGLRenderer` (sprites, lines and quads). Add no DOM elements, no second canvas in the page and no DOM text for it. Digits come from a glyph atlas drawn once on a detached in-memory canvas. The HUD contains no words, labels, titles, logos or FPS readouts. Every HUD element is a pure function of `simTime` and the event table. Keep the HUD clear of the bottom 90 px of the viewport (the dock) and of the centre of the screen during the countdown.

- **Boss health bar:** A wide bar centred near the top edge (inside the top 10% of the viewport). It shows health out of `2000`, drops at each strike, and a paler trailing segment catches up over 0.6 s.
- **Stagger gauge:** A thinner bar directly under the health bar, filling at the strikes as listed in the event table, pulsing while the stagger is active and draining to empty by `simTime = 16.000`.
- **Weak-point brackets:** Four corner brackets around each intact, exposed weak point, positioned by projecting its 3D position to the screen every frame and scaled with distance. The bracket of the hunter's current target is brighter. Brackets disappear when a weak point is broken.
- **Off-screen threat arrow:** When the Titan's chest projects outside the viewport, or when an attack wind-up is under way and the attacking fist is outside the viewport, an arrow at the screen edge points toward it.
- **Damage numbers:** Each strike spawns its damage value (`400`, `600`, `500`, `500`) at the weak point's projected position; it rises 60 px and fades over 0.9 s of `simTime`, staying anchored to the 3D point as the camera moves.

---

### 6. Synthesized Sound Effects (No Music)
All sound is synthesized at runtime with the Web Audio API. Use no audio files, no `<audio>` elements, no other audio libraries and no music.

- **Start-up without extra UI:** Create one `AudioContext` at load and call `resume()` on it immediately, and again on the first `pointerdown` or `keydown` anywhere on the page, so sound starts by itself where the browser allows autoplay and after the first click otherwise. Add no start screen, mute button, volume control or any other element.
- **Sound follows the playback state:** Sound is audible only in the `PLAYING` state. In `COUNTDOWN`, `PAUSED`, `REFIRE_HOLD` and `ENDED`, and while the scrubber is being dragged, the master gain fades to silence within 50 ms and every one-shot sound still ringing is stopped. Audio only reads the simulation state and never changes it.
- **Driven by `simTime`:** Every frame, set each continuous sound's pitch, volume and filter from the simulation state at the current `simTime`, so sound is correct after any scrub or Re-fire. Trigger a one-shot sound when forward playback carries `simTime` across its event time; scrubbing or Re-fire never triggers one-shots. At playback speeds other than `1x`, sounds keep the pitch they have at that `simTime` and are not pitch-shifted by the speed selector.
- **Separate seeded randomness:** Noise buffers and any variation in sound use their own seeded generator (seed `4242`), never the simulation's generator and never `Math.random()`.
- **Listener & positioning:** The listener is at the active camera and jumps with each camera cut. Titan and hunter sounds are positioned in 3D with distance falloff.
- **Storm bed (continuous):** Wind as band-passed noise with slow gusting, and rain as brighter filtered noise that gets slightly louder and duller as `wetness` rises. Both run for the whole timeline.
- **Titan body (continuous, follows gameplay state):** A deep grinding rumble of stone on stone whose pitch and volume follow the angular speed of the Titan's fastest-moving limb, and an electrical crackle-hum whose brightness and level follow the Titan's average `charge` (louder in attacks, thin during the stagger, dying away through the collapse).
- **Footfalls & impacts:** A sub-bass thud with a noise burst for each footfall, a much larger one for the fist slam at `7.500` and for the knee at `13.000`, and a scatter of smaller thuds as boulders land during the collapse.
- **Tethers:** A sharp launch snap when each tether is fired, a metallic clink when it attaches, and a reel whine while a tether is attached whose pitch follows the hunter's speed.
- **Strikes:** A bright metallic impact with a short ring for each strike, pitched higher for each successive strike. During each hit-stop the storm bed ducks by about 12 dB and returns as motion resumes.
- **Hunter:** A whoosh following the hunter's speed through the air, a heavy body impact at `19.000`, and soft thumps as the ragdoll tumbles.
- **Thunder:** For each sky lightning strike, a crack followed by a long low rumble, delayed by the strike's distance from the camera at 340 m/s.
- **Collapse:** As each bone loses charge, a falling electrical whine that cuts out; then only wind and rain for the aftermath.
- **Output:** Route everything through one master gain and a `DynamicsCompressorNode`, with levels set so the mix never clips.

---

### 7. Performance & Self-Report
- **Frame-rate target:** 60 fps at `1920×1080` in current desktop Chrome on a mid-range discrete GPU. The instance counts above (100,000 grass blades, 20,000 rain streaks, 120 boulders, 40 arcs) are targets. If you must reduce one to hold the frame rate, reduce it and report the real number below. A smooth scene with honest, lower numbers is better than one that meets every count and stutters.
- **Real systems, not imitations:** A system only counts if it does what its description says. A tether drawn as a curve with no chain simulation is not a Verlet rope; a hunter that plays a canned tumble is not a ragdoll. If you simplify or omit a system, say so in the report.
- **Machine-readable report:** Define this global in your main script, with truthful values:
  ```js
  window.BENCH_REPORT = {
    counts: { grassBlades: 0, rainStreaks: 0, boulders: 0, arcs: 0, ropePoints: 0, ragdollPoints: 0 },
    systems: {            // each value: "full", "simplified" or "missing"
      titanSkeleton: "", grass: "", rainAndWetness: "", tethers: "", combatHitStop: "",
      ragdollBlend: "", camera: "", hud: "", audio: "", collapse: ""
    },
    simplifications: [],  // one short string per simplified or missing system, saying what was done instead
    testedInBrowser: false, // true only if you loaded the finished file in a browser during this session
    measuredFps: null       // a number only if you measured it; otherwise null
  };
  ```
- **Final message:** End your session with a short summary of the same facts: what is fully implemented, what was simplified or cut (with the real numbers), and whether you ran the file in a browser. Keep what you verified separate from what you assume. Do not describe untested code as working.

---

### 8. Implementation Strategy Tips (Three.js)
- Make everything you can a closed-form function of `simTime` (through `motionTime` where section 1 says so): the Titan's bone angles from the event table, boulder offsets, grass bending in the vertex shader from a small uniform array of footfall and shockwave events, rain, arcs, sparks, collapse trajectories, wetness, the camera, trauma and the whole HUD. Then any `simTime` renders in one pass with no history, and scrubbing is instant.
- Only the three tethers and the ragdoll need stepped simulation, and each has a known start time and a small state (a few dozen points). Step them at `1 / 240` s from their own start time and cache the result at each step (or at checkpoints) the first time it is computed, so playback is cheap, backward scrubbing re-reads the cache, and results never depend on frame rate. Drive the hunter's body from the event table and let the ropes and ragdoll react to it.
