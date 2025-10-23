# Smart DevOps Assistant
## 📌 Project Overview
Smart DevOps Assistant is an agentic AI application designed to help DevOps engineers monitor, troubleshoot, and optimize cloud infrastructure. It leverages NVIDIA's NIM microservices and AWS deployment tools to provide real-time insights, recommendations, and retrieval-augmented responses based on logs, metrics, and documentation.
🧠 Architecture Explanation
The assistant integrates multiple components:
- AWS CloudWatch: Source of logs and metrics
- Retrieval Embedding NIM: Embeds and retrieves relevant documentation and historical data
- LLM (llama-3 1-nemotron-nano-8B-v1): Processes queries and generates intelligent responses
- Amazon SageMaker: Hosts the AI endpoint
- UI Layer: CLI or web interface for user interaction
 <img width="1536" height="1024" alt="Designer" src="https://github.com/user-attachments/assets/0c39d4e9-6ea0-4ebe-a68e-ae0d19319ade" />

Figure: Smart DevOps Assistant Architecture
## ⚙️ Setup Instructions
1. Deploy the Retrieval Embedding NIM and LLM NIM using NVIDIA's microservice framework.
2. Configure Amazon SageMaker to host the LLM endpoint.
3. Connect AWS CloudWatch to stream logs and metrics.
4. Build a simple UI using Streamlit or React to interact with the assistant.
5. Integrate the components using Python SDKs and REST APIs.
## 🚀 Usage Guide
Once deployed, users can interact with the assistant via the UI or CLI. The assistant can:
- Analyze logs and detect anomalies
- Suggest fixes and scaling strategies
- Retrieve relevant documentation and GitHub issues
- Provide contextual recommendations based on historical data
## 🎬 Sample Demo Script
User Scenario: A DevOps engineer wants to troubleshoot a failed deployment and get advice on scaling.
Interaction Flow:
User: Hey DevOps Assistant, check the latest logs from CloudWatch for service `auth-api`.
Assistant: Analyzing logs... Found repeated 502 errors and latency spikes in the last 15 minutes. Possible cause: overloaded instance or misconfigured load balancer.
User: What should I do?
Assistant: Recommended actions:
1. Scale up the instance count from 2 to 4.
2. Check load balancer health checks and timeout settings.
Would you like me to retrieve the relevant AWS documentation?
User: Yes, please.
Assistant: Here’s the link to AWS Load Balancer Health Check configuration guide. Also retrieved a similar GitHub issue from last month where the fix was updating the timeout to 60s.
