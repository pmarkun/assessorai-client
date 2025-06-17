# Design Guidelines

These guidelines outline the design principles used in the project. Follow them when creating new pages or components.

## Principles

- **Minimalism** – keep the interface simple and reduce unnecessary elements.
- **Consistency** – reuse common patterns for navigation, spacing and typography.
- **Responsiveness** – layouts must adapt to mobile, tablet and desktop screens.
- **Accessibility** – prefer semantic HTML and ensure good colour contrast.
- **Clarity** – content should be easy to scan with clear headings and sections.

## Layout

- A sidebar navigation is available on larger screens. On small screens it can be toggled via the menu button.
- Pages should wrap content inside a `max-w-7xl mx-auto` container to maintain comfortable widths.
- Use Tailwind CSS utility classes for spacing and typography.

## Colours and Typography

- Primary colour: `#A541FF`.
- Backgrounds should generally be light (`bg-gray-50` or `bg-white`).
- Text is dark gray (`text-gray-900`) with headings slightly darker.
- Use system fonts for a clean look (`font-sans`).

## Components

- Buttons use rounded corners and change shade on hover.
- Forms should be stacked on mobile and align horizontally on larger screens using grid utilities.

Following these rules helps keep the UI elegant and functional as the project grows.
