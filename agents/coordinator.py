"""
Coordinator Agent - Orchestrates all worker agents
"""

from typing import Dict, List, Any
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.memory_agent import MemoryAgent
from utils.logger import SystemLogger

class CoordinatorAgent:
    def __init__(self):
        self.research = ResearchAgent()
        self.analysis = AnalysisAgent()
        self.memory = MemoryAgent()
        self.logger = SystemLogger()
        self.name = "Coordinator"
        
    def process_query(self, query: str) -> str:
        """
        Main entry point for processing user queries
        Analyzes complexity and routes to appropriate handlers
        """
        self.logger.log_agent_action(self.name, "Processing Query", query)
        
        # Check if it's a memory query
        if self._is_memory_query(query):
            return self._handle_memory_query(query)
        
        # Analyze query complexity
        complexity = self._analyze_complexity(query)
        self.logger.log_agent_action(self.name, f"Complexity: {complexity}", query)
        
        # Route based on complexity
        if complexity == "simple":
            return self._handle_simple_query(query)
        elif complexity == "complex":
            return self._handle_complex_query(query)
        else:  # multi-step
            return self._handle_multistep_query(query)
    
    def _is_memory_query(self, query: str) -> bool:
        """Detect if query is asking about past conversations"""
        memory_keywords = [
            'what did', 'earlier', 'discussed', 'learned', 
            'talked about', 'previous', 'before', 'remember'
        ]
        query_lower = query.lower()
        return any(kw in query_lower for kw in memory_keywords)
    
    def _analyze_complexity(self, query: str) -> str:
        """
        Analyze query complexity to determine routing strategy
        Returns: 'simple', 'complex', or 'multi-step'
        """
        query_lower = query.lower()
        
        # Keywords indicating complexity
        complex_keywords = [
            'analyze', 'compare', 'research', 'identify', 
            'summarize', 'tradeoffs', 'evaluate'
        ]
        
        multistep_keywords = [
            'and then', 'after that', 'recommend', 'find and analyze',
            'first', 'next', 'finally'
        ]
        
        # Count complex operations
        complex_count = sum(1 for kw in complex_keywords if kw in query_lower)
        has_multistep = any(kw in query_lower for kw in multistep_keywords)
        
        if has_multistep or complex_count >= 2:
            return "multi-step"
        elif complex_count >= 1:
            return "complex"
        else:
            return "simple"
    
    def _handle_memory_query(self, query: str) -> str:
        """Handle queries about past conversations"""
        self.logger.log_agent_action(self.name, "Routing to Memory", query)
        
        # Retrieve from memory
        memory_result = self.memory.retrieve(query)
        
        if memory_result['results']:
            response = f"📚 I found {memory_result['count']} relevant items from our previous discussions:\n\n"
            
            for idx, record in enumerate(memory_result['results'][:5], 1):
                response += f"{idx}. Topic: {record['key']}\n"
                response += f"   Timestamp: {record['metadata']['timestamp']}\n"
                response += f"   Confidence: {record['metadata']['confidence']:.2f}\n"
                
                # Show summary of value
                if isinstance(record['value'], dict):
                    if 'research' in record['value']:
                        response += f"   Research findings: {len(record['value']['research'])} topics\n"
                    if 'analysis' in record['value']:
                        analysis_preview = record['value']['analysis'][:100]
                        response += f"   Analysis: {analysis_preview}...\n"
                elif isinstance(record['value'], list):
                    response += f"   Contains {len(record['value'])} items\n"
                
                response += "\n"
            
            return response
        else:
            return "❌ I couldn't find any previous discussions on that topic. Try asking something else!"
    
    def _handle_simple_query(self, query: str) -> str:
        """
        Handle simple queries that only need research
        Flow: Research -> Store in Memory -> Respond
        """
        self.logger.log_agent_action(self.name, "Simple Query - Research Only", query)
        
        # Step 1: Research
        research_result = self.research.search(query)
        
        if not research_result['success'] or not research_result['data']:
            return "❌ I couldn't find information on that topic in the knowledge base. Try rephrasing your question."
        
        # Step 2: Format response
        response = "✅ Here's what I found:\n\n"
        
        for item in research_result['data']:
            topic = item['topic']
            data = item['data']
            
            response += f"📌 {topic.upper()}\n"
            response += "─" * 50 + "\n"
            
            # Display different types of data
            if 'types' in data:
                response += f"Types:\n"
                for t in data['types']:
                    response += f"  • {t}\n"
            
            if 'description' in data:
                response += f"\nDescription: {data['description']}\n"
            
            if 'techniques' in data:
                response += f"Techniques:\n"
                for tech in data['techniques']:
                    response += f"  • {tech}\n"
            
            response += "\n"
        
        # Step 3: Store in memory
        self.memory.store(
            key=query,
            value=research_result['data'],
            metadata={
                'agent': 'Research',
                'confidence': research_result['confidence'],
                'query_type': 'simple'
            }
        )
        
        return response
    
    def _handle_complex_query(self, query: str) -> str:
        """
        Handle complex queries requiring research + analysis
        Flow: Research -> Analysis -> Store in Memory -> Respond
        """
        self.logger.log_agent_action(self.name, "Complex Query - Research + Analysis", query)
        
        # Step 1: Research
        research_result = self.research.search(query)
        
        if not research_result['success'] or not research_result['data']:
            return "❌ I couldn't find sufficient information to analyze. Try a different question."
        
        # Step 2: Analysis
        analysis_result = self.analysis.analyze(
            data=research_result['data'],
            analysis_type=query
        )
        
        # Step 3: Format response
        response = "✅ RESEARCH & ANALYSIS RESULTS\n"
        response += "=" * 70 + "\n\n"
        
        response += "📊 RESEARCH FINDINGS:\n"
        response += "─" * 70 + "\n"
        for item in research_result['data']:
            response += f"  • {item['topic']}\n"
        
        response += f"\n🔍 ANALYSIS:\n"
        response += "─" * 70 + "\n"
        response += analysis_result['analysis']
        
        response += f"\n\n📈 Confidence Score: {analysis_result['confidence']:.2f}\n"
        
        # Step 4: Store in memory
        self.memory.store(
            key=query,
            value={
                'research': research_result['data'],
                'analysis': analysis_result['analysis']
            },
            metadata={
                'agents': ['Research', 'Analysis'],
                'confidence': (research_result['confidence'] + analysis_result['confidence']) / 2,
                'query_type': 'complex'
            }
        )
        
        return response
    
    def _handle_multistep_query(self, query: str) -> str:
        """
        Handle multi-step queries with multiple operations
        Flow: Research -> Analysis -> Synthesis -> Store -> Respond
        """
        self.logger.log_agent_action(self.name, "Multi-Step Query - Full Pipeline", query)
        
        response = "✅ MULTI-STEP ANALYSIS\n"
        response += "=" * 70 + "\n\n"
        
        # Step 1: Research
        response += "🔎 STEP 1: RESEARCH\n"
        response += "─" * 70 + "\n"
        
        research_result = self.research.search(query)
        
        if research_result['data']:
            for item in research_result['data']:
                response += f"  ✓ Found: {item['topic']}\n"
        else:
            response += "  ✗ No data found\n"
        
        # Step 2: Analysis
        response += f"\n🧠 STEP 2: ANALYSIS\n"
        response += "─" * 70 + "\n"
        
        if research_result['data']:
            analysis_result = self.analysis.analyze(
                data=research_result['data'],
                analysis_type=query
            )
            response += analysis_result['analysis']
        else:
            response += "  ✗ Cannot analyze without data\n"
            analysis_result = {'analysis': 'No analysis performed', 'confidence': 0.0}
        
        # Step 3: Synthesis & Recommendation
        response += f"\n💡 STEP 3: SYNTHESIS & RECOMMENDATIONS\n"
        response += "─" * 70 + "\n"
        
        if 'recommend' in query.lower():
            response += "Based on the research and analysis:\n\n"
            response += "  • Consider the tradeoffs identified above\n"
            response += "  • The best approach depends on your specific requirements\n"
            response += "  • Evaluate based on your use case constraints\n"
        else:
            response += "Key findings have been analyzed and stored.\n"
            response += "You can ask follow-up questions or request memory recall.\n"
        
        # Step 4: Store comprehensive result
        self.memory.store(
            key=query,
            value={
                'research': research_result['data'],
                'analysis': analysis_result['analysis'],
                'type': 'multi-step'
            },
            metadata={
                'agents': ['Research', 'Analysis', 'Memory'],
                'confidence': 0.85,
                'query_type': 'multi-step'
            }
        )
        
        return response