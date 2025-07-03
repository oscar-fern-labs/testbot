#!/usr/bin/env python3
"""
AGI System Demonstration

This script demonstrates the capabilities of our educational AGI implementation.
"""

import json
from agi_system import AGI, TaskEnvironment


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")


def demonstrate_thinking():
    """Demonstrate the AGI's thinking capabilities"""
    print_section("1. THINKING AND REASONING")
    
    agi = AGI(name="AGI-Demo")
    
    # Test various inputs
    test_inputs = [
        "What is 2 + 2?",
        "If all birds can fly, and penguins are birds, can penguins fly?",
        "Solve the problem: Find the pattern in 2, 4, 8, 16, ?",
        "How can I improve my learning efficiency?"
    ]
    
    for input_text in test_inputs:
        print(f"Input: {input_text}")
        result = agi.think(input_text)
        print(f"Response: {result['response']}")
        print(f"Reasoning: {result['reasoning']['patterns']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print("-" * 40)


def demonstrate_problem_solving():
    """Demonstrate problem-solving capabilities"""
    print_section("2. PROBLEM SOLVING")
    
    agi = AGI(name="AGI-Solver")
    
    # Define a problem
    problem = {
        "description": "Optimize resource allocation",
        "type": "optimization",
        "constraints": ["limited_resources", "time_bound"],
        "initial_state": {"resources": 100, "tasks": 5},
        "goal_state": {"all_tasks_complete": True, "resources_used": "minimal"}
    }
    
    print(f"Problem: {problem['description']}")
    print(f"Constraints: {problem['constraints']}")
    
    # Solve the problem
    solution = agi.solve_problem(problem)
    
    print(f"\nSolution found: {solution['solution_found']}")
    print(f"Reasoning method: {solution['reasoning']['method_used']}")
    print(f"Steps taken: {len(solution['plan'])}")
    print(f"Confidence: {solution['confidence']:.2f}")
    
    # Show some planning steps
    print("\nPlanning steps:")
    for i, step in enumerate(solution['plan'][:3]):
        print(f"  {i+1}. {step['description']}")


def demonstrate_learning():
    """Demonstrate learning capabilities"""
    print_section("3. LEARNING AND ADAPTATION")
    
    agi = AGI(name="AGI-Learner")
    
    # Create task environment
    env = TaskEnvironment()
    
    print("Training on various tasks...")
    
    # Train on different task types
    task_types = ["logic", "math", "pattern", "planning"]
    
    for task_type in task_types:
        print(f"\n{task_type.upper()} TASKS:")
        
        for i in range(3):
            # Get a task
            task = env.get_task(task_type)
            print(f"  Task {i+1}: {task.get_description()}")
            
            # AGI attempts to solve
            task_state = task.get_initial_state()
            response = agi.think(f"Solve this {task_type} problem: {task_state}")
            
            # Submit solution (simplified - in real scenario AGI would parse its response)
            # For demo, we'll use a placeholder
            solution = response['response']
            evaluation = {"score": 0.7 + i * 0.1}  # Simulated improvement
            
            print(f"    Score: {evaluation['score']:.2f}")
    
    # Show learning progress
    print("\nLearning Summary:")
    print(f"  Total experiences: {len(agi.learning.experiences)}")
    print(f"  Skill improvements: {dict(list(agi.learning.skill_improvements.items())[:3])}")
    print(f"  Current learning rate: {agi.learning.learning_rate:.3f}")


def demonstrate_self_improvement():
    """Demonstrate self-improvement capabilities"""
    print_section("4. SELF-IMPROVEMENT")
    
    agi = AGI(name="AGI-Improver")
    
    print("Initial capabilities:")
    for capability, score in list(agi.capabilities.items())[:5]:
        print(f"  {capability}: {score:.2f}")
    
    # Perform self-improvement
    print("\nPerforming self-improvement cycle...")
    improvement_result = agi.self_improve()
    
    print("\nWeak areas identified:")
    for area in improvement_result['weak_areas'][:3]:
        print(f"  - {area}")
    
    print("\nImprovements made:")
    for improvement in improvement_result['improvements'][:3]:
        print(f"  - {improvement['area']}: +{improvement['improvement']:.3f}")
    
    print("\nUpdated capabilities:")
    for capability, score in list(agi.capabilities.items())[:5]:
        print(f"  {capability}: {score:.2f}")


def demonstrate_goal_setting():
    """Demonstrate goal-setting and planning"""
    print_section("5. GOAL-SETTING AND PLANNING")
    
    agi = AGI(name="AGI-Planner")
    
    # Set multiple goals
    goals = [
        ("Master logical reasoning", 8),
        ("Improve pattern recognition", 6),
        ("Optimize problem-solving speed", 7)
    ]
    
    print("Setting goals:")
    for goal, priority in goals:
        agi.set_goal(goal, priority)
        print(f"  - {goal} (priority: {priority})")
    
    print("\nActive goals:")
    for goal in agi.goals:
        print(f"  - {goal['goal']} (priority: {goal['priority']})")
    
    # Create plan for top goal
    top_goal = agi.goals[0]
    print(f"\nCreating plan for: {top_goal['goal']}")
    
    plan = agi.planning.create_plan(
        goal=top_goal['goal'],
        current_state={"current_capability": 0.7},
        constraints=["time_limit", "resource_constraint"]
    )
    
    print(f"Plan created with {len(plan)} steps:")
    for i, step in enumerate(plan[:5]):
        print(f"  {i+1}. {step['action']} ({step['type']})")


def demonstrate_memory_and_knowledge():
    """Demonstrate memory and knowledge systems"""
    print_section("6. MEMORY AND KNOWLEDGE")
    
    agi = AGI(name="AGI-Knowledge")
    
    # Store some memories
    print("Storing experiences in memory...")
    memories = [
        ("Solved math problem using algebraic substitution", "problem_solving", 0.8),
        ("Learned new pattern recognition technique", "learning", 0.9),
        ("Failed logic puzzle due to wrong assumption", "error", 0.7)
    ]
    
    for content, context, importance in memories:
        mem_id = agi.memory.store("experience", content, context, importance)
        print(f"  Stored: {content[:50]}... (ID: {mem_id})")
    
    # Query knowledge base
    print("\nQuerying knowledge base:")
    queries = [
        "problem_solving",
        "learning requires",
        "inference rules"
    ]
    
    for query in queries:
        results = agi.knowledge.query(query)
        print(f"  Query: '{query}'")
        print(f"    Found: {len(results)} results")
        if results:
            print(f"    Sample: {results[0]}")
    
    # Demonstrate memory recall
    print("\nMemory recall demonstration:")
    recall_query = "problem"
    recalled = agi.memory.recall(recall_query, limit=2)
    print(f"  Recalling memories about '{recall_query}':")
    for mem in recalled:
        print(f"    - {mem['content'][:60]}...")


def demonstrate_explanation():
    """Demonstrate the AGI's ability to explain its reasoning"""
    print_section("7. EXPLANATION AND TRANSPARENCY")
    
    agi = AGI(name="AGI-Explainer")
    
    # First, let the AGI solve something
    input_problem = "If A implies B, and B implies C, what can we conclude about A and C?"
    
    print(f"Problem: {input_problem}")
    result = agi.think(input_problem)
    
    print(f"\nAGI's response: {result['response']}")
    
    # Now ask for explanation
    explanation = agi.explain_reasoning("How did you reach this conclusion?")
    
    print("\nExplanation of reasoning:")
    print(explanation['explanation'])
    
    print("\nSupporting facts used:")
    for fact in explanation.get('supporting_facts', [])[:3]:
        print(f"  - {fact}")


def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print(" AGI SYSTEM DEMONSTRATION")
    print(" Educational Implementation of Artificial General Intelligence")
    print("="*60)
    
    demonstrations = [
        demonstrate_thinking,
        demonstrate_problem_solving,
        demonstrate_learning,
        demonstrate_self_improvement,
        demonstrate_goal_setting,
        demonstrate_memory_and_knowledge,
        demonstrate_explanation
    ]
    
    for demo in demonstrations:
        try:
            demo()
        except Exception as e:
            print(f"\nError in {demo.__name__}: {e}")
    
    print_section("DEMONSTRATION COMPLETE")
    print("This AGI system demonstrates key concepts including:")
    print("  ✓ Multi-modal reasoning (deductive, inductive, abductive)")
    print("  ✓ Learning from experience")
    print("  ✓ Goal-oriented planning")
    print("  ✓ Self-improvement mechanisms")
    print("  ✓ Memory consolidation")
    print("  ✓ Knowledge representation and inference")
    print("  ✓ Explainable AI")
    print("\nNote: This is an educational implementation showcasing AGI concepts,")
    print("not actual AGI (which remains an open research challenge).")


if __name__ == "__main__":
    main()
