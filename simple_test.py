"""
Simple test to verify both solutions work correctly.
"""

from count_assignments import count_assignments as count_original
from count_assignments_alternative_solution import count_assignments as count_alternative
from count_assignments import AbsoluteHint, NeighborHint, Animal, Color, Floor
from count_assignments_alternative_solution import AbsoluteHint as AltAbsoluteHint, NeighborHint as AltNeighborHint

# Test Example 1
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

result1_original = count_original(hints_ex1)
result1_alternative = count_alternative(hints_ex1_alt)

print(f"Example 1 - Original: {result1_original}, Alternative: {result1_alternative}")
print(f"Results match: {result1_original == result1_alternative}")
print(f"Expected: 2")

# Test empty hints
result_empty_original = count_original([])
result_empty_alternative = count_alternative([])

print(f"\nEmpty hints - Original: {result_empty_original}, Alternative: {result_empty_alternative}")
print(f"Results match: {result_empty_original == result_empty_alternative}")
print(f"Expected: 14400") 