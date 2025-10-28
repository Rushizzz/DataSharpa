## 🧠 Concept
Build an agentic application called DataSherpa, a GenAI-powered assistant that helps Data Engineers debug, optimize, and document large-scale data pipelines in real time. It uses the llama-3 1-nemotron-nano-8B-v1 model for reasoning and a Retrieval Embedding NIM to index and search pipeline logs, error traces, and documentation. The app is deployed on Amazon EKS for scalability and integrates with Apache Spark, Airflow, and Linux shell logs.

## 🔧 Key Features
Natural Language Debugging Ask questions like “Why is my Spark job failing on stage 3?” or “What does this Airflow DAG error mean?” and get contextual answers with log trace references.

Log Embedding & Retrieval Upload pipeline logs, shell outputs, or Airflow metadata. The Retrieval Embedding NIM indexes them for semantic search and fast troubleshooting.

Shell Command Generator Based on your query, it suggests optimized Bash one-liners using awk, sed, grep, etc., tailored to your log format and error pattern.

Resource Optimization Advisor Suggests Spark executor/core/memory configurations based on job history and cluster metrics.

Auto-Documentation Agent Converts pipeline logic and DAGs into markdown documentation with embedded code snippets and diagrams.

Open-Source Ready Includes a CLI tool that can be integrated into CI/CD workflows for automated pipeline health checks and documentation generation.