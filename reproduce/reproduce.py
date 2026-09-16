"""Reproduce the validation figures of the companion paper.

Run it from the repository root:

    python reproduce/reproduce.py

Each case study is solved with the shipped engine and the quantities that the
figures plot are rebuilt. Two kinds of check are printed.

  reference   the external solution the paper compares against (PSCAD for the
              CIGRE system, pandapower for the three-winding system). The
              deviation printed here is the one quoted in the paper.
  regression  the solution this repository produced at release v1.0.1-paper,
              stored under reproduce/reference/. A non-zero value means this
              machine solves the case differently.

The MatACDC comparison of Fig. 6 is not rebuilt here. MatACDC is a third-party
MATLAB package and is not shipped with this repository, so only the regression
check runs for that figure.

Computed series are written to reproduce/output/ as CSV.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from load_case import load_case          # noqa: E402
from acdc_engine import run_acdc         # noqa: E402

# The external references are stored with six decimals, so a deviation built
# from two rounded numbers can exceed the reported one by up to this much.
RESOLUTION = 1e-6

REF = Path(__file__).resolve().parent / "reference"
OUT = Path(__file__).resolve().parent / "output"
FIGDIR = Path(__file__).resolve().parent / "figures"

# Grid file per scenario, grouped by the figure it feeds.
FIGURES = {
    "Fig. 6": {
        "slug": "fig06",
        "system": "Modified IEEE RTS-96",
        "external": None,                      # MatACDC, not shipped
        "scenarios": {
            "A1": "grids/rts96_scenario1_constant_vdc.xlsx",
            "A2": "grids/rts96_scenario2_droop.xlsx",
        },
        "reported": {"vm_pu": 8.0e-6, "angle_deg": 3.1e-3},
    },
    "Fig. 8": {
        "slug": "fig08",
        "system": "Modified CIGRE benchmark",
        "external": ("fig08_cigre_pscad.csv", "pscad"),
        "scenarios": {
            "B1": "grids/cigre_scenario1_constant_vdc.xlsx",
            "B2": "grids/cigre_scenario2_droop.xlsx",
        },
        "reported": {"vm_pu": 4.6e-4, "angle_deg": 1.6e-2},
    },
    "Fig. 10": {
        "slug": "fig10",
        "system": "71-bus islanded microgrid",
        "external": None,                      # the figure plots this solution itself
        "scenarios": {
            "C1": "grids/mg71_S1_baseline.xlsx",
            "C2": "grids/mg71_S2_deadband.xlsx",
            "C3": "grids/mg71_S3_gen_qlimit.xlsx",
            "C4": "grids/mg71_S4_ic_limit.xlsx",
        },
        "reported": {},
    },
    "Fig. S3": {
        "slug": "figS3",
        "system": "AC/DC three-winding transformer system",
        "external": ("figS3_3w_pandapower.csv", "pandapower"),
        "scenarios": {"S": "grids/pandapower_3w.xlsx"},
        "reported": {"vm_pu": 3.66e-6, "angle_deg": 1.38e-4},
    },
}


def solve(grid):
    """Solve one grid and return the plotted series: |V| over AC then DC buses,
    and the voltage angle over the AC buses."""
    result = run_acdc(load_case(ROOT / grid))
    ac = result["AC_result"]
    dc = result.get("DC_result") or []
    vm = [row[1] for row in ac] + [row[1] for row in dc]
    angle = [row[3] for row in ac]
    return {"vm_pu": vm, "angle_deg": angle}, int(round(float(result["iter_count"])))


def max_deviation(a, b):
    n = min(len(a), len(b))
    return max(abs(a[i] - b[i]) for i in range(n)) if n else float("nan")


def load_reference(name, column):
    df = pd.read_csv(REF / name)
    if "scenario" not in df.columns:
        df["scenario"] = "S"
    return {(s, q): g[column].tolist()
            for (s, q), g in df.groupby(["scenario", "quantity"], sort=False)}


def plot(figure, spec, series, external):
    """Redraw the figure from the rebuilt series. Needs matplotlib."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    scenarios = list(spec["scenarios"])
    FIGDIR.mkdir(exist_ok=True)
    name = spec["slug"] + ".png"
    # Fig. 6 plots deviations from MatACDC, which is not rebuilt here, so what
    # is drawn for it is the solution the deviations were taken from.
    lead = f"{figure} rebuilt" if (external or figure == "Fig. 10") else f"Solution behind {figure}"

    if figure == "Fig. 10":
        # One panel: the voltage profile of every bus, one line per scenario.
        fig, ax = plt.subplots(figsize=(7.2, 2.8), dpi=200)
        for scenario, style in zip(scenarios, ["-", "--", ":", "-."]):
            vm = series[(scenario, "vm_pu")]
            ax.plot(range(1, len(vm) + 1), vm, style, lw=1.2, label=scenario)
        ax.set_xlabel("Bus"); ax.set_ylabel("Voltage magnitude |V| [p.u.]")
        ax.grid(alpha=0.25); ax.legend(ncol=4, fontsize=8, frameon=False)
        ax.set_title(f"{lead}: {spec['system']}", fontsize=9)
        fig.tight_layout(); fig.savefig(FIGDIR / name); plt.close(fig)
        return name

    # The validation figures: magnitude on the left axis, angle on the right,
    # the external solution solid and this solution dashed.
    fig, axes = plt.subplots(len(scenarios), 1, figsize=(7.2, 2.6 * len(scenarios)),
                             dpi=200, squeeze=False)
    for ax, scenario in zip(axes[:, 0], scenarios):
        vm = series[(scenario, "vm_pu")]
        ang = series[(scenario, "angle_deg")]
        if external:
            ref = external[(scenario, "vm_pu")]
            ax.plot(range(1, len(ref) + 1), ref, "-", color="0.35", lw=1.1,
                    label=f"|V| {spec['external'][1]}")
        ax.plot(range(1, len(vm) + 1), vm, "--", color="tab:blue", lw=1.1,
                label="|V| rebuilt")
        ax.set_ylabel("|V| [p.u.]"); ax.grid(alpha=0.25)
        ax.legend(loc="lower left", fontsize=7, frameon=False)
        ax2 = ax.twinx()
        if external:
            refa = external[(scenario, "angle_deg")]
            ax2.plot(range(1, len(refa) + 1), refa, "-", color="darkred", lw=0.9,
                     label=f"angle {spec['external'][1]}")
        ax2.plot(range(1, len(ang) + 1), ang, "--", color="tab:red", lw=0.9,
                 label="angle rebuilt")
        ax2.legend(loc="upper right", fontsize=7, frameon=False)
        ax2.set_ylabel("Angle [deg]", color="tab:red")
        ax2.tick_params(axis="y", colors="tab:red")
        title = f"{lead}: {spec['system']}"
        ax.set_title(title if len(scenarios) == 1 else f"{title} - Scenario {scenario}",
                     fontsize=9)
    axes[-1, 0].set_xlabel("Bus")
    fig.tight_layout(); fig.savefig(FIGDIR / name); plt.close(fig)
    return name


def main(write_reference=False, make_plots=False):
    OUT.mkdir(exist_ok=True)
    rows = []
    for figure, spec in FIGURES.items():
        external = load_reference(*spec["external"]) if spec["external"] else None
        ref_name = spec["slug"] + "_proposed.csv"
        stored = None
        if not write_reference and (REF / ref_name).exists():
            stored = load_reference(ref_name, "proposed")
        computed = []
        drawn = {}
        for scenario, grid in spec["scenarios"].items():
            series, iters = solve(grid)
            for quantity, values in series.items():
                drawn[(scenario, quantity)] = values
            for quantity, values in series.items():
                for i, v in enumerate(values, start=1):
                    computed.append([scenario, quantity, i, v])
                row = {"figure": figure, "scenario": scenario, "quantity": quantity,
                       "iterations": iters, "reference": "", "reported": "",
                       "regression": ""}
                if external is not None:
                    dev = max_deviation(external[(scenario, quantity)], values)
                    row["reference"] = f"{dev:.3e}"
                    reported = spec["reported"].get(quantity)
                    if reported is not None:
                        ok = dev <= reported + RESOLUTION
                        row["reported"] = f"{reported:.2e} ({'ok' if ok else 'OVER'})"
                if stored is not None:
                    row["regression"] = f"{max_deviation(stored[(scenario, quantity)], values):.3e}"
                rows.append(row)
        frame = pd.DataFrame(computed, columns=["scenario", "quantity", "index", "proposed"])
        target = (REF if write_reference else OUT) / ref_name
        frame.to_csv(target, index=False)
        print(f"{figure:8s} {spec['system']:42s} -> {target.relative_to(ROOT)}")
        if make_plots:
            drawn_name = plot(figure, spec, drawn, external)
            print(f"{'':8s} {'':42s} -> {(FIGDIR / drawn_name).relative_to(ROOT)}")

    print()
    print(pd.DataFrame(rows).to_string(index=False))
    if write_reference:
        print("\nreference files rewritten")


if __name__ == "__main__":
    main(write_reference="--write-reference" in sys.argv,
         make_plots="--plot" in sys.argv)
