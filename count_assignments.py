from enum import Enum, IntEnum
from itertools import permutations
import math


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


class FloorAssignment:
    """Represents a complete assignment of animals and colors to floors"""
    def __init__(self, floor, animal, color):
        self.floor = floor
        self.animal = animal
        self.color = color

    def __repr__(self):
        return f"FloorAssignment(floor={self.floor}, animal={self.animal}, color={self.color})"


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
    Represents a hint of a relation between two floor
    that are of a certain distance of each other.
    Examples:
    The red floor is above the blue floor:
        RelativeHint(Color.Red, Color.Blue, 1)
    The frog lives three floor below the yellow floor:
        RelativeHint(Animal.Frog, Color.Yellow, -3)
    The third floor is two floors below the fifth floor:
        RelativeHint(Floor.Third, Floor.Fifth, -2)
    """
    def __init__(self, attr1, attr2, difference):
        self._attr1 = attr1
        self._attr2 = attr2
        self._difference = difference

    def check_if_satisfied(self, assignments):
        """Check if this hint is satisfied by the given assignments"""
        if len(assignments) < 2:
            return True  # Can't check relative hints with less than 2 assignments

        # Find assignments that match our attributes
        attr1_assignments = [a for a in assignments if self._check_attr_match(a, self._attr1)]
        attr2_assignments = [a for a in assignments if self._check_attr_match(a, self._attr2)]

        for a1 in attr1_assignments:
            for a2 in attr2_assignments:
                if a1.floor.value - a2.floor.value == self._difference:
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


class NeighborHint(Hint):
    """
    Represents a hint of a relation between two floors that are adjacent
    (first either above or below the second).
    Examples:
    The green floor is neighboring the floor where the chicken lives:
        NeighborHint(Color.Green, Animal.Chicken)
    The grasshopper is a neighbor of the rabbit:
        NeighborHint(Animal.Grasshopper, Animal.Rabbit)
    The yellow floor is neighboring the third floor:
        NeighborHint(Color.Yellow, Floor.Third)
    """
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2

    def check_if_satisfied(self, assignments):
        """Check if this hint is satisfied by the given assignments"""
        if len(assignments) < 2:
            return True  # Can't check neighbor hints with less than 2 assignments

        # Find assignments that match our attributes
        attr1_assignments = [a for a in assignments if self._check_attr_match(a, self._attr1)]
        attr2_assignments = [a for a in assignments if self._check_attr_match(a, self._attr2)]

        for a1 in attr1_assignments:
            for a2 in attr2_assignments:
                if abs(a1.floor.value - a2.floor.value) == 1:
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


def count_assignments(hints):
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
    """
    if not hints:
        # No hints means all possible assignments are valid
        return math.factorial(5) * math.factorial(5)  # 5! * 5! = 14400

    # Generate all possible assignments
    floors = list(Floor)
    animals = list(Animal)
    colors = list(Color)

    valid_count = 0

    # Generate all permutations of animals and colors
    for animal_perm in permutations(animals):
        for color_perm in permutations(colors):
            # Create assignment
            assignment = []
            for i, floor in enumerate(floors):
                assignment.append(FloorAssignment(floor, animal_perm[i], color_perm[i]))

            # Check if this assignment satisfies all hints
            if all(hint.check_if_satisfied(assignment) for hint in hints):
                valid_count += 1

    return valid_count


HINTS_EX1 = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    NeighborHint(Color.Yellow, Color.Green),
]

HINTS_EX2 = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Floor.First, Color.Green),
    AbsoluteHint(Animal.Frog, Color.Yellow),
    NeighborHint(Animal.Frog, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Orange),
    RelativeHint(Animal.Chicken, Color.Blue, -4)
]

HINTS_EX3 = [
    RelativeHint(Animal.Rabbit, Color.Green, -2)
]


def test():
    assert count_assignments(HINTS_EX1) == 2, 'Failed on example #1'
    assert count_assignments(HINTS_EX2) == 4, 'Failed on example #2'
    assert count_assignments(HINTS_EX3) == 1728, 'Failed on example #3'
    print('Success!')


if __name__ == '__main__':
    test()
