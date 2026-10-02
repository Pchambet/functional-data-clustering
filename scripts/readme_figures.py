# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib>=3.9", "numpy>=2.0", "pandas>=2.2"]
# ///
"""README figures and headline numbers, rebuilt from the committed result tables.

The R pipeline writes its results as CSV (and, for the silhouette/ARI paradox, as a
generated LaTeX table). This script only reads those files, so the README can be
regenerated and checked without R:

    uv run --script scripts/readme_figures.py           # rewrite docs/figures/
    uv run --script scripts/readme_figures.py --check   # fail if README drifted
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures"
SIM = ROOT / "experiments" / "03_simulated_hybride" / "results" / "metrics_all_runs.csv"
REAL = {
    "Canadian Weather": ROOT / "docs" / "exports" / "comparaison_canadian_weather.csv",
    "Berkeley Growth": ROOT / "docs" / "exports" / "comparaison_growth.csv",
    "Tecator": ROOT / "docs" / "exports" / "comparaison_tecator.csv",
}
PARADOX_TEX = ROOT / "docs" / "generated" / "paradox_silhouette_ari.tex"
NSELECT = ROOT / "experiments" / "01_instabilite" / "results"
NSELECT_SIM = (
    ROOT
    / "experiments"
    / "01_instabilite"
    / "results_simulated"
    / "nselectboot_simulated_all_runs.csv"
)
TRUE_K = {"canadian": 4, "growth": 2, "tecator": 3}

INK, TEAL, AMBER, SLATE, GRID = "#0f172a", "#0d9488", "#d97706", "#64748b", "#e2e8f0"

# Display names, in the order used in every table and figure.
METHODS = {
    "D0": "Curves only: level $D_0$",
    "D1": "Curves only: derivative $D_1$",
    "Df_silopt": r"Curves only: $D_p(\alpha)$, silhouette",
    "Ds": "Covariates only: $D_s$",
    "A": "A: FPCA scores + Z, k-means",
    "B_silopt": r"B: weighted $D_w(\alpha,\omega)$, silhouette",
    "C_DK_ancien": "C: Gaussian kernel product $D_K$",
    "DK_reconstruit": "HFV hybrid PCA + $D_K$",
}
REAL_KEYS = {
    "Baseline D0": "D0",
    "Baseline Ds": "Ds",
    "A (": "A",
    "B (": "B_silopt",
    "C (": "C_DK_ancien",
    "HFV": "DK_reconstruit",
}


def style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": SLATE,
            "axes.labelcolor": INK,
            "axes.titlecolor": INK,
            "xtick.color": SLATE,
            "ytick.color": INK,
            "text.color": INK,
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
        }
    )


def num(tex: str) -> float:
    return float(tex.replace("{,}", ".").strip(" $"))


def load_paradox() -> pd.DataFrame:
    """Rows of the generated silhouette/ARI table (strategy B, real datasets).

    The table's gap column is computed in R on unrounded ARIs, so it can differ by 0.001 from
    the difference of the 3-decimal ARIs it prints (0.898 - 0.616 = 0.282, table 0.283). The
    README and the figure quote those 3-decimal ARIs, so the gap is recomputed from them.
    """
    rows = []
    for line in PARADOX_TEX.read_text().splitlines():
        cells = [c.strip() for c in line.rstrip("\\ ").split("&")]
        if len(cells) != 9 or not cells[1].isdigit():
            continue
        sil_pt = re.findall(r"\d\{,\}\d+", cells[2])
        best_pt = re.findall(r"\d\{,\}\d+", cells[5])
        rows.append(
            {
                "dataset": cells[0].replace("Growth", "Berkeley Growth"),
                "k": int(cells[1]),
                "sil_alpha": num(sil_pt[0]),
                "sil_omega": num(sil_pt[1]),
                "sil_silhouette": num(cells[3]),
                "sil_ari": num(cells[4]),
                "best_alpha": num(best_pt[0]),
                "best_omega": num(best_pt[1]),
                "best_silhouette": num(cells[6]),
                "best_ari": num(cells[7]),
                "ari_gap": round(num(cells[7]) - num(cells[4]), 3),
            }
        )
        if abs(rows[-1]["ari_gap"] - num(cells[8])) > 0.0015:
            raise ValueError(f"{cells[0]}: gap column {cells[8]} does not match the ARIs")
    if len(rows) != 3:
        raise ValueError(f"expected 3 datasets in {PARADOX_TEX}, parsed {len(rows)}")
    return pd.DataFrame(rows)


def d1_from_grid(paradox: pd.DataFrame) -> pd.DataFrame:
    """Derivative baseline D1 where the committed grid table records it.

    D_w(1, 1) = D1 / max(D1), and PAM, silhouette and ARI are invariant to a global
    rescaling of the dissimilarity, so the (alpha=1, omega=1) corner of B's grid *is*
    the D1 baseline. The pipeline does not export D1 on real data; the paradox table
    only records it when the silhouette choice or the ARI maximum falls on that corner.
    """
    rows = []
    for r in paradox.itertuples():
        for pre in ("sil", "best"):
            if getattr(r, f"{pre}_alpha") == 1 and getattr(r, f"{pre}_omega") == 1:
                rows.append(
                    {
                        "dataset": r.dataset,
                        "method": "D1",
                        "Silhouette": getattr(r, f"{pre}_silhouette"),
                        "ARI": getattr(r, f"{pre}_ari"),
                    }
                )
                break
    return pd.DataFrame(rows, columns=["dataset", "method", "Silhouette", "ARI"])


def load_real() -> pd.DataFrame:
    frames = []
    for name, path in REAL.items():
        df = pd.read_csv(path)
        df["method"] = [
            next(v for k, v in REAL_KEYS.items() if s.startswith(k)) for s in df.Strategie
        ]
        df["dataset"] = name
        frames.append(df[["dataset", "method", "Silhouette", "ARI"]])
    frames.append(d1_from_grid(load_paradox()))
    return pd.concat(frames, ignore_index=True)


def simulated_summary(runs: pd.DataFrame) -> pd.DataFrame:
    g = runs.groupby(["scenario", "method"]).ari
    s = g.agg(["mean", "std", "count"]).reset_index()
    s["ci95"] = 1.96 * s["std"] / np.sqrt(s["count"])
    return s


def nselect_hits() -> dict[str, dict[str, float]]:
    out = {}
    for name, k in TRUE_K.items():
        df = pd.read_csv(NSELECT / f"nselectboot_{name}.csv")
        out[name] = {
            "true_k": k,
            "cells": len(df),
            "hits": int((df.k_opt == k).sum()),
            "median_k": float(df.k_opt.median()),
            "k_opt_counts": {
                str(i): int(n) for i, n in df.k_opt.value_counts().sort_index().items()
            },
        }
    sim = pd.read_csv(NSELECT_SIM)
    for sc, df in sim.groupby("scenario"):
        k = int(df.k_vrai.iloc[0])
        out[sc] = {"true_k": k, "cells": len(df), "hits": int((df.k_opt == k).sum())}
    for v in out.values():
        v["share"] = round(v["hits"] / v["cells"], 3)
    return out


def r3(x: float) -> float:
    return round(float(x), 3)


def summarize() -> dict:
    """Every number quoted in the README, computed from the result files."""
    runs = pd.read_csv(SIM)
    sim = simulated_summary(runs)
    paradox = load_paradox()
    real = load_real()
    wide = runs.pivot_table(index=["scenario", "seed"], columns="method", values="ari")
    c_vs_hfv = wide["C_DK_ancien"] - wide["DK_reconstruit"]
    b_corner = runs[runs.method == "B_silopt"].groupby("scenario")
    return {
        "simulated": {
            "runs": len(runs),
            "seeds_per_scenario": int(runs.groupby("scenario").seed.nunique().min()),
            "mean_ari": {
                sc: {m: r3(v) for m, v in d.set_index("method")["mean"].items()}
                for sc, d in sim.groupby("scenario")
            },
            "ci95": {
                sc: {m: r3(v) for m, v in d.set_index("method")["ci95"].items()}
                for sc, d in sim.groupby("scenario")
            },
            "winner": {
                sc: d.loc[d["mean"].idxmax(), "method"] for sc, d in sim.groupby("scenario")
            },
            "overall_mean_ari": {
                m: r3(v) for m, v in runs.groupby("method").ari.mean().sort_values().items()
            },
            "c_beats_hfv_share": {sc: r3((v > 0).mean()) for sc, v in c_vs_hfv.groupby(level=0)},
            "c_minus_hfv_mean": {sc: r3(v.mean()) for sc, v in c_vs_hfv.groupby(level=0)},
            "b_silhouette_corner_share": {
                sc: {
                    "derivative (1, 1)": r3(((d.alpha == 1) & (d.omega == 1)).mean()),
                    "level (0, 1)": r3(((d.alpha == 0) & (d.omega == 1)).mean()),
                }
                for sc, d in b_corner
            },
            "b_equals_d1_share": {
                sc: r3(((v.B_silopt - v.D1).abs() < 1e-12).mean())
                for sc, v in wide[["B_silopt", "D1"]].groupby(level=0)
            },
        },
        "real": {
            ds: {
                m: {"silhouette": r3(s), "ari": r3(a)}
                for m, s, a in zip(d.method, d.Silhouette, d.ARI, strict=True)
            }
            for ds, d in real.groupby("dataset", sort=False)
        },
        "paradox": paradox.set_index("dataset").to_dict(orient="index"),
        "nselectboot_true_k": nselect_hits(),
    }


def corner_name(alpha: float, omega: float) -> str:
    """Plain-word reading of a point of B's grid."""
    if omega == 0:
        return "covariates only"
    if omega == 1 and alpha == 0:
        return "curve level only"
    if omega == 1 and alpha == 1:
        return "derivative only"
    return f"mixed: α={alpha:g}, ω={omega:g}"


def fig_hero(paradox: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 3.9))
    order = paradox.iloc[::-1].reset_index(drop=True)
    y = np.arange(len(order))
    ax.hlines(y, order.sil_ari, order.best_ari, color=GRID, lw=6, zorder=1)
    ax.scatter(order.sil_ari, y, s=90, color=AMBER, zorder=3, edgecolor="white", lw=1.5)
    ax.scatter(order.best_ari, y, s=90, color=TEAL, zorder=3, edgecolor="white", lw=1.5)
    for yi, r in order.iterrows():
        ax.annotate(
            f"{r.sil_ari:.3f}\n{corner_name(r.sil_alpha, r.sil_omega)}",
            (r.sil_ari, yi),
            xytext=(0, -24),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color=SLATE,
        )
        ax.annotate(
            f"{r.best_ari:.3f}\n{corner_name(r.best_alpha, r.best_omega)}",
            (r.best_ari, yi),
            xytext=(0, -24),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color=SLATE,
        )
        ax.annotate(
            f"−{r.ari_gap:.3f} ARI",
            ((r.sil_ari + r.best_ari) / 2, yi),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )
    ax.set_yticks(y, order.dataset)
    ax.set_ylim(-0.8, len(order) - 0.4)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Adjusted Rand Index against the true labels (1 = perfect recovery)")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    ax.text(
        0.0,
        1.21,
        f"Silhouette tuning lands {paradox.ari_gap.min():.3f}–{paradox.ari_gap.max():.3f} "
        "ARI below the best grid point",
        transform=ax.transAxes,
        fontsize=12.5,
        fontweight="bold",
    )
    ax.text(
        0.0,
        1.04,
        "Strategy B: PAM on $D_w(α, ω)$, 21 × 21 grid, k = true number of classes\n"
        "ω = weight on curves vs covariates, α = weight on derivative vs curve level",
        transform=ax.transAxes,
        fontsize=9,
        color=SLATE,
    )
    top = order.iloc[-1]
    for x, label, color, ha in (
        (top.sil_ari, "chosen by silhouette\n(unsupervised)", AMBER, "right"),
        (top.best_ari, "best point on the grid\n(oracle: needs the labels)", TEAL, "left"),
    ):
        ax.annotate(
            label,
            (x, len(order) - 1),
            xytext=(-8 if ha == "right" else 8, 8),
            textcoords="offset points",
            ha=ha,
            fontsize=8.5,
            color=color,
            fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_simulated(summary: pd.DataFrame, path: Path) -> None:
    scen = {
        "S1": "S1 · both blocks informative",
        "S2": "S2 · covariate signal halved",
        "S3": "S3 · curve signal halved",
        "S4": "S4 · everything halved",
    }
    fig, axes = plt.subplots(1, 4, figsize=(12, 4.2), sharey=True)
    keys = list(METHODS)[::-1]
    y = np.arange(len(keys))
    for ax, (sc, title) in zip(axes, scen.items(), strict=True):
        d = summary[summary.scenario == sc].set_index("method").loc[keys]
        best = d["mean"].idxmax()
        colors = [TEAL if m == best else (AMBER if m == "B_silopt" else SLATE) for m in keys]
        ax.hlines(y, d["mean"] - d.ci95, d["mean"] + d.ci95, color=colors, lw=2)
        ax.scatter(d["mean"], y, color=colors, s=36, zorder=3)
        ax.annotate(
            f"{d.loc[best, 'mean']:.2f}",
            (d.loc[best, "mean"], keys.index(best)),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            fontsize=8.5,
            color=INK,
            fontweight="bold",
        )
        ax.set_title(title, fontsize=9.5, loc="left")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
        ax.grid(axis="y", visible=False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(y, [METHODS[k] for k in keys])
    fig.supxlabel("Mean ARI over 50 seeds (bars: 95% CI), n = 300, k = 3", fontsize=9.5, color=INK)
    fig.suptitle(
        "No method wins every scenario: the kernel product leads in S1–S2, "
        "then the ranking reshuffles",
        x=0.01,
        ha="left",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def write_figures() -> dict:
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    summary = summarize()
    fig_hero(load_paradox(), OUT / "hero_silhouette_gap.png")
    fig_simulated(simulated_summary(pd.read_csv(SIM)), OUT / "simulated_benchmark.png")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return summary


def headline_strings(s: dict) -> list[str]:
    """Headline numbers both READMEs must quote (3 decimals)."""
    out = []
    for r in s["paradox"].values():
        out += [f"{r['sil_ari']:.3f}", f"{r['best_ari']:.3f}"]
    for ds in s["real"].values():
        out.append(f"{max(v['ari'] for v in ds.values()):.3f}")
    for sc, m in s["simulated"]["winner"].items():
        out.append(f"{s['simulated']['mean_ari'][sc][m]:.3f}")
    out.append(f"{max(s['simulated']['overall_mean_ari'].values()):.3f}")
    return out


def pct(x: float) -> str:
    return f"{round(100 * x)} %"


def detail_strings(s: dict) -> list[str]:
    """Every other number of README.md: table cells, shares, counts."""
    sim = s["simulated"]
    out = [
        f"{v['ari']:.3f} ({v['silhouette']:.3f})" for ds in s["real"].values() for v in ds.values()
    ]
    nb = s["nselectboot_true_k"]
    for name in ("canadian", "growth", "tecator"):
        out.append(f"{nb[name]['hits']} / {nb[name]['cells']}")
        out.append(f"{nb[name]['k_opt_counts'].get('2', 0)} / {nb[name]['cells']}")
    sims = [nb[sc] for sc in ("S1", "S2", "S3", "S4")]
    out.append(" / ".join(str(v["hits"]) for v in sims) + f" of {sims[0]['cells']}")
    share = sim["c_beats_hfv_share"].values()
    gap = sim["c_minus_hfv_mean"].values()
    out += [
        f"{round(100 * min(share))} % to {pct(max(share))}",
        f"{min(gap):.3f} to {max(gap):.3f}",
    ]
    gaps = [r["ari_gap"] for r in s["paradox"].values()]
    hfv = [abs(d["C_DK_ancien"]["ari"] - d["DK_reconstruit"]["ari"]) for d in s["real"].values()]
    out += [f"{min(gaps):.3f} to {max(gaps):.3f}", f"within {max(hfv):.3f}"]
    corner = sim["b_silhouette_corner_share"]
    out += [
        pct(min(corner[sc]["level (0, 1)"] for sc in ("S3", "S4"))),
        f"{sim['mean_ari']['S1']['B_silopt']:.3f}",
        f"{sim['mean_ari']['S3']['B_silopt']:.3f}",
    ]
    return out


def flat(path: Path) -> str:
    """README text with bold markers and line breaks removed, for substring checks."""
    return " ".join(path.read_text().replace("**", "").split())


def to_fr(v: str) -> str:
    return v.replace(".", ",")


def check() -> int:
    committed = json.loads((OUT / "summary.json").read_text())
    fresh = json.loads(json.dumps(summarize(), ensure_ascii=False))
    errors = []
    if committed != fresh:
        errors.append("docs/figures/summary.json is stale: run `make figures`")
    readme, readme_fr = (flat(ROOT / doc) for doc in ("README.md", "README.fr.md"))
    errors += [
        f"README.md does not quote {v}"
        for v in headline_strings(fresh) + detail_strings(fresh)
        if v not in readme
    ]
    errors += [
        f"README.fr.md does not quote {to_fr(v)}"
        for v in headline_strings(fresh)
        if to_fr(v) not in readme_fr
    ]
    for doc in ("README.md", "README.fr.md"):
        text = (ROOT / doc).read_text()
        for target in re.findall(r"\]\(([^)#\s]+)\)", text):
            if not target.startswith("http") and not (ROOT / target).exists():
                errors.append(f"{doc}: broken link {target}")
    for e in errors:
        print(e, file=sys.stderr)
    print("ok" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--check", action="store_true", help="verify instead of writing")
    if p.parse_args().check:
        return check()
    s = write_figures()
    print(json.dumps({"winner": s["simulated"]["winner"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
