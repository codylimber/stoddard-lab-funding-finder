# Stoddard Lab Funding Finder

Grants, fellowships and travel funds for the Stoddard Lab at Princeton EEB (avian vision, coloration, evolution, ecology), with Princeton internal funds. Live site: **https://codylimber.github.io/stoddard-lab-funding-finder/**. Or open `index.html` in a browser.

## Update it
1. Edit rows in `catalog/programs/*.json` (`lab-societies.json`, `princeton.json`, `general-reused.json`) and tips in `catalog/notes.json`.
2. Run `python3 engine/build.py` (`--check` validates only).
3. Commit `index.html` and `data/programs.json`.

Rows with an `unv` field show an "unconfirmed" tag. Remove it only after reading the funder's own page. Princeton rows use ids starting `princeton-` and an optional `pu` step `{d, t, u}`.

## Credits
Adapted from the [Yale Life Science Funding Finder](https://github.com/vhorsley/yale-life-science-funding-finder) (MIT code, CC BY 4.0 catalog), which adapts Chiara Mingarelli's [Funding Finders](https://github.com/ChiaraMingarelli/funding-finders) (MIT). Design inspired by marycstoddard.com and Princeton's brand colors. Not an official Princeton page.

## Keeping it current
See [UPDATING.md](UPDATING.md) for the weekly, monthly and quarterly routine, how to recheck a row, and where to look for new programs. A GitHub Action opens a weekly recheck issue and fails any commit where `index.html` is out of date.

## Suggest a program
Use the form on the site, or [open a suggestion](https://github.com/codylimber/stoddard-lab-funding-finder/issues/new?template=suggest-program.yml).
