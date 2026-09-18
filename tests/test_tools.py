from datetime import date

from tools import (
    calculate_experience,
    create_learning_plan,
    skills_gap,
)


def test_calculate_experience():
    result = (
        calculate_experience(
            start_year=2020
        )
    )

    assert (
        result[
            "years_of_experience"
        ]
        ==
        date.today().year
        - 2020
    )


def test_skills_gap():
    result = skills_gap(
        current_skills=[
            "Python",
            "Docker",
        ],
        target_skills=[
            "Python",
            "Docker",
            "Kubernetes",
        ],
    )

    assert (
        result[
            "matching_skills"
        ]
        ==
        [
            "docker",
            "python",
        ]
    )

    assert (
        result[
            "missing_skills"
        ]
        ==
        [
            "kubernetes"
        ]
    )


def test_learning_plan():
    result = create_learning_plan(
        skills=[
            "Python",
            "MLflow",
        ],
        weeks=4,
    )

    assert (
        result[
            "duration_weeks"
        ]
        == 4
    )

    assert len(
        result["plan"]
    ) == 4
