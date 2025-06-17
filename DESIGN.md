# Design Guidelines

These guidelines describe the visual language and UX principles for the project.

## Principles
- **Minimalism**: keep interfaces clean with lots of whitespace and limited color use.
- **Consistency**: reuse components and spacing throughout the project.
- **Accessibility**: ensure sufficient color contrast and keyboard-friendly navigation.
- **Responsiveness**: layouts must adapt gracefully from mobile to desktop screens.
- **Usability**: actions should be obvious and navigation straightforward.

## Color Palette
- **Primary accent**: `#A541FF`
- **Background**: `#F8F8F8`
- **Text**: `#1E1E1E`

## Layout
- Navigation is presented as a collapsible sidebar on small screens and fixed on wider screens.
- The main content area uses flexible spacing and centers elements with a maximum width for readability.
- Forms and buttons rely on Tailwind utility classes with custom CSS overrides.

## Components
- **Header**: contains branding and a menu toggle on small screens.
- **Sidebar**: holds navigation links and logout action.
- **Main**: area for template content using `{% block content %}`.

Follow these rules when adding new pages so the experience remains coherent and professional.
