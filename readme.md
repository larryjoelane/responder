# Responder

Responder is a small CSS library for responsive pages. It is still a row and column layout. Colors, type, spacing, and the other knobs live in one theme file. There is no Sass, no gulp, and no build step.

The manual is at [https://larryjoelane.github.io/responder/](https://larryjoelane.github.io/responder/).

## Use it

Copy the `css` folder into your site.

Everything, green theme:

```html
<link rel="stylesheet" href="css/responder.css">
```

Light or dark instead:

```html
<link rel="stylesheet" href="css/responder-light.css">
<link rel="stylesheet" href="css/responder-dark.css">
```

Only what a page needs. Link the theme first:

```html
<link rel="stylesheet" href="css/themes/green.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/grid.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/utilities.css">
```

```html
<div class="row">
  <div class="column-50">50% width Column 1</div>
  <div class="column-50">50% width Column 2</div>
</div>
```

`responder.css`, `responder-light.css`, and `responder-dark.css` are `@import` manifests. One link tag loads the theme and every component file. The browser requests each file, so there is nothing to compile and nothing that can drift from the modules. The cost is those extra requests, which is small on HTTP/2 or HTTP/3. Concatenating them into one physical file would need a build, or a second copy maintained by hand.

The old path `responder.css` at the repository root still works. It imports `css/responder.css`.

## Theme

The default theme is `css/themes/green.css`: saturated green `#00c853` for the page, deep green `#053422` for buttons and links, white cards. `css/themes/light.css` is neutral gray. `css/themes/dark.css` is neutral charcoal. Each file defines the same custom properties. Every component reads those properties.

Swap a whole site by linking a different bundle. A no-JS switcher links the green bundle plus the two alternate files. Light applies while `#theme-light` is checked. Dark applies while `#theme-dark` is checked.

```html
<link rel="stylesheet" href="css/responder.css">
<link rel="stylesheet" href="css/themes/light.css">
<link rel="stylesheet" href="css/themes/dark.css">

<input type="radio" name="theme" id="theme-green" checked>
<label for="theme-green">Green</label>
<input type="radio" name="theme" id="theme-light">
<label for="theme-light">Light</label>
<input type="radio" name="theme" id="theme-dark">
<label for="theme-dark">Dark</label>
```

The manual's header uses that pattern. Nothing is stored across reloads.

Text and UI colors in all three themes meet WCAG 2.2 AA: 4.5:1 for text, 3:1 for borders, buttons, and focus rings. `scripts/check-contrast.py` checks the pairs.

Breakpoint tokens in the theme file are the documented widths (480px, 768px, 992px). Media queries cannot read custom properties, so `grid.css`, `nav.css`, and `utilities.css` repeat those numbers. Change a breakpoint in the token and in those files together.

## Files

| File | Role |
| --- | --- |
| `css/responder.css` | Green theme and every component |
| `css/responder-light.css` | Light theme and every component |
| `css/responder-dark.css` | Dark theme and every component |
| `css/responder-components.css` | Every component, no theme |
| `css/themes/green.css` | Green custom properties (default) |
| `css/themes/light.css` | Neutral light custom properties |
| `css/themes/dark.css` | Neutral dark custom properties |
| `css/base.css` | Box model, type, links, focus |
| `css/grid.css` | `.row` and `.column-*` |
| `css/layout.css` | Header, footer, wrap, container |
| `css/nav.css` | Horizontal nav, disclosure menu, legacy mobile menu |
| `css/media.css` | Responsive images |
| `css/button.css` | Buttons |
| `css/card.css` | Cards |
| `css/accordion.css` | `<details>` accordion |
| `css/tabs.css` | Radio-button tabs |
| `css/popover.css` | Native popover |
| `css/table.css` | Tables |
| `css/form.css` | Fields |
| `css/notice.css` | Notices |
| `css/utilities.css` | Show, hide, stack, alignment |
| `docs/` | Manual, served by GitHub Pages |

## Docs and previews

GitHub Pages serves the `gh-pages` branch. Production is the root, published from `master` by `.github/workflows/pages.yml`. A pull request publishes `docs/` to `pr-preview/pr-<number>/` with [rossjrw/pr-preview-action](https://github.com/rossjrw/pr-preview-action). The preview URL looks like:

`https://larryjoelane.github.io/responder/pr-preview/pr-1/`

Two repository settings are required, and only someone with admin access can change them:

1. **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch **gh-pages**, folder **/ (root)**. The "GitHub Actions" source does not work with the preview action.
2. **Settings → Actions → General → Workflow permissions → Read and write permissions**, so the preview workflow can push to `gh-pages`.

The Pages workflow copies `docs/` and `css/` into a publish folder and rewrites `../css/` to `css/`. That is packaging for the site root. The library itself is not built. Opening `docs/index.html` from the repository still uses `../css/`.

If Pages is not enabled yet, the branch can be viewed through a raw HTML preview, for example:

`https://htmlpreview.github.io/?https://github.com/larryjoelane/responder/blob/cursor/modern-css-library-a530/docs/index.html`

## What changed

Column classes keep the Sass names (`.column-50`). The 2014 names (`.column50`) are aliases. `#header`, `#wrap`, `#footer`, `.nav-horizontal`, `.mobile-menu`, `.responsive-image`, `.hide`, and the breakpoint hide classes still exist. The manual's `id="column100"` was never a CSS hook; use `class="column-100"`.

Details, including what was left out because it would need JavaScript, are in the manual's Changes section.
