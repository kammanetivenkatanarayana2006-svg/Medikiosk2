# MediKiosk - UI Design System (Phase 4 Complete)

## Design Philosophy
MediKiosk presents itself as a PREMIUM + FUTURISTIC + TRUSTWORTHY + CLINICAL + ACCESSIBLE medical technology platform.

## Visual Direction
- **Style:** Modern healthcare interfaces with subtle glassmorphism
- **Foundation:** Dark medical navy with cyan/teal accents
- **Feel:** Professional, trustworthy, technologically advanced
- **Balance:** Futuristic elements while maintaining clinical professionalism

## Color System

### Dark Theme (Default)
- **Background:** Deep navy (#0a0e1a)
- **Surface:** Dark blue-gray (#111827)
- **Elevated Surface:** Lighter navy (#1a2332)
- **Primary:** Medical cyan (#06b6d4)
- **Secondary:** Cool blue (#3b82f6)
- **Success:** Green (#10b981)
- **Warning:** Amber (#f59e0b)
- **Danger:** Red (#ef4444)

### Light Theme
- Professional white/light-gray surfaces
- Same primary colors adjusted for contrast
- Maintains medical trust

## Typography System
- **Primary Font:** Inter (clean, modern, readable)
- **Monospace:** JetBrains Mono (for technical/medical codes)
- **Hierarchy:** Display → H1 → H2 → H3 → Body → Caption
- **Sizes:** 12px to 48px with responsive scaling
- **Weights:** Light (300) to Bold (700)

## Spacing System
- **Base Unit:** 4px
- **Scale:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px
- **Consistent:** No arbitrary values

## Border Radius & Elevation
- **Small:** 4px (buttons)
- **Medium:** 8px (inputs)
- **Large:** 12px (cards)
- **Extra Large:** 16-24px (modal, containers)
- **Full:** 9999px (pills, badges)
- **Shadows:** Subtle layered shadows for depth

## Responsive Breakpoints
- **Mobile:** 480px
- **Tablet:** 768px
- **Laptop:** 1024px
- **Desktop:** 1280px
- **Kiosk:** 1920px

## Kiosk-First Design
- **Minimum touch target:** 44px
- **Comfortable touch target:** 48px
- **Large touch target:** 56px
- **Spacing:** Generous for touch interaction
- **No hover-dependent interactions**

## Accessibility Standards
- WCAG 2.1 AA compliance
- Semantic HTML
- Keyboard navigation
- Visible focus states
- Reduced motion support
- Screen reader compatible
- High contrast modes

## Animation Principles
- Subtle and purposeful
- Fast (150-350ms) for kiosk interaction
- Never blocks user interaction
- Respects prefers-reduced-motion

## Medical Trust & Visual Safety
- AI outputs clearly labeled as "AI-assisted"
- Doctor verification prominently displayed
- No alarming unnecessary medical animations
- Clear information hierarchy

## Component Library (Phase 4)
- **Button:** Primary, Secondary, Outline, Ghost variants
- **Card:** Default, Glass, Elevated variants
- **Badge:** Status indicators
- **Input:** Form inputs with labels and validation
- **Progress:** Bar and Circular indicators

## Theme Architecture
- CSS variables for all design tokens
- Dark/Light theme support
- System preference detection
- Extensible for future themes

# MediKiosk - UI Design System

[Previous content preserved...]

## Cinematic Welcome Principles (Phase 5)

### Visual Sequence
1. Medical background with subtle grid
2. MediKiosk logo reveal
3. Heartbeat waveform animation
4. Welcome message entrance
5. AI orb visual
6. Start consultation CTA

### Animation Rules
- Smooth, subtle, purposeful
- Fast transitions (150-350ms)
- Respects prefers-reduced-motion
- No blocking animations
- Performance optimized (CSS/Canvas)

### AI Orb Visual Rules
- Soft pulsing core
- Orbital rings
- Subtle particle effects
- Medical cyan color scheme
- No aggressive animations

### Heartbeat Waveform Rules
- Canvas-based for performance
- Subtle heartbeat pattern
- No audio recording implication
- Purely decorative visualization

### Kiosk Interaction Guidelines
- Large touch targets (44px+)
- Clear primary action
- Skip intro option
- No hover-dependent interactions
- Keyboard accessible

### Reduced Motion Behavior
- Disables major animations
- Uses simple fades
- All information immediately visible
- Start button immediately available
# MediKiosk - UI Design System

[Previous content preserved...]

## Patient Onboarding Patterns (Phase 6)

### Patient Type Cards
- Large, touch-friendly cards
- Clear visual icons
- Hover and focus states
- Keyboard accessible
- Responsive grid layout

### Medical Form Controls
- Large inputs (48px+ height)
- Clear labels
- Visible focus states
- Error messages below fields
- Accessible validation

### Confirmation Screen
- Clear data display
- Edit and confirm actions
- AI-assisted documentation notice
- Medical trust messaging

### Validation UX
- Real-time validation on blur
- Clear error messages
- Focus first invalid field
- No color-only error indication

### Kiosk Interaction
- All controls 44px+ touch targets
- Keyboard navigation support
- Visible focus indicators
- No hover-dependent actions