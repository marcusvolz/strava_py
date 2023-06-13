# Release Checklist

- [ ] Get `main` to the appropriate code release state.

- [ ] Update `version` in `setup.cfg` and commit and push.

* [ ] Start from a freshly cloned repo:

```bash
cd /tmp
rm -rf strava_py
git clone https://github.com/marcusvolz/strava_py
cd strava_py
```

- [ ] (Optional) Create a distribution and release on **TestPyPI**:

```bash
python -m pip install -U pip build keyring twine
rm -rf build dist
python -m build
twine check --strict dist/* && twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

- [ ] (Optional) Check **test** installation:

```bash
python -m pip uninstall -y stravavis
python -m pip install -U -i https://test.pypi.org/simple/ stravavis
stravavis --help
```

- [ ] Tag with the version number:

```bash
git tag -a v0.0.1 -m "Release 0.0.1"
```

- [ ] Create a distribution and release on **live PyPI**:

```bash
python -m pip install -U pip build keyring twine
rm -rf build dist
python -m build
twine check --strict dist/* && twine upload -r pypi dist/*
```

- [ ] Check installation:

```bash
python -m pip uninstall -y stravavis
python -m pip install -U stravavis
stravavis --help
```

- [ ] Push tag:

```bash
git push --tags
```

- [ ] Create a new release: https://github.com/marcusvolz/strava_py/releases/new

- [ ] Click "Choose a tag" and select newest.

- [ ] Click "Auto-generate release notes", amend as required and "Publish release".
