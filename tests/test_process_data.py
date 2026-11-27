from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from stravavis.process_data import process_data, process_file, process_tcx

TESTS_DIR = Path(__file__).parent
GPX_FILE = TESTS_DIR / "gpx" / "activity_7348460494.gpx"
TCX_FILE = TESTS_DIR / "tcx" / "activity_synthetic_run.tcx"
TCX_INDOOR = TESTS_DIR / "tcx" / "indoor-no-position.tcx"
TCX_PARTIAL = TESTS_DIR / "tcx" / "partial-no-namespace.tcx"

COLUMNS = ["lon", "lat", "ele", "time", "name", "dist"]


def test_process_tcx() -> None:
    df = process_tcx(str(TCX_FILE))

    assert df is not None
    assert list(df.columns) == COLUMNS
    assert len(df) == 60
    assert (df["name"] == str(TCX_FILE)).all()
    assert df["lat"].between(44.99, 45.01).all()
    assert df["lon"].between(6.99, 7.02).all()
    assert df["ele"].notna().all()
    assert df["time"].iloc[0] == pd.Timestamp("2022-05-14T07:30:00Z")
    assert df["time"].is_monotonic_increasing
    assert df["dist"].iloc[0] == 0
    assert df["dist"].is_monotonic_increasing


def test_process_tcx_matches_gpx_shape() -> None:
    gpx = process_file(str(GPX_FILE))
    tcx = process_file(str(TCX_FILE))

    assert gpx is not None
    assert tcx is not None
    assert list(tcx.columns) == list(gpx.columns)
    assert tcx["time"].dtype == gpx["time"].dtype
    # Both can be concatenated without timezone or dtype issues
    combined = pd.concat([gpx, tcx])
    assert len(combined) == len(gpx) + len(tcx)


def test_process_tcx_no_position() -> None:
    # Indoor or treadmill activities have no GPS position at all
    df = process_tcx(str(TCX_INDOOR))

    assert df is not None
    assert df.empty
    assert list(df.columns) == COLUMNS


def test_process_tcx_partial_data() -> None:
    # No namespace, some trackpoints without position, altitude or time
    df = process_tcx(str(TCX_PARTIAL))

    assert df is not None
    assert len(df) == 3
    assert df["lat"].tolist() == [45.01, 45.011, 45.012]
    assert df["ele"].isna().tolist() == [False, True, False]
    assert df["time"].isna().tolist() == [False, False, True]


def test_process_tcx_invalid(tmp_path: Path) -> None:
    bad = tmp_path / "bad.tcx"
    bad.write_text("<TrainingCenterDatabase><Activities>", encoding="utf-8")

    assert process_tcx(str(bad)) is None


def test_process_data_mixed_gpx_and_tcx(tmp_path: Path) -> None:
    for fixture in (GPX_FILE, TCX_FILE, TCX_INDOOR):
        shutil.copy(fixture, tmp_path)
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")
    filenames = sorted(str(p) for p in tmp_path.glob("*"))

    df = process_data(filenames)

    names = set(df["name"])
    assert names == {str(tmp_path / GPX_FILE.name), str(tmp_path / TCX_FILE.name)}
    assert list(df.columns) == COLUMNS
    assert str(df["time"].dt.tz) == "UTC"
