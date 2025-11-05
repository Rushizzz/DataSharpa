"""
Resource Optimization Advisor Service
Provides Spark configuration recommendations
"""
from typing import Dict, Optional
from services.llm_service import LLMService


class ResourceOptimizer:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def analyze_and_recommend(
        self, 
        job_history: str,
        cluster_metrics: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze job history and provide optimization recommendations
        """
        # Get LLM analysis
        analysis = self.llm_service.analyze_resource_optimization(
            job_history, 
            cluster_metrics
        )
        
        # Add rule-based recommendations
        recommendations = {
            "llm_analysis": analysis,
            "quick_wins": self._get_quick_wins(job_history),
            "configuration_template": self._get_config_template()
        }
        
        return recommendations
    
    def _get_quick_wins(self, job_history: str) -> list:
        """
        Get quick optimization wins based on common patterns
        """
        quick_wins = []
        
        job_lower = job_history.lower()
        
        if "out of memory" in job_lower or "oom" in job_lower:
            quick_wins.append({
                "issue": "Out of Memory errors detected",
                "recommendation": "Increase executor memory",
                "config": "--executor-memory 8g --driver-memory 4g"
            })
        
        if "shuffle" in job_lower and ("slow" in job_lower or "timeout" in job_lower):
            quick_wins.append({
                "issue": "Shuffle performance issues",
                "recommendation": "Optimize shuffle partitions",
                "config": "--conf spark.sql.shuffle.partitions=200"
            })
        
        if "spill" in job_lower:
            quick_wins.append({
                "issue": "Memory spilling detected",
                "recommendation": "Increase memory fraction for execution",
                "config": "--conf spark.memory.fraction=0.8"
            })
        
        if "gc" in job_lower or "garbage collection" in job_lower:
            quick_wins.append({
                "issue": "GC overhead detected",
                "recommendation": "Tune GC settings",
                "config": "--conf spark.executor.extraJavaOptions='-XX:+UseG1GC'"
            })
        
        return quick_wins
    
    def _get_config_template(self) -> Dict:
        """
        Get recommended Spark configuration template
        """
        return {
            "small_cluster": {
                "executor_cores": 4,
                "executor_memory": "8g",
                "driver_memory": "4g",
                "executor_instances": 2,
                "additional_configs": {
                    "spark.sql.shuffle.partitions": 100,
                    "spark.default.parallelism": 8,
                    "spark.memory.fraction": 0.75
                }
            },
            "medium_cluster": {
                "executor_cores": 5,
                "executor_memory": "16g",
                "driver_memory": "8g",
                "executor_instances": 10,
                "additional_configs": {
                    "spark.sql.shuffle.partitions": 200,
                    "spark.default.parallelism": 50,
                    "spark.memory.fraction": 0.8
                }
            },
            "large_cluster": {
                "executor_cores": 6,
                "executor_memory": "32g",
                "driver_memory": "16g",
                "executor_instances": 50,
                "additional_configs": {
                    "spark.sql.shuffle.partitions": 500,
                    "spark.default.parallelism": 300,
                    "spark.memory.fraction": 0.8,
                    "spark.sql.adaptive.enabled": True
                }
            }
        }
