"""
Picasso Tower Solver - Comprehensive Test Suite

This module provides comprehensive testing for the Picasso Tower assignment solver,
including unit tests, performance benchmarks, and validation tests.
"""

import time
import math
from typing import List, Dict, Any
from count_assignments import (
    count_assignments, count_assignments_optimized,
    AbsoluteHint, RelativeHint, NeighborHint,
    Animal, Color, Floor, FloorAssignment,
    TowerState, AssignmentValidator
)


class PerformanceTimer:
    """Context manager for measuring execution time"""
    
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


class TestResult:
    """Represents a test result with metadata"""
    
    def __init__(self, name: str, expected: int, actual: int, time_taken: float):
        self.name = name
        self.expected = expected
        self.actual = actual
        self.time_taken = time_taken
        self.passed = expected == actual
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} | {self.name}: Expected {self.expected}, Got {self.actual} ({self.time_taken:.4f}s)"


def test_assignment_examples() -> List[TestResult]:
    """Test the assignment examples from the problem description"""
    print("🧪 Testing Assignment Examples")
    print("=" * 50)
    
    results = []
    
    # Example 1
    hints_ex1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Yellow),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Blue),
        NeighborHint(Color.Red, Color.Green),
    ]
    
    with PerformanceTimer("Example 1"):
        result1 = count_assignments(hints_ex1)
    results.append(TestResult("Example 1", 2, result1, 0.0))
    
    # Example 2
    hints_ex2 = [
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Floor.First, Color.Green),
        AbsoluteHint(Animal.Frog, Color.Yellow),
        NeighborHint(Animal.Frog, Animal.Grasshopper),
        NeighborHint(Color.Red, Color.Orange),
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    ]
    
    with PerformanceTimer("Example 2"):
        result2 = count_assignments(hints_ex2)
    results.append(TestResult("Example 2", 4, result2, 0.0))
    
    # Example 3
    hints_ex3 = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]
    
    with PerformanceTimer("Example 3"):
        result3 = count_assignments(hints_ex3)
    results.append(TestResult("Example 3", 1728, result3, 0.0))
    
    for result in results:
        print(result)
    
    return results


def test_edge_cases() -> List[TestResult]:
    """Test edge cases and boundary conditions"""
    print("\n🔍 Testing Edge Cases")
    print("=" * 30)
    
    results = []
    
    # Empty hints
    with PerformanceTimer("Empty hints"):
        result_empty = count_assignments([])
    expected_empty = math.factorial(5) * math.factorial(5)  # 14400
    results.append(TestResult("Empty hints", expected_empty, result_empty, 0.0))
    
    # Single absolute hint
    single_hint = [AbsoluteHint(Animal.Rabbit, Floor.First)]
    with PerformanceTimer("Single absolute hint"):
        result_single = count_assignments(single_hint)
    expected_single = math.factorial(4) * math.factorial(4)  # 576
    results.append(TestResult("Single absolute hint", expected_single, result_single, 0.0))
    
    # Contradicting hints
    contradicting_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Bird, Floor.First)
    ]
    with PerformanceTimer("Contradicting hints"):
        result_contradict = count_assignments(contradicting_hints)
    results.append(TestResult("Contradicting hints", 0, result_contradict, 0.0))
    
    # Complete assignment
    complete_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Animal.Bird),
        AbsoluteHint(Floor.Fourth, Animal.Frog),
        AbsoluteHint(Floor.Fifth, Animal.Grasshopper),
        AbsoluteHint(Floor.First, Color.Red),
        AbsoluteHint(Floor.Second, Color.Green),
        AbsoluteHint(Floor.Third, Color.Blue),
        AbsoluteHint(Floor.Fourth, Color.Yellow),
        AbsoluteHint(Floor.Fifth, Color.Orange),
    ]
    with PerformanceTimer("Complete assignment"):
        result_complete = count_assignments(complete_hints)
    results.append(TestResult("Complete assignment", 1, result_complete, 0.0))
    
    for result in results:
        print(result)
    
    return results


def test_hint_types() -> List[TestResult]:
    """Test different types of hints"""
    print("\n🎯 Testing Hint Types")
    print("=" * 25)
    
    results = []
    
    # Multiple relative hints
    relative_hints = [
        RelativeHint(Animal.Rabbit, Color.Green, -2),
        RelativeHint(Animal.Chicken, Color.Blue, -1),
        RelativeHint(Animal.Frog, Color.Red, 1)
    ]
    with PerformanceTimer("Multiple relative hints"):
        result_relative = count_assignments(relative_hints)
    results.append(TestResult("Multiple relative hints", 0, result_relative, 0.0))
    
    # Multiple neighbor hints
    neighbor_hints = [
        NeighborHint(Animal.Rabbit, Animal.Chicken),
        NeighborHint(Color.Red, Color.Blue),
        NeighborHint(Animal.Frog, Color.Green)
    ]
    with PerformanceTimer("Multiple neighbor hints"):
        result_neighbor = count_assignments(neighbor_hints)
    results.append(TestResult("Multiple neighbor hints", 0, result_neighbor, 0.0))
    
    # Mixed hint types
    mixed_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        RelativeHint(Animal.Chicken, Color.Blue, -2),
        NeighborHint(Color.Red, Color.Green)
    ]
    with PerformanceTimer("Mixed hint types"):
        result_mixed = count_assignments(mixed_hints)
    results.append(TestResult("Mixed hint types", 0, result_mixed, 0.0))
    
    for result in results:
        print(result)
    
    return results


def test_optimized_version() -> List[TestResult]:
    """Test the optimized version against the original"""
    print("\n🚀 Testing Optimized Version")
    print("=" * 35)
    
    results = []
    
    # Test with example 1
    hints_ex1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Yellow),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Blue),
        NeighborHint(Color.Red, Color.Green),
    ]
    
    with PerformanceTimer("Original version"):
        result_original = count_assignments(hints_ex1)
    
    with PerformanceTimer("Optimized version"):
        result_optimized = count_assignments_optimized(hints_ex1)
    
    results.append(TestResult("Optimized vs Original", result_original, result_optimized, 0.0))
    
    for result in results:
        print(result)
    
    return results


def test_tower_state_class() -> List[TestResult]:
    """Test the TowerState class functionality"""
    print("\n🏗️  Testing TowerState Class")
    print("=" * 35)
    
    results = []
    
    # Test TowerState
    tower = TowerState()
    
    # Test adding valid assignment
    assignment1 = FloorAssignment(Floor.First, Animal.Rabbit, Color.Red)
    success1 = tower.add_assignment(assignment1)
    results.append(TestResult("Add valid assignment", True, success1, 0.0))
    
    # Test adding invalid assignment (duplicate animal)
    assignment2 = FloorAssignment(Floor.Second, Animal.Rabbit, Color.Green)
    success2 = tower.add_assignment(assignment2)
    results.append(TestResult("Add invalid assignment", False, success2, 0.0))
    
    # Test adding invalid assignment (duplicate color)
    assignment3 = FloorAssignment(Floor.Second, Animal.Chicken, Color.Red)
    success3 = tower.add_assignment(assignment3)
    results.append(TestResult("Add duplicate color", False, success3, 0.0))
    
    # Test is_complete
    complete = tower.is_complete()
    results.append(TestResult("Is complete (false)", False, complete, 0.0))
    
    for result in results:
        print(result)
    
    return results


def test_assignment_validator() -> List[TestResult]:
    """Test the AssignmentValidator class"""
    print("\n✅ Testing AssignmentValidator")
    print("=" * 35)
    
    results = []
    
    # Test validation
    assignments = [
        FloorAssignment(Floor.First, Animal.Rabbit, Color.Red),
        FloorAssignment(Floor.Second, Animal.Chicken, Color.Green),
    ]
    
    hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
    ]
    
    is_valid = AssignmentValidator.validate_all_hints(assignments, hints)
    results.append(TestResult("Validate all hints", True, is_valid, 0.0))
    
    # Test invalid assignment
    invalid_assignments = [
        FloorAssignment(Floor.First, Animal.Bird, Color.Red),
        FloorAssignment(Floor.Second, Animal.Chicken, Color.Green),
    ]
    
    is_invalid = AssignmentValidator.validate_all_hints(invalid_assignments, hints)
    results.append(TestResult("Validate invalid hints", False, is_invalid, 0.0))
    
    for result in results:
        print(result)
    
    return results


def run_performance_benchmark() -> Dict[str, Any]:
    """Run performance benchmark tests"""
    print("\n📊 Performance Benchmark")
    print("=" * 30)
    
    benchmark_results = {}
    
    # Test with different hint complexities
    test_cases = [
        ("Empty", [], math.factorial(5) * math.factorial(5)),
        ("Single", [AbsoluteHint(Animal.Rabbit, Floor.First)], math.factorial(4) * math.factorial(4)),
        ("Example 1", [
            AbsoluteHint(Animal.Rabbit, Floor.First),
            AbsoluteHint(Animal.Chicken, Floor.Second),
            AbsoluteHint(Floor.Third, Color.Yellow),
            AbsoluteHint(Animal.Bird, Floor.Fifth),
            AbsoluteHint(Animal.Grasshopper, Color.Blue),
            NeighborHint(Color.Red, Color.Green),
        ], 2),
    ]
    
    for name, hints, expected in test_cases:
        with PerformanceTimer(f"{name} test"):
            result = count_assignments(hints)
        benchmark_results[name] = {
            "expected": expected,
            "actual": result,
            "passed": expected == result
        }
    
    return benchmark_results


def run_all_tests():
    """Run all tests and return summary"""
    print("🧪 Picasso Tower Solver - Comprehensive Test Suite")
    print("=" * 60)
    
    all_results = []
    
    # Run all test suites
    all_results.extend(test_assignment_examples())
    all_results.extend(test_edge_cases())
    all_results.extend(test_hint_types())
    all_results.extend(test_optimized_version())
    all_results.extend(test_tower_state_class())
    all_results.extend(test_assignment_validator())
    
    # Run performance benchmark
    benchmark_results = run_performance_benchmark()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 20)
    
    passed = sum(1 for result in all_results if result.passed)
    total = len(all_results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📊 Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed!")
    
    return all_results, benchmark_results


if __name__ == "__main__":
    run_all_tests()
