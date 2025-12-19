"""
Multi-Agent Chat System
Main entry point for the system
"""

import json
import sys
from datetime import datetime
from agents.coordinator import CoordinatorAgent
from utils.logger import SystemLogger

class MultiAgentChatSystem:
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.logger = SystemLogger()
        self.running = True
        
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*70)
        print("🤖 MULTI-AGENT CHAT SYSTEM")
        print("="*70)
        print("\nAvailable Agents:")
        print("  • Coordinator - Orchestrates all agents")
        print("  • Research Agent - Information retrieval")
        print("  • Analysis Agent - Data analysis and reasoning")
        print("  • Memory Agent - Knowledge persistence")
        print("\nCommands:")
        print("  • Type your question and press Enter")
        print("  • Type 'exit' or 'quit' to end session")
        print("  • Type 'memory' to view stored knowledge")
        print("  • Type 'clear' to clear conversation history")
        print("="*70 + "\n")
    
    def display_menu(self):
        """Display sample queries menu"""
        print("\n📋 Sample Queries:")
        print("1. What are the main types of neural networks?")
        print("2. Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs.")
        print("3. What did we discuss about neural networks earlier?")
        print("4. Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges.")
        print("5. Compare machine learning optimization techniques and recommend which is better.")
        print("\nOr type your own question...\n")
    
    def handle_special_commands(self, user_input):
        """Handle special system commands"""
        command = user_input.lower().strip()
        
        if command in ['exit', 'quit']:
            print("\n👋 Ending session. Goodbye!")
            self.running = False
            return True
        
        elif command == 'memory':
            self.show_memory_contents()
            return True
        
        elif command == 'clear':
            print("\n🗑️  Conversation history cleared.")
            return True
        
        elif command == 'help':
            self.display_welcome()
            return True
        
        elif command == 'menu':
            self.display_menu()
            return True
        
        return False
    
    def show_memory_contents(self):
        """Display current memory contents"""
        print("\n" + "="*70)
        print("💾 MEMORY CONTENTS")
        print("="*70)
        
        memory = self.coordinator.memory
        
        # Show conversation count
        conv_count = len(memory.conversation_memory)
        print(f"\n📝 Conversations stored: {conv_count}")
        
        # Show knowledge base
        kb_count = len(memory.knowledge_base)
        print(f"📚 Knowledge base entries: {kb_count}")
        
        if kb_count > 0:
            print("\nRecent knowledge:")
            for i, (key, record) in enumerate(list(memory.knowledge_base.items())[-5:]):
                print(f"\n  {i+1}. {key}")
                print(f"     Confidence: {record['metadata'].get('confidence', 'N/A')}")
                print(f"     Timestamp: {record['metadata'].get('timestamp', 'N/A')}")
        
        # Show agent states
        state_count = len(memory.agent_states)
        print(f"\n🤖 Agent states tracked: {state_count}")
        
        print("="*70 + "\n")
    
    def process_query(self, query):
        """Process user query through the coordinator"""
        print(f"\n{'='*70}")
        print(f"🔄 PROCESSING QUERY")
        print(f"{'='*70}\n")
        
        # Log the query
        self.logger.log_user_query(query)
        
        # Process through coordinator
        try:
            response = self.coordinator.process_query(query)
            
            # Display response
            print(f"\n{'='*70}")
            print(f"💬 RESPONSE")
            print(f"{'='*70}\n")
            print(response)
            print(f"\n{'='*70}\n")
            
            # Log the response
            self.logger.log_assistant_response(response)
            
        except Exception as e:
            print(f"\n❌ Error processing query: {str(e)}")
            self.logger.log_error(str(e))
    
    def run(self):
        """Main run loop"""
        self.display_welcome()
        self.display_menu()
        
        while self.running:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    continue
                
                # Process the query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 End of input. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                continue

def main():
    """Entry point"""
    system = MultiAgentChatSystem()
    system.run()

if __name__ == "__main__":
    main()