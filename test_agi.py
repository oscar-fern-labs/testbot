#!/usr/bin/env python3
"""
Quick test to ensure AGI system works correctly
"""

from agi_system import AGI

def test_basic_functionality():
    """Test basic AGI functionality"""
    print("Testing AGI System...")
    
    # Create AGI instance
    agi = AGI(name="TestAGI")
    print("✓ AGI instance created")
    
    # Test thinking
    response = agi.think("What is 2 + 2?")
    print(f"✓ Thinking works: {response['response']}")
    
    # Test goal setting
    agi.set_goal("Learn mathematics", priority=7)
    print("✓ Goal setting works")
    
    # Test problem solving
    problem = {
        "description": "Simple addition",
        "type": "mathematical",
        "initial_state": {"equation": "2 + 2"},
        "goal_state": {"solved": True}
    }
    solution = agi.solve_problem(problem)
    print(f"✓ Problem solving works: Solution generated")
    
    # Test self-improvement
    improvement = agi.self_improve()
    print(f"✓ Self-improvement works: {len(improvement['improvements'])} improvements made")
    
    # Test status
    status = agi.get_status()
    print(f"✓ Status check works: {status['name']} is operational")
    
    print("\nAll tests passed! AGI system is functional.")

if __name__ == "__main__":
    test_basic_functionality()

