"""Ten Gods and element analysis."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping

from fortune_telling_core.traditions.four_pillars.config import Element
from fortune_telling_core.traditions.four_pillars.stems_branches import STEMS, branch, stem

_GENERATES = {
    Element.WOOD: Element.FIRE,
    Element.FIRE: Element.EARTH,
    Element.EARTH: Element.METAL,
    Element.METAL: Element.WATER,
    Element.WATER: Element.WOOD,
}
_CONTROLS = {
    Element.WOOD: Element.EARTH,
    Element.EARTH: Element.WATER,
    Element.WATER: Element.FIRE,
    Element.FIRE: Element.METAL,
    Element.METAL: Element.WOOD,
}


def ten_god(day_stem_index: int, other_stem_index: int) -> str:
    day = stem(day_stem_index)
    other = stem(other_stem_index)
    same_polarity = day.polarity == other.polarity
    if other.element == day.element:
        return "friend" if same_polarity else "rob_wealth"
    if _GENERATES[day.element] == other.element:
        return "eating_god" if same_polarity else "hurting_officer"
    if _GENERATES[other.element] == day.element:
        return "indirect_resource" if same_polarity else "direct_resource"
    if _CONTROLS[day.element] == other.element:
        return "indirect_wealth" if same_polarity else "direct_wealth"
    return "seven_killings" if same_polarity else "direct_officer"


def hidden_ten_gods(day_stem_index: int, branch_index: int) -> tuple[str, ...]:
    return tuple(ten_god(day_stem_index, hidden) for hidden in branch(branch_index).hidden_stems)


def element_distribution(
    stem_indices: tuple[int, ...], branch_indices: tuple[int, ...]
) -> Mapping[str, int]:
    counts: Counter[str] = Counter()
    for index in stem_indices:
        counts[stem(index).element.value] += 1
    for index in branch_indices:
        counts[branch(index).element.value] += 1
        for hidden in branch(index).hidden_stems:
            counts[stem(hidden).element.value] += 1
    return dict(counts)


def day_master_strength(day_stem_index: int, branch_indices: tuple[int, ...]) -> str:
    day_element = stem(day_stem_index).element
    support = 0
    for index in branch_indices:
        branch_element = branch(index).element
        if branch_element == day_element or _GENERATES[branch_element] == day_element:
            support += 1
    if support >= 3:
        return "strong"
    if support == 2:
        return "balanced"
    return "weak"


TEN_GOD_LABELS = {
    "friend": "Friend",
    "rob_wealth": "Rob Wealth",
    "eating_god": "Eating God",
    "hurting_officer": "Hurting Officer",
    "indirect_wealth": "Indirect Wealth",
    "direct_wealth": "Direct Wealth",
    "seven_killings": "Seven Killings",
    "direct_officer": "Direct Officer",
    "indirect_resource": "Indirect Resource",
    "direct_resource": "Direct Resource",
}

__all__ = [
    "STEMS",
    "TEN_GOD_LABELS",
    "day_master_strength",
    "element_distribution",
    "hidden_ten_gods",
    "ten_god",
]
