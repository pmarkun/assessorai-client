# Design Guidelines

This project follows a minimalist and responsive design built with Tailwind CSS.

## Principles
- **Minimalism**: keep interfaces clean with plenty of whitespace.
- **Consistency**: reuse components and the established color palette (`#A541FF` as the primary accent).
- **Responsiveness**: all pages must work well on mobile and desktop. Utilize Tailwind's responsive utilities (`sm:`, `md:`, `lg:`).
- **Accessibility**: use semantic HTML and maintain good color contrast.
- **Simplicity**: avoid unnecessary effects or complex markup.

## Layout
- Extend `theme/templates/base.html` for new pages.
- The sidebar collapses on small screens; use the built-in toggle.
- Main content should be wrapped in the `block content` region.

## Adding New Features
- Use Tailwind utility classes instead of custom CSS whenever possible.
- Keep components flexible and reusable.
- Test layouts on mobile, tablet and desktop sizes.

