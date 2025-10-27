# Release Checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/marcusvolz/strava_py/actions) should be
      running cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/marcusvolz/strava_py/workflows/Test/badge.svg)](https://github.com/marcusvolz/strava_py/actions)

- [ ] Go to the [Releases page](https://github.com/marcusvolz/strava_py/releases) and
  - [ ] Click "Draft a new release"

  - [ ] Click "Choose a tag"

  - [ ] Type the next `vX.Y.Z` version and select "**Create new tag: vX.Y.Z** on
        publish"

  - [ ] Leave the "Release title" blank (it will be autofilled)

  - [ ] Click "Generate release notes" and amend as required

  - [ ] Click "Publish release"

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/marcusvolz/strava_py/actions/workflows/deploy.yml)
      has deployed to [PyPI](https://pypi.org/project/stravavis/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y stravavis && pip3 install -U stravavis && stravavis --help
```
