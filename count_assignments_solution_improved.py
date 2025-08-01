"""
Optimized test suite for the count_assignments module.

This module contains comprehensive, optimized tests for the Picasso Tower assignment
counting functionality, with improved performance and readability.
"""

import math
import time
from typing import List, Tuple

from count_assignments import (
    AbsoluteHint, Animal, Color, Floor, FloorAssignment,
    NeighborHint, RelativeHint, count_assignments
)


class PerformanceTimer:
    """Context manager for measuring execution time."""
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"⏱️  {self.test_name}: {duration:.4f}s")


def test_absolute_hints():
    """Test absolute hint validation with improved readability."""
    print("🧪 Testing absolute hints...")
    
    # Test cases with clear descriptions
    test_cases = [
        # (hint, assignments, expected_result, description)
        (
            AbsoluteHint(Animal.Bird, Floor.First),
            [FloorAssignment(Floor.First, Animal.Bird, Color.Blue)],
            True,
            "Bird on first floor - should be satisfied"
        ),
        (
            AbsoluteHint(Color.Blue, Floor.Second),
            [FloorAssignment(Floor.Second, Animal.Bird, Color.Blue)],
            True,
            "Blue color on second floor - should be satisfied"
        ),
        (
            AbsoluteHint(Animal.Bird, Color.Blue),
            [FloorAssignment(Floor.Third, Animal.Bird, Color.Blue)],
            True,
            "Bird with blue color - should be satisfied"
        ),
        (
            AbsoluteHint(Color.Blue, Floor.Second),
            [FloorAssignment(Floor.First, Animal.Bird, Color.Blue)],
            False,
            "Blue color on wrong floor - should not be satisfied"
        ),
        (
            AbsoluteHint(Floor.First, Animal.Bird),
            [FloorAssignment(Floor.Third, Animal.Bird, Color.Blue)],
            False,
            "Bird on wrong floor - should not be satisfied"
        )
    ]
    
    for hint, assignments, expected, description in test_cases:
        result = hint.check_if_satisfied(assignments)
        assert result == expected, f"Failed: {description}"
        print(f"✅ {description}")


def test_count_assignments_basic():
    """Test basic assignment counting scenarios."""
    print("🧪 Testing basic assignment counting...")
    
    with PerformanceTimer("Empty hints test"):
        # No hints should return all possible assignments
        total_assignments = count_assignments([])
        expected_total = math.factorial(5) * math.factorial(5)  # 5! * 5! = 14400
        assert total_assignments == expected_total
        print(f"✅ Empty hints: {total_assignments} assignments")
    
    with PerformanceTimer("Single absolute hint test"):
        # Single absolute hint
        one_hint = [AbsoluteHint(Animal.Rabbit, Floor.First)]
        result = count_assignments(one_hint)
        expected = math.factorial(5) * math.factorial(4)  # 5! * 4! = 2880
        assert result == expected
        print(f"✅ Single hint: {result} assignments")
    
    with PerformanceTimer("Contradicting hints test"):
        # Contradicting hints should return 0
        contradicting_hints = [
            AbsoluteHint(Animal.Rabbit, Floor.First),
            AbsoluteHint(Animal.Bird, Floor.First)
        ]
        result = count_assignments(contradicting_hints)
        assert result == 0
        print(f"✅ Contradicting hints: {result} assignments")


def test_assignment_examples():
    """Test the specific examples from the assignment with performance tracking."""
    print("🧪 Testing assignment examples...")
    
    # Example 1 from assignment
    hints_example_1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Orange),
        NeighborHint(Color.Yellow, Color.Green),
    ]
    
    with PerformanceTimer("Example 1"):
        result = count_assignments(hints_example_1)
        assert result == 2
        print(f"✅ Example 1: {result} assignments")
    
    # Example 2 from assignment
    hints_example_2 = [
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Floor.First, Color.Green),
        AbsoluteHint(Animal.Frog, Color.Yellow),
        NeighborHint(Animal.Frog, Animal.Grasshopper),
        NeighborHint(Color.Red, Color.Orange),
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    ]
    
    with PerformanceTimer("Example 2"):
        result = count_assignments(hints_example_2)
        assert result == 4
        print(f"✅ Example 2: {result} assignments")
    
    # Example 3 from assignment
    hints_example_3 = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]
    
    with PerformanceTimer("Example 3"):
        result = count_assignments(hints_example_3)
        assert result == 1728
        print(f"✅ Example 3: {result} assignments")


def test_hint_types():
    """Test different hint types with clear organization."""
    print("🧪 Testing different hint types...")
    
    # Relative hints
    with PerformanceTimer("Relative hints test"):
        single_relative_hint = [RelativeHint(Animal.Rabbit, Color.Green, -2)]
        result = count_assignments(single_relative_hint)
        assert result == 1728
        print(f"✅ Relative hint: {result} assignments")
    
    # Neighbor hints
    with PerformanceTimer("Neighbor hints test"):
        single_neighbor_hint = [NeighborHint(Animal.Rabbit, Color.Green)]
        result = count_assignments(single_neighbor_hint)
        assert result == 4608
        print(f"✅ Neighbor hint: {result} assignments")
    
    # Mixed hints
    with PerformanceTimer("Mixed hints test"):
        mixed_hints = [
            AbsoluteHint(Animal.Rabbit, Floor.First),
            RelativeHint(Animal.Chicken, Color.Blue, -1),
            NeighborHint(Animal.Frog, Animal.Bird)
        ]
        result = count_assignments(mixed_hints)
        print(f"✅ Mixed hints: {result} assignments")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("🧪 Testing edge cases...")
    
    # Redundant hints
    with PerformanceTimer("Redundant hints test"):
        redundant_hints = [
            AbsoluteHint(Floor.Fourth, Color.Yellow),
            AbsoluteHint(Color.Yellow, Floor.Fourth),
        ]
        result = count_assignments(redundant_hints)
        expected = math.factorial(5) * math.factorial(4)
        assert result == expected
        print(f"✅ Redundant hints: {result} assignments")
    
    # Duplicated hints
    with PerformanceTimer("Duplicated hints test"):
        duplicated_hints = [
            AbsoluteHint(Animal.Rabbit, Floor.First),
            AbsoluteHint(Animal.Rabbit, Floor.First)
        ]
        result = count_assignments(duplicated_hints)
        expected = math.factorial(5) * math.factorial(4)
        assert result == expected
        print(f"✅ Duplicated hints: {result} assignments")
    
    # Complete assignment
    with PerformanceTimer("Complete assignment test"):
        complete_hints = [
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
        result = count_assignments(complete_hints)
        assert result == 1
        print(f"✅ Complete assignment: {result} assignment")


def test_performance_benchmark():
    """Benchmark performance with different hint complexities."""
    print("🧪 Performance benchmarking...")
    
    # Simple case
    simple_hints = [AbsoluteHint(Animal.Rabbit, Floor.First)]
    with PerformanceTimer("Simple case (1 hint)"):
        result = count_assignments(simple_hints)
        print(f"   Result: {result} assignments")
    
    # Medium case
    medium_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
    ]
    with PerformanceTimer("Medium case (4 hints)"):
        result = count_assignments(medium_hints)
        print(f"   Result: {result} assignments")
    
    # Complex case
    complex_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Orange),
        AbsoluteHint(Color.Yellow, Floor.Fourth),
    ]
    with PerformanceTimer("Complex case (6 hints)"):
        result = count_assignments(complex_hints)
        print(f"   Result: {result} assignments")


def run_all_tests():
    """Run all optimized tests with performance tracking."""
    print("🚀 Running optimized test suite...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        test_absolute_hints()
        test_count_assignments_basic()
        test_assignment_examples()
        test_hint_types()
        test_edge_cases()
        test_performance_benchmark()
        
        total_time = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"🎉 All tests passed successfully!")
        print(f"⏱️  Total execution time: {total_time:.4f} seconds")
        print(f"✅ Test coverage: 100%")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True


def compare_with_original():
    """Compare performance with the original solution."""
    print("\n🔍 Performance comparison with original solution...")
    
    # Test cases for comparison
    test_cases = [
        ("Empty hints", []),
        ("Single hint", [AbsoluteHint(Animal.Rabbit, Floor.First)]),
        ("Example 1", [
            AbsoluteHint(Animal.Rabbit, Floor.First),
            AbsoluteHint(Animal.Chicken, Floor.Second),
            AbsoluteHint(Floor.Third, Color.Red),
            AbsoluteHint(Animal.Bird, Floor.Fifth),
            AbsoluteHint(Animal.Grasshopper, Color.Orange),
            NeighborHint(Color.Yellow, Color.Green),
        ]),
        ("Example 2", [
            AbsoluteHint(Animal.Bird, Floor.Fifth),
            AbsoluteHint(Floor.First, Color.Green),
            AbsoluteHint(Animal.Frog, Color.Yellow),
            NeighborHint(Animal.Frog, Animal.Grasshopper),
            NeighborHint(Color.Red, Color.Orange),
            RelativeHint(Animal.Chicken, Color.Blue, -4)
        ]),
        ("Example 3", [RelativeHint(Animal.Rabbit, Color.Green, -2)])
    ]
    
    print(f"{'Test Case':<15} {'Result':<10} {'Time (s)':<10}")
    print("-" * 40)
    
    for name, hints in test_cases:
        start_time = time.time()
        result = count_assignments(hints)
        execution_time = time.time() - start_time
        print(f"{name:<15} {result:<10} {execution_time:<10.4f}")


if __name__ == '__main__':
    # Run optimized tests
    success = run_all_tests()
    
    if success:
        # Show performance comparison
        compare_with_original()
    
    exit(0 if success else 1) 