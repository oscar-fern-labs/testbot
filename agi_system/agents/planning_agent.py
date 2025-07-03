"""
Planning Agent Module

Handles goal-oriented planning, strategy formation, and action sequencing.
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from collections import deque


class PlanningAgent:
    """
    Agent responsible for creating and executing plans to achieve goals
    """
    
    def __init__(self):
        self.planning_methods = [
            "hierarchical",
            "means_ends_analysis",
            "forward_chaining",
            "backward_chaining",
            "partial_order"
        ]
        self.plan_library = []
        self.execution_history = []
        
    def create_plan(self, goal: str, current_state: Dict[str, Any], 
                   constraints: List[str] = None) -> List[Dict[str, Any]]:
        """
        Create a plan to achieve a goal from current state
        
        Args:
            goal: The goal to achieve
            current_state: Current state of the system
            constraints: List of constraints to consider
            
        Returns:
            List of plan steps
        """
        constraints = constraints or []
        
        # Select planning method based on goal complexity
        method = self._select_planning_method(goal, constraints)
        
        # Generate plan using selected method
        if method == "hierarchical":
            plan = self._hierarchical_planning(goal, current_state, constraints)
        elif method == "means_ends_analysis":
            plan = self._means_ends_analysis(goal, current_state, constraints)
        elif method == "forward_chaining":
            plan = self._forward_chaining(goal, current_state, constraints)
        elif method == "backward_chaining":
            plan = self._backward_chaining(goal, current_state, constraints)
        else:
            plan = self._partial_order_planning(goal, current_state, constraints)
        
        # Optimize plan
        plan = self._optimize_plan(plan)
        
        # Store in library for future reference
        self.plan_library.append({
            "goal": goal,
            "plan": plan,
            "method": method,
            "success_probability": self._estimate_success_probability(plan)
        })
        
        return plan
    
    def plan_solution(self, problem: Dict[str, Any], 
                     reasoning_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create a plan specifically for solving a problem
        
        Args:
            problem: Problem specification
            reasoning_result: Results from reasoning analysis
            
        Returns:
            Solution plan steps
        """
        # Extract key information
        problem_type = problem.get("type", "general")
        complexity = problem.get("complexity", 0.5)
        
        # Determine approach based on problem characteristics
        if complexity > 0.7:
            # Complex problem - use decomposition
            sub_problems = self._decompose_problem(problem)
            plan = []
            
            for sub_problem in sub_problems:
                sub_plan = self._create_sub_plan(sub_problem, reasoning_result)
                plan.extend(sub_plan)
        else:
            # Simple problem - direct approach
            plan = self._create_direct_plan(problem, reasoning_result)
        
        # Add validation steps
        plan.append({
            "type": "validate",
            "action": "verify_solution",
            "description": "Validate that solution meets all requirements"
        })
        
        return plan
    
    def create_improvement_plan(self, weak_areas: List[str], 
                               performance_metrics: Dict[str, float]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create a plan for self-improvement
        
        Args:
            weak_areas: Areas that need improvement
            performance_metrics: Current performance metrics
            
        Returns:
            Improvement plan for each weak area
        """
        improvement_plan = {}
        
        for area in weak_areas:
            current_performance = performance_metrics.get(area, 0.5)
            target_performance = min(1.0, current_performance + 0.2)
            
            actions = []
            
            # Determine improvement strategies
            if area in ["reasoning_accuracy", "logical_reasoning"]:
                actions.extend([
                    {
                        "action": "practice_logic_puzzles",
                        "duration": "continuous",
                        "expected_improvement": 0.05
                    },
                    {
                        "action": "analyze_reasoning_errors",
                        "duration": "periodic",
                        "expected_improvement": 0.03
                    }
                ])
            
            elif area in ["learning_ability", "adaptation"]:
                actions.extend([
                    {
                        "action": "increase_experience_diversity",
                        "duration": "continuous",
                        "expected_improvement": 0.04
                    },
                    {
                        "action": "meta_learning_optimization",
                        "duration": "periodic",
                        "expected_improvement": 0.06
                    }
                ])
            
            elif area in ["creative_thinking", "pattern_recognition"]:
                actions.extend([
                    {
                        "action": "explore_novel_combinations",
                        "duration": "continuous",
                        "expected_improvement": 0.03
                    },
                    {
                        "action": "cross_domain_learning",
                        "duration": "periodic",
                        "expected_improvement": 0.04
                    }
                ])
            
            else:
                # Generic improvement actions
                actions.append({
                    "action": f"focused_practice_{area}",
                    "duration": "continuous",
                    "expected_improvement": 0.05
                })
            
            improvement_plan[area] = actions
        
        return improvement_plan
    
    def _select_planning_method(self, goal: str, constraints: List[str]) -> str:
        """Select appropriate planning method based on goal and constraints"""
        # Analyze goal characteristics
        if "hierarchical" in goal.lower() or "complex" in goal.lower():
            return "hierarchical"
        elif "optimize" in goal.lower() or "efficient" in goal.lower():
            return "means_ends_analysis"
        elif len(constraints) > 3:
            return "partial_order"
        elif "step" in goal.lower() or "sequence" in goal.lower():
            return "forward_chaining"
        else:
            return random.choice(self.planning_methods)
    
    def _hierarchical_planning(self, goal: str, current_state: Dict[str, Any], 
                              constraints: List[str]) -> List[Dict[str, Any]]:
        """Create a hierarchical plan with multiple levels of abstraction"""
        plan = []
        
        # High-level decomposition
        high_level_tasks = [
            {"level": "high", "task": "analyze_requirements", "type": "analysis"},
            {"level": "high", "task": "design_approach", "type": "planning"},
            {"level": "high", "task": "execute_solution", "type": "execution"},
            {"level": "high", "task": "validate_results", "type": "validation"}
        ]
        
        # Expand each high-level task
        for task in high_level_tasks:
            # Add high-level task
            plan.append({
                "type": task["type"],
                "action": task["task"],
                "level": "high",
                "description": f"High-level: {task['task']}"
            })
            
            # Add sub-tasks
            if task["task"] == "analyze_requirements":
                plan.extend([
                    {
                        "type": "analysis",
                        "action": "identify_inputs",
                        "level": "low",
                        "description": "Identify all inputs and requirements"
                    },
                    {
                        "type": "analysis",
                        "action": "define_success_criteria",
                        "level": "low",
                        "description": "Define what constitutes success"
                    }
                ])
            elif task["task"] == "execute_solution":
                plan.extend([
                    {
                        "type": "execution",
                        "action": "implement_core_logic",
                        "level": "low",
                        "description": "Implement the main solution logic"
                    },
                    {
                        "type": "execution",
                        "action": "handle_edge_cases",
                        "level": "low",
                        "description": "Handle special cases and exceptions"
                    }
                ])
        
        return plan
    
    def _means_ends_analysis(self, goal: str, current_state: Dict[str, Any], 
                            constraints: List[str]) -> List[Dict[str, Any]]:
        """Use means-ends analysis to create plan"""
        plan = []
        
        # Identify differences between current and goal state
        differences = self._identify_differences(current_state, goal)
        
        # For each difference, find means to reduce it
        for diff in differences:
            means = self._find_means_for_difference(diff)
            plan.append({
                "type": "reduce_difference",
                "action": means["action"],
                "target": diff,
                "description": f"Reduce difference: {diff}"
            })
        
        return plan
    
    def _forward_chaining(self, goal: str, current_state: Dict[str, Any], 
                         constraints: List[str]) -> List[Dict[str, Any]]:
        """Create plan using forward chaining from current state"""
        plan = []
        state = current_state.copy()
        
        steps = 0
        max_steps = 10
        
        while not self._goal_achieved(state, goal) and steps < max_steps:
            # Find applicable actions
            applicable_actions = self._find_applicable_actions(state, constraints)
            
            if not applicable_actions:
                break
            
            # Select best action
            action = self._select_best_action(applicable_actions, goal)
            
            plan.append({
                "type": "forward",
                "action": action["name"],
                "preconditions": action.get("preconditions", []),
                "effects": action.get("effects", []),
                "description": f"Apply {action['name']}"
            })
            
            # Update state
            state = self._apply_action_effects(state, action)
            steps += 1
        
        return plan
    
    def _backward_chaining(self, goal: str, current_state: Dict[str, Any], 
                          constraints: List[str]) -> List[Dict[str, Any]]:
        """Create plan using backward chaining from goal"""
        plan = deque()
        
        # Start from goal and work backwards
        subgoals = deque([goal])
        
        while subgoals:
            current_subgoal = subgoals.popleft()
            
            # Find action that achieves this subgoal
            achieving_actions = self._find_achieving_actions(current_subgoal)
            
            if achieving_actions:
                action = achieving_actions[0]  # Select first viable action
                
                plan.appendleft({
                    "type": "backward",
                    "action": action["name"],
                    "achieves": current_subgoal,
                    "requires": action.get("preconditions", []),
                    "description": f"To achieve {current_subgoal}: {action['name']}"
                })
                
                # Add preconditions as new subgoals
                for precondition in action.get("preconditions", []):
                    if not self._satisfied_in_state(precondition, current_state):
                        subgoals.append(precondition)
        
        return list(plan)
    
    def _partial_order_planning(self, goal: str, current_state: Dict[str, Any], 
                               constraints: List[str]) -> List[Dict[str, Any]]:
        """Create a partial-order plan allowing parallel execution"""
        # Simplified partial-order planning
        all_actions = self._generate_all_required_actions(goal, current_state)
        
        # Determine dependencies
        dependencies = self._determine_dependencies(all_actions)
        
        # Create partial order
        plan = []
        for action in all_actions:
            plan_step = {
                "type": "partial_order",
                "action": action["name"],
                "dependencies": dependencies.get(action["name"], []),
                "can_parallel": len(dependencies.get(action["name"], [])) == 0,
                "description": f"Action: {action['name']}"
            }
            plan.append(plan_step)
        
        return plan
    
    def _optimize_plan(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize plan for efficiency"""
        # Remove redundant steps
        optimized = []
        seen_actions = set()
        
        for step in plan:
            action_key = (step["type"], step["action"])
            if action_key not in seen_actions:
                optimized.append(step)
                seen_actions.add(action_key)
        
        # Reorder for efficiency (simplified)
        # Put analysis steps first, execution in middle, validation last
        analysis_steps = [s for s in optimized if s["type"] == "analysis"]
        execution_steps = [s for s in optimized if s["type"] in ["execution", "forward", "backward"]]
        validation_steps = [s for s in optimized if s["type"] == "validation"]
        other_steps = [s for s in optimized if s["type"] not in ["analysis", "execution", "forward", "backward", "validation"]]
        
        return analysis_steps + execution_steps + other_steps + validation_steps
    
    def _estimate_success_probability(self, plan: List[Dict[str, Any]]) -> float:
        """Estimate probability of plan success"""
        if not plan:
            return 0.0
        
        # Base probability
        base_prob = 0.8
        
        # Adjust based on plan length (longer plans are riskier)
        length_factor = max(0.5, 1.0 - len(plan) * 0.02)
        
        # Adjust based on plan type diversity
        plan_types = set(step["type"] for step in plan)
        diversity_factor = min(1.0, len(plan_types) * 0.2 + 0.4)
        
        return base_prob * length_factor * diversity_factor
    
    def _decompose_problem(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose complex problem into sub-problems"""
        # Simplified decomposition
        sub_problems = [
            {"name": "understand_requirements", "complexity": 0.3},
            {"name": "identify_components", "complexity": 0.4},
            {"name": "design_solution", "complexity": 0.6},
            {"name": "implement_components", "complexity": 0.5},
            {"name": "integrate_solution", "complexity": 0.7}
        ]
        
        return sub_problems
    
    def _create_sub_plan(self, sub_problem: Dict[str, Any], 
                        reasoning_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create plan for a sub-problem"""
        return [
            {
                "type": "sub_problem",
                "action": f"solve_{sub_problem['name']}",
                "complexity": sub_problem["complexity"],
                "description": f"Solve: {sub_problem['name']}"
            }
        ]
    
    def _create_direct_plan(self, problem: Dict[str, Any], 
                           reasoning_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create direct plan for simple problem"""
        return [
            {
                "type": "direct",
                "action": "analyze_problem",
                "description": "Analyze the problem"
            },
            {
                "type": "direct",
                "action": "apply_solution",
                "description": "Apply direct solution"
            }
        ]
    
    def _identify_differences(self, current_state: Dict[str, Any], goal: str) -> List[str]:
        """Identify differences between current state and goal"""
        # Simplified difference identification
        differences = []
        
        if "solve" in goal.lower() and not current_state.get("solved", False):
            differences.append("problem_not_solved")
        
        if "optimize" in goal.lower() and current_state.get("efficiency", 0.5) < 0.8:
            differences.append("not_optimized")
        
        if "learn" in goal.lower() and not current_state.get("learned", False):
            differences.append("knowledge_gap")
        
        return differences if differences else ["general_goal_not_met"]
    
    def _find_means_for_difference(self, difference: str) -> Dict[str, str]:
        """Find means to reduce a specific difference"""
        means_map = {
            "problem_not_solved": {"action": "apply_problem_solving"},
            "not_optimized": {"action": "optimize_performance"},
            "knowledge_gap": {"action": "acquire_knowledge"},
            "general_goal_not_met": {"action": "work_toward_goal"}
        }
        
        return means_map.get(difference, {"action": "general_action"})
    
    def _goal_achieved(self, state: Dict[str, Any], goal: str) -> bool:
        """Check if goal is achieved in current state"""
        # Simplified goal checking
        return state.get("goal_achieved", False) or state.get("steps_taken", 0) > 5
    
    def _find_applicable_actions(self, state: Dict[str, Any], 
                                constraints: List[str]) -> List[Dict[str, Any]]:
        """Find actions applicable in current state"""
        # Simplified action generation
        actions = [
            {
                "name": "analyze",
                "preconditions": [],
                "effects": ["understanding_increased"]
            },
            {
                "name": "process",
                "preconditions": ["understanding_increased"],
                "effects": ["data_processed"]
            },
            {
                "name": "synthesize",
                "preconditions": ["data_processed"],
                "effects": ["solution_created"]
            }
        ]
        
        # Filter by preconditions
        applicable = []
        for action in actions:
            if all(self._satisfied_in_state(pre, state) for pre in action["preconditions"]):
                applicable.append(action)
        
        return applicable if applicable else [actions[0]]  # Always have at least one action
    
    def _select_best_action(self, actions: List[Dict[str, Any]], goal: str) -> Dict[str, Any]:
        """Select best action from available actions"""
        # Simple heuristic: prefer actions with more effects
        return max(actions, key=lambda a: len(a.get("effects", [])))
    
    def _apply_action_effects(self, state: Dict[str, Any], 
                             action: Dict[str, Any]) -> Dict[str, Any]:
        """Apply action effects to state"""
        new_state = state.copy()
        
        for effect in action.get("effects", []):
            new_state[effect] = True
        
        new_state["steps_taken"] = state.get("steps_taken", 0) + 1
        
        return new_state
    
    def _find_achieving_actions(self, subgoal: str) -> List[Dict[str, Any]]:
        """Find actions that can achieve a subgoal"""
        # Simplified action database
        action_db = {
            "solve_problem": [{"name": "apply_algorithm", "preconditions": ["problem_understood"]}],
            "understand_problem": [{"name": "analyze_requirements", "preconditions": []}],
            "optimize_solution": [{"name": "refine_approach", "preconditions": ["initial_solution"]}]
        }
        
        # Match subgoal to actions
        for key in action_db:
            if key in subgoal.lower() or subgoal.lower() in key:
                return action_db[key]
        
        # Default action
        return [{"name": "work_on_subgoal", "preconditions": []}]
    
    def _satisfied_in_state(self, condition: str, state: Dict[str, Any]) -> bool:
        """Check if condition is satisfied in state"""
        return state.get(condition, False)
    
    def _generate_all_required_actions(self, goal: str, 
                                      current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate all actions required for goal"""
        # Simplified generation
        return [
            {"name": "initialize", "type": "setup"},
            {"name": "analyze_goal", "type": "analysis"},
            {"name": "gather_resources", "type": "preparation"},
            {"name": "execute_main_task", "type": "execution"},
            {"name": "verify_completion", "type": "validation"}
        ]
    
    def _determine_dependencies(self, actions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Determine dependencies between actions"""
        dependencies = {
            "analyze_goal": ["initialize"],
            "gather_resources": ["analyze_goal"],
            "execute_main_task": ["gather_resources"],
            "verify_completion": ["execute_main_task"]
        }
        
        return dependencies
