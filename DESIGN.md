---
name: Muhammad Abubakar — GitHub Profile
description: A phosphor-green terminal session standing in for a portfolio — whoami, not "about me".
colors:
  ground-dark: "#070B08"
  surface-dark: "#121712"
  border-dark: "#1F2A22"
  phosphor-bright: "#33FF66"
  phosphor-mid: "#1B6E3A"
  phosphor-dim: "#145C33"
  ground-light: "#F4F7F5"
  surface-light: "#E7EEE9"
  border-light: "#D3DED7"
  phosphor-bright-light: "#0F5132"
  phosphor-mid-light: "#146C43"
  phosphor-dim-light: "#3C6152"
  chrome-red: "#FF5F56"
  chrome-amber: "#FFBD2E"
  chrome-green: "#27C93F"
typography:
  display:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "46px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "normal"
  body:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: 1.3
  label:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "14px"
    fontWeight: 400
    letterSpacing: "normal"
rounded:
  window: "16px"
  dot: "50%"
spacing:
  banner-inset: "40px"
  line-step: "34px"
components:
  banner-window:
    backgroundColor: "{colors.ground-dark}"
    textColor: "{colors.phosphor-mid}"
    rounded: "{rounded.window}"
    padding: "44px 40px 0"
  readout-block:
    backgroundColor: "{colors.ground-dark}"
    textColor: "{colors.phosphor-mid}"
    typography: "{typography.label}"
---

# Design System: Muhammad Abubakar — GitHub Profile

## Overview

**Creative North Star: "Green-Phosphor Terminal in a Midnight Machine Room"**

The profile is built on one governing idea: prove production competence through *format*, not adjectives. A recruiter shouldn't read claims about a system that ships and stays in production — they should land on a page that behaves like one: a live terminal session, near-black CRT ground, phosphor-green monospace, a `whoami` that answers in status-readout register. Nothing on the page performs enthusiasm; everything on the page reports.

This is a hard constraint of the medium as much as a choice — GitHub profile READMEs render static GFM only, no CSS, no JS, no live components. The world has to hold together with pre-rendered SVG and disciplined typographic hierarchy alone. So the terminal metaphor does double duty: it's the aesthetic *and* the excuse for staying static — a real terminal is mostly still, waiting at a prompt, which is exactly what a GFM page can honestly be.

Built from concept-seed direction 5 (CLI/terminal session), fused with the dealt challenger world "phosphor-terminal-midnight" (scanline glow, cursor bloom, P1 phosphor green `#33FF66`), seed key `9f37b2b5`.

**Key Characteristics:**
- Near-black CRT ground with a soft radial vignette, not flat black
- One accent color, phosphor green, spent sparingly — most text sits in a dimmer green register
- Real terminal chrome (macOS-style traffic lights, title bar) framing the content, not decorating it
- The only motion on the entire page is a blinking cursor — a signature, not an effect
- 80-column / ≤36-character discipline in every fenced block, carried from the banner into the README body itself

## Colors

A single hue family (phosphor green) at three brightness steps against a near-black or near-white ground — color is used as an information register (bright = active/output, dim = ambient/label), never decoration.

### Primary
- **Phosphor Bright** (`#33FF66` dark / `#0F5132` light): reserved for the payload — the `whoami` command name, the display-scale name text (with glow filter), and the blinking cursor. Appears nowhere else; its rarity is what makes it read as "live output" rather than styling.

### Secondary
- **Phosphor Mid** (`#1B6E3A` dark / `#146C43` light): the terminal's own voice — prompts (`guest@github:~$`), title-bar label, role line, tagline. This is the "ambient green" the whole world sits in.
- **Phosphor Dim** (`#145C33` dark / `#3C6152` light): lowest-emphasis text — the tech-stack summary line. Present but recedes behind the mid tone.

### Neutral
- **Ground** (`#070B08` dark / `#F4F7F5` light): the CRT surface itself.
- **Surface** (`#121712` dark / `#E7EEE9` light): title-bar plate, one step off the ground.
- **Border** (`#1F2A22` dark / `#D3DED7` light): hairline window edge and title-bar divider — never used for emphasis.
- **Chrome dots** (`#FF5F56` red / `#FFBD2E` amber / `#27C93F` green): the macOS-style traffic lights. Decorative signage only; not part of the phosphor palette and not reused elsewhere.

### Named Rules
**The One Bright Rule.** `#33FF66` (or its light-mode counterpart `#0F5132`) touches exactly three things: the `whoami` keyword, the name text, and the cursor. Every other character on the banner sits in mid or dim green. If a new line needs emphasis, reach for weight or position before reaching for the bright green.

## Typography

**Display / Body / Label Font:** `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` (one stack, no separate families)

**Character:** A single monospace voice throughout — the point isn't type pairing, it's that a terminal only ever has one font. Hierarchy comes entirely from size, weight, and color register, never from a second typeface.

### Hierarchy
- **Display** (700, 46px, line-height 1): the name, `Muhammad Abubakar`, set once in the banner with the phosphor glow filter. The only place `font-weight: 700` appears.
- **Body** (400, 20px, line-height ~1.3): role line and tagline directly under the name; the `whoami` prompt line.
- **Label** (400, 16px): the one-line proof statement ("6+ yrs shipping AI that stays in production").
- **Mono-label** (400, 14–15px): title-bar text and the tech-stack line — the smallest, quietest register.
- **Readout body** (GFM default monospace, unstyled): everything inside the README's fenced ```text```/```yaml``` blocks. GitHub's own `<pre>` rendering carries this; no custom sizing is applied or possible.

### Named Rules
**The Column Discipline Rule.** Every line inside a fenced block — banner or README body — stays at or under 36 characters. This isn't stylistic; it's what keeps the terminal illusion from breaking into horizontal scroll on a 360px mobile GitHub view. Verified by direct measurement, not assumption.

## Layout

The banner is a fixed 1200×320 SVG canvas embedded at `width="100%"` (GFM gives no other sizing lever for an `<img>`/`<picture>`). Inside it: a 44px title bar, then body content left-aligned at `x=40` with a roughly 34–40px line-step between rows, mimicking real terminal line spacing rather than typographic rhythm.

Past the banner, the README body continues the same left-aligned, monospace, line-oriented layout using GFM fenced code blocks as "terminal panes" — `$ status --check`, `## deploy log`, `## stack`, `## education` each read as a distinct command's output. There is no card grid, no multi-column layout, no imagery beyond the two banner SVGs and the (best-effort) stats cards — the page is one continuous vertical terminal scrollback, which is the honest shape GFM allows.

## Elevation & Depth

Flat by necessity (GFM has no shadow/blur beyond what's baked into the SVGs), but the banner fakes CRT depth two ways: a radial vignette (`black, 0→55% opacity from center to edge`) darkens the corners like a real monitor's falloff, and a `feGaussianBlur` + `feMerge` glow filter blooms the bright-green name text outward, the way real phosphor over-saturates a CRT pixel. Everything else — chrome, prompts, code blocks — sits perfectly flat.

### Named Rules
**The Bloom-Is-Earned Rule.** The glow filter (`filter: url(#glow-d)`) is applied to exactly one element: the display-scale name. It is not a reusable "hover" or "emphasis" effect — applying it elsewhere would cheapen the one moment it's meant to sell.

## Shapes

Rounded-rectangle window at `rx=16` with a 1.5px hairline stroke border — soft enough to read as a real OS window, not a sharp card. Traffic-light dots are perfect circles (`r=6`). The cursor is a small solid rectangle (11×18) rather than a thin caret — closer to a legacy block cursor, which suits the CRT/terminal register better than a modern thin I-beam. No other corner radius, shadow, or clipping appears anywhere in the system.

## Components

### Banner (Terminal Window)
- **Shape:** 16px-rounded window, 1.5px border, 44px title bar with three traffic-light dots and a centered `muhammad@production: ~` label.
- **Body:** `whoami` prompt line → display-scale name (glowed) → role line → proof line → tech-stack line → idle prompt with blinking cursor.
- **Theming:** dark and light variants ship as sibling SVGs (`assets/banner-dark.svg`, `assets/banner-light.svg`), switched via `<picture>` + `prefers-color-scheme` media sources — the only personalization GFM allows, and it's load-bearing here since the whole page is otherwise static.
- **Motion:** the cursor rect animates opacity `1→1→0→0→1` over 1.1s via SMIL `<animate>` (no CSS/JS available in GFM). It is the single moving element on the entire profile.

### Readout Blocks (fenced code sections)
- **Style:** plain GFM ```text```/```yaml``` fences, relying on GitHub's native `<pre>` styling — no custom background or color is applied or achievable here.
- **Discipline:** every line ≤36 characters (see Column Discipline Rule); content is written as terminal/log output (`[ok] ...`, indented sub-lines under a company/role header) rather than prose, to stay consistent with the banner's register.

### Stats Cards (github-readme-stats)
- **Style:** external SVG service, themed via query-string hex params to match the phosphor palette (`bg_color`, `title_color`, `icon_color`, `text_color`), swapped dark/light through the same `<picture>` pattern as the banner.
- **Known risk:** this is a third-party free-tier service (github-readme-stats.vercel.app) with a history of outages; shipped anyway per explicit user decision. Not a component this system controls the reliability of.

## Do's and Don'ts

### Do:
- **Do** keep the bright phosphor green (`#33FF66` / `#0F5132`) to the three elements named in the One Bright Rule — name, `whoami`, cursor.
- **Do** hold every fenced-block line to ≤36 characters (Column Discipline Rule) — this is a measured mobile-safety constraint, not a stylistic preference.
- **Do** write readout content as status/log lines (`[ok] ...`, dated role headers with indented bullets), matching the terminal-scrollback register established by the banner.
- **Do** keep both banner variants (`banner-dark.svg` / `banner-light.svg`) in sync structurally (same layout, text, cursor position) — only the palette should differ between them.

### Don't:
- **Don't** use ANSI-escape–colored fenced code blocks (```ansi```) — confirmed via `gh api markdown` that GitHub does not render them in color; they show raw escape bytes instead.
- **Don't** add a second typeface, drop shadow, gradient fill, or corner radius outside what's cataloged here — the whole system is one monospace family, one accent color, one window shape.
- **Don't** state a metric, claim, or project detail beyond what PRODUCT.md's verified LinkedIn-sourced list supports — the terminal register implies "this is a real system status," so an invented number would break the page's own premise, not just its accuracy.
- **Don't** apply the glow filter to more than the name text (Bloom-Is-Earned Rule).
