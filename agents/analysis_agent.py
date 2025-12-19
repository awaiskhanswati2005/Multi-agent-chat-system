"""
Analysis Agent - Data analysis and reasoning
"""

from typing import Dict, List, Any
from utils.logger import SystemLogger

class AnalysisAgent:
    def __init__(self):
        self.name = "Analysis"
        self.logger = SystemLogger()
    
    def analyze(self, data: List[Dict], analysis_type: str) -> Dict[str, Any]:
        """
        Analyze data based on the type of analysis requested
        """
        self.logger.log_agent_action(self.name, "Analyzing", analysis_type)
        
        if not data:
            return {
                'success': False,
                'analysis': 'No data provided for analysis',
                'confidence': 0.0
            }
        
        analysis_lower = analysis_type.lower()
        
        # Determine analysis type and route accordingly
        if 'compare' in analysis_lower or 'effectiveness' in analysis_lower:
            return self._compare_data(data)
        
        elif 'efficiency' in analysis_lower or 'tradeoff' in analysis_lower:
            return self._analyze_tradeoffs(data)
        
        elif 'challenge' in analysis_lower or 'methodology' in analysis_lower or 'identify' in analysis_lower:
            return self._identify_patterns(data)
        
        elif 'recommend' in analysis_lower:
            return self._generate_recommendations(data)
        
        else:
            return self._general_analysis(data)
    
    def _compare_data(self, data: List[Dict]) -> Dict[str, Any]:
        """Compare different items and identify best options"""
        analysis = "COMPARISON ANALYSIS:\n\n"
        
        for item in data:
            topic = item['topic']
            content = item['data']
            
            analysis += f"📊 {topic.upper()}:\n"
            
            # Look for effectiveness, efficiency, or comparison metrics
            if 'effectiveness' in content:
                analysis += f"  • Effectiveness: {content['effectiveness']}\n"
            
            if 'efficiency' in content:
                analysis += f"  • Efficiency: {content['efficiency']}\n"
            
            if 'techniques' in content:
                analysis += f"  • Available techniques: {len(content['techniques'])}\n"
                analysis += f"    Best options: {', '.join(content['techniques'][:3])}\n"
            
            if 'description' in content:
                analysis += f"  • Summary: {content['description'][:100]}...\n"
            
            analysis += "\n"
        
        # Add comparative insights
        analysis += "🔍 COMPARATIVE INSIGHTS:\n"
        if len(data) > 1:
            analysis += f"  • Analyzed {len(data)} different approaches\n"
            analysis += "  • Each has distinct advantages for specific use cases\n"
            analysis += "  • Consider your specific requirements when choosing\n"
        else:
            analysis += "  • Single approach analyzed\n"
            analysis += "  • Consider comparing with alternatives\n"
        
        return {
            'success': True,
            'analysis': analysis,
            'confidence': 0.85
        }
    
    def _analyze_tradeoffs(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze tradeoffs and efficiency considerations"""
        analysis = "TRADEOFF ANALYSIS:\n\n"
        
        for item in data:
            topic = item['topic']
            content = item['data']
            
            analysis += f"⚖️  {topic.upper()}:\n"
            
            if 'tradeoffs' in content:
                analysis += f"  Tradeoffs: {content['tradeoffs']}\n\n"
            
            if 'efficiency' in content:
                analysis += f"  Efficiency: {content['efficiency']}\n\n"
            
            # Extract pros and cons if available
            if 'key_components' in content:
                analysis += f"  Key Components:\n"
                for comp in content['key_components']:
                    analysis += f"    • {comp}\n"
                analysis += "\n"
            
            if 'examples' in content:
                analysis += f"  Real-world Examples: {', '.join(content['examples'])}\n\n"
        
        # Summary
        analysis += "📈 EFFICIENCY CONSIDERATIONS:\n"
        analysis += "  • Computational cost vs performance gains\n"
        analysis += "  • Memory requirements vs accuracy\n"
        analysis += "  • Training time vs inference speed\n"
        analysis += "  • Complexity vs interpretability\n"
        
        return {
            'success': True,
            'analysis': analysis,
            'confidence': 0.80
        }
    
    def _identify_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Identify patterns, challenges, and methodologies"""
        analysis = "PATTERN IDENTIFICATION:\n\n"
        
        all_challenges = []
        all_methodologies = []
        all_applications = []
        
        for item in data:
            topic = item['topic']
            content = item['data']
            
            analysis += f"🔬 {topic.upper()}:\n"
            
            if 'challenges' in content:
                analysis += "  Challenges:\n"
                for challenge in content['challenges']:
                    analysis += f"    • {challenge}\n"
                    all_challenges.append(challenge)
                analysis += "\n"
            
            if 'methodologies' in content:
                analysis += "  Methodologies:\n"
                for method in content['methodologies']:
                    analysis += f"    • {method}\n"
                    all_methodologies.append(method)
                analysis += "\n"
            
            if 'papers' in content:
                analysis += f"  Research Papers: {len(content['papers'])} found\n"
                for paper in content['papers'][:3]:
                    analysis += f"    • {paper}\n"
                analysis += "\n"
            
            if 'applications' in content:
                all_applications.extend(content['applications'])
        
        # Common patterns across all data
        if all_challenges:
            analysis += "🎯 COMMON CHALLENGES:\n"
            unique_challenges = list(set(all_challenges))[:5]
            for challenge in unique_challenges:
                analysis += f"  • {challenge}\n"
            analysis += "\n"
        
        if all_methodologies:
            analysis += "📚 COMMON METHODOLOGIES:\n"
            unique_methods = list(set(all_methodologies))[:5]
            for method in unique_methods:
                analysis += f"  • {method}\n"
            analysis += "\n"
        
        if all_applications:
            analysis += "🚀 APPLICATIONS:\n"
            unique_apps = list(set(all_applications))[:5]
            for app in unique_apps:
                analysis += f"  • {app}\n"
        
        return {
            'success': True,
            'analysis': analysis,
            'confidence': 0.82
        }
    
    def _generate_recommendations(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate recommendations based on analysis"""
        analysis = "RECOMMENDATIONS:\n\n"
        
        for idx, item in enumerate(data, 1):
            topic = item['topic']
            content = item['data']
            
            analysis += f"{idx}. {topic.upper()}:\n"
            
            # Generate contextual recommendations
            if 'effectiveness' in content:
                analysis += f"   ✓ Recommended for: {content['effectiveness']}\n"
            
            if 'applications' in content:
                analysis += f"   ✓ Best suited for: {', '.join(content['applications'][:3])}\n"
            
            if 'techniques' in content:
                best_technique = content['techniques'][0] if content['techniques'] else "N/A"
                analysis += f"   ✓ Start with: {best_technique}\n"
            
            analysis += "\n"
        
        # Overall recommendation
        analysis += "💡 OVERALL RECOMMENDATION:\n"
        analysis += "  • Evaluate based on your specific use case requirements\n"
        analysis += "  • Consider available resources (compute, data, time)\n"
        analysis += "  • Start with simpler approaches and scale up as needed\n"
        analysis += "  • Monitor performance metrics and iterate\n"
        
        return {
            'success': True,
            'analysis': analysis,
            'confidence': 0.78
        }
    
    def _general_analysis(self, data: List[Dict]) -> Dict[str, Any]:
        """Perform general analysis when specific type is unclear"""
        analysis = "GENERAL ANALYSIS:\n\n"
        
        analysis += f"📊 Analyzed {len(data)} topic(s):\n\n"
        
        for item in data:
            topic = item['topic']
            content = item['data']
            
            analysis += f"• {topic.upper()}\n"
            
            # Count different types of information
            info_types = []
            if 'types' in content:
                info_types.append(f"{len(content['types'])} types")
            if 'techniques' in content:
                info_types.append(f"{len(content['techniques'])} techniques")
            if 'challenges' in content:
                info_types.append(f"{len(content['challenges'])} challenges")
            if 'applications' in content:
                info_types.append(f"{len(content['applications'])} applications")
            
            if info_types:
                analysis += f"  Found: {', '.join(info_types)}\n"
            
            if 'description' in content:
                analysis += f"  Summary: {content['description'][:100]}...\n"
            
            analysis += "\n"
        
        analysis += "ℹ️  For more specific analysis, try asking about:\n"
        analysis += "  • Comparisons and effectiveness\n"
        analysis += "  • Efficiency and tradeoffs\n"
        analysis += "  • Challenges and methodologies\n"
        analysis += "  • Recommendations\n"
        
        return {
            'success': True,
            'analysis': analysis,
            'confidence': 0.75
        }
    
    def calculate_confidence(self, data: List[Dict], analysis_result: str) -> float:
        """Calculate confidence score for analysis"""
        confidence = 0.5
        
        # More data = higher confidence
        confidence += min(len(data) * 0.1, 0.3)
        
        # Longer analysis = more detailed = higher confidence
        if len(analysis_result) > 500:
            confidence += 0.2
        
        return min(confidence, 1.0)