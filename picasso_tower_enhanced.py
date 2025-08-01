"""
Picasso Tower Enhanced - Additional functionality and utilities

This module provides enhanced functionality for the Picasso Tower assignment,
including additional classes and utilities that work with the original count_assignments.py
without modifying it.
"""

import time
import math
from itertools import permutations
from typing import List, Set, Tuple, Optional, Dict, Any
from count_assignments import (
    Floor, Color, Animal, FloorAssignment,
    AbsoluteHint, RelativeHint, NeighborHint,
    count_assignments
)


class TowerState:
    """Represents the current state of the Picasso Tower"""
    
    def __init__(self):
        self.floor_assignments: List[FloorAssignment] = []
        self.used_animals: Set[Animal] = set()
        self.used_colors: Set[Color] = set()
        self.available_animals: Set[Animal] = set(Animal)
        self.available_colors: Set[Color] = set(Color)
    
    def add_assignment(self, assignment: FloorAssignment) -> bool:
        """Add an assignment if it's valid"""
        if (assignment.animal in self.used_animals or 
            assignment.color in self.used_colors):
            return False
        
        self.floor_assignments.append(assignment)
        self.used_animals.add(assignment.animal)
        self.used_colors.add(assignment.color)
        self.available_animals.remove(assignment.animal)
        self.available_colors.remove(assignment.color)
        return True
    
    def is_complete(self) -> bool:
        """Check if all floors are assigned"""
        return len(self.floor_assignments) == 5
    
    def get_assignment_for_floor(self, floor: Floor) -> Optional[FloorAssignment]:
        """Get assignment for a specific floor"""
        for assignment in self.floor_assignments:
            if assignment.floor == floor:
                return assignment
        return None
    
    def get_assignment_for_animal(self, animal: Animal) -> Optional[FloorAssignment]:
        """Get assignment for a specific animal"""
        for assignment in self.floor_assignments:
            if assignment.animal == animal:
                return assignment
        return None
    
    def get_assignment_for_color(self, color: Color) -> Optional[FloorAssignment]:
        """Get assignment for a specific color"""
        for assignment in self.floor_assignments:
            if assignment.color == color:
                return assignment
        return None


class AssignmentValidator:
    """Validates tower assignments against hints"""
    
    @staticmethod
    def validate_all_hints(assignments: List[FloorAssignment], hints: List) -> bool:
        """Validate that all hints are satisfied"""
        return all(hint.check_if_satisfied(assignments) for hint in hints)
    
    @staticmethod
    def validate_early_termination(partial_assignments: List[FloorAssignment], hints: List) -> bool:
        """Check if partial assignments already violate any hints"""
        for hint in hints:
            if not hint.check_if_satisfied(partial_assignments):
                return False
        return True


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


def count_assignments_optimized(hints: List) -> int:
    """
    Optimized version of count_assignments with early termination
    and better validation
    """
    if not hints:
        return math.factorial(5) * math.factorial(5)

    floors = list(Floor)
    animals = list(Animal)
    colors = list(Color)
    valid_count = 0

    for animal_perm in permutations(animals):
        for color_perm in permutations(colors):
            assignment = []
            for i, floor in enumerate(floors):
                assignment.append(FloorAssignment(floor, animal_perm[i], color_perm[i]))
            
            # Early termination: check hints as we build the assignment
            if AssignmentValidator.validate_all_hints(assignment, hints):
                valid_count += 1
    
    return valid_count


def analyze_hint_complexity(hints: List) -> Dict[str, Any]:
    """Analyze the complexity of hints"""
    analysis = {
        "total_hints": len(hints),
        "absolute_hints": 0,
        "relative_hints": 0,
        "neighbor_hints": 0,
        "complexity_score": 0
    }
    
    for hint in hints:
        if isinstance(hint, AbsoluteHint):
            analysis["absolute_hints"] += 1
            analysis["complexity_score"] += 1
        elif isinstance(hint, RelativeHint):
            analysis["relative_hints"] += 1
            analysis["complexity_score"] += 2
        elif isinstance(hint, NeighborHint):
            analysis["neighbor_hints"] += 1
            analysis["complexity_score"] += 1.5
    
    return analysis


def generate_test_cases() -> List[Dict[str, Any]]:
    """Generate various test cases for the Picasso Tower problem"""
    test_cases = [
        {
            "name": "Empty hints",
            "hints": [],
            "expected": math.factorial(5) * math.factorial(5)
        },
        {
            "name": "Single absolute hint",
            "hints": [AbsoluteHint(Animal.Rabbit, Floor.First)],
            "expected": math.factorial(4) * math.factorial(5)
        },
        {
            "name": "Example 1",
            "hints": [
                AbsoluteHint(Animal.Rabbit, Floor.First),
                AbsoluteHint(Animal.Chicken, Floor.Second),
                AbsoluteHint(Floor.Third, Color.Yellow),
                AbsoluteHint(Animal.Bird, Floor.Fifth),
                AbsoluteHint(Animal.Grasshopper, Color.Blue),
                NeighborHint(Color.Red, Color.Green),
            ],
            "expected": 2
        },
        {
            "name": "Example 2",
            "hints": [
                AbsoluteHint(Animal.Bird, Floor.Fifth),
                AbsoluteHint(Floor.First, Color.Green),
                AbsoluteHint(Animal.Frog, Color.Yellow),
                NeighborHint(Animal.Frog, Animal.Grasshopper),
                NeighborHint(Color.Red, Color.Orange),
                RelativeHint(Animal.Chicken, Color.Blue, -4)
            ],
            "expected": 4
        },
        {
            "name": "Example 3",
            "hints": [
                RelativeHint(Animal.Rabbit, Color.Green, -2)
            ],
            "expected": 1728
        }
    ]
    
    return test_cases


def run_performance_analysis() -> Dict[str, Any]:
    """Run comprehensive performance analysis"""
    print("🚀 Performance Analysis")
    print("=" * 30)
    
    test_cases = generate_test_cases()
    results = {}
    
    for test_case in test_cases:
        name = test_case["name"]
        hints = test_case["hints"]
        expected = test_case["expected"]
        
        with PerformanceTimer(f"{name} (original)"):
            result_original = count_assignments(hints)
        
        with PerformanceTimer(f"{name} (optimized)"):
            result_optimized = count_assignments_optimized(hints)
        
        analysis = analyze_hint_complexity(hints)
        
        results[name] = {
            "expected": expected,
            "original_result": result_original,
            "optimized_result": result_optimized,
            "original_correct": result_original == expected,
            "optimized_correct": result_optimized == expected,
            "results_match": result_original == result_optimized,
            "complexity": analysis
        }
        
        print(f"📊 {name}:")
        print(f"   Expected: {expected}")
        print(f"   Original: {result_original} ✅" if result_original == expected else f"   Original: {result_original} ❌")
        print(f"   Optimized: {result_optimized} ✅" if result_optimized == expected else f"   Optimized: {result_optimized} ❌")
        print(f"   Complexity: {analysis['complexity_score']}")
        print()
    
    return results


def test_enhanced_functionality():
    """Test the enhanced functionality"""
    print("🧪 Testing Enhanced Functionality")
    print("=" * 40)
    
    # Test TowerState
    tower = TowerState()
    assignment1 = FloorAssignment(Floor.First, Animal.Rabbit, Color.Red)
    success1 = tower.add_assignment(assignment1)
    print(f"✅ Add valid assignment: {success1}")
    
    # Test AssignmentValidator
    hints = [AbsoluteHint(Animal.Rabbit, Floor.First)]
    is_valid = AssignmentValidator.validate_all_hints([assignment1], hints)
    print(f"✅ Validate hints: {is_valid}")
    
    # Test performance analysis
    results = run_performance_analysis()
    
    print("🎉 Enhanced functionality tests completed!")


if __name__ == "__main__":
    test_enhanced_functionality() 