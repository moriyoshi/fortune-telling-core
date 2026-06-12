from fortune_telling_core import RandomRng, SequenceRng
from fortune_telling_core.traditions.geomancy.shield import cast_shield

# Per Mother row, float < 0.5 -> single point (1), >= 0.5 -> double (0).
_ALL_SINGLE = [0.0] * 16
_ALL_DOUBLE = [0.9] * 16


def test_judge_always_has_even_points() -> None:
    # Classical theorem: the Judge is always an even figure.
    for seed in range(200):
        shield = cast_shield(RandomRng(seed))
        assert shield.judge.points % 2 == 0


def test_all_single_mothers_give_via_and_populus_judge() -> None:
    shield = cast_shield(SequenceRng(floats=_ALL_SINGLE))

    assert all(mother.slug == "via" for mother in shield.mothers)
    # Via + Via = Populus, propagating down to the Judge.
    assert shield.judge.slug == "populus"


def test_all_double_mothers_give_populus_everywhere() -> None:
    shield = cast_shield(SequenceRng(floats=_ALL_DOUBLE))

    figures = (*shield.mothers, *shield.daughters, *shield.nieces, shield.judge)
    assert all(figure.slug == "populus" for figure in figures)


def test_daughters_are_the_transpose_of_mothers() -> None:
    floats = [
        0.0, 0.0, 0.9, 0.9,  # Mother 1 rows: 1,1,0,0
        0.9, 0.9, 0.9, 0.9,  # Mother 2 rows: 0,0,0,0
        0.0, 0.9, 0.9, 0.9,  # Mother 3 rows: 1,0,0,0
        0.9, 0.9, 0.9, 0.0,  # Mother 4 rows: 0,0,0,1
    ]  # fmt: skip
    shield = cast_shield(SequenceRng(floats=floats))

    mothers = [m.rows for m in shield.mothers]
    for j, daughter in enumerate(shield.daughters):
        assert daughter.rows == tuple(mothers[i][j] for i in range(4))
