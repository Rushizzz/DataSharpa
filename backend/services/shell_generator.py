"""
Shell Command Generator Service
Generates optimized bash commands for log processing
"""
from typing import Dict, Optional
from services.llm_service import LLMService


class ShellCommandGenerator:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.command_templates = {
            "error_count": "grep -i 'error' {file} | wc -l",
            "unique_errors": "grep -i 'error' {file} | sort | uniq -c | sort -rn",
            "time_range": "awk '$1 >= \"{start}\" && $1 <= \"{end}\"' {file}",
            "extract_field": "awk -F'{delimiter}' '{{print ${field}}}' {file}",
            "filter_pattern": "grep -E '{pattern}' {file}",
            "top_errors": "grep -i 'error' {file} | awk '{{print $NF}}' | sort | uniq -c | sort -rn | head -n {n}",
        }
    
    def generate_command(
        self, 
        query: str, 
        log_format: Optional[str] = None,
        error_pattern: Optional[str] = None
    ) -> Dict:
        """
        Generate shell command based on natural language query
        """
        # Use LLM to generate command
        result = self.llm_service.generate_shell_command(query, log_format, error_pattern)
        
        # Add common examples
        examples = self._get_examples(query)
        result["examples"] = examples
        
        return result
    
    def _get_examples(self, query: str) -> list:
        """
        Get relevant command examples based on query
        """
        query_lower = query.lower()
        examples = []
        
        if "error" in query_lower and "count" in query_lower:
            examples.append({
                "description": "Count all errors in log file",
                "command": "grep -i 'error' application.log | wc -l"
            })
            examples.append({
                "description": "Count unique error types",
                "command": "grep -i 'error' application.log | awk '{print $NF}' | sort | uniq -c"
            })
        
        if "time" in query_lower or "range" in query_lower:
            examples.append({
                "description": "Filter logs by time range",
                "command": "awk '$1 >= \"2024-01-01\" && $1 <= \"2024-01-31\"' application.log"
            })
        
        if "extract" in query_lower or "field" in query_lower:
            examples.append({
                "description": "Extract specific field from CSV",
                "command": "awk -F',' '{print $3}' data.csv"
            })
        
        if "top" in query_lower or "most" in query_lower:
            examples.append({
                "description": "Top 10 most frequent errors",
                "command": "grep -i 'error' application.log | sort | uniq -c | sort -rn | head -10"
            })
        
        return examples
