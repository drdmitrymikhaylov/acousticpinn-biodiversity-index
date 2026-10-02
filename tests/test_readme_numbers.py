"""Pin the README section "The two repairs, measured" to the results files.

Needs only the standard library and the two JSON files in results/.

    python -m pytest tests            (or: python tests/test_readme_numbers.py)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REP = json.loads((ROOT / "results" / "stability_repairs.json").read_text())
LOSS = json.loads((ROOT / "results" / "species_loss_levels.json").read_text())
README = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())

V = ("per_species", "weighted", "pooled")
L, Q, C, D = REP["species_loss"], REP["going_quiet"], REP["contamination"], REP["dominance"]


def f3(x):
    return "%.3f" % x


def row(label, cells):
    return "| %s | %s |" % (label, " | ".join(cells))


def test_published_term_is_the_one_already_on_the_page():
    """The per-species column must be the species-order table published in September."""
    assert REP["communities"] == 3000 and REP["reps_per_level"] == 40
    for lev in LOSS["levels"]:
        r = L["levels"][str(lev["species_remaining"])]
        assert abs(r["abi_per_species"] - lev["abi_geom"]) < 5e-5
        assert abs(r["stability_per_species"] - lev["stability"]) < 5e-5
        assert r["above_intact_per_species"] == lev["reps_above_intact"]
    assert L["species_lost_before_mean_falls_per_species"] == \
        LOSS["summary"]["species_lost_before_index_falls"] == 8


def test_table_rows():
    lv = L["levels"]
    rows = [
        row("species lost before the mean index falls",
            [str(L["species_lost_before_mean_falls_" + v]) for v in V]),
        row("communities scored above intact with 3 species gone",
            ["%d / 40" % lv["21"]["above_intact_" + v] for v in V]),
        row("ABI, 24 species to 3",
            ["%s to %s" % (f3(lv["24"]["abi_" + v]), f3(lv["3"]["abi_" + v])) for v in V]),
        row("stability term, 24 species to 3",
            ["%s to %s" % (f3(lv["24"]["stability_" + v]), f3(lv["3"]["stability_" + v])) for v in V]),
        row("going quiet, steady to most clumped",
            ["%s to %s" % (f3(Q["abi_steady_" + v]), f3(Q["abi_clumped_" + v])) for v in V]),
        row("going quiet, half-way (clumping 0.5)",
            [f3(Q["curve"][v][Q["x"].index(0.5)]) for v in V]),
        row("noise sources for the 12-species site to outscore the forest",
            [str(C["sources_to_outscore_forest_" + v]) for v in V]),
        row("one species from 5 % to 95 % of detections",
            ["%s to %s" % (f3(D["abi_first_" + v]), f3(D["abi_last_" + v])) for v in V]),
    ]
    for r in rows:
        assert r in README, r
    top = "| | same step with stability weighted by abundance (measured, not adopted) | %s | %s |" % (
        f3(lv["24"]["abi_weighted"]), f3(lv["21"]["abi_weighted"]))
    assert top in README, top


def test_both_repairs_close_the_blind_spot():
    assert [L["species_lost_before_mean_falls_" + v] for v in V] == [8, 1, 1]
    assert [L["monotone_fall_" + v] for v in V] == [False, True, True]
    assert len(L["levels"]) == 22          # 24 down to 3 species: 21 steps
    assert [L["levels"]["21"]["above_intact_" + v] for v in V] == [31, 0, 0]
    assert [L["levels"]["23"]["above_intact_" + v] for v in V] == [26, 2, 0]
    for v in ("weighted", "pooled"):
        assert all(r["above_intact_" + v] == 0 for k, r in L["levels"].items() if int(k) <= 22)
    for text in ("falls from the first species lost and keeps falling at each of the 21 steps",
                 "2 of 40 still do under the weighted term and none under the pooled one"):
        assert text in README, text


def test_pooled_term_barely_sees_a_community_going_quiet():
    i = Q["x"].index(0.5)
    lost = {v: 1 - Q["curve"][v][i] / Q["curve"][v][0] for v in V}
    assert "%.0f" % (100 * lost["per_species"]) == "97"
    assert "%.0f" % (100 * lost["pooled"]) == "9"
    assert "%.0f" % (100 * Q["abi_clumped_pooled"] / Q["abi_steady_pooled"]) == "36"
    assert Q["first_x_below_half_per_species"] == 0.7
    assert Q["first_x_below_half_weighted"] == 0.5
    assert Q["abi_clumped_weighted"] < 1e-3 and Q["abi_clumped_per_species"] < 1e-3
    for text in ("has lost 97 % of its value and the pooled one 9 %",
                 "0.330, 36 % of its steady value",
                 "clumping 0.5 where the published term crosses at 0.7"):
        assert text in README, text


def test_shannon_cannot_see_it_and_the_direction_is_right():
    assert f3(Q["shannon_steady"]) == "2.686" and f3(Q["shannon_clumped"]) == "2.688"
    assert "| community going quiet, same species and totals | Shannon | 2.686 | 2.688 |" in README
    assert "Shannon moves from 2.686 to 2.688" in README


def test_neither_repair_protects_against_contamination():
    assert [C["sources_to_outscore_forest_" + v] for v in V] == [7, 11, 10]
    share = ["%.0f" % (100 * C["clean_site_" + v] / C["forest_" + v]) for v in V]
    assert share == ["79", "78", "77"]
    assert "(0.851 against 0.837, and 0.922 against 0.920)" in README
    assert f3(C["abi_at_that_point_weighted"]) == "0.851" and f3(C["forest_weighted"]) == "0.837"
    assert f3(C["abi_at_that_point_pooled"]) == "0.922" and f3(C["forest_pooled"]) == "0.920"
    assert "79 % of the forest's score under the published term, 78 % and 77 % under the repairs" in README


def test_dominance_collapse_is_lost():
    assert "%.2f" % D["evenness_last"] == "0.11"
    assert D["stability_last_per_species"] == 0.0
    assert "%.2f" % D["stability_last_weighted"] == "0.86"
    assert "%.0f" % (100 * D["abi_last_weighted"] / D["abi_first_weighted"]) == "52"
    assert "%.0f" % (100 * D["abi_last_pooled"] / D["abi_first_pooled"]) == "48"
    for text in ("evenness alone (J = 0.11)", "52 % and 48 % of the score"):
        assert text in README, text


def test_the_clumping_axis_is_not_even():
    c = Q["curve"]["per_species"]
    assert f3(c[0]) == "0.729" and f3(c[1]) == "0.507" and abs(Q["x"][1] - 0.95) < 1e-9
    assert "%.0f" % (100 * (c[0] - c[1]) / (c[0] - c[-1])) == "30"
    assert len(Q["x"]) == 20
    assert "30 % of the published index's fall (0.729 to 0.507) happens in the first of 19 steps" in README


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok  ", fn.__name__)
    print(f"{len(fns)} checks passed")
