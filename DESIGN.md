---
name: Kinetic Operational Mesh
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#45464d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#4648d4'
  on-secondary: '#ffffff'
  secondary-container: '#6063ee'
  on-secondary-container: '#fffbff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#001d31'
  on-tertiary-container: '#188ace'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#e1e0ff'
  secondary-fixed-dim: '#c0c1ff'
  on-secondary-fixed: '#07006c'
  on-secondary-fixed-variant: '#2f2ebe'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  telemetry-num:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 22px
    letterSpacing: -0.02em
  telemetry-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  space-2xs: 0.125rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-base: 1rem
  space-lg: 1.25rem
  space-xl: 1.5rem
  space-2xl: 2rem
  space-3xl: 3rem
  gutter-hud: 0.75rem
  margin-screen: 1rem
---

## Brand & Style

This design system serves high-stakes civic and transit operations where split-second decisions dictate urban flow, commuter safety, and fleet efficiency across multimodal transport networks. The visual language blends mission-critical precision with futuristic intelligence. It avoids the dark, fatigued aesthetics of legacy SCADA screens in favor of an alert, crisp, daytime-operational light architecture.

### Personality & Emotional Response
- **Sovereign & Authoritative:** Instills immediate trust, structural stability, and institutional rigor through disciplined layout hierarchy and deep navy structural framing.
- **Predictive & Intelligent:** Electric violet and indigo accents highlight proactive alerts, AI machine inference, synthetic schedules, and incident predictions before physical bottlenecks manifest.
- **Zero-Latency Clarity:** Minimizes cognitive payload under pressure. The operator feels completely in command, supported by high legibility, strict contrast boundaries, and instant telemetry parsing.

### Visual Style
- **Technical Minimalist / Operations HUD:** Low-chroma functional canvases accented with electric telemetry nodes, crisp micro-borders, ultra-clean monospace telemetry figures, and multi-layered stacked surfaces.
- **Structured Data Density:** Compact component geometry engineered to handle geospatial mapping, sensor streams, live feeds, dispatch tables, and timeline scrubbers on high-resolution command bridge displays.

## Colors

The system uses a calibrated palette prioritizing long-shift ergonomic comfort, explicit hierarchy, and instant status recognition across ambient control room lighting.

### Base Structural Palette
- **Canvas Base (`#F8FAFC`):** Master background providing a soft, non-glare foundation.
- **Surface Layer 1 (`#FFFFFF`):** High-priority card panels, elevated control pods, and active modals.
- **Surface Layer 2 (`#F1F5F9`):** Sub-panels, docked side-trays, table row alternations, and sunken tracking wells.
- **Dividers & Structural Borders (`#E2E8F0`):** Precise 1px borders delineating high-density modules without visual noise.
- **Deep Slate Anchors (`#0F172A`, `#1E293B`):** Dominant text, navigation headers, command bars, and structural anchors.

### Intelligence & System Accents
- **AI Primary (`#6366F1`):** Predictive vectors, automated recommendations, and ML clustering overlays.
- **AI Action Dark (`#4F46E5`):** Interactive hover states and confirmed machine automated overrides.
- **AI Accent Glow (`#818CF8`):** Focus rings, trajectory paths, and predictive boundary halos.
- **Telemetry & Informational Sky (`#0284C7`):** GPS waypoints, bus corridor trackers, sensor telemetry, and live status readouts.

### Critical Status Indicators
- **Nominal / Smooth Flow (`#10B981`):** Normal transit corridors, on-time arrivals, and operational hardware nodes.
- **Advisory / Friction Warning (`#F59E0B`):** Speed deviations, signal phase delays, and localized capacity crowding.
- **Critical Disruption / Incident (`#EF4444`):** Accidents, track faults, severe route blockages, and system overrides.

Status colors are strictly reserved for operational health and telemetry values; they are never co-opted for decorative marketing elements.

## Typography

Typography prioritizes tabular scanning speed, micro-scale legibility, and visual differentiation between static meta-labels and dynamic live telemetric feeds.

### Type Hierarchy Structure
- **Primary Interface (Inter):** Leveraged across layout headers, contextual descriptions, modal alerts, and interactive control surfaces. Features tight tracking and crisp optical apertures for rapid scanning.
- **Operational Data & Telemetry (JetBrains Mono):** Mandated for timestamping, vehicle IDs, GPS latitude/longitude, speed gauges, headway variances, and delta KPIs. The monospaced alignment prevents layout jitter during high-frequency live data updates.

### Numerical Guidelines
- Always render live numerical streams with OpenType tabular figures (`tnum`) enabled.
- Capitalize operational metadata abbreviations (e.g., `ETA`, `RTPI`, `AVL`, `GEO-FENCE`) and format in `label-md` with tracking expanded to `+0.04em` for instant badge scanning.

## Layout & Spacing

The control center layout is built on a high-density, multi-pane fluid workspace model optimized for multi-monitor workstations (1440p to 4K ultra-wide) while maintaining responsive single-column containment for field tablets.

### Layout Model & Grid
- **HUD Multi-Pane Shell:** A persistent 64px structural toolbar anchors the left edge, a top-level telemetry strip tracks city-wide pulses, and the center viewport accommodates fluid GIS / vector map layers.
- **Dockable Operational Panels:** Data decks, incident feeds, and route graphs dock into 320px or 400px side-rail widths, utilizing `space-md` (12px) gutters to maximize viewport real estate.
- **Base Rhythm:** Follows a strict 4px / 8px incremental scale. Dense tables and nested lists standardize on 28px–32px row heights with `space-sm` (8px) internal cell padding to sustain elevated data throughput.

### Breakpoint Matrix
- **Command Multi-Display (>= 1920px):** Simultaneous 3-to-4 column modular matrix alongside persistent live GIS canvas.
- **Desk Console (1280px - 1919px):** Split-screen layout: Primary spatial viewport (65% width) + stacked secondary inspector rail (35% width).
- **Tactical Field Device (768px - 1279px):** Collapsible drawer architecture; full-bleed map with bottom-sheet control panels sliding on `space-base` increments.

## Elevation & Depth

Visual hierarchy uses fine-line outlines combined with multi-stop, ambient low-opacity drop shadows to separate physical map layers from abstract analytical overlays without causing eye fatigue.

### Elevation Levels

1. **Sub-Surface / Sunken Trackers (`Level -1`):**
   - Background: `#F1F5F9`
   - Border: 1px solid `#E2E8F0`
   - Shadow: Inset `0 1px 2px rgba(15, 23, 42, 0.05)`
   - Used for search query inputs, terminal logs, and data track troughs.

2. **Base Operational Canvas (`Level 0`):**
   - Background: `#F8FAFC`
   - Border: None
   - Used as the root viewport for map canvas and background views.

3. **Floating HUD Panels & Control Cards (`Level 1`):**
   - Background: `#FFFFFF`
   - Border: 1px solid `#E2E8F0`
   - Shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.04)`, `0 4px 12px 0 rgba(15, 23, 42, 0.03)`
   - Used for live metric pods, fleet health lists, and simulation controls.

4. **Active Flight Decks & Popover Flyouts (`Level 2`):**
   - Background: `#FFFFFF`
   - Border: 1px solid `#CBD5E1`
   - Shadow: `0 4px 6px -1px rgba(15, 23, 42, 0.06)`, `0 12px 24px -4px rgba(15, 23, 42, 0.08)`
   - Used for route wayfinding tooltips, signal timeline overrides, and vehicle inspector pods.

5. **Critical Incident & Intervention Modals (`Level 3`):**
   - Background: `#FFFFFF`
   - Border: 1px solid `#94A3B8`
   - Shadow: `0 20px 30px -8px rgba(15, 23, 42, 0.16)`, `0 1px 3px rgba(15, 23, 42, 0.08)`
   - Used for emergency broadcast dialogs and network-wide signal preemption confirmations.

### Outline-First Hierarchy
Every elevated element must possess a crisp 1px border. Depth is verified through border contrast shifts rather than heavy blurs, ensuring vector clarity on tactical displays.

## Shapes

The design system employs a disciplined, soft-cornered geometry (roundedness level 1) reflecting technical precision, high space efficiency, and industrial resilience.

### Corner Radii Guidelines
- **Base Controls & Inputs (`rounded`):** `0.25rem` (4px). Applied to action buttons, text fields, status badges, telemetry pills, and table selection highlights. Maximizes screen utilization by eliminating loose, wasted corner space.
- **HUD Cards & Overlay Shells (`rounded-lg`):** `0.5rem` (8px). Applied to floating data pods, route profile panels, and diagnostic modals.
- **Nested Inner Containers (`rounded-sm`):** `0.125rem` (2px). Applied to progress bars, sub-item highlights, and sparkline bounds.
- **Circular Indicators:** Used strictly for live status beacons (pulsing green/amber/red nodes) and avatar pips. No pill-shaped inputs or oversized round elements are permitted.

## Components

### Buttons
- **Primary AI/Action:** Background `#6366F1`, text `#FFFFFF`, border none, `0.25rem` radius. Hover: `#4F46E5`. Active: `#4338CA`.
- **Command Structure Secondary:** Background `#0F172A`, text `#FFFFFF`, border none. Used for final authorization actions. Hover: `#1E293B`.
- **Outline Operational:** Background `#FFFFFF`, text `#1E293B`, border `1px solid #E2E8F0`. Hover: `#F1F5F9`, border `#CBD5E1`.
- **Destructive/Override:** Background `#FEF2F2`, text `#DC2626`, border `1px solid #FCA5A5`. Hover: Background `#FEE2E2`.
- **Sizing:** Compact (28px height, 8px padding, 12px font) for HUDs; Standard (36px height, 14px padding, 13px font) for global headers.

### Badges & Telemetry Status Chips
- Built with monospace numbers (`JetBrains Mono`, 11px) paired with an optical status pip (6px circle).
- **Nominal:** Background `#ECFDF5`, text `#065F46`, border `1px solid #A7F3D0`.
- **Warning:** Background `#FFFBEB`, text `#92400E`, border `1px solid #FDE68A`.
- **Critical:** Background `#FEF2F2`, text `#991B1B`, border `1px solid #FECACA`.
- **Telemetry Info:** Background `#F0F9FF`, text `#075985`, border `1px solid #BAE6FD`.
- **AI Recommendation:** Background `#EEF2FF`, text `#3730A3`, border `1px solid #C7D2FE`.

### High-Density Data Tables
- **Header:** Height 32px, background `#F8FAFC`, uppercase `JetBrains Mono` label at 11px, text `#64748B`, bottom border `1px solid #CBD5E1`.
- **Rows:** Height 32px base (expandable to 44px with subtext), alternating background `#FFFFFF` and `#F8FAFC`. Bottom border `1px solid #F1F5F9`.
- **Hover State:** Background `#EEF2FF` with a 2px left border accent in `#6366F1`.

### Form Controls & Inputs
- **Text Inputs:** Height 32px, background `#FFFFFF`, border `1px solid #CBD5E1`, text `#0F172A`, typography `Inter` 13px. Focus: Border `#6366F1` with an outer glow `0 0 0 2px rgba(99, 102, 241, 0.2)`.
- **Checkboxes & Radios:** 14px square/round elements with `#0F172A` fill when active. Subtle `#CBD5E1` default border.

### HUD Control Pods & Cards
- Rigid structural container with a 36px header zone separated by a 1px border (`#E2E8F0`).
- Header holds an icon, panel title (`Inter` semi-bold 12px), monospaced timestamp, and quick-dock icon actions.
- Body area contains modular grid slots for sparkline mini-charts, predictive line forecasts, and vehicle load bars.

### Predictive Simulation Widgets
- Encased in an electric violet hairline border (`#818CF8`).
- Highlights potential bottlenecks with an amber-to-red dotted timeline bar and presents clear, machine-generated intervention buttons (e.g., "Reroute 14 Buses via OMR Bypass").