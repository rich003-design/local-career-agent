"""
Tools available to the local Career Agent.
"""

import json
from datetime import date
from pathlib import Path
from typing import Any

from config import NOTES_FILE


def calculate_experience(
    start_year: int,
) -> dict[str, int]:
    """
    Calculate approximate professional experience.

    Args:
        start_year:
            The year when the person's professional career started.

    Returns:
        The start year, current year, and years of experience.
    """

    current_year = date.today().year

    if start_year < 1900:
        raise ValueError(
            "start_year must be 1900 or later."
        )

    if start_year > current_year:
        raise ValueError(
            "start_year cannot be in the future."
        )

    years = (
        current_year - start_year
    )

    return {
        "start_year": start_year,
        "current_year": current_year,
        "years_of_experience": years,
    }


def skills_gap(
    current_skills: list[str],
    target_skills: list[str],
) -> dict[str, list[str]]:
    """
    Compare existing skills with target skills.

    Args:
        current_skills:
            Skills currently known by the user.

        target_skills:
            Skills needed for the user's target role.

    Returns:
        Matching and missing skills.
    """

    current = {
        skill.strip().lower()
        for skill in current_skills
        if skill.strip()
    }

    target = {
        skill.strip().lower()
        for skill in target_skills
        if skill.strip()
    }

    matching = sorted(
        current & target
    )

    missing = sorted(
        target - current
    )

    return {
        "matching_skills": matching,
        "missing_skills": missing,
    }


def create_learning_plan(
    skills: list[str],
    weeks: int = 8,
) -> dict[str, Any]:
    """
    Create a simple learning plan for a list of skills.

    Args:
        skills:
            Skills the user wants to learn.

        weeks:
            Number of weeks available.

    Returns:
        A structured weekly learning plan.
    """

    cleaned_skills = [
        skill.strip()
        for skill in skills
        if skill.strip()
    ]

    if not cleaned_skills:
        raise ValueError(
            "At least one skill is required."
        )

    if weeks < 1:
        raise ValueError(
            "weeks must be at least 1."
        )

    plan: list[dict[str, Any]] = []

    for week in range(
        1,
        weeks + 1,
    ):
        skill = cleaned_skills[
            (week - 1)
            % len(cleaned_skills)
        ]

        plan.append(
            {
                "week": week,
                "focus": skill,
                "activities": [
                    f"Study core concepts of {skill}",
                    f"Complete one hands-on exercise using {skill}",
                    f"Write short notes explaining {skill}",
                ],
            }
        )

    return {
        "duration_weeks": weeks,
        "skills": cleaned_skills,
        "plan": plan,
    }


def save_note(
    title: str,
    content: str,
) -> dict[str, str]:
    """
    Save a note to the agent's local notes file.

    Args:
        title:
            Short note title.

        content:
            Note contents.

    Returns:
        Confirmation of the saved note.
    """

    path = Path(
        NOTES_FILE
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    notes = []

    if path.exists():
        try:
            notes = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError:
            notes = []

    notes.append(
        {
            "title": title,
            "content": content,
        }
    )

    path.write_text(
        json.dumps(
            notes,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "status": "saved",
        "title": title,
    }


def read_notes() -> list[dict[str, str]]:
    """
    Read previously saved local notes.

    Returns:
        All locally stored notes.
    """

    path = Path(
        NOTES_FILE
    )

    if not path.exists():
        return []

    try:
        notes = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        return []

    return notes
