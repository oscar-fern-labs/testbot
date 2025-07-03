"""
Memory System Module

Implements short-term and long-term memory for the AGI system.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import deque, defaultdict
import json


class MemorySystem:
    """
    Memory system with short-term and long-term storage
    """
    
    def __init__(self, short_term_capacity: int = 100, long_term_capacity: int = 10000):
        # Short-term memory (working memory)
        self.short_term = deque(maxlen=short_term_capacity)
        
        # Long-term memory organized by category
        self.long_term = defaultdict(list)
        self.long_term_capacity = long_term_capacity
        
        # Episodic memory for experiences
        self.episodic_memory = deque(maxlen=1000)
        
        # Semantic memory for facts and concepts
        self.semantic_memory = {}
        
        # Memory indexing for fast retrieval
        self.memory_index = defaultdict(list)
        
        # Memory consolidation queue
        self.consolidation_queue = deque()
        
        self.total_memories = 0
        
    def store(self, memory_type: str, content: Any, context: str = None, 
              importance: float = 0.5) -> str:
        """
        Store a memory in the system
        
        Args:
            memory_type: Type of memory (e.g., "experience", "fact", "skill")
            content: The memory content
            context: Context in which memory was formed
            importance: Importance score (0-1)
            
        Returns:
            Memory ID
        """
        memory_id = f"mem_{self.total_memories}"
        
        memory_entry = {
            "id": memory_id,
            "type": memory_type,
            "content": content,
            "context": context,
            "importance": importance,
            "timestamp": datetime.now(),
            "access_count": 0,
            "last_accessed": datetime.now()
        }
        
        # Store in short-term memory
        self.short_term.append(memory_entry)
        
        # Index the memory
        self._index_memory(memory_entry)
        
        # Queue for consolidation if important
        if importance > 0.7:
            self.consolidation_queue.append(memory_entry)
        
        self.total_memories += 1
        
        # Consolidate memories if needed
        if len(self.consolidation_queue) > 10:
            self._consolidate_memories()
        
        return memory_id
    
    def recall(self, query: Any, context: str = None, 
               limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recall memories based on query
        
        Args:
            query: Query for memory retrieval
            context: Context to help retrieval
            limit: Maximum number of memories to return
            
        Returns:
            List of relevant memories
        """
        # Search short-term memory first
        short_term_results = self._search_short_term(query, context)
        
        # Search long-term memory
        long_term_results = self._search_long_term(query, context)
        
        # Combine and rank results
        all_results = short_term_results + long_term_results
        ranked_results = self._rank_memories(all_results, query, context)
        
        # Update access counts
        for memory in ranked_results[:limit]:
            memory["access_count"] += 1
            memory["last_accessed"] = datetime.now()
        
        return ranked_results[:limit]
    
    def get_recent(self, memory_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories, optionally filtered by type"""
        recent = list(self.short_term)
        
        if memory_type:
            recent = [m for m in recent if m["type"] == memory_type]
        
        return recent[-limit:]
    
    def forget(self, memory_id: str) -> bool:
        """
        Remove a memory from the system
        
        Args:
            memory_id: ID of memory to forget
            
        Returns:
            True if memory was forgotten
        """
        # Remove from short-term
        self.short_term = deque(
            [m for m in self.short_term if m["id"] != memory_id],
            maxlen=self.short_term.maxlen
        )
        
        # Remove from long-term
        for category in self.long_term:
            self.long_term[category] = [
                m for m in self.long_term[category] 
                if m["id"] != memory_id
            ]
        
        # Remove from indices
        self._remove_from_index(memory_id)
        
        return True
    
    def consolidate(self) -> int:
        """
        Consolidate short-term memories into long-term storage
        
        Returns:
            Number of memories consolidated
        """
        return self._consolidate_memories()
    
    def size(self) -> Dict[str, int]:
        """Get memory system size statistics"""
        return {
            "short_term": len(self.short_term),
            "long_term": sum(len(mems) for mems in self.long_term.values()),
            "episodic": len(self.episodic_memory),
            "semantic": len(self.semantic_memory),
            "total": self.total_memories
        }
    
    def _index_memory(self, memory: Dict[str, Any]):
        """Index memory for fast retrieval"""
        # Index by type
        self.memory_index[f"type:{memory['type']}"].append(memory["id"])
        
        # Index by context
        if memory["context"]:
            self.memory_index[f"context:{memory['context']}"].append(memory["id"])
        
        # Index by content keywords (simplified)
        content_str = str(memory["content"])
        keywords = content_str.lower().split()[:5]  # First 5 words
        for keyword in keywords:
            if len(keyword) > 3:  # Only meaningful words
                self.memory_index[f"keyword:{keyword}"].append(memory["id"])
    
    def _search_short_term(self, query: Any, context: str = None) -> List[Dict[str, Any]]:
        """Search short-term memory"""
        results = []
        query_str = str(query).lower()
        
        for memory in self.short_term:
            relevance = self._calculate_relevance(memory, query_str, context)
            if relevance > 0.3:
                results.append(memory)
        
        return results
    
    def _search_long_term(self, query: Any, context: str = None) -> List[Dict[str, Any]]:
        """Search long-term memory"""
        results = []
        query_str = str(query).lower()
        
        # Search relevant categories
        relevant_categories = self._identify_relevant_categories(query_str, context)
        
        for category in relevant_categories:
            for memory in self.long_term.get(category, []):
                relevance = self._calculate_relevance(memory, query_str, context)
                if relevance > 0.3:
                    results.append(memory)
        
        return results
    
    def _calculate_relevance(self, memory: Dict[str, Any], 
                           query: str, context: str = None) -> float:
        """Calculate relevance of memory to query"""
        relevance = 0.0
        
        # Content similarity
        content_str = str(memory["content"]).lower()
        query_words = query.split()
        matches = sum(1 for word in query_words if word in content_str)
        relevance += matches / max(len(query_words), 1) * 0.5
        
        # Context match
        if context and memory["context"] == context:
            relevance += 0.3
        
        # Recency bonus
        time_diff = (datetime.now() - memory["timestamp"]).total_seconds()
        recency_score = max(0, 1 - time_diff / (24 * 3600))  # Decay over 24 hours
        relevance += recency_score * 0.1
        
        # Importance factor
        relevance += memory["importance"] * 0.1
        
        return min(1.0, relevance)
    
    def _rank_memories(self, memories: List[Dict[str, Any]], 
                      query: Any, context: str = None) -> List[Dict[str, Any]]:
        """Rank memories by relevance"""
        query_str = str(query).lower()
        
        scored_memories = []
        for memory in memories:
            score = self._calculate_relevance(memory, query_str, context)
            scored_memories.append((score, memory))
        
        # Sort by score descending
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        return [memory for score, memory in scored_memories]
    
    def _consolidate_memories(self) -> int:
        """Consolidate memories from short-term to long-term"""
        consolidated = 0
        
        while self.consolidation_queue:
            memory = self.consolidation_queue.popleft()
            
            # Determine category for long-term storage
            category = self._categorize_memory(memory)
            
            # Check capacity
            if len(self.long_term[category]) >= self.long_term_capacity // 10:
                # Remove least important old memory
                self._remove_least_important(category)
            
            # Store in long-term
            self.long_term[category].append(memory)
            
            # Store in episodic if it's an experience
            if memory["type"] == "experience":
                self.episodic_memory.append(memory)
            
            # Store in semantic if it's a fact
            if memory["type"] == "fact":
                fact_key = self._extract_fact_key(memory["content"])
                self.semantic_memory[fact_key] = memory
            
            consolidated += 1
        
        return consolidated
    
    def _categorize_memory(self, memory: Dict[str, Any]) -> str:
        """Categorize memory for long-term storage"""
        memory_type = memory["type"]
        
        category_map = {
            "experience": "episodic",
            "fact": "semantic",
            "skill": "procedural",
            "emotion": "emotional",
            "goal": "motivational"
        }
        
        return category_map.get(memory_type, "general")
    
    def _remove_least_important(self, category: str):
        """Remove least important memory from category"""
        if not self.long_term[category]:
            return
        
        # Find memory with lowest importance and access count
        least_important = min(
            self.long_term[category],
            key=lambda m: m["importance"] + m["access_count"] / 100
        )
        
        self.long_term[category].remove(least_important)
        self._remove_from_index(least_important["id"])
    
    def _remove_from_index(self, memory_id: str):
        """Remove memory from all indices"""
        for key in list(self.memory_index.keys()):
            self.memory_index[key] = [
                mid for mid in self.memory_index[key] 
                if mid != memory_id
            ]
            if not self.memory_index[key]:
                del self.memory_index[key]
    
    def _identify_relevant_categories(self, query: str, context: str = None) -> List[str]:
        """Identify which categories might contain relevant memories"""
        categories = []
        
        # Check based on query content
        if any(word in query for word in ["remember", "experience", "when", "happened"]):
            categories.append("episodic")
        
        if any(word in query for word in ["fact", "know", "what", "define"]):
            categories.append("semantic")
        
        if any(word in query for word in ["how", "procedure", "method", "skill"]):
            categories.append("procedural")
        
        # Default to all categories if none specific
        if not categories:
            categories = list(self.long_term.keys())
        
        return categories
    
    def _extract_fact_key(self, content: Any) -> str:
        """Extract key for semantic memory storage"""
        if isinstance(content, dict) and "subject" in content:
            return content["subject"]
        elif isinstance(content, str):
            # Use first few words as key
            return content.split()[:3].join("_")
        else:
            return str(content)[:50]
    
    def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve specific memory by ID"""
        # Check short-term
        for memory in self.short_term:
            if memory["id"] == memory_id:
                return memory
        
        # Check long-term
        for category in self.long_term:
            for memory in self.long_term[category]:
                if memory["id"] == memory_id:
                    return memory
        
        return None
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get detailed memory statistics"""
        total_access = sum(m["access_count"] for m in self.short_term)
        
        for mems in self.long_term.values():
            total_access += sum(m["access_count"] for m in mems)
        
        return {
            "size": self.size(),
            "total_accesses": total_access,
            "categories": list(self.long_term.keys()),
            "consolidation_pending": len(self.consolidation_queue),
            "index_size": len(self.memory_index)
        }
