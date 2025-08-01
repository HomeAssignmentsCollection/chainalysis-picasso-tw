from enum import Enum, IntEnum
from itertools import permutations
import math
from typing import List, Set, Tuple, Optional


class Floor(IntEnum):
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Fifth = 5


class Color(Enum):
    Red = 'Red'
    Green = 'Green'
    Blue = 'Blue'
    Yellow = 'Yellow'
    Orange = 'Orange'


class Animal(Enum):
    Frog = 'Frog'
    Rabbit = 'Rabbit'
    Grasshopper = 'Grasshopper'
    Bird = 'Bird'
    Chicken = 'Chicken'


class AttributeType(Enum):
    Floor = 'Floor'
    Color = 'Color'
    Animal = 'Animal'


class TowerState:
    """Represents the current state of the Picasso Tower"""
    
    def __init__(self):
        self.floor_assignments: List[FloorAssignment] = []
        self.used_animals: Set[Animal] = set()
        self.used_colors: Set[Color] = set()
        self.available_animals: Set[Animal] = set(Animal)
        self.available_colors: Set[Color] = set(Color)
    
    def add_assignment(self, assignment: 'FloorAssignment') -> bool:
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
    
    def get_assignment_for_floor(self, floor: Floor) -> Optional['FloorAssignment']:
        """Get assignment for a specific floor"""
        for assignment in self.floor_assignments:
            if assignment.floor == floor:
                return assignment
        return None
    
    def get_assignment_for_animal(self, animal: Animal) -> Optional['FloorAssignment']:
        """Get assignment for a specific animal"""
        for assignment in self.floor_assignments:
            if assignment.animal == animal:
                return assignment
        return None
    
    def get_assignment_for_color(self, color: Color) -> Optional['FloorAssignment']:
        """Get assignment for a specific color"""
        for assignment in self.floor_assignments:
            if assignment.color == color:
                return assignment
        return None


class AssignmentValidator:
    """Validates tower assignments against hints"""
    
    @staticmethod
    def validate_all_hints(assignments: List['FloorAssignment'], hints: List['Hint']) -> bool:
        """Validate that all hints are satisfied"""
        return all(hint.check_if_satisfied(assignments) for hint in hints)
    
    @staticmethod
    def validate_early_termination(partial_assignments: List['FloorAssignment'], hints: List['Hint']) -> bool:
        """Check if partial assignments already violate any hints"""
        for hint in hints:
            if not hint.check_if_satisfied(partial_assignments):
                return False
        return True


class FloorAssignment:
    """Represents a complete assignment of animals and colors to floors"""
    def __init__(self, floor, animal, color):
        self.floor = floor
        self.animal = animal
        self.color = color

    def __repr__(self):
        return f"FloorAssignment(floor={self.floor}, animal={self.animal}, color={self.color})"
    
    def __eq__(self, other):
        if not isinstance(other, FloorAssignment):
            return False
        return (self.floor == other.floor and 
                self.animal == other.animal and 
                self.color == other.color)
    
    def __hash__(self):
        return hash((self.floor, self.animal, self.color))


class Hint(object):
    """Base class for all the hint classes"""
    pass


class AbsoluteHint(Hint):
    """
    Represents a hint on a specific floor. Examples:
    The third floor is red:
        AbsoluteHint(Floor.Third, Color.Red)
    The frog lives on the fifth floor:
        AbsoluteHint(Animal.Frog, Floor.Fifth)
    The orange floor is the floor where the chicken lives:
        AbsoluteHint(Color.Orange, Animal.Chicken)
    """
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    def check_if_satisfied(self, assignments):
        """Check if this hint is satisfied by the given assignments"""
        for assignment in assignments:
            # Check if both attributes are satisfied by this assignment
            if self._check_attr_match(assignment, self._attr1) and self._check_attr_match(assignment, self._attr2):
                return True
        return False

    def _check_attr_match(self, assignment, attr):
        """Check if an assignment matches a given attribute"""
        if isinstance(attr, Floor):
            return assignment.floor == attr
        elif isinstance(attr, Color):
            return assignment.color == attr
        elif isinstance(attr, Animal):
            return assignment.animal == attr
        return False

    def get_possible_floor_assignments(self, empty_floors, all_animal_options, all_color_options, floor_assignments):
        """Get possible floor assignments that satisfy this hint"""
        possible_assignments = []

        # Check if this hint can be satisfied with the given constraints
        for floor in empty_floors:
            for animal in all_animal_options:
                for color in all_color_options:
                    assignment = FloorAssignment(floor, animal, color)
                    if self._check_attr_match(assignment, self._attr1) and self._check_attr_match(assignment, self._attr2):
                        possible_assignments.append(assignment)

        return possible_assignments


class RelativeHint(Hint):
    """
    Represents a hint on the relative position of two attributes. Examples:
    The rabbit lives 2 floors below the green floor:
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    The chicken lives 4 floors below the blue floor:
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    """
    def __init__(self, attr1, attr2, difference):
        self._attr1 = attr1
        self._attr2 = attr2
        self._difference = difference

    def check_if_satisfied(self, assignments):
        """Check if this hint is satisfied by the given assignments"""
        # Find assignments that match the attributes
        attr1_assignment = None
        attr2_assignment = None
        
        for assignment in assignments:
            if self._check_attr_match(assignment, self._attr1):
                attr1_assignment = assignment
            if self._check_attr_match(assignment, self._attr2):
                attr2_assignment = assignment
        
        # Check if both attributes are assigned and the difference is correct
        if attr1_assignment and attr2_assignment:
            return attr1_assignment.floor - attr2_assignment.floor == self._difference
        return False

    def _check_attr_match(self, assignment, attr):
        """Check if an assignment matches a given attribute"""
        if isinstance(attr, Floor):
            return assignment.floor == attr
        elif isinstance(attr, Color):
            return assignment.color == attr
        elif isinstance(attr, Animal):
            return assignment.animal == attr
        return False


class NeighborHint(Hint):
    """
    Represents a hint that two attributes are neighbors. Examples:
    The red floor and the green floors are neighboring floors:
        NeighborHint(Color.Red, Color.Green)
    The frog is a neighbor of the grasshopper:
        NeighborHint(Animal.Frog, Animal.Grasshopper)
    """
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    def check_if_satisfied(self, assignments):
        """Check if this hint is satisfied by the given assignments"""
        # Find assignments that match the attributes
        attr1_assignment = None
        attr2_assignment = None
        
        for assignment in assignments:
            if self._check_attr_match(assignment, self._attr1):
                attr1_assignment = assignment
            if self._check_attr_match(assignment, self._attr2):
                attr2_assignment = assignment
        
        # Check if both attributes are assigned and are neighbors
        if attr1_assignment and attr2_assignment:
            floor_diff = abs(attr1_assignment.floor - attr2_assignment.floor)
            return floor_diff == 1
        return False

    def _check_attr_match(self, assignment, attr):
        """Check if an assignment matches a given attribute"""
        if isinstance(attr, Floor):
            return assignment.floor == attr
        elif isinstance(attr, Color):
            return assignment.color == attr
        elif isinstance(attr, Animal):
            return assignment.animal == attr
        return False


def count_assignments(hints):
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
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
            if all(hint.check_if_satisfied(assignment) for hint in hints):
                valid_count += 1
    return valid_count


def count_assignments_optimized(hints: List[Hint]) -> int:
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


def test():
    """Test the count_assignments function with the provided examples"""
    # Example 1
    hints1 = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Chicken, Floor.Second),
        AbsoluteHint(Floor.Third, Color.Yellow),
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Animal.Grasshopper, Color.Blue),
        NeighborHint(Color.Red, Color.Green),
    ]
    result1 = count_assignments(hints1)
    print(f"Example 1: {result1}")  # Expected: 2

    # Example 2
    hints2 = [
        AbsoluteHint(Animal.Bird, Floor.Fifth),
        AbsoluteHint(Floor.First, Color.Green),
        AbsoluteHint(Animal.Frog, Color.Yellow),
        NeighborHint(Animal.Frog, Animal.Grasshopper),
        NeighborHint(Color.Red, Color.Orange),
        RelativeHint(Animal.Chicken, Color.Blue, -4)
    ]
    result2 = count_assignments(hints2)
    print(f"Example 2: {result2}")  # Expected: 4

    # Example 3
    hints3 = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]
    result3 = count_assignments(hints3)
    print(f"Example 3: {result3}")  # Expected: 1728


if __name__ == "__main__":
    test()
