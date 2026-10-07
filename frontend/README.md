# Tailwind UI

This Django site uses Tailwind CSS with project-specific components and native JavaScript.

## Development

Run `npm ci` once, then `npm run css:watch` alongside the Django development server.
Run `npm run css:build` before reviewing or deploying changes.

- Edit `frontend/css/app.css` for theme tokens and shared components.
- Fonts are served locally from `static/fonts/`, using the existing UI preview font files and their OFL licenses. The initial TTF assets are about 12 MB in total; WOFF2/subsetting can be evaluated during production optimization.
- Use `ui-list-item` for list cards. `list-item` is a Tailwind display utility and overrides component grid layouts.
- Use utilities in the existing Django templates; shared markup lives in `core/templates/core/components/`.
- `static/css/app.css` is generated and committed so deployments can serve the UI without Node at runtime. Never edit it directly.
- Run the CSS build before Django's normal static-file collection step.
- Tailwind scans only the explicitly listed application templates and JavaScript directories.
- Use complete utility names rather than constructing partial class names with Django variables.
- Keep JavaScript action hooks in `data-*` attributes.

## Browser verification

Use an environment with the repository's Python requirements installed:

```sh
python -m frontend.tests.seed
python manage.py runserver 127.0.0.1:8765 --settings=frontend.tests.settings --noreload
# In another terminal:
npx playwright install chromium
npm run css:build
npm run test:ui
```

The UI settings never import `.env`. They use a separate SQLite database in the
system temporary directory and a local-memory email backend. The seed account
is `ui@example.test`, password `ui-preview-password`; these fixtures must never
be used in production. Browser tests create and update only this isolated data.
Stop the preview server after verification. The normal development server
continues to use the project's existing settings and database.

Run Django regression tests with:

```sh
python manage.py test --settings=frontend.tests.settings
```

The watcher dependency is overridden to `@parcel/watcher@2.6.0` to avoid the
vulnerable braces/micromatch chain in the CLI's older watcher dependency.
Revisit this override when updating Tailwind.

The first UI pass includes real forms and server data. Decorative illustrations use the specified construction placeholders. Learning statistics, recent-answer history, MC Quiz and admin announcement publishing remain future work. Current-page server enforcement for batch updates remains deferred by the owner.

Browser support follows Tailwind 4 (Safari 16.4+, Chrome 111+, Firefox 128+). The layout supports widths from 320 CSS pixels, short viewports and mobile safe areas.
