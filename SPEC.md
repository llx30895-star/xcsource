# XCSOURCE Website — Specification

## 1. Concept & Vision

A premium corporate website for XCSOURCE — a cross-border e-Commerce company with global ambition. The site communicates professionalism, ambition, and global connectivity through a bold dark theme punctuated by vibrant accent colors. Every section should feel like an invitation to a world without borders — elegant, purposeful, and inspiring.

---

## 2. Design Language

### Aesthetic Direction
**"Midnight Global Commerce"** — Deep, sophisticated dark palette evoking the 24-hour global marketplace. Warm orange accents signal energy and opportunity. Clean geometric forms suggest precision and structure. Inspired by premium fintech and logistics brands.

### Color Palette
| Role | Hex | Usage |
|---|---|---|
| Background Dark | `#0B1120` | Primary background |
| Surface | `#0F1929` | Cards, nav |
| Surface Light | `#162035` | Hover states, secondary surfaces |
| Border | `#1E3054` | Subtle dividers |
| Primary (Orange) | `#E8830A` | CTAs, accents, highlights |
| Primary Light | `#FF9A2E` | Gradient endpoints |
| Primary Glow | `rgba(232,131,10,0.2)` | Glow effects |
| Text Primary | `#FFFFFF` | Headings |
| Text Secondary | `#A8B8D8` | Body text |
| Text Muted | `#5C6E8A` | Labels, captions |

### Typography
- **Display/H1**: `Syne` (700, 800) — Bold, geometric, distinctive for hero text
- **Headings H2–H4**: `Syne` (600, 700)
- **Body**: `DM Sans` (400, 500) — Clean and readable
- **Mono/Labels**: `JetBrains Mono` (500) — For technical/brand accent text

### Spatial System
- Base unit: 8px
- Section padding: 120px top/bottom (desktop), 80px (tablet), 60px (mobile)
- Max content width: 1200px
- Card border-radius: 16px; Small elements: 8px; Pills: 999px

### Motion Philosophy
- **Entrance animations**: Staggered fade-up on scroll (Intersection Observer), 600ms ease-out
- **Hover interactions**: Scale 1.02–1.05 with color shift, 250ms ease
- **Navigation**: Smooth scroll to sections, active link highlight
- **Hero**: Subtle floating animation on globe element
- **Counters**: Animated number counting when scrolled into view

### Visual Assets
- **Icons**: Lucide icon set via CDN (SVG)
- **Decorative**: CSS gradient orbs, grid patterns, geometric shapes
- **Globe**: Custom CSS/SVG animation representing global connectivity
- **No external images**: Pure CSS/SVG decorative elements

---

## 3. Layout & Structure

### Page Structure
```
[Sticky Navigation Bar]
[Hero Section] — Full-viewport, dark with animated globe, brand tagline
[About Section] — Company mission with animated stat counters
[Brand Story Section] — "X for Cross, C for Countries" with visual metaphor
[Values Section] — 4 core values in a grid
[CTA Section] — Contact/partnership call-to-action
[Footer] — Minimal footer with links
```

### Visual Pacing
- Hero: Maximum visual impact, minimal text, floating globe animation
- About: Clean, text-focused, trust-building stats
- Brand Story: Visually rich, two-column layout with decorative elements
- Values: Card grid, breathing room between items
- CTA: Bold, contrast, single action
- Footer: Understated, professional

### Responsive Strategy
- Desktop: 3–4 column grids, large typography
- Tablet (768px): 2 column grids, reduced spacing
- Mobile (480px): Single column, stacked layouts, hamburger nav

---

## 4. Features & Interactions

### Navigation
- Sticky header with blur backdrop
- Logo + nav links (About, Mission, Brand, Values, Contact)
- Mobile: Hamburger menu with slide-in overlay
- Active section highlighting via scroll spy

### Hero Section
- Animated SVG globe that slowly rotates/floats
- Main headline: large Syne font with gradient text
- Subheadline: DM Sans, muted color
- CTA button: "Discover Our Story" with hover glow
- Background: Dark with subtle grid pattern overlay

### About / Mission Section
- Section title with horizontal rule decoration
- Full mission statement text
- 3 animated stat counters (countries served, customers, team members)

### Brand Story Section
- Two-column layout: text on left, animated visual on right
- "X · C · SOURCE" letters with animated reveal
- Decorative gradient orb behind text

### Values Section
- 4 cards in a grid
- Each card: icon (Lucide), title, description
- Cards: `Potentials`, `Skills`, `Growth`, `Rewards`
- Hover: lift + border glow

### CTA Section
- Bold headline: "Ready to connect across borders?"
- Orange gradient button
- Background: gradient orb

### Footer
- XCSOURCE logo + tagline
- Copyright + year

---

## 5. Component Inventory

### NavBar
- States: default (transparent), scrolled (blur + border), mobile-open
- Logo: text "XCSOURCE" in Syne Bold
- Links: hover underline animation

### HeroGlobe (SVG)
- Animated SVG circle with lat/lon lines
- Slow rotation keyframe
- Floating translateY animation

### StatCounter
- Large number + label
- Animates from 0 to target value when in viewport
- Triggers once per session

### ValueCard
- Default: dark surface, border
- Hover: elevated shadow, orange border glow, icon color change

### CTAButton
- Primary: orange gradient, white text
- Hover: lighter orange, subtle scale + glow shadow
- Active: pressed effect (scale 0.98)

### MobileMenu
- Full-screen overlay
- Slide-in from right
- Large nav links with hover highlight

---

## 6. Technical Approach

- **Single HTML file** with embedded CSS and JavaScript
- **No frameworks** — Vanilla HTML5, CSS3, ES6+ JavaScript
- **Google Fonts**: Syne, DM Sans, JetBrains Mono
- **Lucide Icons**: via unpkg CDN
- **Intersection Observer API**: Scroll-triggered animations
- **CSS Custom Properties**: Full theming support
- **Smooth scroll**: CSS `scroll-behavior: smooth` + JS for nav
- **Responsive**: CSS Grid + Flexbox, mobile-first media queries
