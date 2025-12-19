"""
System Logger - Logging and tracing utility
"""

import json
from datetime import datetime
from typing import Any, Dict
import os

class SystemLogger:
    def __init__(self, log_file: str = "logs/system.log"):
        self.log_file = log_file
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log_agent_action(self, agent_name: str, action: str, details: str = ""):
        """Log an agent action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'agent_action',
            'agent': agent_name,
            'action': action,
            'details': details
        }
        self._write_log(log_entry)
        self._print_log(agent_name, action, details)
    
    def log_user_query(self, query: str):
        """Log user query"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'user_query',
            'query': query
        }
        self._write_log(log_entry)
    
    def log_assistant_response(self, response: str):
        """Log assistant response"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'assistant_response',
            'response': response[:200] + "..." if len(response) > 200 else response
        }
        self._write_log(log_entry)
    
    def log_error(self, error_message: str):
        """Log error"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'message': error_message
        }
        self._write_log(log_entry)
        print(f"❌ ERROR: {error_message}")
    
    def _write_log(self, log_entry: Dict[str, Any]):
        """Write log entry to file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def _print_log(self, agent_name: str, action: str, details: str):
        """Print log to console with nice formatting"""
        icons = {
            'Coordinator': '🎯',
            'Research': '🔍',
            'Analysis': '📊',
            'Memory': '💾'
        }
        icon = icons.get(agent_name, '🤖')
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {icon} {agent_name}: {action}")
        if details and len(details) < 100:
            print(f"         └─ {details[:80]}")
    
    def get_logs(self, log_type: str = None, limit: int = 100) -> list:
        """Retrieve logs from file"""
        logs = []
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            log_entry = json.loads(line.strip())
                            if log_type is None or log_entry.get('type') == log_type:
                                logs.append(log_entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"Warning: Could not read log file: {e}")
        
        return logs[-limit:] if limit else logs