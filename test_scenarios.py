"""
Automated test scenarios for the Multi-Agent Chat System
Runs all 5 required test cases and saves outputs
"""

import sys
import os
from datetime import datetime
from agents.coordinator import CoordinatorAgent

class TestScenarios:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.output_dir = "outputs"
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_output(self, filename: str, query: str, response: str):
        """Save test output to file"""
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"TEST: {filename.replace('.txt', '').replace('_', ' ').upper()}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
            f.write(f"QUERY:\n{query}\n\n")
            f.write("="*70 + "\n")
            f.write("RESPONSE:\n")
            f.write("="*70 + "\n\n")
            f.write(response)
            f.write("\n\n" + "="*70 + "\n")
            f.write("END OF TEST\n")
            f.write("="*70 + "\n")
        
        print(f"✅ Saved: {filepath}")
    
    def test_simple_query(self):
        """Test Scenario 1: Simple Query"""
        print("\n" + "="*70)
        print("TEST 1: SIMPLE QUERY")
        print("="*70 + "\n")
        
        query = "What are the main types of neural networks?"
        print(f"Query: {query}\n")
        
        response = self.coordinator.process_query(query)
        print(f"\nResponse:\n{response}\n")
        
        self.save_output("simple_query.txt", query, response)
    
    def test_complex_query(self):
        """Test Scenario 2: Complex Query"""
        print("\n" + "="*70)
        print("TEST 2: COMPLEX QUERY")
        print("="*70 + "\n")
        
        query = "Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs."
        print(f"Query: {query}\n")
        
        response = self.coordinator.process_query(query)
        print(f"\nResponse:\n{response}\n")
        
        self.save_output("complex_query.txt", query, response)
    
    def test_memory_query(self):
        """Test Scenario 3: Memory Test"""
        print("\n" + "="*70)
        print("TEST 3: MEMORY QUERY")
        print("="*70 + "\n")
        
        query = "What did we discuss about neural networks earlier?"
        print(f"Query: {query}\n")
        
        response = self.coordinator.process_query(query)
        print(f"\nResponse:\n{response}\n")
        
        self.save_output("memory_test.txt", query, response)
    
    def test_multistep_query(self):
        """Test Scenario 4: Multi-step Query"""
        print("\n" + "="*70)
        print("TEST 4: MULTI-STEP QUERY")
        print("="*70 + "\n")
        
        query = "Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges."
        print(f"Query: {query}\n")
        
        response = self.coordinator.process_query(query)
        print(f"\nResponse:\n{response}\n")
        
        self.save_output("multi_step.txt", query, response)
    
    def test_collaborative_query(self):
        """Test Scenario 5: Collaborative Query"""
        print("\n" + "="*70)
        print("TEST 5: COLLABORATIVE QUERY")
        print("="*70 + "\n")
        
        query = "Compare machine learning optimization techniques and recommend which is better."
        print(f"Query: {query}\n")
        
        response = self.coordinator.process_query(query)
        print(f"\nResponse:\n{response}\n")
        
        self.save_output("collaborative.txt", query, response)
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("\n" + "🚀 "*35)
        print("RUNNING ALL TEST SCENARIOS")
        print("🚀 "*35 + "\n")
        
        try:
            # Test 1: Simple Query
            self.test_simple_query()
            
            # Test 2: Complex Query
            self.test_complex_query()
            
            # Test 3: Memory Query (after previous tests)
            self.test_memory_query()
            
            # Test 4: Multi-step Query
            self.test_multistep_query()
            
            # Test 5: Collaborative Query
            self.test_collaborative_query()
            
            print("\n" + "✅ "*35)
            print("ALL TESTS COMPLETED SUCCESSFULLY")
            print("✅ "*35 + "\n")
            print(f"\nOutputs saved in: {self.output_dir}/")
            print("\nFiles created:")
            print("  • simple_query.txt")
            print("  • complex_query.txt")
            print("  • memory_test.txt")
            print("  • multi_step.txt")
            print("  • collaborative.txt")
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """Main entry point for automated testing"""
    tester = TestScenarios()
    tester.run_all_tests()

if __name__ == "__main__":
    main()