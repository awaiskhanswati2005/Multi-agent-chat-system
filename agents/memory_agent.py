"""
Memory Agent - Knowledge persistence and retrieval with vector search
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np
from utils.logger import SystemLogger

class MemoryAgent:
    def __init__(self):
        self.name = "Memory"
        self.logger = SystemLogger()
        
        # Memory storage structures
        self.conversation_memory = []
        self.knowledge_base = {}
        self.agent_states = {}
        
        # Simple vector storage (in production, use FAISS or Chroma)
        self.vector_store = {}
        
    def store(self, key: str, value: Any, metadata: Dict[str, Any]) -> Dict[str, bool]:
        """
        Store information with metadata and vector representation
        """
        self.logger.log_agent_action(self.name, "Storing", key)
        
        # Create record with timestamp
        record = {
            'key': key,
            'value': value,
            'metadata': {
                **metadata,
                'timestamp': datetime.now().isoformat(),
                'confidence': metadata.get('confidence', 0.8)
            }
        }
        
        # Store in knowledge base
        self.knowledge_base[key] = record
        
        # Store in conversation memory
        self.conversation_memory.append(record)
        
        # Create and store vector representation
        vector = self._create_vector(key, value)
        self.vector_store[key] = vector
        
        return {'success': True, 'stored': key}
    
    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Retrieve relevant information using keyword and vector similarity search
        """
        self.logger.log_agent_action(self.name, "Retrieving", query)
        
        # Keyword search
        keyword_results = self._keyword_search(query)
        
        # Vector similarity search
        vector_results = self._vector_search(query, top_k)
        
        # Merge and deduplicate results
        all_results = self._merge_results(keyword_results, vector_results)
        
        return {
            'success': True,
            'results': all_results[:top_k],
            'count': len(all_results),
            'query': query
        }
    
    def _keyword_search(self, query: str) -> List[Dict]:
        """Search using keyword matching"""
        query_lower = query.lower()
        results = []
        
        for key, record in self.knowledge_base.items():
            # Check key match
            if any(word in key.lower() for word in query_lower.split()):
                results.append({
                    **record,
                    'match_type': 'keyword_key',
                    'score': 1.0
                })
                continue
            
            # Check value match
            value_str = json.dumps(record['value']).lower()
            if any(word in value_str for word in query_lower.split() if len(word) > 3):
                results.append({
                    **record,
                    'match_type': 'keyword_value',
                    'score': 0.8
                })
        
        # Also search conversation memory
        for record in self.conversation_memory:
            if record['key'] in [r['key'] for r in results]:
                continue
            
            record_str = json.dumps(record).lower()
            if any(word in record_str for word in query_lower.split() if len(word) > 3):
                results.append({
                    **record,
                    'match_type': 'conversation',
                    'score': 0.7
                })
        
        return results
    
    def _vector_search(self, query: str, top_k: int) -> List[Dict]:
        """Search using vector similarity (cosine similarity)"""
        if not self.vector_store:
            return []
        
        query_vector = self._create_vector(query, query)
        
        similarities = []
        for key, stored_vector in self.vector_store.items():
            similarity = self._cosine_similarity(query_vector, stored_vector)
            if similarity > 0.3:  # Threshold
                similarities.append({
                    'key': key,
                    'similarity': similarity
                })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Get full records
        results = []
        for sim in similarities[:top_k]:
            if sim['key'] in self.knowledge_base:
                record = self.knowledge_base[sim['key']]
                results.append({
                    **record,
                    'match_type': 'vector',
                    'score': sim['similarity']
                })
        
        return results
    
    def _merge_results(self, keyword_results: List[Dict], vector_results: List[Dict]) -> List[Dict]:
        """Merge and deduplicate search results"""
        merged = {}
        
        # Add keyword results
        for result in keyword_results:
            key = result['key']
            merged[key] = result
        
        # Add or update with vector results
        for result in vector_results:
            key = result['key']
            if key in merged:
                # Combine scores
                merged[key]['score'] = (merged[key]['score'] + result['score']) / 2
            else:
                merged[key] = result
        
        # Sort by score
        results = list(merged.values())
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def _create_vector(self, text: str, content: Any) -> np.ndarray:
        """
        Create simple vector representation (bag of words with TF-IDF-like weighting)
        In production, use proper embeddings (OpenAI, Sentence Transformers, etc.)
        """
        # Combine text and content
        full_text = text + " " + json.dumps(content)
        full_text = full_text.lower()
        
        # Simple vocabulary (top 100 ML terms)
        vocab = [
            'neural', 'network', 'learning', 'deep', 'machine', 'data', 'model',
            'training', 'optimization', 'gradient', 'descent', 'transformer',
            'attention', 'layer', 'algorithm', 'classification', 'regression',
            'supervised', 'unsupervised', 'reinforcement', 'cnn', 'rnn', 'lstm',
            'gan', 'autoencoder', 'embedding', 'feature', 'backpropagation',
            'loss', 'accuracy', 'precision', 'recall', 'f1', 'score',
            'overfitting', 'underfitting', 'regularization', 'dropout',
            'batch', 'normalization', 'activation', 'relu', 'sigmoid', 'softmax',
            'convolutional', 'recurrent', 'feedforward', 'architecture',
            'weights', 'bias', 'parameter', 'hyperparameter', 'epoch',
            'tensorflow', 'pytorch', 'keras', 'vision', 'nlp', 'speech',
            'image', 'text', 'sequence', 'time', 'series', 'prediction',
            'inference', 'deployment', 'research', 'paper', 'study',
            'experiment', 'dataset', 'preprocessing', 'augmentation',
            'transfer', 'fine', 'tuning', 'pretrained', 'bert', 'gpt',
            't5', 'roberta', 'xlnet', 'efficientnet', 'resnet', 'vgg',
            'yolo', 'mask', 'rcnn', 'segmentation', 'detection', 'recognition',
            'generation', 'synthesis', 'style', 'adversarial', 'q-learning',
            'policy', 'value', 'reward', 'agent', 'environment', 'state', 'action'
        ]
        
        # Create vector
        vector = np.zeros(len(vocab))
        words = full_text.split()
        
        for i, term in enumerate(vocab):
            # Count occurrences
            count = sum(1 for word in words if term in word)
            # Simple TF-IDF-like weighting
            vector[i] = count * (1 + np.log(1 + len(vocab)))
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def update_agent_state(self, agent_name: str, state: Dict[str, Any]) -> Dict[str, bool]:
        """Update the state of a specific agent"""
        self.logger.log_agent_action(self.name, "Updating Agent State", agent_name)
        
        self.agent_states[agent_name] = {
            **state,
            'last_updated': datetime.now().isoformat()
        }
        
        return {'success': True, 'agent': agent_name}
    
    def get_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve the state of a specific agent"""
        return self.agent_states.get(agent_name)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_memory[-limit:]
    
    def clear_memory(self) -> Dict[str, bool]:
        """Clear all memory (useful for testing)"""
        self.logger.log_agent_action(self.name, "Clearing Memory", "all")
        
        self.conversation_memory = []
        self.knowledge_base = {}
        self.agent_states = {}
        self.vector_store = {}
        
        return {'success': True}
    
    def get_statistics(self) -> Dict[str, int]:
        """Get memory statistics"""
        return {
            'conversations': len(self.conversation_memory),
            'knowledge_items': len(self.knowledge_base),
            'agent_states': len(self.agent_states),
            'vectors': len(self.vector_store)
        }