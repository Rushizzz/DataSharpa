#!/usr/bin/env python3
"""
DataSherpa CLI Tool
Command-line interface for pipeline health checks and documentation generation
"""
import argparse
import requests
import json
import sys
from pathlib import Path
from typing import Optional


class DataSherpaCLI:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
    
    def health_check(self) -> bool:
        """
        Check if the API is healthy
        """
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ DataSherpa API is healthy")
                return True
            else:
                print(f"✗ API returned status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Failed to connect to API: {e}")
            return False
    
    def upload_logs(self, log_file: str) -> bool:
        """
        Upload log file for indexing
        """
        try:
            file_path = Path(log_file)
            if not file_path.exists():
                print(f"✗ Log file not found: {log_file}")
                return False
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'text/plain')}
                response = requests.post(
                    f"{self.api_url}/upload-logs",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Uploaded {result['filename']}")
                print(f"  Indexed {result['chunks_indexed']} chunks")
                return True
            else:
                print(f"✗ Upload failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error uploading logs: {e}")
            return False
    
    def debug_query(self, question: str, context: Optional[str] = None) -> bool:
        """
        Ask a debugging question
        """
        try:
            payload = {
                "question": question,
                "context": context
            }
            
            response = requests.post(
                f"{self.api_url}/debug",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n📝 Question: {result['question']}\n")
                print(f"💡 Answer:\n{result['answer']}\n")
                
                if result.get('relevant_logs'):
                    print("📋 Relevant Log Traces:")
                    for i, log in enumerate(result['relevant_logs'][:3], 1):
                        print(f"\n{i}. {log['filename']} (score: {log['score']:.2f})")
                        print(f"   {log['text'][:200]}...")
                
                return True
            else:
                print(f"✗ Query failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error querying: {e}")
            return False
    
    def generate_shell_command(self, query: str) -> bool:
        """
        Generate shell command for a task
        """
        try:
            payload = {"query": query}
            
            response = requests.post(
                f"{self.api_url}/generate-shell-command",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n🔧 Query: {result['query']}\n")
                print(f"💻 Command:\n{result['command']}\n")
                print(f"📖 Explanation:\n{result['explanation']}\n")
                
                if result.get('examples'):
                    print("📚 Examples:")
                    for ex in result['examples']:
                        print(f"\n  • {ex['description']}")
                        print(f"    {ex['command']}")
                
                return True
            else:
                print(f"✗ Generation failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error generating command: {e}")
            return False
    
    def generate_documentation(self, code_file: str, output_file: Optional[str] = None) -> bool:
        """
        Generate documentation from pipeline code
        """
        try:
            file_path = Path(code_file)
            if not file_path.exists():
                print(f"✗ Code file not found: {code_file}")
                return False
            
            with open(file_path, 'r') as f:
                code = f.read()
            
            payload = {"pipeline_code": code}
            
            response = requests.post(
                f"{self.api_url}/generate-documentation",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                documentation = result['documentation']
                
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(documentation)
                    print(f"✓ Documentation saved to {output_file}")
                else:
                    print("\n📄 Generated Documentation:\n")
                    print(documentation)
                
                return True
            else:
                print(f"✗ Documentation generation failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error generating documentation: {e}")
            return False
    
    def optimize_resources(self, job_history_file: str) -> bool:
        """
        Get resource optimization recommendations
        """
        try:
            file_path = Path(job_history_file)
            if not file_path.exists():
                print(f"✗ Job history file not found: {job_history_file}")
                return False
            
            with open(file_path, 'r') as f:
                job_history = f.read()
            
            payload = {"job_history": job_history}
            
            response = requests.post(
                f"{self.api_url}/optimize-resources",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                recommendations = result['recommendations']
                
                print("\n🎯 Resource Optimization Recommendations:\n")
                print(recommendations.get('llm_analysis', ''))
                
                if recommendations.get('quick_wins'):
                    print("\n⚡ Quick Wins:")
                    for win in recommendations['quick_wins']:
                        print(f"\n  • {win['issue']}")
                        print(f"    → {win['recommendation']}")
                        print(f"    Config: {win['config']}")
                
                return True
            else:
                print(f"✗ Optimization failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error optimizing resources: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="DataSherpa CLI - GenAI-powered Data Engineering Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--api-url',
        default='http://localhost:8000',
        help='DataSherpa API URL (default: http://localhost:8000)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Health check command
    subparsers.add_parser('health', help='Check API health')
    
    # Upload logs command
    upload_parser = subparsers.add_parser('upload', help='Upload log file for indexing')
    upload_parser.add_argument('log_file', help='Path to log file')
    
    # Debug query command
    debug_parser = subparsers.add_parser('debug', help='Ask a debugging question')
    debug_parser.add_argument('question', help='Your debugging question')
    debug_parser.add_argument('--context', help='Additional context')
    
    # Shell command generator
    shell_parser = subparsers.add_parser('shell', help='Generate shell command')
    shell_parser.add_argument('query', help='Describe what you want to do')
    
    # Documentation generator
    docs_parser = subparsers.add_parser('docs', help='Generate documentation')
    docs_parser.add_argument('code_file', help='Path to pipeline code file')
    docs_parser.add_argument('--output', help='Output file for documentation')
    
    # Resource optimizer
    optimize_parser = subparsers.add_parser('optimize', help='Get resource optimization recommendations')
    optimize_parser.add_argument('job_history_file', help='Path to job history file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = DataSherpaCLI(api_url=args.api_url)
    
    success = False
    
    if args.command == 'health':
        success = cli.health_check()
    elif args.command == 'upload':
        success = cli.upload_logs(args.log_file)
    elif args.command == 'debug':
        success = cli.debug_query(args.question, args.context)
    elif args.command == 'shell':
        success = cli.generate_shell_command(args.query)
    elif args.command == 'docs':
        success = cli.generate_documentation(args.code_file, args.output)
    elif args.command == 'optimize':
        success = cli.optimize_resources(args.job_history_file)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
