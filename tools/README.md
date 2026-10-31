# Tester guide builder (MAS-707)

The pages under `docs/` (served by GitHub Pages) are generated. Edit `build_site.py`, never the HTML by hand, or the next rebuild drops the edit.

```
python3 -I tools/build_site.py . tools/privacy-notice.adf.json
git diff -- docs        # review; an unchanged build prints nothing
```

- `privacy-notice.adf.json`: the privacy notice Adar approved (Jira MAS-707, comment 14402), placed on the privacy pages verbatim. Never retype it.
- `check_notice.py <page> <adf.json> <he|en>`: checks that a privacy page still carries the notice byte for byte.
- Images live in `docs/img/`: real screenshots cropped to the dialog, with the button to press marked.
- After a push: `npm run check:public-links` in the master-step repo.

This folder is not served; Pages serves `docs/` only.
