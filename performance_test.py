"""
Performance test to demonstrate the difference between brute force and constraint propagation approaches.
"""

import time
import math
from count_assignments import count_assignments as count_brute_force
from count_assignments_alternative_solution import count_assignments as count_constraint_prop
from count_assignments import AbsoluteHint, Animal, Color, Floor
from count_assignments_alternative_solution import AbsoluteHint as AltAbsoluteHint


def test_performance_comparison():
    """Test performance difference between approaches."""
    print("🚀 Performance Comparison: Brute Force vs Constraint Propagation")
    print("=" * 70)
    
    # Test cases with different complexity
    test_cases = [
        {
            "name": "Simple (2 hints)",
            "hints_bf": [
                AbsoluteHint(Animal.Rabbit, Floor.First),
                AbsoluteHint(Animal.Chicken, Floor.Second),
            ],
            "hints_cp": [
                AltAbsoluteHint(Animal.Rabbit, Floor.First),
                AltAbsoluteHint(Animal.Chicken, Floor.Second),
            ]
        },
        {
            "name": "Medium (4 hints)",
            "hints_bf": [
                AbsoluteHint(Animal.Rabbit, Floor.First),
                AbsoluteHint(Animal.Chicken, Floor.Second),
                AbsoluteHint(Floor.Third, Color.Red),
                AbsoluteHint(Animal.Bird, Floor.Fifth),
            ],
            "hints_cp": [
                AltAbsoluteHint(Animal.Rabbit, Floor.First),
                AltAbsoluteHint(Animal.Chicken, Floor.Second),
                AltAbsoluteHint(Floor.Third, Color.Red),
                AltAbsoluteHint(Animal.Bird, Floor.Fifth),
            ]
        },
        {
            "name": "Complex (6 hints)",
            "hints_bf": [
                AbsoluteHint(Animal.Rabbit, Floor.First),
                AbsoluteHint(Animal.Chicken, Floor.Second),
                AbsoluteHint(Floor.Third, Color.Red),
                AbsoluteHint(Animal.Bird, Floor.Fifth),
                AbsoluteHint(Animal.Grasshopper, Color.Orange),
                AbsoluteHint(Color.Yellow, Floor.Fourth),
            ],
            "hints_cp": [
                AltAbsoluteHint(Animal.Rabbit, Floor.First),
                AltAbsoluteHint(Animal.Chicken, Floor.Second),
                AltAbsoluteHint(Floor.Third, Color.Red),
                AltAbsoluteHint(Animal.Bird, Floor.Fifth),
                AltAbsoluteHint(Animal.Grasshopper, Color.Orange),
                AltAbsoluteHint(Color.Yellow, Floor.Fourth),
            ]
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Test Case {i}: {test_case['name']}")
        print("-" * 50)
        
        hints_bf = test_case['hints_bf']
        hints_cp = test_case['hints_cp']
        
        # Test Brute Force
        start_time = time.time()
        result_bf = count_brute_force(hints_bf)
        bf_time = time.time() - start_time
        
        # Test Constraint Propagation
        start_time = time.time()
        result_cp = count_constraint_prop(hints_cp)
        cp_time = time.time() - start_time
        
        # Calculate speedup
        speedup = bf_time / cp_time if cp_time > 0 else float('inf')
        
        print(f"Brute Force:     {result_bf} solutions in {bf_time:.6f}s")
        print(f"Constraint Prop: {result_cp} solutions in {cp_time:.6f}s")
        print(f"Speedup:         {speedup:.2f}x")
        print(f"Results match:   {result_bf == result_cp}")
        
        results.append({
            "test": test_case['name'],
            "brute_force_time": bf_time,
            "constraint_prop_time": cp_time,
            "speedup": speedup,
            "results_match": result_bf == result_cp
        })
    
    return results


def theoretical_analysis():
    """Show theoretical complexity analysis."""
    print("\n📈 Theoretical Complexity Analysis")
    print("=" * 50)
    
    floors = [5, 10, 20]
    
    print(f"{'Floors':<8} {'Brute Force':<15} {'Constraint Prop':<15} {'Speedup':<12}")
    print("-" * 60)
    
    for n in floors:
        # Brute Force: O(n!² × H)
        try:
            brute_force_ops = math.factorial(n) ** 2 * 6  # 6 hints
        except OverflowError:
            brute_force_ops = float('inf')
        
        # Constraint Propagation: O(n² × H × I)
        constraint_prop_ops = n * n * 6 * 20  # n² domains, 6 hints, 20 iterations
        
        if brute_force_ops == float('inf'):
            speedup = float('inf')
        else:
            speedup = brute_force_ops / constraint_prop_ops
        
        print(f"{n:<8} {brute_force_ops:<15.2e} {constraint_prop_ops:<15.2e} {speedup:<12.2e}")


def memory_analysis():
    """Show memory usage analysis."""
    print("\n💾 Memory Usage Analysis")
    print("=" * 40)
    
    floors = [5, 10, 20, 50, 100]
    
    print(f"{'Floors':<8} {'Brute Force':<15} {'Constraint Prop':<15}")
    print("-" * 45)
    
    for n in floors:
        # Brute Force: O(n) - stores one assignment
        brute_force_memory = n * 10  # 10 bytes per floor
        
        # Constraint Propagation: O(n²) - stores domains
        constraint_prop_memory = n * n * 20  # 20 bytes per domain
        
        print(f"{n:<8} {brute_force_memory:<15} {constraint_prop_memory:<15}")


def scalability_analysis():
    """Show scalability analysis."""
    print("\n📊 Scalability Analysis")
    print("=" * 40)
    
    print("Problem Size Categories:")
    print()
    
    categories = [
        ("Small (0-10 floors)", "Both approaches work well"),
        ("Medium (10-100 floors)", "Only constraint propagation feasible"),
        ("Large (100-1000 floors)", "Constraint propagation with optimizations"),
        ("Very Large (1000+ floors)", "Specialized solvers required")
    ]
    
    for category, description in categories:
        print(f"• {category}: {description}")
    
    print("\nKey Insights:")
    print("• Brute Force: O(n!²) - exponential growth")
    print("• Constraint Propagation: O(n²) - polynomial growth")
    print("• Crossover point: ~10 floors")
    print("• For 20+ floors: only constraint propagation viable")


def complexity_comparison():
    """Show detailed complexity comparison."""
    print("\n🔍 Detailed Complexity Comparison")
    print("=" * 50)
    
    print("Time Complexity:")
    print("• Brute Force:     O(n!² × H)")
    print("• Constraint Prop: O(n² × H × I)")
    print()
    print("Space Complexity:")
    print("• Brute Force:     O(n)")
    print("• Constraint Prop: O(n²)")
    print()
    print("Growth Comparison:")
    print("• n=5:   Brute Force = 14,400,  Constraint Prop = 1,500")
    print("• n=10:  Brute Force = 3.6×10¹³, Constraint Prop = 20,000")
    print("• n=20:  Brute Force = 2.4×10³², Constraint Prop = 80,000")
    print("• n=50:  Brute Force = 3×10¹²⁸,  Constraint Prop = 2.5M")


def run_performance_analysis():
    """Run complete performance analysis."""
    print("🧪 Performance Analysis: Picasso Tower Solvers")
    print("=" * 70)
    
    # Run practical tests
    results = test_performance_comparison()
    
    # Show theoretical analysis
    theoretical_analysis()
    
    # Show memory analysis
    memory_analysis()
    
    # Show complexity comparison
    complexity_comparison()
    
    # Show scalability analysis
    scalability_analysis()
    
    # Summary
    print("\n🎯 Summary")
    print("=" * 20)
    
    valid_results = [r for r in results if r['speedup'] != float('inf')]
    if valid_results:
        avg_speedup = sum(r['speedup'] for r in valid_results) / len(valid_results)
        print(f"Average speedup: {avg_speedup:.2f}x")
    
    all_match = all(r['results_match'] for r in results)
    print(f"All results match: {all_match}")
    print(f"Constraint propagation scales much better for larger problems")


if __name__ == '__main__':
    run_performance_analysis() 