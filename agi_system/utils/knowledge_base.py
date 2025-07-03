"""
Knowledge Base Module

Manages structured knowledge, facts, and relationships for the AGI system.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict
import json


class KnowledgeBase:
    """
    Knowledge base for storing and retrieving structured information
    """
    
    def __init__(self):
        # Facts stored as triples: (subject, predicate, object)
        self.facts = []
        
        # Concepts and their properties
        self.concepts = {}
        
        # Relationships between concepts
        self.relationships = defaultdict(list)
        
        # Domain-specific knowledge
        self.domains = {
            "general": {},
            "mathematics": {},
            "logic": {},
            "language": {},
            "problem_solving": {},
            "planning": {},
            "learning": {}
        }
        
        # Inference rules
        self.rules = []
        
        # Initialize with basic knowledge
        self._initialize_basic_knowledge()
        
    def _initialize_basic_knowledge(self):
        """Initialize knowledge base with fundamental concepts"""
        # Basic logical concepts
        self.add_concept("true", {"type": "boolean", "value": True})
        self.add_concept("false", {"type": "boolean", "value": False})
        
        # Basic relationships
        self.add_concept("is_a", {"type": "relationship", "transitive": True})
        self.add_concept("part_of", {"type": "relationship", "transitive": True})
        self.add_concept("causes", {"type": "relationship", "transitive": False})
        
        # Basic inference rules
        self.add_rule({
            "name": "transitive_property",
            "if": ["(A, R, B)", "(B, R, C)", "R.transitive = True"],
            "then": "(A, R, C)"
        })
        
        self.add_rule({
            "name": "symmetry",
            "if": ["(A, R, B)", "R.symmetric = True"],
            "then": "(B, R, A)"
        })
        
        # Problem-solving knowledge
        self.add_fact("problem_solving", "requires", "analysis")
        self.add_fact("problem_solving", "requires", "planning")
        self.add_fact("problem_solving", "produces", "solution")
        
        # Learning knowledge
        self.add_fact("learning", "improves", "performance")
        self.add_fact("learning", "requires", "experience")
        self.add_fact("learning", "requires", "feedback")
        
    def add_concept(self, concept: str, properties: Dict[str, Any]) -> bool:
        """
        Add a concept to the knowledge base
        
        Args:
            concept: Name of the concept
            properties: Properties of the concept
            
        Returns:
            Success status
        """
        self.concepts[concept] = properties
        
        # Add to appropriate domain
        domain = properties.get("domain", "general")
        if domain in self.domains:
            self.domains[domain][concept] = properties
        
        return True
    
    def add_fact(self, subject: str, predicate: str, obj: str) -> bool:
        """
        Add a fact to the knowledge base
        
        Args:
            subject: Subject of the fact
            predicate: Relationship/predicate
            obj: Object of the fact
            
        Returns:
            Success status
        """
        fact = (subject, predicate, obj)
        
        if fact not in self.facts:
            self.facts.append(fact)
            
            # Update relationships index
            self.relationships[subject].append((predicate, obj))
            
            # Check for inverse relationships
            if predicate in self.concepts:
                if self.concepts[predicate].get("inverse"):
                    inverse_pred = self.concepts[predicate]["inverse"]
                    self.facts.append((obj, inverse_pred, subject))
                    self.relationships[obj].append((inverse_pred, subject))
        
        return True
    
    def add_rule(self, rule: Dict[str, Any]) -> bool:
        """
        Add an inference rule
        
        Args:
            rule: Rule specification with 'if' and 'then' clauses
            
        Returns:
            Success status
        """
        if "name" in rule and "if" in rule and "then" in rule:
            self.rules.append(rule)
            return True
        return False
    
    def query(self, query: str) -> List[Any]:
        """
        Query the knowledge base
        
        Args:
            query: Natural language or structured query
            
        Returns:
            List of relevant facts/concepts
        """
        results = []
        
        # Parse query (simplified)
        query_lower = query.lower()
        
        # Check for concept queries
        for concept in self.concepts:
            if concept.lower() in query_lower:
                results.append({
                    "type": "concept",
                    "name": concept,
                    "properties": self.concepts[concept]
                })
        
        # Check for fact queries
        for fact in self.facts:
            if any(term.lower() in query_lower for term in fact):
                results.append({
                    "type": "fact",
                    "subject": fact[0],
                    "predicate": fact[1],
                    "object": fact[2]
                })
        
        # Apply inference if needed
        if "infer" in query_lower or "deduce" in query_lower:
            inferred = self._apply_inference(query)
            results.extend(inferred)
        
        return results
    
    def get_related(self, concept: str, relationship: str = None) -> List[Tuple[str, str]]:
        """
        Get concepts related to a given concept
        
        Args:
            concept: Concept to find relations for
            relationship: Specific relationship to filter by
            
        Returns:
            List of (relationship, related_concept) tuples
        """
        if concept not in self.relationships:
            return []
        
        if relationship:
            return [
                (pred, obj) for pred, obj in self.relationships[concept]
                if pred == relationship
            ]
        else:
            return self.relationships[concept]
    
    def infer_new_facts(self) -> List[Tuple[str, str, str]]:
        """
        Apply inference rules to derive new facts
        
        Returns:
            List of newly inferred facts
        """
        new_facts = []
        
        for rule in self.rules:
            # Apply each rule
            inferred = self._apply_rule(rule)
            for fact in inferred:
                if fact not in self.facts and fact not in new_facts:
                    new_facts.append(fact)
        
        # Add new facts to knowledge base
        for fact in new_facts:
            self.add_fact(fact[0], fact[1], fact[2])
        
        return new_facts
    
    def explain(self, fact: Tuple[str, str, str]) -> Dict[str, Any]:
        """
        Explain how a fact was derived
        
        Args:
            fact: Fact to explain
            
        Returns:
            Explanation including derivation chain
        """
        if fact in self.facts:
            # Check if it's a base fact
            base_facts = self._get_base_facts()
            if fact in base_facts:
                return {
                    "fact": fact,
                    "type": "base_fact",
                    "explanation": "This is a fundamental fact in the knowledge base"
                }
            
            # Try to find derivation
            for rule in self.rules:
                if self._fact_matches_rule_conclusion(fact, rule):
                    premises = self._get_rule_premises_for_fact(fact, rule)
                    return {
                        "fact": fact,
                        "type": "derived",
                        "rule": rule["name"],
                        "premises": premises,
                        "explanation": f"Derived using {rule['name']} rule"
                    }
        
        return {
            "fact": fact,
            "type": "unknown",
            "explanation": "Fact not found or derivation unknown"
        }
    
    def get_domains(self) -> List[str]:
        """Get list of knowledge domains"""
        return list(self.domains.keys())
    
    def get_domain_knowledge(self, domain: str) -> Dict[str, Any]:
        """Get all knowledge in a specific domain"""
        if domain in self.domains:
            return self.domains[domain]
        return {}
    
    def _apply_inference(self, query: str) -> List[Dict[str, Any]]:
        """Apply inference based on query"""
        inferred = []
        
        # Simple inference based on transitivity
        for rule in self.rules:
            if rule["name"] == "transitive_property":
                # Find transitive chains
                for fact1 in self.facts:
                    for fact2 in self.facts:
                        if (fact1[2] == fact2[0] and 
                            fact1[1] == fact2[1] and
                            fact1[1] in self.concepts and
                            self.concepts[fact1[1]].get("transitive", False)):
                            
                            new_fact = (fact1[0], fact1[1], fact2[2])
                            if new_fact not in self.facts:
                                inferred.append({
                                    "type": "inferred_fact",
                                    "subject": new_fact[0],
                                    "predicate": new_fact[1],
                                    "object": new_fact[2],
                                    "rule": "transitivity"
                                })
        
        return inferred
    
    def _apply_rule(self, rule: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        """Apply a single inference rule"""
        new_facts = []
        
        if rule["name"] == "transitive_property":
            # Find all transitive relationships
            for rel in self.concepts:
                if self.concepts[rel].get("transitive", False):
                    # Find chains
                    for fact1 in self.facts:
                        if fact1[1] == rel:
                            for fact2 in self.facts:
                                if fact2[1] == rel and fact1[2] == fact2[0]:
                                    new_fact = (fact1[0], rel, fact2[2])
                                    if new_fact not in self.facts:
                                        new_facts.append(new_fact)
        
        return new_facts
    
    def _get_base_facts(self) -> List[Tuple[str, str, str]]:
        """Get facts that were not derived"""
        # For simplicity, return first 10 facts as base facts
        return self.facts[:10]
    
    def _fact_matches_rule_conclusion(self, fact: Tuple[str, str, str], 
                                     rule: Dict[str, Any]) -> bool:
        """Check if fact matches rule conclusion pattern"""
        # Simplified pattern matching
        conclusion = rule.get("then", "")
        
        if isinstance(conclusion, str) and "(" in conclusion:
            # Extract pattern
            return True  # Simplified
        
        return False
    
    def _get_rule_premises_for_fact(self, fact: Tuple[str, str, str], 
                                   rule: Dict[str, Any]) -> List[Any]:
        """Get premises that led to fact through rule"""
        # Simplified - return some related facts
        premises = []
        
        for f in self.facts:
            if f[0] == fact[0] or f[2] == fact[0]:
                premises.append(f)
                if len(premises) >= 2:
                    break
        
        return premises
    
    def export_knowledge(self) -> Dict[str, Any]:
        """Export knowledge base to dictionary"""
        return {
            "concepts": self.concepts,
            "facts": [{"subject": f[0], "predicate": f[1], "object": f[2]} 
                     for f in self.facts],
            "rules": self.rules,
            "domains": {d: list(k.keys()) for d, k in self.domains.items()}
        }
    
    def import_knowledge(self, knowledge_dict: Dict[str, Any]):
        """Import knowledge from dictionary"""
        # Import concepts
        for concept, props in knowledge_dict.get("concepts", {}).items():
            self.add_concept(concept, props)
        
        # Import facts
        for fact in knowledge_dict.get("facts", []):
            self.add_fact(fact["subject"], fact["predicate"], fact["object"])
        
        # Import rules
        for rule in knowledge_dict.get("rules", []):
            self.add_rule(rule)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get knowledge base statistics"""
        return {
            "total_concepts": len(self.concepts),
            "total_facts": len(self.facts),
            "total_rules": len(self.rules),
            "total_relationships": sum(len(rels) for rels in self.relationships.values()),
            "domains_populated": sum(1 for d in self.domains.values() if d)
        }
