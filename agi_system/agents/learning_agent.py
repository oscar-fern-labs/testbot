"""
Learning Agent Module

Handles learning from experience, pattern recognition, and knowledge acquisition.
"""

import random
from typing import Dict, List, Any, Optional
from collections import defaultdict


class LearningAgent:
    """
    Agent responsible for learning and adapting from experience
    """
    
    def __init__(self):
        self.learning_rate = 0.1
        self.experiences = []
        self.learned_patterns = defaultdict(list)
        self.skill_improvements = defaultdict(float)
        self.meta_learning_insights = []
        
    def learn_from_experience(self, input_data: Any, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Learn from a new experience
        
        Args:
            input_data: The input that was processed
            analysis: The analysis/results from processing
            
        Returns:
            Learning outcomes and improvements
        """
        experience = {
            "input": input_data,
            "analysis": analysis,
            "timestamp": len(self.experiences),
            "success_score": self._evaluate_success(analysis)
        }
        
        self.experiences.append(experience)
        
        # Extract patterns
        patterns = self._extract_patterns(input_data, analysis)
        for pattern in patterns:
            self.learned_patterns[pattern["type"]].append(pattern)
        
        # Update skills based on experience
        improvements = self._calculate_improvements(analysis)
        
        # Meta-learning: learn about learning
        meta_insight = self._meta_learn(experience)
        if meta_insight:
            self.meta_learning_insights.append(meta_insight)
        
        return {
            "patterns_learned": len(patterns),
            "improvements": improvements,
            "total_experiences": len(self.experiences),
            "meta_insights": meta_insight
        }
    
    def update_from_problem(self, problem: Dict[str, Any], solution: Dict[str, Any]):
        """Update learning based on problem-solving experience"""
        # Analyze problem-solution pair
        learning_data = {
            "problem_type": problem.get("type", "unknown"),
            "solution_method": solution.get("method_used", "unknown"),
            "success": solution.get("solution_found", False),
            "steps": len(solution.get("reasoning_steps", []))
        }
        
        # Update learning rate based on success
        if learning_data["success"]:
            self.learning_rate = min(0.3, self.learning_rate * 1.05)
        else:
            self.learning_rate = max(0.05, self.learning_rate * 0.95)
        
        # Store problem-solution pattern
        self.learned_patterns["problem_solutions"].append({
            "problem": problem,
            "solution": solution,
            "learning": learning_data
        })
    
    def suggest_improvements(self, solution: Any) -> List[Dict[str, Any]]:
        """Suggest improvements based on learned patterns"""
        suggestions = []
        
        # Analyze solution against known patterns
        similar_experiences = self._find_similar_experiences(solution)
        
        for exp in similar_experiences[:3]:
            if exp.get("success_score", 0) > 0.8:
                suggestion = {
                    "based_on": "previous_success",
                    "improvement": self._generate_improvement_from_experience(exp),
                    "confidence": exp.get("success_score", 0.5)
                }
                suggestions.append(suggestion)
        
        # Add meta-learning suggestions
        if self.meta_learning_insights:
            latest_insight = self.meta_learning_insights[-1]
            suggestions.append({
                "based_on": "meta_learning",
                "improvement": latest_insight.get("recommendation", "Continue learning"),
                "confidence": 0.7
            })
        
        return suggestions
    
    def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a learning step"""
        step_type = step.get("learning_type", "supervised")
        
        if step_type == "supervised":
            result = self._supervised_learning(step.get("data"), step.get("labels"))
        elif step_type == "unsupervised":
            result = self._unsupervised_learning(step.get("data"))
        elif step_type == "reinforcement":
            result = self._reinforcement_learning(step.get("state"), step.get("reward"))
        else:
            result = {"learned": "Unknown learning type"}
        
        return {
            "status": "completed",
            "result": result,
            "learning_progress": self._calculate_learning_progress()
        }
    
    def _evaluate_success(self, analysis: Dict[str, Any]) -> float:
        """Evaluate the success of an analysis/outcome"""
        score = 0.5  # Base score
        
        # Adjust based on certainty
        score += (analysis.get("certainty", 0.5) - 0.5) * 0.3
        
        # Adjust based on goal achievement
        if analysis.get("goal_achieved", False):
            score += 0.2
        
        # Adjust based on efficiency
        if analysis.get("steps_taken", 10) < 5:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _extract_patterns(self, input_data: Any, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract learnable patterns from experience"""
        patterns = []
        
        # Input-output pattern
        if isinstance(input_data, str) and "patterns" in analysis:
            for pattern_type in analysis["patterns"]:
                patterns.append({
                    "type": "input_pattern",
                    "pattern": pattern_type,
                    "frequency": 1,
                    "context": str(input_data)[:100]
                })
        
        # Success patterns
        if analysis.get("certainty", 0) > 0.8:
            patterns.append({
                "type": "high_certainty_pattern",
                "features": self._extract_success_features(analysis),
                "outcome": "successful"
            })
        
        return patterns
    
    def _calculate_improvements(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate skill improvements from analysis"""
        improvements = {}
        
        for capability in analysis.get("required_capabilities", []):
            current_skill = self.skill_improvements.get(capability, 0)
            improvement = self.learning_rate * (1 - current_skill) * random.uniform(0.5, 1.0)
            self.skill_improvements[capability] = current_skill + improvement
            improvements[capability] = improvement
        
        return improvements
    
    def _meta_learn(self, experience: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Learn about the learning process itself"""
        if len(self.experiences) < 10:
            return None
        
        # Analyze recent learning effectiveness
        recent_scores = [
            exp.get("success_score", 0.5) 
            for exp in self.experiences[-10:]
        ]
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        # Generate meta-insight
        if avg_recent > 0.7:
            return {
                "insight": "Current learning approach is effective",
                "recommendation": "Maintain current learning rate",
                "effectiveness": avg_recent
            }
        elif avg_recent < 0.4:
            return {
                "insight": "Learning effectiveness is low",
                "recommendation": "Increase exploration and try new approaches",
                "effectiveness": avg_recent
            }
        
        return None
    
    def _find_similar_experiences(self, solution: Any) -> List[Dict[str, Any]]:
        """Find experiences similar to the current solution"""
        similar = []
        
        solution_str = str(solution)[:100]
        
        for exp in self.experiences[-20:]:  # Check recent experiences
            exp_str = str(exp.get("input", ""))[:100]
            similarity = self._calculate_similarity(solution_str, exp_str)
            
            if similarity > 0.5:
                similar.append(exp)
        
        return sorted(similar, key=lambda x: x.get("success_score", 0), reverse=True)
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Simple similarity calculation between strings"""
        # Very simplified - in real AGI would use embeddings
        common_words = set(str1.split()) & set(str2.split())
        total_words = set(str1.split()) | set(str2.split())
        
        if not total_words:
            return 0.0
            
        return len(common_words) / len(total_words)
    
    def _generate_improvement_from_experience(self, experience: Dict[str, Any]) -> str:
        """Generate improvement suggestion from successful experience"""
        success_features = experience.get("analysis", {}).get("patterns", [])
        
        if success_features:
            return f"Apply {success_features[0]} pattern for better results"
        
        return "Replicate successful approach from similar problem"
    
    def _calculate_learning_progress(self) -> float:
        """Calculate overall learning progress"""
        if not self.skill_improvements:
            return 0.0
            
        avg_improvement = sum(self.skill_improvements.values()) / len(self.skill_improvements)
        return min(1.0, avg_improvement)
    
    def _supervised_learning(self, data: Any, labels: Any) -> Dict[str, Any]:
        """Perform supervised learning"""
        # Simplified supervised learning simulation
        accuracy = random.uniform(0.7, 0.95)
        
        return {
            "type": "supervised",
            "accuracy": accuracy,
            "patterns_learned": random.randint(1, 5),
            "model_updated": True
        }
    
    def _unsupervised_learning(self, data: Any) -> Dict[str, Any]:
        """Perform unsupervised learning"""
        # Simplified clustering simulation
        clusters_found = random.randint(2, 5)
        
        return {
            "type": "unsupervised",
            "clusters_found": clusters_found,
            "patterns_discovered": random.randint(1, 3),
            "anomalies_detected": random.randint(0, 2)
        }
    
    def _reinforcement_learning(self, state: Any, reward: float) -> Dict[str, Any]:
        """Perform reinforcement learning"""
        # Simplified Q-learning simulation
        action_values_updated = random.randint(1, 4)
        
        return {
            "type": "reinforcement",
            "reward_received": reward,
            "action_values_updated": action_values_updated,
            "exploration_rate": max(0.1, 1.0 - len(self.experiences) / 100)
        }
    
    def _extract_success_features(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract features that led to success"""
        features = []
        
        if analysis.get("certainty", 0) > 0.8:
            features.append("high_certainty")
        
        if analysis.get("patterns"):
            features.extend(analysis["patterns"][:2])
        
        if analysis.get("goal_achieved", False):
            features.append("goal_achieved")
        
        return features
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of all learning"""
        return {
            "total_experiences": len(self.experiences),
            "pattern_types_learned": list(self.learned_patterns.keys()),
            "skills_improved": dict(self.skill_improvements),
            "current_learning_rate": self.learning_rate,
            "meta_insights_count": len(self.meta_learning_insights)
        }
