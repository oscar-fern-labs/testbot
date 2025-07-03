"""
Task Environment Module

Provides various environments and tasks for the AGI to solve and learn from.
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod


class Task(ABC):
    """Abstract base class for tasks"""
    
    @abstractmethod
    def get_description(self) -> str:
        """Get task description"""
        pass
    
    @abstractmethod
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        """Evaluate a solution"""
        pass
    
    @abstractmethod
    def get_initial_state(self) -> Any:
        """Get initial state for the task"""
        pass


class LogicPuzzle(Task):
    """Logic puzzle tasks"""
    
    def __init__(self, puzzle_type: str = "syllogism"):
        self.puzzle_type = puzzle_type
        self.puzzle = self._generate_puzzle()
        
    def _generate_puzzle(self) -> Dict[str, Any]:
        """Generate a logic puzzle"""
        if self.puzzle_type == "syllogism":
            premises = [
                "All humans are mortal",
                "Socrates is a human"
            ]
            question = "Is Socrates mortal?"
            answer = True
        elif self.puzzle_type == "knights_knaves":
            premises = [
                "Knights always tell the truth",
                "Knaves always lie",
                "Person A says: 'I am a knave'"
            ]
            question = "What is Person A?"
            answer = "knave"  # If they were a knight, they couldn't say they're a knave
        else:
            premises = ["If it rains, the ground gets wet", "The ground is wet"]
            question = "Did it rain?"
            answer = "possibly"  # Could be other causes
            
        return {
            "premises": premises,
            "question": question,
            "answer": answer
        }
    
    def get_description(self) -> str:
        return f"Logic Puzzle ({self.puzzle_type}): Given the premises, answer the question."
    
    def get_initial_state(self) -> Any:
        return {
            "premises": self.puzzle["premises"],
            "question": self.puzzle["question"]
        }
    
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        correct = str(solution).lower() == str(self.puzzle["answer"]).lower()
        
        return {
            "correct": correct,
            "expected": self.puzzle["answer"],
            "provided": solution,
            "score": 1.0 if correct else 0.0
        }


class MathProblem(Task):
    """Mathematical problem tasks"""
    
    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.problem = self._generate_problem()
        
    def _generate_problem(self) -> Dict[str, Any]:
        """Generate a math problem"""
        if self.difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
            operation = random.choice(["+", "-", "*"])
            if operation == "+":
                answer = a + b
            elif operation == "-":
                answer = a - b
            else:
                answer = a * b
            expression = f"{a} {operation} {b}"
        elif self.difficulty == "medium":
            a = random.randint(1, 10)
            b = random.randint(2, 5)
            answer = a ** b
            expression = f"{a}^{b}"
        else:  # hard
            # Simple equation
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            answer = (b - 5) / a if a != 0 else 0
            expression = f"{a}x + 5 = {b}"
            
        return {
            "expression": expression,
            "answer": answer,
            "type": "arithmetic" if self.difficulty == "easy" else "algebra"
        }
    
    def get_description(self) -> str:
        return f"Math Problem ({self.difficulty}): Solve the expression"
    
    def get_initial_state(self) -> Any:
        return {
            "expression": self.problem["expression"],
            "type": self.problem["type"]
        }
    
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        try:
            numeric_solution = float(solution)
            error = abs(numeric_solution - self.problem["answer"])
            correct = error < 0.001
            score = max(0, 1 - error / abs(self.problem["answer"] + 1))
        except:
            correct = False
            score = 0.0
            
        return {
            "correct": correct,
            "expected": self.problem["answer"],
            "provided": solution,
            "score": score
        }


class PatternRecognition(Task):
    """Pattern recognition tasks"""
    
    def __init__(self, pattern_type: str = "numeric"):
        self.pattern_type = pattern_type
        self.pattern = self._generate_pattern()
        
    def _generate_pattern(self) -> Dict[str, Any]:
        """Generate a pattern recognition task"""
        if self.pattern_type == "numeric":
            # Arithmetic sequence
            start = random.randint(1, 10)
            diff = random.randint(1, 5)
            sequence = [start + i * diff for i in range(5)]
            answer = sequence[-1] + diff
            sequence = sequence[:-1]  # Remove last for question
        elif self.pattern_type == "geometric":
            # Geometric sequence
            start = random.randint(2, 5)
            ratio = random.randint(2, 3)
            sequence = [start * (ratio ** i) for i in range(4)]
            answer = sequence[-1] * ratio
            sequence = sequence[:-1]
        else:  # alphabetic
            # Simple letter pattern
            start_ord = ord('A') + random.randint(0, 20)
            step = random.randint(1, 3)
            sequence = [chr(start_ord + i * step) for i in range(4)]
            answer = chr(start_ord + 4 * step)
            sequence = sequence[:-1]
            
        return {
            "sequence": sequence,
            "answer": answer,
            "rule": f"{self.pattern_type} pattern"
        }
    
    def get_description(self) -> str:
        return f"Pattern Recognition ({self.pattern_type}): Find the next element in the sequence"
    
    def get_initial_state(self) -> Any:
        return {
            "sequence": self.pattern["sequence"],
            "type": self.pattern_type
        }
    
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        correct = str(solution) == str(self.pattern["answer"])
        
        return {
            "correct": correct,
            "expected": self.pattern["answer"],
            "provided": solution,
            "score": 1.0 if correct else 0.0,
            "pattern_rule": self.pattern["rule"]
        }


class PlanningTask(Task):
    """Planning and optimization tasks"""
    
    def __init__(self, task_type: str = "path_finding"):
        self.task_type = task_type
        self.task = self._generate_task()
        
    def _generate_task(self) -> Dict[str, Any]:
        """Generate a planning task"""
        if self.task_type == "path_finding":
            # Simple grid path finding
            grid_size = 5
            start = (0, 0)
            goal = (4, 4)
            obstacles = [(2, 2), (2, 3), (3, 2)]
            optimal_length = 8  # Manhattan distance with obstacles
            
            return {
                "grid_size": grid_size,
                "start": start,
                "goal": goal,
                "obstacles": obstacles,
                "optimal_length": optimal_length
            }
        else:  # resource allocation
            resources = 100
            tasks = [
                {"name": "A", "cost": 30, "value": 50},
                {"name": "B", "cost": 40, "value": 60},
                {"name": "C", "cost": 50, "value": 65},
                {"name": "D", "cost": 20, "value": 30}
            ]
            optimal_selection = ["A", "B", "D"]  # Total cost: 90, value: 140
            
            return {
                "resources": resources,
                "tasks": tasks,
                "optimal": optimal_selection
            }
    
    def get_description(self) -> str:
        return f"Planning Task ({self.task_type}): Find optimal solution"
    
    def get_initial_state(self) -> Any:
        return self.task
    
    def evaluate(self, solution: Any) -> Dict[str, Any]:
        if self.task_type == "path_finding":
            # Evaluate path
            if isinstance(solution, list):
                valid_path = self._validate_path(solution)
                path_length = len(solution)
                optimality = self.task["optimal_length"] / path_length if path_length > 0 else 0
                score = optimality if valid_path else 0.0
            else:
                valid_path = False
                score = 0.0
                
            return {
                "correct": valid_path and path_length == self.task["optimal_length"],
                "valid_path": valid_path,
                "path_length": len(solution) if isinstance(solution, list) else 0,
                "optimal_length": self.task["optimal_length"],
                "score": score
            }
        else:  # resource allocation
            if isinstance(solution, list):
                total_cost = sum(t["cost"] for t in self.task["tasks"] if t["name"] in solution)
                total_value = sum(t["value"] for t in self.task["tasks"] if t["name"] in solution)
                valid = total_cost <= self.task["resources"]
                
                optimal_value = sum(t["value"] for t in self.task["tasks"] 
                                  if t["name"] in self.task["optimal"])
                score = (total_value / optimal_value) if valid and optimal_value > 0 else 0.0
            else:
                valid = False
                score = 0.0
                total_cost = 0
                total_value = 0
                
            return {
                "correct": set(solution) == set(self.task["optimal"]) if isinstance(solution, list) else False,
                "valid": valid,
                "total_cost": total_cost,
                "total_value": total_value,
                "score": score
            }
    
    def _validate_path(self, path: List[Tuple[int, int]]) -> bool:
        """Validate if path is valid"""
        if not path or path[0] != self.task["start"] or path[-1] != self.task["goal"]:
            return False
            
        # Check each step
        for i in range(1, len(path)):
            prev = path[i-1]
            curr = path[i]
            
            # Check if valid move (adjacent)
            if abs(prev[0] - curr[0]) + abs(prev[1] - curr[1]) != 1:
                return False
                
            # Check if not in obstacle
            if curr in self.task["obstacles"]:
                return False
                
        return True


class TaskEnvironment:
    """
    Environment providing various tasks for AGI training and evaluation
    """
    
    def __init__(self):
        self.task_types = {
            "logic": LogicPuzzle,
            "math": MathProblem,
            "pattern": PatternRecognition,
            "planning": PlanningTask
        }
        
        self.current_task = None
        self.task_history = []
        self.performance_stats = {
            task_type: {"attempted": 0, "solved": 0, "total_score": 0.0}
            for task_type in self.task_types
        }
        
    def get_task(self, task_type: str = None, difficulty: str = None) -> Task:
        """
        Get a new task
        
        Args:
            task_type: Type of task (logic, math, pattern, planning)
            difficulty: Difficulty level
            
        Returns:
            Task instance
        """
        if task_type is None:
            task_type = random.choice(list(self.task_types.keys()))
            
        if task_type in self.task_types:
            task_class = self.task_types[task_type]
            
            # Create task with appropriate parameters
            if task_type == "logic":
                puzzle_types = ["syllogism", "knights_knaves", "conditional"]
                task = task_class(random.choice(puzzle_types))
            elif task_type == "math":
                difficulty = difficulty or random.choice(["easy", "medium", "hard"])
                task = task_class(difficulty)
            elif task_type == "pattern":
                pattern_types = ["numeric", "geometric", "alphabetic"]
                task = task_class(random.choice(pattern_types))
            else:  # planning
                planning_types = ["path_finding", "resource_allocation"]
                task = task_class(random.choice(planning_types))
                
            self.current_task = task
            return task
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    def submit_solution(self, solution: Any) -> Dict[str, Any]:
        """
        Submit a solution for the current task
        
        Args:
            solution: Proposed solution
            
        Returns:
            Evaluation results
        """
        if self.current_task is None:
            return {"error": "No active task"}
            
        # Evaluate solution
        evaluation = self.current_task.evaluate(solution)
        
        # Update statistics
        task_type = self._get_task_type(self.current_task)
        self.performance_stats[task_type]["attempted"] += 1
        if evaluation.get("correct", False):
            self.performance_stats[task_type]["solved"] += 1
        self.performance_stats[task_type]["total_score"] += evaluation.get("score", 0.0)
        
        # Store in history
        self.task_history.append({
            "task": self.current_task,
            "solution": solution,
            "evaluation": evaluation,
            "task_type": task_type
        })
        
        return evaluation
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance statistics"""
        report = {}
        
        for task_type, stats in self.performance_stats.items():
            if stats["attempted"] > 0:
                report[task_type] = {
                    "attempted": stats["attempted"],
                    "solved": stats["solved"],
                    "success_rate": stats["solved"] / stats["attempted"],
                    "average_score": stats["total_score"] / stats["attempted"]
                }
            else:
                report[task_type] = {
                    "attempted": 0,
                    "solved": 0,
                    "success_rate": 0.0,
                    "average_score": 0.0
                }
                
        report["overall"] = {
            "total_attempted": sum(s["attempted"] for s in self.performance_stats.values()),
            "total_solved": sum(s["solved"] for s in self.performance_stats.values()),
            "overall_success_rate": (
                sum(s["solved"] for s in self.performance_stats.values()) /
                max(1, sum(s["attempted"] for s in self.performance_stats.values()))
            )
        }
        
        return report
    
    def get_task_batch(self, size: int = 5, balanced: bool = True) -> List[Task]:
        """Get a batch of tasks"""
        tasks = []
        
        if balanced:
            # Get equal number of each type
            for task_type in self.task_types:
                for _ in range(size // len(self.task_types)):
                    tasks.append(self.get_task(task_type))
            
            # Fill remaining with random tasks
            while len(tasks) < size:
                tasks.append(self.get_task())
        else:
            # Random selection
            for _ in range(size):
                tasks.append(self.get_task())
                
        return tasks
    
    def _get_task_type(self, task: Task) -> str:
        """Determine task type from task instance"""
        for task_type, task_class in self.task_types.items():
            if isinstance(task, task_class):
                return task_type
        return "unknown"
    
    def create_custom_task(self, task_spec: Dict[str, Any]) -> Task:
        """Create a custom task from specification"""
        # This would be extended to support custom task creation
        # For now, return a random task
        return self.get_task()
