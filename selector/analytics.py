"""Compatibility statistics computed with Pandas.

Aggregates the stored :class:`~selector.models.MatchResult` rows into the three
figures shown on the statistics page: the average compatibility score, the top
five plants, and the distribution of results by care difficulty.
"""

from __future__ import annotations

import pandas as pd

from catalog.models import Plant

from .models import MatchResult, RoomCondition

# Natural ordering for the care-difficulty axis.
_DIFFICULTY_ORDER = list(Plant.CareDifficulty.values)
_DIFFICULTY_LABELS = dict(Plant.CareDifficulty.choices)


def build_statistics() -> dict:
    """Return a JSON-friendly summary of all recorded matches."""
    rows = list(
        MatchResult.objects.values(
            "plant__name", "plant__care_difficulty", "match_score"
        )
    )
    selections = RoomCondition.objects.count()
    frame = pd.DataFrame.from_records(rows)

    if frame.empty:
        return {"has_data": False, "total_selections": selections}

    average_score = round(float(frame["match_score"].mean()), 1)

    # Top 5 plants by average compatibility across every selection.
    top = (
        frame.groupby("plant__name")["match_score"]
        .mean()
        .round(1)
        .sort_values(ascending=False)
        .head(5)
    )
    top_plants = [
        {"name": name, "avg_score": float(score)} for name, score in top.items()
    ]

    # Count and average score grouped by care difficulty.
    grouped = frame.groupby("plant__care_difficulty")["match_score"].agg(
        ["count", "mean"]
    )
    difficulty = [
        {
            "code": code,
            "label": _DIFFICULTY_LABELS.get(code, code),
            "count": int(stats["count"]),
            "avg_score": round(float(stats["mean"]), 1),
        }
        for code, stats in grouped.iterrows()
    ]
    difficulty.sort(key=lambda item: _DIFFICULTY_ORDER.index(item["code"]))

    return {
        "has_data": True,
        "total_selections": selections,
        "total_matches": int(len(frame)),
        "average_score": average_score,
        "top_plants": top_plants,
        "difficulty": difficulty,
    }
