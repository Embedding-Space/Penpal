# CSS Style Guide

## Context

Universal CSS/styling decisions. These apply regardless of specific component libraries or frameworks.

## Core Decisions

### Approach: Utility-First
- Always use utility classes (Tailwind)
- No component CSS files
- No CSS-in-JS

```jsx
// Good - utilities
<div className="flex items-center p-4">

// Bad - component CSS
<div className="user-card">
```

### Class Name Formatting
- Break long class lists when it helps readability
- No strict formatting rules
- Keep related utilities together

```jsx
// Good - readable
<div className="flex items-center justify-between p-4">

// Good - broken for clarity
<div 
  className="flex items-center justify-between p-4 
             bg-white dark:bg-gray-900 rounded-lg shadow-md"
>

// Bad - arbitrary line breaks
<div className="flex 
  items-center justify-between 
  p-4">
```

### Conditional Classes: Always clsx
```jsx
// Good - clsx for conditionals
import clsx from 'clsx';

<div className={clsx(
  "p-4 rounded",
  isActive && "bg-blue-500",
  isDisabled && "opacity-50 cursor-not-allowed"
)}>

// Bad - template literals
<div className={`p-4 rounded ${isActive ? 'bg-blue-500' : ''}`}>
```

### Colors: Project-Specific
- Define color approach per project
- Be consistent within each project

### Spacing: Tailwind Scale Only
```jsx
// Good - use Tailwind spacing tokens (e.g., p-4, mt-8, mb-2)
<div className="p-4 mt-8 mb-2">

// Bad - arbitrary values
<div className="p-[17px] mt-[31px]">
```

### Custom CSS: Almost Never
Only acceptable for:
- Complex animations not in Tailwind
- Third-party library integration
- Canvas/WebGL styling

```css
/* Acceptable - complex animation */
@keyframes pulse-scale {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Bad - use utilities */
.card {
  padding: 1rem;
  border-radius: 0.5rem;
}
```

## Non-Negotiable Rules

### Never Use
- `!important` - fix specificity properly
- Inline styles - use utilities
- IDs for styling - classes only
- CSS Modules - use utilities
- Styled Components - use utilities

```jsx
// All bad
<div style={{ padding: '16px' }}>  // No inline
<div id="header">  // No ID styling
<div className={styles.card}>  // No CSS Modules
const StyledDiv = styled.div`...`;  // No CSS-in-JS
```

### Always Include
- Hover states for interactive elements
- Focus states for keyboard navigation (use `:focus-visible` when appropriate)
- Disabled states when applicable
 - Respect `prefers-reduced-motion` for animations; offer a reduced-motion variant

```jsx
// Good - interactive states
<button className="... hover:... focus:... disabled:...">
```

## The CSS Meta Rule

Utilities solve 99% of styling needs. For the 1% that utilities can't handle, document why. If you're writing CSS, you're probably doing it wrong.
