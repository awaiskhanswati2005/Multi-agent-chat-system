"""
Research Agent - Information retrieval and search
"""

from typing import Dict, List, Any
from utils.logger import SystemLogger

class ResearchAgent:
    def __init__(self):
        self.name = "Research"
        self.logger = SystemLogger()
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """
        Initialize mock knowledge base
        In production, this would connect to actual data sources
        """
        return {
            'neural networks': {
                'types': [
                    'Feedforward Neural Networks (FNN)',
                    'Convolutional Neural Networks (CNN)',
                    'Recurrent Neural Networks (RNN)',
                    'Long Short-Term Memory (LSTM)',
                    'Generative Adversarial Networks (GAN)',
                    'Transformer Networks',
                    'Autoencoders'
                ],
                'description': 'Neural networks are computing systems inspired by biological neural networks that constitute animal brains. They consist of interconnected nodes (neurons) that process information.',
                'applications': ['Image recognition', 'Natural language processing', 'Speech recognition', 'Game playing']
            },
            'machine learning optimization': {
                'techniques': [
                    'Gradient Descent',
                    'Stochastic Gradient Descent (SGD)',
                    'Mini-batch Gradient Descent',
                    'Adam Optimizer',
                    'RMSprop',
                    'AdaGrad',
                    'AdaDelta',
                    'Momentum'
                ],
                'effectiveness': 'Adam optimizer is generally most effective for deep learning due to adaptive learning rates. SGD with momentum works well for general cases and has good convergence properties.',
                'description': 'Optimization techniques adjust model parameters to minimize loss functions during training.'
            },
            'transformer architectures': {
                'info': 'Transformers use self-attention mechanisms to process sequences in parallel, enabling better capture of long-range dependencies.',
                'efficiency': 'High computational cost (O(n²) complexity) but excellent parallelization capabilities. Training is resource-intensive but inference can be optimized.',
                'tradeoffs': 'Memory intensive and requires large datasets, but captures long-range dependencies better than RNNs and processes sequences in parallel.',
                'examples': ['BERT', 'GPT', 'T5', 'Vision Transformer (ViT)'],
                'key_components': ['Self-attention', 'Multi-head attention', 'Positional encoding', 'Feed-forward networks']
            },
            'reinforcement learning': {
                'papers': [
                    'Q-Learning for Robotics Control',
                    'Deep Q-Networks (DQN) - Atari Games',
                    'Policy Gradient Methods in Continuous Control',
                    'Actor-Critic Approaches for RL',
                    'Proximal Policy Optimization (PPO)',
                    'Trust Region Policy Optimization (TRPO)'
                ],
                'methodologies': [
                    'Model-free learning (direct policy/value learning)',
                    'Model-based learning (learn environment model)',
                    'Value-based methods (Q-learning, DQN)',
                    'Policy-based methods (REINFORCE, PPO)',
                    'Actor-Critic methods (A3C, SAC)',
                    'Multi-agent RL'
                ],
                'challenges': [
                    'Sample efficiency - requires many interactions',
                    'Exploration vs exploitation tradeoff',
                    'Credit assignment problem',
                    'Reward design and shaping',
                    'Stability and convergence issues',
                    'Partial observability',
                    'Non-stationary environments'
                ],
                'applications': ['Robotics', 'Game AI', 'Autonomous vehicles', 'Resource management']
            },
            'deep learning': {
                'description': 'Deep learning uses neural networks with multiple layers to progressively extract higher-level features from raw input.',
                'techniques': ['Backpropagation', 'Dropout', 'Batch normalization', 'Transfer learning'],
                'frameworks': ['TensorFlow', 'PyTorch', 'Keras', 'JAX']
            },
            'computer vision': {
                'tasks': ['Image classification', 'Object detection', 'Semantic segmentation', 'Instance segmentation'],
                'architectures': ['ResNet', 'VGG', 'YOLO', 'Mask R-CNN', 'EfficientNet'],
                'applications': ['Facial recognition', 'Medical imaging', 'Autonomous driving', 'Quality control']
            },
            'natural language processing': {
                'tasks': ['Text classification', 'Named entity recognition', 'Machine translation', 'Question answering'],
                'models': ['BERT', 'GPT', 'T5', 'RoBERTa', 'ELECTRA'],
                'challenges': ['Ambiguity', 'Context understanding', 'Multi-lingual support']
            }
        }
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Search the knowledge base for relevant information
        Simulates web search with mock data
        """
        self.logger.log_agent_action(self.name, "Searching", query)
        
        query_lower = query.lower()
        results = []
        
        # Search through knowledge base
        for topic, data in self.knowledge_base.items():
            # Check if topic is in query or query keywords match topic
            if self._is_relevant(query_lower, topic, data):
                results.append({
                    'topic': topic,
                    'data': data,
                    'relevance_score': self._calculate_relevance(query_lower, topic, data)
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Calculate confidence based on results
        confidence = 0.9 if results else 0.3
        
        return {
            'success': True,
            'data': results,
            'confidence': confidence,
            'source': 'knowledge_base',
            'query': query
        }
    
    def _is_relevant(self, query: str, topic: str, data: Dict) -> bool:
        """Check if topic/data is relevant to query"""
        # Direct topic match
        if topic in query or any(word in query for word in topic.split()):
            return True
        
        # Check data fields
        data_str = str(data).lower()
        query_words = query.split()
        
        # Check if significant query words appear in data
        relevant_words = [w for w in query_words if len(w) > 3]
        matches = sum(1 for word in relevant_words if word in data_str)
        
        return matches >= 1
    
    def _calculate_relevance(self, query: str, topic: str, data: Dict) -> float:
        """Calculate relevance score for ranking"""
        score = 0.0
        
        # Exact topic match
        if topic in query:
            score += 1.0
        
        # Partial topic match
        topic_words = topic.split()
        query_words = query.split()
        matching_words = set(topic_words) & set(query_words)
        score += len(matching_words) * 0.3
        
        # Data content match
        data_str = str(data).lower()
        for word in query_words:
            if len(word) > 3 and word in data_str:
                score += 0.1
        
        return min(score, 2.0)  # Cap at 2.0
    
    def get_topic_details(self, topic: str) -> Dict[str, Any]:
        """Get detailed information about a specific topic"""
        self.logger.log_agent_action(self.name, "Fetching Details", topic)
        
        topic_lower = topic.lower()
        
        if topic_lower in self.knowledge_base:
            return {
                'success': True,
                'topic': topic,
                'data': self.knowledge_base[topic_lower]
            }
        
        return {
            'success': False,
            'topic': topic,
            'data': None,
            'message': 'Topic not found'
        }