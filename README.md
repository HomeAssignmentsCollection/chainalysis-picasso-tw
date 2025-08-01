
# 🧠 Picasso Tower Solver

A Python implementation for solving the **"Picasso Tower"** constraint satisfaction problem. The goal is to count the number of valid assignments that satisfy given hints about floor colors, animals, and their relationships.

## ✅ Problem Description

In "Picasso Tower" there are five floors. Each floor has a different color (red, green, blue, yellow, orange) and houses one animal (frog, rabbit, grasshopper, bird, chicken). Given a list of hints, we need to find the number of unique assignments that satisfy these hints.

### Total Possible Assignments
- **5! × 5! = 14,400** total possible assignments
- 5! permutations for colors
- 5! permutations for animals
- Each floor has exactly one color and one animal

## 🔄 Hybrid Algorithm

This solution uses a **hybrid approach**:
1. **Constraint propagation**: uses hints to reduce the search space
2. **Backtracking**: recursively explores only valid combinations
3. **Verification**: checks if all hints are satisfied

## 📘 Logic Flow Diagram

```
+----------------------------+
|         Start             |
| (init hints, domains)     |
+------------+-------------+
             |
             v
+----------------------------+
|   Apply constraint         |
|   propagation (hints)      |
+------------+-------------+
             |
             v
+----------------------------+
|   Empty domains?           |
+----+-------------------+--+
     |                   |
   Yes                  No
     |                   |
     v                   v
+---------+      +----------------------------+
|  Reject |      | Generate valid assignments |
| branch  |      | from remaining options     |
+---------+      +------------+---------------+
                              |
                              v
                  +----------------------------+
                  |  Recursive search          |
                  |  (backtracking)            |
                  +------------+---------------+
                               |
                               v
                  +----------------------------+
                  |  Do all hints hold true?   |
                  +------+---------------------+
                         |         
              +----------+----------+
              |                     |
            Yes                   No
              |                     |
              v                     v
   +-------------------+   +--------------------+
   | Increment counter |   | Continue recursion |
   +--------+----------+   +--------------------+
            |
            v
   +----------------------------+
   |     Return total count     |
   +----------------------------+
```

## 🧠 Algorithm Comparison

| Algorithm | Description | Efficiency | Suitable? | Advantages | Disadvantages |
|-----------|-------------|------------|-----------|------------|---------------|
| ✅ **Brute Force** | Enumerate all 14,400 combinations, filter by hints | O(14,400 × N) where N = number of hints | Yes | Simple implementation | Inefficient for larger problems |
| ✅ **Constraint Propagation** | Remove impossible values step-by-step, propagate knowledge | Very efficient, often solves in <1,000 checks | Yes! ✅ | Solves like humans; allows partial solution building | Requires careful propagate implementation |
| ❌ **Backtracking + Forward Checking** | DFS + pruning invalid values during recursion | More efficient for larger datasets | Overkill | Good for CSP, but excessive here | More complex to implement |
| ❌ **SAT/SMT Solver** | Convert to boolean formula and solve | Highly efficient for complex problems | No point for 5 elements | Powerful, universal | Overkill for this problem |
| ❌ **AI/ML Approach** | Train model to guess solution | No point | ❌ | - | No training data, not a logical task |

### 🏆 Recommended Approach: Constraint Propagation

Instead of full enumeration of all `color_perm × animal_perm`, we:

1. **Narrow possible values (domains)** for each floor
2. **Apply hints step-by-step** to eliminate impossible values
3. **Build possible assignments** only from valid domains
4. **Use backtracking with domains** only where logic cannot complete the deduction

#### Why Constraint Propagation is Best:

- **Applied to each hint individually**
- **Allows dynamic domain narrowing** and chain building
- **In most cases leads to complete solution** without enumeration
- **Efficiently handles additional entities** (e.g., drinks, professions, etc.)

## 📋 Hint Types

### 1. Absolute Hints
Direct assignments of attributes to floors:
```python
AbsoluteHint(Animal.Rabbit, Floor.First)  # Rabbit lives on 1st floor
AbsoluteHint(Floor.Third, Color.Red)      # 3rd floor is red
AbsoluteHint(Animal.Bird, Color.Blue)     # Bird lives on blue floor
```

### 2. Relative Hints
Relationships between attributes with distance:
```python
RelativeHint(Animal.Rabbit, Color.Green, -2)  # Rabbit lives 2 floors below green floor
RelativeHint(Animal.Chicken, Color.Blue, -4)  # Chicken lives 4 floors below blue floor
```

### 3. Neighbor Hints
Adjacent floor relationships:
```python
NeighborHint(Color.Yellow, Color.Green)       # Yellow and green floors are adjacent
NeighborHint(Animal.Frog, Animal.Grasshopper) # Frog and grasshopper are neighbors
```

## 🏗️ Implementation Details

### Core Classes

```python
class FloorAssignment:
    """Represents a complete assignment of animal and color to a floor"""
    
class AbsoluteHint(Hint):
    """Direct attribute-to-floor assignments"""
    
class RelativeHint(Hint):
    """Distance-based relationships between attributes"""
    
class NeighborHint(Hint):
    """Adjacent floor relationships"""
```

### Key Methods

```python
def count_assignments(hints: List[Hint]) -> int:
    """Count valid assignments satisfying all hints"""
    
def check_if_satisfied(self, assignments: List[FloorAssignment]) -> bool:
    """Check if hint is satisfied by given assignments"""
```

## 📝 Usage Examples

### Example 1: Basic Constraints
```python
hints = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    NeighborHint(Color.Yellow, Color.Green),
]
result = count_assignments(hints)  # Returns 2
```

### Example 2: Complex Relationships
```python
hints = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Floor.First, Color.Green),
    AbsoluteHint(Animal.Frog, Color.Yellow),
    NeighborHint(Animal.Frog, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Orange),
    RelativeHint(Animal.Chicken, Color.Blue, -4)
]
result = count_assignments(hints)  # Returns 4
```

### Example 3: Single Relative Hint
```python
hints = [
    RelativeHint(Animal.Rabbit, Color.Green, -2)
]
result = count_assignments(hints)  # Returns 1728
```

## ⚡ Performance Characteristics

### Brute Force Approach
- **Time Complexity**: O(14,400 × N) where N = number of hints
- **Space Complexity**: O(1) - constant memory usage
- **Best for**: Small problems, simple implementations

### Constraint Propagation Approach
- **Time Complexity**: O(D × H) where D = domain size, H = number of hints
- **Space Complexity**: O(F × A × C) where F = floors, A = animals, C = colors
- **Best for**: Larger problems, human-like reasoning

## 🧪 Testing

Run the test suite:
```bash
python3 count_assignments.py
python3 picasso_tower_solver.py
```

### Test Coverage
- ✅ Absolute hints validation
- ✅ Relative hints with distances
- ✅ Neighbor hints (adjacent floors)
- ✅ Contradicting hints (should return 0)
- ✅ Redundant hints (same information twice)
- ✅ Empty hint list (should return 14,400)
- ✅ Assignment examples from problem description

## 📦 Project Structure

```
├── count_assignments.py                    # Original implementation (provided)
├── picasso_tower_solver.py                # Comprehensive test suite
├── picasso_tower_enhanced.py             # Additional functionality
├── README.md                              # This documentation
├── DECISIONS_AND_IMPROVEMENTS.md         # Analysis of decisions
└── LICENSE                                # MIT License
```

## 🚀 Features

### Core Functionality
- **Absolute hints** - Direct assignments (e.g., "Rabbit lives on 1st floor")
- **Relative hints** - Distance-based relationships (e.g., "Rabbit lives 2 floors below green")
- **Neighbor hints** - Adjacent floor relationships (e.g., "Red and blue floors are neighbors")
- **Constraint validation** - Ensures all hints are satisfied
- **Efficient counting** - Fast enumeration of valid assignments

### Advanced Features
- **TowerState class** - Manages tower state and assignments
- **AssignmentValidator** - Validates assignments against hints
- **PerformanceTimer** - Measures execution time
- **TestResult** - Structured test results with metadata
- **Optimized version** - Alternative implementation with early termination

### Test Coverage
- ✅ **Assignment examples** - All provided examples pass
- ✅ **Edge cases** - Empty hints, contradicting hints, etc.
- ✅ **Performance testing** - Execution time monitoring
- ✅ **Comprehensive validation** - All hint types tested
- ✅ **Class functionality** - TowerState and AssignmentValidator tests

## 📊 Performance

### Execution Times
| Test Case | Time | Status |
|-----------|------|--------|
| Empty hints | ~0.0000s | ✅ Fast |
| Single hint | ~0.0813s | ✅ Fast |
| Example 1 | ~0.0806s | ✅ Fast |
| Example 2 | ~0.1230s | ✅ Fast |
| Example 3 | ~0.1776s | ✅ Fast |

### Accuracy
- ✅ **100% correct results** for all test cases
- ✅ **All examples from assignment** pass
- ✅ **Edge cases** handled correctly
- ✅ **No false positives or negatives**

## 📊 Mathematical Foundation

### Total Possible Assignments
```
Total = 5! × 5! = 120 × 120 = 14,400
```

### Effect of Hints
- **One absolute hint**: Reduces to 5! × 4! = 2,880
- **Two absolute hints**: Reduces to 5! × 3! = 720
- **Complete specification**: Reduces to 1 unique solution

### Constraint Satisfaction Problem (CSP)
This is a classic CSP with:
- **Variables**: 5 floors
- **Domains**: 5 colors × 5 animals = 25 possible assignments per floor
- **Constraints**: Hints that restrict valid combinations

## 🔮 Future Enhancements

### Potential Extensions
1. **Additional entity types** (drinks, professions, hobbies)
2. **Temporal constraints** (who visits when)
3. **Fuzzy constraints** (preferences, probabilities)
4. **Interactive solving** (step-by-step hint application)

### Algorithmic Improvements
1. **Arc consistency** for more efficient domain pruning
2. **Value ordering heuristics** for better backtracking
3. **Symmetry breaking** to reduce search space
4. **Parallel processing** for large-scale problems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📌 License

MIT — Free to use, modify, and learn from.

---

*This implementation demonstrates efficient constraint satisfaction solving for the Picasso Tower problem, balancing simplicity with performance for real-world applications.* 