"""
Test file to compare both solutions for the Picasso Tower problem.

This file tests both the original brute force solution and the alternative
constraint propagation solution to ensure they produce identical results.
"""

import math
from count_assignments import (
    AbsoluteHint, Animal, Color, Floor, FloorAssignment,
    NeighborHint, RelativeHint, count_assignments as count_assignments_original
)
from count_assignments_alternative_solution import (
    AbsoluteHint as AltAbsoluteHint,
    NeighborHint as AltNeighborHint,
    RelativeHint as AltRelativeHint,
    count_assignments as count_assignments_alternative
)


def test_basic_examples():
    """Test the basic examples from the assignment."""
    print("Testing basic examples from assignment...")
    
    # Example 1
    hints_ex1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Orange),
        NeighborHint(Color.Yellow, Color.Green),
    ]
    
    hints_ex1_alt = [
        AltAbsoluteHint(Animal.Rabbit, Floor.First),
        AltAbsoluteHint(Animal.Chicken, Floor.Second),
        AltAbsoluteHint(Floor.Third, Color.Red),
        AltAbsoluteHint(Animal.Bird, Floor.Fifth),
        AltAbsoluteHint(Animal.Grasshopper, Color.Orange),
        AltNeighborHint(Color.Yellow, Color.Green),
    ]
    
    result1_original = count_assignments_original(hints_ex1)
    result1_alternative = count_assignments_alternative(hints_ex1_alt)
    
    print(f"Example 1 - Original: {result1_original}, Alternative: {result1_alternative}")
    assert result1_original == result1_alternative == 2, f"Example 1 failed: {result1_original} != {result1_alternative}"
    
    # Example 2
    hints_ex2 = [
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Floor.First, Color.Green),
        AbsoluteHint(Animal.Frog, Color.Yellow),
        NeighborHint(Animal.Frog, Animal.Grasshopper),
        NeighborHint(Color.Red, Color.Orange),
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    ]
    
    hints_ex2_alt = [
        AltAbsoluteHint(Animal.Bird, Floor.Fifth),
        AltAbsoluteHint(Floor.First, Color.Green),
        AltAbsoluteHint(Animal.Frog, Color.Yellow),
        AltNeighborHint(Animal.Frog, Animal.Grasshopper),
        AltNeighborHint(Color.Red, Color.Orange),
        AltRelativeHint(Animal.Chicken, Color.Blue, -4)
    ]
    
    result2_original = count_assignments_original(hints_ex2)
    result2_alternative = count_assignments_alternative(hints_ex2_alt)
    
    print(f"Example 2 - Original: {result2_original}, Alternative: {result2_alternative}")
    assert result2_original == result2_alternative == 4, f"Example 2 failed: {result2_original} != {result2_alternative}"
    
    # Example 3
    hints_ex3 = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]
    
    hints_ex3_alt = [
        AltRelativeHint(Animal.Rabbit, Color.Green, -2)
    ]
    
    result3_original = count_assignments_original(hints_ex3)
    result3_alternative = count_assignments_alternative(hints_ex3_alt)
    
    print(f"Example 3 - Original: {result3_original}, Alternative: {result3_alternative}")
    assert result3_original == result3_alternative == 1728, f"Example 3 failed: {result3_original} != {result3_alternative}"
    
    print("✅ All basic examples passed!")


def test_edge_cases():
    """Test edge cases and special scenarios."""
    print("\nTesting edge cases...")
    
    # Empty hints
    result_empty_original = count_assignments_original([])
    result_empty_alternative = count_assignments_alternative([])
    
    print(f"Empty hints - Original: {result_empty_original}, Alternative: {result_empty_alternative}")
    assert result_empty_original == result_empty_alternative == 14400, f"Empty hints failed: {result_empty_original} != {result_empty_alternative}"
    
    # Single absolute hint
    single_hint = [AbsoluteHint(Animal.Rabbit, Floor.First)]
    single_hint_alt = [AltAbsoluteHint(Animal.Rabbit, Floor.First)]
    result_single_original = count_assignments_original(single_hint)
    result_single_alternative = count_assignments_alternative(single_hint_alt)
    
    print(f"Single absolute hint - Original: {result_single_original}, Alternative: {result_single_alternative}")
    assert result_single_original == result_single_alternative == 2880, f"Single hint failed: {result_single_original} != {result_single_alternative}"
    
    # Contradicting hints
    contradicting_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Bird, Floor.First)
    ]
    contradicting_hints_alt = [
        AltAbsoluteHint(Animal.Rabbit, Floor.First),
        AltAbsoluteHint(Animal.Bird, Floor.First)
    ]
    result_contradict_original = count_assignments_original(contradicting_hints)
    result_contradict_alternative = count_assignments_alternative(contradicting_hints_alt)
    
    print(f"Contradicting hints - Original: {result_contradict_original}, Alternative: {result_contradict_alternative}")
    assert result_contradict_original == result_contradict_alternative == 0, f"Contradicting hints failed: {result_contradict_original} != {result_contradict_alternative}"
    
    print("✅ All edge cases passed!")


def test_complex_scenarios():
    """Test more complex scenarios."""
    print("\nTesting complex scenarios...")
    
    # Complete assignment (should be 1)
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
    
    complete_hints_alt = [
        AltAbsoluteHint(Animal.Rabbit, Floor.First),
        AltAbsoluteHint(Animal.Chicken, Floor.Second),
        AltAbsoluteHint(Floor.Third, Animal.Bird),
        AltAbsoluteHint(Floor.Fourth, Animal.Frog),
        AltAbsoluteHint(Floor.Fifth, Animal.Grasshopper),
        AltAbsoluteHint(Floor.Fifth, Color.Green),
        AltAbsoluteHint(Animal.Chicken, Color.Blue),
        AltAbsoluteHint(Animal.Rabbit, Color.Orange),
        AltAbsoluteHint(Floor.Third, Color.Red),
        AltAbsoluteHint(Floor.Fourth, Color.Yellow),
    ]
    
    result_complete_original = count_assignments_original(complete_hints)
    result_complete_alternative = count_assignments_alternative(complete_hints_alt)
    
    print(f"Complete assignment - Original: {result_complete_original}, Alternative: {result_complete_alternative}")
    assert result_complete_original == result_complete_alternative == 1, f"Complete assignment failed: {result_complete_original} != {result_complete_alternative}"
    
    # Multiple relative hints
    relative_hints = [
        RelativeHint(Animal.Rabbit, Color.Green, -2),
        RelativeHint(Animal.Chicken, Color.Blue, -1),
        RelativeHint(Animal.Frog, Color.Red, 1)
    ]
    
    relative_hints_alt = [
        AltRelativeHint(Animal.Rabbit, Color.Green, -2),
        AltRelativeHint(Animal.Chicken, Color.Blue, -1),
        AltRelativeHint(Animal.Frog, Color.Red, 1)
    ]
    
    result_relative_original = count_assignments_original(relative_hints)
    result_relative_alternative = count_assignments_alternative(relative_hints_alt)
    
    print(f"Multiple relative hints - Original: {result_relative_original}, Alternative: {result_relative_alternative}")
    assert result_relative_original == result_relative_alternative, f"Multiple relative hints failed: {result_relative_original} != {result_relative_alternative}"
    
    # Multiple neighbor hints
    neighbor_hints = [
        NeighborHint(Animal.Rabbit, Animal.Chicken),
        NeighborHint(Color.Red, Color.Blue),
        NeighborHint(Animal.Frog, Color.Green)
    ]
    
    neighbor_hints_alt = [
        AltNeighborHint(Animal.Rabbit, Animal.Chicken),
        AltNeighborHint(Color.Red, Color.Blue),
        AltNeighborHint(Animal.Frog, Color.Green)
    ]
    
    result_neighbor_original = count_assignments_original(neighbor_hints)
    result_neighbor_alternative = count_assignments_alternative(neighbor_hints_alt)
    
    print(f"Multiple neighbor hints - Original: {result_neighbor_original}, Alternative: {result_neighbor_alternative}")
    assert result_neighbor_original == result_neighbor_alternative, f"Multiple neighbor hints failed: {result_neighbor_original} != {result_neighbor_alternative}"
    
    print("✅ All complex scenarios passed!")


def test_performance_comparison():
    """Compare performance between the two approaches."""
    print("\nTesting performance comparison...")
    
    import time
    
    # Test with a moderately complex scenario
    test_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Red),
        NeighborHint(Color.Yellow, Color.Green),
        RelativeHint(Animal.Frog, Color.Blue, -2)
    ]
    
    test_hints_alt = [
        AltAbsoluteHint(Animal.Rabbit, Floor.First),
        AltAbsoluteHint(Animal.Chicken, Floor.Second),
        AltAbsoluteHint(Floor.Third, Color.Red),
        AltNeighborHint(Color.Yellow, Color.Green),
        AltRelativeHint(Animal.Frog, Color.Blue, -2)
    ]
    
    # Time original solution
    start_time = time.time()
    result_original = count_assignments_original(test_hints)
    original_time = time.time() - start_time
    
    # Time alternative solution
    start_time = time.time()
    result_alternative = count_assignments_alternative(test_hints_alt)
    alternative_time = time.time() - start_time
    
    print(f"Performance test results:")
    print(f"  Original solution: {original_time:.4f} seconds")
    print(f"  Alternative solution: {alternative_time:.4f} seconds")
    print(f"  Speedup: {original_time / alternative_time:.2f}x")
    print(f"  Results match: {result_original == result_alternative}")
    
    assert result_original == result_alternative, "Performance test results don't match"


def run_all_tests():
    """Run all tests."""
    print("🧪 Testing both solutions for Picasso Tower problem")
    print("=" * 60)
    
    try:
        test_basic_examples()
        test_edge_cases()
        test_complex_scenarios()
        test_performance_comparison()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! Both solutions produce identical results.")
        print("✅ Original solution: Brute force with verification")
        print("✅ Alternative solution: Constraint propagation + backtracking")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1) 