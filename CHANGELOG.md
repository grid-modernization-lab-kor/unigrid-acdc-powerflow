# Changelog

All notable changes to this repository are recorded here. Releases are tagged,
and the tag is what a citation should name, because the default branch keeps
moving.

## Unreleased

### Added
- A grid file can be passed on the command line
  (`python run_unigrid.py grids/cigre_scenario2_droop.xlsx`), so a case runs
  without editing the SETTINGS block. The command line wins over the block.
- This changelog, and a citation section in the README.
- `reproduce/reproduce.py` rebuilds the quantities plotted in the validation
  figures and checks them against the external references and against the
  solution stored at v1.0.1-paper, and redraws them with `--plot`.
- The validation figures of the paper and the supplementary material, under
  `docs/paper/`, with the IEEE copyright notice.

### Changed
- Results are saved under `results/<grid name>/` instead of one shared folder,
  so running several cases no longer overwrites the previous one.
- The README names the companion paper and its review state.

## [v1.0.1-paper] - 2026-09-15

### Fixed
- `grids/rts96_scenario2_droop.xlsx` was an earlier droop calibration. Solved
  with the same engine, the two files differ by 3.9e-2 p.u. in voltage
  magnitude and 3.05 deg in angle, so the published file did not reproduce the
  droop scenario of the paper.
- `grids/pandapower_3w.xlsx` was the AC-only 30-bus network. The three-winding
  transformer case is an AC/DC system (24 AC buses, 7 DC buses, 3 interlinking
  converters); the new file reproduces the reported curves.

## [v1.0-paper] - 2026-09-15

First tagged snapshot of the code and data behind the companion paper.

### Added
- Compiled engines for macOS and Windows, built from the same source.
- Case files for the three case-study systems and for the two systems in the
  supplementary material.

### Changed
- The engine ships with the convergence tolerance used for the paper (1e-6 for
  the hybrid and AC-only solvers). Running a case as it comes reproduces the
  deviations reported in the paper; no settings need to be changed.
