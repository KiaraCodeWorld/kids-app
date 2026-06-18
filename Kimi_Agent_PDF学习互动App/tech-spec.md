# Math Quest — Technical Specification

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.3.0 | UI framework |
| react-dom | ^18.3.0 | React DOM renderer |
| typescript | ^5.6.0 | Type safety |
| vite | ^6.0.0 | Build tool |
| @vitejs/plugin-react | ^4.3.0 | Vite React plugin |
| tailwindcss | ^3.4.0 | Utility CSS |
| framer-motion | ^11.0.0 | Page transitions, animations |
| canvas-confetti | ^1.9.0 | Celebration confetti effect |
| @types/canvas-confetti | ^1.6.0 | TypeScript types for confetti |
| lucide-react | ^0.400.0 | SVG icons (star, check, trophy, etc.) |
| clsx | ^2.1.0 | Conditional class names |
| tailwind-merge | ^2.6.0 | Merge Tailwind classes |

Google Fonts: Nunito (400, 600, 700, 800) loaded via `<link>` in index.html.

## Component Inventory

### Layout
- **Navbar** — Fixed top bar with logo, progress segments, score display
- **Footer** — Simple dark footer with tagline

### Sections
- **WelcomeScreen** — Hero with headline, subheadline, CTA, floating symbols bg
- **ProblemScreen** — Main two-column layout: ProblemCard + MathBuddy
- **CelebrationScreen** — Completion screen with confetti, summary, reset button

### Reusable Components
- **ProblemCard** — White card with question badge, points badge, problem image/text, options grid, submit button
- **MathBuddy** — Character SVG + speech bubble with dynamic messages
- **ExplanationPanel** — Expandable numbered steps with "Remember" box
- **OptionButton** — Individual option card with select/correct/wrong states
- **ProgressBar** — Segmented progress indicator (35 segments)
- **StarTracker** — Row of 35 star icons showing earned/empty
- **FloatingSymbols** — Background decoration with animated math symbols

## Animation Implementation

| Animation | Library | Implementation Approach | Complexity |
|-----------|---------|------------------------|------------|
| Floating math symbols background | CSS keyframes | Absolutely positioned divs with `@keyframes float-up`, random drift via CSS custom properties, 15-20 symbols | Low |
| Welcome entrance sequence | Framer Motion | `motion.div` with `initial/animate`, staggered delays (0s, 0.2s, 0.4s) | Low |
| Option selection pulse | CSS transitions | `transition-all` with `scale(1.02)` and border color change on `.selected` class | Low |
| Answer reveal sequence | Framer Motion | Chained `AnimatePresence` — loading spinner → checkmark/X bounce → speech bubble slide-in | Medium |
| Typewriter text effect | Custom hook | `useTypewriter(text, speed)` — uses `useEffect` with `setInterval` to append chars one by one | Medium |
| Star fly animation | Framer Motion | `motion.div` with `animate` calculating target X/Y from problem card to progress bar | Medium |
| Problem transition slide | Framer Motion | `AnimatePresence` with `exit={{x: -300}}` and `enter={{x: 300}}` on ProblemCard | Medium |
| Confetti celebration | canvas-confetti | Fire 150 particles, 5 gravity, custom colors, 5s duration | Low |
| MathBuddy speech bubble | Framer Motion | `initial={{x: 50, opacity: 0}}` `animate={{x: 0, opacity: 1}}` on reveal | Low |

## State & Logic

### State Management: React useState (no external library needed)
- Single source of truth in App component, passed down as props
- 7 state variables: `currentQuestion`, `selectedOption`, `answerSubmitted`, `isCorrect`, `score`, `starsEarned[35]`, `hintShown`

### Data Flow
```
App (state container)
├── Navbar ← score, currentQuestion
├── WelcomeScreen → onStart → sets screen to 'problem'
├── ProblemScreen ← currentProblem, selectedOption, answerSubmitted, isCorrect, hintShown
│   ├── ProblemCard → onSelectOption, onSubmit
│   ├── MathBuddy → message based on state
│   └── ExplanationPanel → steps, keyConcept
├── Footer
└── CelebrationScreen ← score (when currentQuestion === 35)
```

### Key Implementation Notes

1. **Problem Data**: All 35 problems stored as a static array in `src/data/problems.ts`. Each includes pre-written kid-friendly explanations extracted from the PDF solutions.

2. **PDF Images**: Diagram images extracted from the PDF stored in `public/images/problems/`. Referenced by filename in the problem data. Images displayed with original aspect ratio, `max-width: 100%`.

3. **Answer Evaluation**: Compare `selectedOption` against `problem.correctAnswer`. Update `starsEarned[currentQuestion]` and `score` accordingly.

4. **Hint System**: Hint is shown on demand (button click). Hint text is pre-written for each problem — a simplified clue without giving away the answer.

5. **Explanation Reveal**: Steps appear one by one with "Show Next Step" button. Student can also "Show All Steps" at once. Each step uses the typewriter animation.

6. **Progress Persistence**: `starsEarned` array stored in `localStorage` so progress survives page refresh. Loaded on mount.

7. **Responsive**: Two-column (problem + buddy) on desktop 1200px+, single column on mobile. MathBuddy becomes an expandable bottom sheet on mobile.

## Build Commands

```bash
cd /mnt/agents/output/app && npm install
npm run build
```

## Project Structure

```
public/
  images/
    problems/         # PDF-extracted diagram images
    math-buddy.svg    # Character illustration
src/
  data/
    problems.ts       # All 35 problems with explanations
  components/
    Navbar.tsx
    Footer.tsx
    WelcomeScreen.tsx
    ProblemScreen.tsx
    CelebrationScreen.tsx
    ProblemCard.tsx
    MathBuddy.tsx
    ExplanationPanel.tsx
    OptionButton.tsx
    ProgressBar.tsx
    StarTracker.tsx
    FloatingSymbols.tsx
  hooks/
    useTypewriter.ts
  types/
    problem.ts        # TypeScript interfaces
  App.tsx
  main.tsx
  index.css
```
