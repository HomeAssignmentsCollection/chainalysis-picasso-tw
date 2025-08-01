"""
Test suite for the count_assignments module.

This module contains comprehensive tests for the Picasso Tower assignment
counting functionality, covering various hint types and edge cases.
"""

import math

from count_assignments import (
    AbsoluteHint, Animal, Color, Floor, FloorAssignment,
    NeighborHint, RelativeHint, count_assignments
)


def test_check_is_satisfied_absolute_hint():
    """Test that absolute hints correctly validate floor assignments."""
    # Test positive cases - hints should be satisfied
    assert AbsoluteHint(Animal.Bird, Floor.First).check_if_satisfied([
        FloorAssignment(floor=Floor.First, animal=Animal.Bird,
                        color=Color.Blue)
    ])
    assert AbsoluteHint(Color.Blue, Floor.Second).check_if_satisfied([
        FloorAssignment(floor=Floor.Second, animal=Animal.Bird,
                        color=Color.Blue)
    ])
    assert AbsoluteHint(Animal.Bird, Color.Blue).check_if_satisfied([
        FloorAssignment(floor=Floor.Third, animal=Animal.Bird,
                        color=Color.Blue)
    ])

    # Test negative cases - hints should not be satisfied
    assert not AbsoluteHint(Color.Blue, Floor.Second).check_if_satisfied([
        FloorAssignment(floor=Floor.First, animal=Animal.Bird,
                        color=Color.Blue)
    ])
    assert not AbsoluteHint(Floor.First, Animal.Bird).check_if_satisfied([
        FloorAssignment(floor=Floor.Third, animal=Animal.Bird,
                        color=Color.Blue)
    ])


def test_get_possible_floor_assignments_absolute_hint_impossible_hint():
    """Test that impossible absolute hints return empty assignment lists."""
    hint = AbsoluteHint(Animal.Bird, Floor.First)
    empty_floors = [Floor.Second, Floor.Third]
    possible_animals = [Animal.Chicken, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]

    possible_assignments = hint.get_possible_floor_assignments(
        empty_floors=empty_floors,
        all_animal_options=possible_animals,
        all_color_options=possible_colors,
        floor_assignments=[]
    )
    assert len(possible_assignments) == 0


def test_get_possible_floor_assignments_absolute_hint_possible_hint():
    """Test that possible absolute hints return valid assignment lists."""
    hint = AbsoluteHint(Animal.Bird, Floor.Second)
    empty_floors = [Floor.Second, Floor.Third]
    possible_animals = [Animal.Bird, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]

    possible_assignments = hint.get_possible_floor_assignments(
        empty_floors=empty_floors,
        all_animal_options=possible_animals,
        all_color_options=possible_colors,
        floor_assignments=[]
    )
    assert len(possible_assignments) == 2


def test_count_assignments_no_hints():
    """Test that empty hint list returns all possible assignments."""
    total_assignments = count_assignments([])
    expected_total = math.factorial(5) * math.factorial(5)  # 5! * 5! = 14400
    assert total_assignments == expected_total


def test_count_assignments_absolute_hints_only():
    """Test counting with only absolute hints."""
    # Test with one absolute hint
    one_absolute_hint = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
    ]

    # Test with contradicting absolute hints
    contradicting_absolute_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Bird, Floor.First),
    ]

    expected_with_one_hint = math.factorial(5) * math.factorial(4)
    assert count_assignments(one_absolute_hint) == expected_with_one_hint
    assert count_assignments(contradicting_absolute_hints) == 0


def test_redundant_hints():
    """Test handling of redundant and overlapping hints."""
    # Complete assignment specification
    complete_assignment_hints = [
        # Expected final assignment:
        # Floor |   Animal    | Color
        #   5   | Grasshopper | Green
        #   4   |    Frog     | Yellow
        #   3   |    Bird     | Red
        #   2   |   Chicken   | Blue
        #   1   |   Rabbit    | Orange

        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Animal.Bird),
        AbsoluteHint(Floor.Fourth, Animal.Frog),
        AbsoluteHint(Floor.Fifth, Animal.Grasshopper),
        AbsoluteHint(Floor.Fifth, Color.Green),
        AbsoluteHint(Animal.Chicken, Color.Blue),
        AbsoluteHint(Animal.Rabbit, Color.Orange),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Floor.Fourth, Color.Yellow),
    ]

    # Redundant absolute hints (same information twice)
    redundant_absolute_hints = [
        AbsoluteHint(Floor.Fourth, Color.Yellow),
        AbsoluteHint(Color.Yellow, Floor.Fourth),
    ]

    # Relative hints with distance 0 (equivalent to absolute hints)
    relative_hints_as_absolute = [
        RelativeHint(Animal.Rabbit, Floor.First, 0),
        RelativeHint(Animal.Chicken, Floor.Second, 0),
        RelativeHint(Floor.Third, Animal.Bird, 0),
        RelativeHint(Floor.Fourth, Animal.Frog, 0),
        RelativeHint(Floor.Fifth, Animal.Grasshopper, 0),
        RelativeHint(Floor.Fifth, Color.Green, 0),
        RelativeHint(Animal.Chicken, Color.Blue, 0),
        RelativeHint(Animal.Rabbit, Color.Orange, 0),
        RelativeHint(Floor.Third, Color.Red, 0),
        RelativeHint(Floor.Fourth, Color.Yellow, 0),
    ]

    # Redundant relative hints (same relationship expressed differently)
    redundant_relative_hints = [
        RelativeHint(Animal.Rabbit, Floor.First, 2),
        RelativeHint(Floor.First, Animal.Rabbit, -2),
    ]

    # Redundant neighbor hints (same relationship expressed differently)
    redundant_neighbor_hints = [
        NeighborHint(Animal.Bird, Color.Blue),
        NeighborHint(Color.Blue, Animal.Bird)
    ]

    # Test assertions
    assert count_assignments(complete_assignment_hints) == 1
    assert count_assignments(redundant_absolute_hints) == (
        math.factorial(5) * math.factorial(4)
    )

    assert count_assignments(relative_hints_as_absolute) == 1
    assert count_assignments(redundant_relative_hints) == (
        math.factorial(5) * math.factorial(4)
    )

    assert count_assignments(redundant_neighbor_hints) == 4608


def test_duplicated_hints():
    """Test handling of duplicated hints."""
    duplicated_absolute_hint = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Rabbit, Floor.First)
    ]

    duplicated_neighbor_hints = [
        NeighborHint(Animal.Chicken, Color.Blue),
        NeighborHint(Animal.Chicken, Color.Blue)
    ]

    expected_with_one_absolute = math.factorial(5) * math.factorial(4)
    expected_with_one_neighbor = 4608  # Actual result for duplicated neighbor hints

    assert count_assignments(duplicated_absolute_hint) == (
        expected_with_one_absolute
    )
    assert count_assignments(duplicated_neighbor_hints) == (
        expected_with_one_neighbor
    )


def test_relative_hints():
    """Test counting with relative hints."""
    single_relative_hint = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]

    # Relative hints with distance 0 should behave like absolute hints
    absolute_hints_in_disguise = [
        RelativeHint(Animal.Rabbit, Floor.First, 0),
    ]

    assert count_assignments(single_relative_hint) == 1728
    assert count_assignments(absolute_hints_in_disguise) == (
        math.factorial(5) * math.factorial(4)
    )


def test_neighbor_hints():
    """Test counting with neighbor hints (derived from relative hints)."""
    single_neighbor_hint = [
        NeighborHint(Animal.Rabbit, Color.Green)
    ]
    assert count_assignments(single_neighbor_hint) == 4608


def test_assignment_examples():
    """Test the specific examples provided in the assignment document."""
    # Example 1 from assignment
    hints_example_1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Orange),
        NeighborHint(Color.Yellow, Color.Green),
    ]

    # Example 2 from assignment
    hints_example_2 = [
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Floor.First, Color.Green),
        AbsoluteHint(Animal.Frog, Color.Yellow),
        NeighborHint(Animal.Frog, Animal.Grasshopper),
        NeighborHint(Color.Red, Color.Orange),
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    ]

    assert count_assignments(hints_example_1) == 2
    assert count_assignments(hints_example_2) == 4


def run_all_tests():
    """Run all test functions."""
    test_check_is_satisfied_absolute_hint()
    test_get_possible_floor_assignments_absolute_hint_impossible_hint()
    test_get_possible_floor_assignments_absolute_hint_possible_hint()
    test_count_assignments_no_hints()
    test_count_assignments_absolute_hints_only()
    test_relative_hints()
    test_neighbor_hints()
    test_assignment_examples()
    test_redundant_hints()
    test_duplicated_hints()
    print('Success! All tests passed.')


if __name__ == '__main__':
    run_all_tests()
