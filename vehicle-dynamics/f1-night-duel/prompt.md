# Benchmark Specification: F1 Night Duel: Floodlit Two-Car Sprint to the Line

Generate a complete, single-file `index.html` application containing a physics-based simulation of a floodlit night race between two highly detailed Formula 1-style single-seaters, one red and one blue, over one standing-start lap of a fixed spline-defined circuit: a five-light start, a nose-to-tail chase through humid night haze on a damp track, and a slipstream pass on the final straight that the blue car wins by about 3 metres. Write the completed deliverable directly to `./index.html` in the current working directory, and do not leave auxiliary files in the working directory.

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
- **Camera:** One `THREE.PerspectiveCamera` (near `0.1`, far `3000`) whose position, look-at target and vertical FOV are a pure function of `simTime` following the exact broadcast shot schedule below. Shots change with hard cuts at the listed times, with no blending, smoothing or damped state, so scrubbing to any `simTime` gives the identical view. `C(s)` and `n(s)` are the track centreline and right-hand normal defined under Circuit, `sR`/`sB` are the red/blue car arc-lengths, and `MID` is the midpoint between the two cars' body centres. The same schedule must keep both cars inside the frame at `16:9` and at portrait `1280×1340`.
  | Shot | `simTime` window | Camera position | Look-at target | FOV |
  | :--- | :--- | :--- | :--- | :--- |
  | 1. Grid, from behind | `[0, 5)` | fixed `(-34, 2.6, 0)` | fixed `(0, 3.0, 0)` | 35° |
  | 2. Chase behind blue | `[5, 11)` | `C(sB - 9) + dB·n + (0, 2.4, 0)` | `C(sB + 14) + (0, 0.9, 0)` | 50° |
  | 3. Trackside, uphill sweep | `[11, 15)` | fixed `C(400) - 18·n(400) + (0, 5, 0)` | `MID` | 24° |
  | 4. Blue onboard (T-cam) | `[15, 20)` | above the blue car's roll hoop, 1.25 m above its floor and 0.2 m behind the hoop, moving and rotating rigidly with the car | 40 m ahead along the blue car's heading, 0.6 m above the road | 75° |
  | 5. Trackside, hairpin | `[20, 24)` | fixed `C(725) + 20·n(725) + (0, 3, 0)` | `MID` | 28° |
  | 6. Aerial | `[24, 30)` | fixed `(-80, 120, 150)` | `MID` | 30° |
  | 7. Trackside, final corner | `[30, 34)` | fixed `C(1300) - 12·n(1300) + (0, 1.2, 0)` | `MID` | 30° |
  | 8. Finish line | `[34, 40]` | fixed `(-20, 4.5, 15)` | `MID` | 32° |

  In shot 4 the blue car's own bodywork (airbox top, halo, nose) may fill no more than the bottom quarter of the frame; the road ahead and the red car fill the rest.
- **Subject / Centerpiece:**
  - **Geometry & Placement:**
    - **Circuit (must be followed exactly):** World units are metres, `+Y` is up. Build the centreline with `new THREE.CatmullRomCurve3(points, true, 'centripetal')` through these `(x, y, z)` points in this order: `(0, 0, 0), (200, 0, 0), (320, 5, 60), (340, 12, 180), (260, 20, 260), (120, 15, 240), (60, 8, 320), (-80, 4, 340), (-200, 0, 260), (-240, 0, 120), (-160, 0, 40), (-80, 0, 0)`. The closed lap length is `L ≈ 1551.65 m`. `C(s)` is the centreline point at arc-length `s` metres from `(0, 0, 0)` in the direction of `(200, 0, 0)`, wrapping modulo `L` (use an arc-length lookup of at least 2,000 samples, e.g. `getPointAt(u)` with `u = (s mod L) / L`); `T(s)` is the unit tangent and `n(s) = normalize(T(s) × (0, 1, 0))` is the right-hand normal (at the start line `n = (0, 0, 1)`).
    - **Road & surroundings:** The asphalt is 14 m wide (`±7 m` along `n`), with a white line at each edge, red-and-white kerbs on the corners, a continuous barrier with catch fencing on both sides about 9 m from the centreline, a chequered start/finish line across the road at `s = 0`, two painted grid boxes, a start gantry spanning the road at `s = 2` carrying five start-light pods that face the grid, a pit wall on the `+Z` side of the main straight and a grandstand on the `-Z` side. Terrain follows the track's elevation and rolls away into dark hills.
    - **Cars:** Two original Formula 1-style single-seaters built entirely from code-generated geometry, each about 5.5 m long, 2.0 m wide and 0.95 m tall with a 3.6 m wheelbase: the **red car, number 7**, and the **blue car, number 23**. Each car must visibly have: a multi-element front wing with endplates; a slender nose; a monocoque with an open cockpit, a halo, a helmeted driver and a steering wheel; sculpted sidepods with radiator inlets and an undercut; an airbox and roll hoop behind the driver; a tapering engine cover; a floor with raised edges and a rear diffuser; a two-element rear wing with endplates and a movable upper flap (DRS); a beam wing; a rear crash structure with a red rain light; exposed front and rear suspension wishbones and push-rods; wing mirrors; and four open wheels (0.72 m diameter, about 0.31 m wide at the front and 0.40 m at the rear) with rims, a coloured sidewall band and brake discs visible inside the front rims. Every listed part must be modelled as its own shaped mesh (not a single box or merged blob standing in for several parts), so each one can be picked out in a close-up; the front wing must have at least three stacked elements, the rear wing endplates must carry louvres, and the wheels must have plain coloured tyre sidewall stripes (no lettering) and visible wheel nuts. Each car's body should have at least 40 separate meshes. Use invented liveries only: no real team, sponsor, manufacturer or driver names or logos.
    - **Placement & motion:** Each car's reference point (centre of its floor, midway between the axles) sits at `C(s) + d·n(s)`, with its body yawed along the direction of travel and pitched to the track gradient. `s` and `d` for both cars are given by the checkpoint table in section 2. Wheels spin by distance travelled, the front wheels steer into corners, and the body pitches slightly under acceleration and braking and rolls slightly in corners.
  - **Materials:** Glossy clear-coated metallic paint (deep racing red `#c8102e` with white accents and number 7; saturated royal blue `#1546c8` with silver accents and number 23 — the two cars must read clearly as red and blue under the floodlights, never pale, pink or white), with numbers and stripes drawn on in-memory canvas textures; bare carbon-fibre weave on the floor, wings' undersides, halo and suspension; slick black rubber tyres with a procedural sidewall texture; a reflective helmet visor; dark damp asphalt with a procedural grain and a low-roughness wet sheen that picks up stretched highlights from the floodlights and the cars' lights; painted steel barriers and galvanised fencing. Generate one night environment map at startup with `THREE.PMREMGenerator` from an in-memory scene (dark sky plus bright floodlight panels) so paint, carbon and visors show crisp reflections.
- **Lighting:** Night, with no daylight at any time. **Exposure target (strict):** the frame must read as a dark night scene, not as day or bright fog. Away from the floodlight pools the asphalt is near-black (sRGB luminance below about 20%), unlit terrain, hills and fencing fade into darkness, and the sky stays darker than any lit surface except near the horizon glow. Contrast comes from pools of light, not from overall brightness: bright pools under each mast, dark gaps between them, glossy wet highlights on the road and cars. Do not light the whole scene with a strong ambient or hemisphere light (keep ambient fill at or below intensity `0.15`), and use `renderer.toneMapping = THREE.ACESFilmicToneMapping` with exposure at or below `1.0`. The haze is dark blue-grey (no lighter than `#1a2230`) and only glows where a light shines through it. Set an opaque night sky as the scene background (deep blue-black gradient, procedural stars, a moon, and a faint warm city glow on one horizon), covering the CSS gradient. The circuit is lit by floodlight masts about 30 m tall placed every 60 to 80 m on alternating sides of the track, each with a bright emissive lamp head and a visible cone of light through the haze; because r128 cannot run that many real lights, light the cars with a small set of cool-white shadow-casting lights that travel with the action, plus a dim blue moonlight fill, and bake or fake the pools of floodlight on the road. Humid haze: exponential fog tinted blue-grey that swallows distant masts and hills and blooms around every lamp. Car lights: the rear rain light blinks at 4 Hz of `simTime`, brake discs glow orange in proportion to deceleration, and the start-gantry lights and grandstand lighting are emissive.

---

### 2. Physical Phenomena & Dynamic Phases
Simulate the sequential physical phases across the exact active simulation timeline from `simTime = 0.000` s to `simTime = 40` s:
**Standardized car motion (must be followed exactly):** The table gives, at each whole second of `simTime`, the arc-length `s` (metres, measured from the start line and not wrapped, so the finish line is `s = 1551.65`) and the lateral offset `d` (metres along `n`, positive to the right of travel) of the red car (`sR`, `dR`) and the blue car (`sB`, `dB`). Between rows, interpolate each column with a monotone cubic Hermite spline (Fritsch–Carlson / PCHIP); a car's speed is the derivative of its `s` and its acceleration is the second derivative. Evaluate this directly from `simTime` so no physics integration is needed for the cars' paths. With this table the blue car draws level at `simTime ≈ 35.33`, crosses the finish line at `simTime ≈ 36.49`, and the red car crosses at `simTime ≈ 36.54`, about 3.3 m behind.

| `simTime` | `sR` | `dR` | `sB` | `dB` |
| ---: | ---: | ---: | ---: | ---: |
| 0 | -8.0 | -2.50 | -16.0 | 2.50 |
| 1 | -8.0 | -2.50 | -16.0 | 2.50 |
| 2 | -8.0 | -2.50 | -16.0 | 2.50 |
| 3 | -8.0 | -2.50 | -16.0 | 2.50 |
| 4 | -2.3 | -2.31 | -11.5 | 2.36 |
| 5 | 14.8 | -1.46 | 3.1 | 1.65 |
| 6 | 42.8 | -0.47 | 29.8 | 0.76 |
| 7 | 81.1 | 0.00 | 68.2 | 0.10 |
| 8 | 128.9 | 0.00 | 115.9 | 0.00 |
| 9 | 185.1 | 0.00 | 172.2 | 0.00 |
| 10 | 248.1 | 0.00 | 235.3 | 0.00 |
| 11 | 310.5 | 0.00 | 297.8 | 0.00 |
| 12 | 354.6 | 0.00 | 342.1 | 0.00 |
| 13 | 403.8 | 0.00 | 391.4 | 0.00 |
| 14 | 456.5 | 0.00 | 444.4 | 0.00 |
| 15 | 500.6 | 0.00 | 488.6 | 0.00 |
| 16 | 553.0 | 0.00 | 541.2 | 0.00 |
| 17 | 590.7 | 0.00 | 579.2 | 0.00 |
| 18 | 627.7 | 0.00 | 616.4 | 0.00 |
| 19 | 674.3 | 0.00 | 663.2 | 0.00 |
| 20 | 716.6 | 0.00 | 705.7 | 0.00 |
| 21 | 744.7 | 0.00 | 734.0 | 0.00 |
| 22 | 782.0 | 0.00 | 771.5 | 0.00 |
| 23 | 821.0 | 0.00 | 810.8 | 0.00 |
| 24 | 855.1 | 0.00 | 845.1 | 0.00 |
| 25 | 899.0 | 0.00 | 889.1 | 0.00 |
| 26 | 951.7 | 0.00 | 942.1 | 0.00 |
| 27 | 1007.7 | 0.00 | 998.2 | 0.00 |
| 28 | 1069.6 | 0.00 | 1060.3 | 0.00 |
| 29 | 1131.7 | 0.00 | 1122.5 | 0.00 |
| 30 | 1194.2 | 0.00 | 1185.1 | 0.00 |
| 31 | 1252.2 | 0.00 | 1243.1 | 0.00 |
| 32 | 1289.7 | 0.00 | 1280.7 | 0.00 |
| 33 | 1333.9 | 0.00 | 1324.9 | 0.00 |
| 34 | 1387.1 | -0.87 | 1380.4 | 1.62 |
| 35 | 1447.7 | -1.20 | 1446.1 | 3.40 |
| 36 | 1514.0 | -1.20 | 1516.7 | 3.40 |
| 37 | 1583.6 | -1.20 | 1587.1 | 3.40 |
| 38 | 1649.5 | -1.20 | 1653.4 | 3.40 |
| 39 | 1710.4 | -1.20 | 1714.9 | 3.40 |
| 40 | 1766.3 | -1.20 | 1771.1 | 3.40 |

1. **Grid & Five-Light Start (`simTime = 0.000s – 3.000s`):** Both cars sit still in their grid boxes with the red car on pole. The five red gantry lights come on one at a time at `simTime = 0.5, 1.0, 1.5, 2.0, 2.5` and all go out together at `simTime = 3.000`. Heat shimmer rises behind each car and the rain lights blink.
2. **Launch (`simTime = 3.000s – 7.000s`):** Both cars launch. The rear tyres spin and throw up tyre smoke and a fine mist of water from the damp track; the blue car gets the slower start and falls in directly behind the red car.
3. **Uphill Chase (`simTime = 7.000s – 20.000s`):** The cars run nose to tail up the climbing first half of the lap. Each car trails a low plume of spray that glows in the floodlights and in the following car's view; brake discs glow orange in each braking zone and fade as they cool; titanium skid blocks throw showers of sparks from under the floor when a car is above 200 km/h or braking hard.
4. **Hairpin & Descent (`simTime = 20.000s – 30.000s`):** Heavy braking into the hairpin with glowing discs and a puff of smoke from the red car's unloaded inside front tyre, then acceleration downhill through the fast sweeping right-handers with spray and sparks.
5. **Final Corner & Slipstream Pass (`simTime = 30.000s – 36.490s`):** The blue car exits the final corner in the red car's slipstream, pulls out to the right at `simTime ≈ 33.3`, and opens its DRS flap (upper rear-wing element rotates open) from `simTime = 33.500` until it crosses the line. The two cars run side by side and the blue car edges ahead.
6. **Finish & Cool-Down (`simTime = 36.490s – 40.000s`):** The blue car takes the finish line first. As it crosses, the five gantry lights flash green at 5 Hz for the rest of the timeline and a burst of camera flashes sparkles across the grandstand. Both cars lift off and slow gently down the straight, DRS closed, discs glowing faintly.

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

- **Unobstructed Viewport (Strict):** Do NOT render any other DOM elements, visible text, titles, headings, watermarks, phase labels, FPS counters, HUD readouts, or 2D canvas text overlays anywhere on screen outside of `#countdown` and `#dock`. Note that `#dock` and `#countdown` use translucent studio styling so their geometry, positions, and control widths are pixel-locked across models while subtly blending over each model's rendered scene.

---

### 5. Synthesized Sound Effects (No Music)
All sound is synthesized at runtime with the Web Audio API. Use no audio files, no `<audio>` elements, no other audio libraries and no music.

- **Start-up without extra UI:** Create one `AudioContext` at load and call `resume()` on it immediately, and again on the first `pointerdown` or `keydown` anywhere on the page, so sound starts by itself where the browser allows autoplay and after the first click otherwise. Add no mute button, volume control or any other element.
- **Sound follows the playback state:** Sound is audible only in the `PLAYING` state. In `COUNTDOWN`, `PAUSED`, `REFIRE_HOLD` and `ENDED`, and while the scrubber is being dragged, the master gain fades to silence within 50 ms and every one-shot sound still ringing is stopped. Audio only reads the simulation state and never changes it.
- **Driven by `simTime`:** Every frame, set each continuous sound's pitch, volume and filter from the simulation state at the current `simTime` (speed, acceleration, camera shot), so sound is correct after any scrub or Re-fire. Trigger a one-shot sound when forward playback carries `simTime` across its event time; scrubbing or Re-fire never triggers one-shots. At playback speeds other than `1x`, sounds keep the pitch they have at that `simTime` and are not pitch-shifted by the speed selector.
- **Separate seeded randomness:** Noise buffers and any variation in sound use their own seeded generator (seed `4242`), never the simulation's generator and never `Math.random()`.
- **Listener & positioning:** The listener is at the active camera and jumps with each camera cut. The two cars' sounds are positioned in 3D with distance falloff and a Doppler pitch shift computed from each car's velocity relative to the camera, so cars audibly sweep past the trackside cameras.
- **Engines (one per car):** A turbo-hybrid V6 voice built from several oscillators at the firing frequency and its harmonics plus filtered noise. RPM comes from an audio-only 8-speed gearbox driven by the car's speed (between about 5,000 and 12,000 RPM), with a brief pitch drop and volume dip on each upshift and a blip on each downshift. The tone is brighter and louder under acceleration and softer when lifting off, with a turbo whistle layer that rises with RPM. Both engines idle with a lumpy burble on the grid and rev up as the fifth light comes on. In shot 4 (blue onboard) the blue engine is heard close and loud through a cockpit low-pass filter with added wind roar.
- **Tyres & track:** A wet-road hiss for each car that rises with speed; wheelspin screech during the launch (`simTime = 3.0 – 5.0`); a softened wet squeal under heavy braking and through the hairpin, following deceleration and cornering load.
- **Sparks & brakes:** A crackling metallic scrape whenever a car's skid blocks are throwing sparks, and a faint brake-disc squeal under the hardest braking.
- **DRS:** A sharp mechanical click when the blue car's flap opens at `simTime = 33.500` and a softer one when it closes at the finish line.
- **Start lights:** A short beep as each of the five lights comes on (`simTime = 0.5, 1.0, 1.5, 2.0, 2.5`); no tone at lights out, only the engines launching.
- **Night ambience:** A soft crowd murmur positioned at the grandstand, a low electrical hum from the floodlights, and a light humid breeze. The crowd swells as the cars come onto the final straight (from `simTime = 33`) and breaks into a roar at the finish (`simTime ≈ 36.49`), with a scatter of camera-shutter clicks matching the grandstand flashes.
- **Camera cuts:** No sound for cuts; the change of listener position is the only audible effect.
- **Output:** Route everything through one master gain and a `DynamicsCompressorNode`, with levels set so the mix never clips. The red and blue engines must be distinguishable (give them slightly different harmonic balance).

---

### 6. Implementation Strategy Tips (Three.js)
- Sample the centreline once at startup into an arc-length table (position, tangent, normal) and build the road, kerbs, barriers, fencing and floodlight masts from it as merged or instanced geometry. Build each car once as a `THREE.Group` of a few dozen meshes and pose both cars directly from the interpolated checkpoint table inside `renderAt(simTime)`, so startup stays under `2s` and any `simTime` renders in under `16ms` for instant scrubbing.
- Make every effect a closed-form function of `simTime`: emit spray, smoke and spark particles from seeded emission times along each car's known path (position of particle `i` = the car's position at its emission time plus a seeded ballistic drift for its age), and derive brake glow, wheel rotation, DRS angle, light states and the camera from the table and the shot schedule, never from accumulated per-frame state.
