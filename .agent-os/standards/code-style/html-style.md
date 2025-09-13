# HTML Style Guide

## Context

Basic HTML formatting rules. For React/JSX, refer to the TypeScript style guide.

## Structure Rules
- Use 2 spaces for indentation
- Place nested elements on new lines with proper indentation
- Content between tags should be on its own line when multi-line

## Attribute Formatting
- Multiple attributes can go on the same line if readable
- Break to multiple lines when it improves clarity
- Keep the closing `>` on the same line as the last attribute

## Example HTML Structure

```html
<div class="container">
  <header>
    <h1>Page Title</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>Article Title</h2>
      <p>
        Content goes here.
      </p>
    </article>
  </main>
</div>
```

## Notes

- This guide covers standard HTML
- For JSX in React components, follow TypeScript conventions
- Project-specific styling approaches (CSS frameworks, etc.) are defined at the product level
- Accessibility basics: provide `alt` text for images, label form controls
- Use semantic landmarks (`header`, `nav`, `main`, `footer`) for structure
