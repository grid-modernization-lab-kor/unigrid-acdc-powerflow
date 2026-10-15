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
  solution stored with this release, and redraws them with `--plot`.
- The validation figures of the paper and its Appendix, under
  `docs/paper/`, with the IEEE copyright notice.

### Changed
- Both compiled packages (`unigrid_pkg_mac`, `unigrid_pkg_win`) now carry
  solver v17 instead of v11. Among other changes, it models DC loads as ZIP
  loads and limits the active power of an interlinking converter at its
  apparent-power capability. Solved with both
  packages, the twelve `grids/*.xlsx` cases agree to within a relative 1e-9 and
  take the same number of iterations.
- All three solvers (hybrid, AC-only, DC-only) default to a convergence
  tolerance of 1e-6, the tolerance behind the paper's numbers.
- `reproduce/` checks the three-winding system against the reference used for
  the Appendix (now stored at full precision, as `figC2_*`), quotes the
  Appendix deviations, and stores the solution of this release for the
  regression check.
- The validation figures under `docs/paper/` are typeset from the current
  paper and Appendix (Fig. 6, 8, 10, and C2).
- The DC Bus Data sheet of the paper's case files now lists the ZIP shares
  `Z_p`, `I_p`, and `P_p` of each DC load (eight columns instead of six).
  Files in the old six-column layout still load.
- Results are saved under `results/<grid name>/` instead of one shared folder,
  so running several cases no longer overwrites the previous one.
- The README names the companion paper and its review state.

### Fixed
- The magnetizing susceptance of a three-winding transformer now scales with
  1/ω, as an inductive shunt and as stated in the Appendix; it scaled with ω
  before. Results change only when the frequency is solved and the transformer
  has a no-load current, which none of the shipped cases has.
- `grids/rts96_scenario1_constant_vdc.xlsx` and `grids/rts96_scenario2_droop.xlsx`
  are now the inputs the paper used. The earlier files stopped at the input check
  of the newer solver, because an interlinking converter and a generator both
  held the voltage of AC bus 215.
- `grids/mg71_S1_baseline.xlsx` to `grids/mg71_S4_ic_limit.xlsx` follow the
  redesigned 71-bus microgrid of the paper.
- `grids/pandapower_3w.xlsx` is the Appendix version, with the frequency range
  set symmetric about the nominal value ([0.98, 1.02] p.u.).
- `setup_windows.bat` installed a package folder that is not in the repository;
  it now installs `unigrid_pkg_win/for_testing`.
- The README follows the paper's current title and author order, calls the
  supplementary document the Appendix, and points to the current repository
  address.

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
