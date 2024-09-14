# Finetuning open source llama models.

The goal of this document is to outline steps needed to serve, train (SFT and RL) open source LLMs for prepared.ai. As of now, serving and training have been tested using OpenAI apis. However OpenAI does not provide RL trianing capability also you are tied down to OpenAI and not leveraging the improvements done in opensource community. This is not good for learning as well.


### **Step 1: Serve LLaMA 8B/70B as an API and test using prompt engineering**
- **Goal**: Get the base models up and running to test prompt engineering in your application, especially as you're transitioning from OpenAI APIs.

- **Best Platform**: **Lambda Labs** or **RunPod**
  - **Why**: Both offer GPU rental with low costs and simple deployment for serving APIs. Since this step is mostly serving, you'll want cost-effective, consistent GPU availability.
  - **Pros**: Low cost, easy setup for hosting APIs, ideal for trying out prompt engineering quickly.
  - **Cons**: May require some setup for managing API endpoints yourself.
- Milestones
  - [x] Test model loading and serving locally.
    -  [Notebook](training/sft_ai_teacher_llama.ipynb)
  - [ ] Test model loading and inference in colab
  - [ ] Serve the model in a GPU serving platform
  - [ ] Test the app loaclly by calling the API.
---

### **Step 2: Train SFT Model on LLaMA 8B and serve it**
- **Goal**: Fine-tune LLaMA 8B using SFT (Supervised Fine-Tuning) and deploy the model to test in your multi-agent AI application.
- **Best Platform**: **AWS Spot Instances** or **Lambda Labs**
  - **Why**: You’ll need powerful GPUs for SFT, but you also want cost-efficiency. **AWS Spot** can save costs if interruptions aren’t a problem. **Lambda Labs** can also provide consistent availability for the training process without interruptions.
  - **Pros**: Both platforms offer V100/A100 GPUs for faster training, and you can launch instances on-demand or for spot prices to save costs.
  - **Cons**: AWS Spot may interrupt, so you need to account for that in long training runs.

---

### **Step 3: Explore RL Techniques for Improving Multi-Agent AI Application**
- **Goal**: Experiment with different reinforcement learning (RL) techniques on LLaMA 8B for your AI application's multi-agent behavior.
- **Best Platform**: **Google Colab Pro+** or **Lambda Labs**
  - **Why**: Since you’ll be experimenting, **Colab Pro+** offers a low-commitment, flexible environment to try out different RL techniques on small scales. **Lambda Labs** can offer cost-efficient GPUs if you need more extended experiments without interruptions.
  - **Pros**: Easy to start with, no infrastructure setup on Colab. Lambda Labs offers more control once you need stable GPUs.
  - **Cons**: Colab Pro+ may have GPU availability issues, but it's still great for experimentation.

---

### **Step 4: Train RL Model on LLaMA 8B with Multiple Iterations and Serve It**
- **Goal**: Fine-tune the model using RL techniques, iterating multiple times to improve performance and then deploy for testing.
- **Best Platform**: **AWS Spot Instances** or **Lambda Labs**
  - **Why**: For extended RL fine-tuning, especially with many iterations, using spot instances will cut down costs while providing powerful hardware like V100 or A100. **Lambda Labs** provides dedicated servers at a low cost with GPU availability.
  - **Pros**: High-performance GPUs for intensive RL fine-tuning. You can handle multiple iterations while optimizing costs with spot pricing.
  - **Cons**: AWS Spot interruptions can affect your workflow unless you carefully plan to checkpoint your models.

---

### **Step 5: Build Final Design and Start Building UI**
- **Goal**: Build the final architecture design and user interface for the application.
- **Best Platform**: **Google Cloud** or **AWS EC2 On-Demand**
  - **Why**: You’ll want a stable environment for UI and API integration. **Google Cloud** is a good choice if you need tight integration with cloud services like databases, serverless computing, etc. **AWS EC2 On-Demand** gives you similar stability with a wider range of services.
  - **Pros**: Stability, high availability, easy cloud integration for API/UI components.
  - **Cons**: Higher cost compared to GPU rental services but great for production-level application building.

---

### **Step 6: Repeat the Above Process with Final Design, Data, and Serve the Model(s)**
- **Goal**: Retrain the models (fine-tuned with RL), refine the design with real data, and serve them.
- **Best Platform**: **AWS Spot Instances** or **Google Cloud**
  - **Why**: For retraining and refining the models, **AWS Spot Instances** will still offer significant cost savings. **Google Cloud** (or AWS On-Demand) is better for serving the final versions in production with consistent uptime.
  - **Pros**: Scalability, large GPU instances (A100, V100), and solid cloud infrastructure for production.
  - **Cons**: AWS Spot interruptions may be a factor during the retraining process. For production, cloud providers tend to be more expensive.

---

### **Step 7: Build the End-to-End App with UI, Database, Model, and Feedback**
- **Goal**: Develop the final product with UI, database, model inference, and feedback mechanisms.
- **Best Platform**: **Google Cloud** or **AWS EC2 On-Demand**
  - **Why**: For a complete end-to-end application, you’ll need a stable, scalable cloud infrastructure. **Google Cloud** offers ease of integration with database services, AI model serving, and feedback loops. **AWS** is highly versatile, with Elastic Inference and serverless architecture if you want flexibility.
  - **Pros**: Scalable, excellent support for production-grade services (e.g., databases, load balancers). **Google Cloud**'s AI offerings can help with model deployment.
  - **Cons**: Higher cost for serving, storage, and databases, but necessary for a full-fledged production app.

---

### **Additional Considerations**
- **Grants**: You could apply for startup or research grants from AWS, Google Cloud, or other cloud providers, which would significantly reduce your costs.
- **Multi-Agent System**: If your multi-agent system requires communication and coordination among agents, think about how the cloud infrastructure will handle this (e.g., using message queues or orchestration frameworks like Kubernetes).

---

In summary:
- For **training** and **RL experimentation**: **AWS Spot Instances** and **Lambda Labs** are cost-efficient with high-performance GPUs.
- For **serving and UI building**: **Google Cloud** or **AWS On-Demand** provide stability, easy scaling, and integration for production environments.
- For **initial fine-tuning** and experimentation: **Google Colab Pro+** offers flexibility at a lower price.

---
Here’s a table that compares different options based on cost, features, pros, and cons for fine-tuning, RL tuning, and serving LLaMA models. This will help you decide which platform suits your needs best.

| **Provider**          | **Cost** (approx.)                                    | **Features**                                                                 | **Pros**                                                      | **Cons**                                                   | **Best Use Case**                                         |
|-----------------------|-------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------|
| **Google Colab Pro/Pro+** | $9.99/month (Pro) $49.99/month (Pro+) | Access to **T4, P100, V100**, and sometimes **A100** GPUs. Sessions last up to 24 hours with Pro+ and 12 hours with Pro. | - Easy to use, no setup required. <br> - Ideal for experimentation. | - No control over exact GPU allocation.<br> - Session disconnections. | Fine-tuning small models like **LLaMA 8B**, RL experimentation, short sessions. |
| **AWS EC2 Spot Instances** | $0.11 - $3.06/hour (T4 to A100) Spot pricing | Wide range of instance types, including **g4dn (T4)**, **p3 (V100)**, **p4 (A100)**.<br> Can launch multiple instances for distributed training. | - Lower cost using Spot instances.<br> - Scalable to larger models.<br> - Full control of instance usage. | - Spot instances may get interrupted.<br> - Setup can be complex. | **Long training** (fine-tuning LLaMA 8B) and **serving** when cost is a priority. |
| **Lambda Labs**       | $1.10/hour (RTX 3090), $2.00/hour (A100) | Access to **RTX 3090**, **V100**, **A100**.<br> Offers Jupyter notebooks or full VM setups.<br> Dedicated servers also available for long-term use. | - Cheaper than AWS.<br> - Easy setup for both training and inference.<br> - Consistent GPU availability. | - Some models might need manual setup.<br> - Limited data storage. | Fine-tuning, **RL tuning**, and **serving** with reliable GPUs at lower costs. |
| **Paperspace Gradient** | $0.51/hour (T4), $2.30/hour (A100) | Offers **T4**, **V100**, and **A100** GPUs.<br> Managed **Jupyter notebooks** for quick experiments.<br> Gradient also has pre-configured ML templates. | - Easy to launch with minimal setup.<br> - Pre-configured environments available.<br> - Good for development. | - Higher cost for **A100** compared to alternatives.<br> - Storage is extra cost. | Fine-tuning **LLaMA 8B** with LoRA and **initial RL experiments**. |
| **RunPod**            | $0.40 - $1.20/hour (T4 to RTX 3090)                   | On-demand GPUs (various, including **T4**, **RTX 3090**).<br> Pay-per-use.<br> Automatic setup scripts for ML workflows. | - Cost-effective.<br> - Wide selection of GPUs.<br> - Quick startup time.<br> - Simple UI. | - Limited documentation and support.<br> - Instances can run out at busy times. | **Fine-tuning** and **serving** small-to-medium models.<br> Ideal for cost-conscious users. |
| **Vast.ai**           | $0.30 - $1.10/hour (T4 to A100)                        | GPU rental marketplace offering **T4**, **RTX 3090**, **V100**, **A100** GPUs.<br> Supports custom Docker setups for ML. | - Cheapest option for **A100** and **3090** GPUs.<br> - Customizable runtime environment.<br> - No need for long-term commitments. | - May require manual setup.<br> - Unreliable availability at peak times.<br> - Minimal support. | **Long-term fine-tuning** and **inference** of LLaMA models on GPUs. |
| **AWS EC2 On-Demand** | $0.50 - $3.91/hour (T4 to A100)                        | Full access to a range of instance types like **p3**, **p4**, **g4dn**.<br> Supports **Elastic Inference** for cost reduction.<br> High availability of instances. | - No interruptions like Spot instances.<br> - Wide variety of GPU types.<br> - Excellent scalability for larger models. | - Higher cost compared to Spot instances.<br> - Expensive for longer training. | **Stable long-term serving** or **distributed RL training** of larger models. |
| **Vultr**             | $0.40 - $2.50/hour (T4 to V100)                       | Offers **T4** and **V100 GPUs**.<br> Simple cloud deployment platform.<br> Supports **bare metal** servers. | - No interruptions (compared to Spot).<br> - Easy to spin up and down.<br> - Competitive pricing. | - Fewer GPU options compared to other providers.<br> - Limited support and documentation. | Mid-term training jobs and serving medium-scale models with **GPU availability**. |
| **Azure**             | $0.90 - $3.06/hour (T4 to A100)                        | **T4, V100, A100 GPUs** with hybrid deployment options.<br> Easy integration with Microsoft ecosystem.<br> High availability of resources. | - Good GPU availability.<br> - Seamless integration with existing Azure services.<br> - Suitable for enterprise users. | - Higher cost than AWS and other providers.<br> - Complex for non-enterprise users. | **Enterprise-level serving** or **model training** with cloud support. |
| **Google Cloud Compute** | $0.35 - $2.47/hour (T4 to A100)                     | Offers **T4, V100, A100** GPU instances.<br> **TPU v4** options for larger-scale jobs.<br> Pay-per-second billing.<br> High availability. | - Integrated with Google Cloud services.<br> - Easy scaling.<br> - Good GPU availability. | - Slightly higher pricing compared to AWS Spot.<br> - Initial setup complexity. | Long-term serving, **fine-tuning** with pay-per-use billing. |

### **Key Differences**
- **Cost**: RunPod, Lambda Labs, and Vast.ai are cheaper than AWS or Google Cloud for short-term training. AWS Spot instances offer good cost savings for longer jobs but come with the risk of interruptions.
- **Features**: Most platforms offer a wide variety of GPUs, with Vast.ai and Lambda Labs being more budget-friendly. AWS, Google Cloud, and Azure provide higher scalability and better integration with cloud ecosystems but at a higher cost.
- **Pros**: Colab Pro is the easiest to get started with, but for consistent access to high-powered GPUs, Lambda Labs and AWS Spot provide better options.
- **Cons**: Colab Pro and Vast.ai have limited availability during busy periods, while AWS Spot instances can be interrupted, leading to potential job loss.

### **Recommendation Based on Your Requirements**
- **For training and initial experimentation (LoRA and RL Tuning)**: Start with **Colab Pro+** for a lower-cost, easy-to-use option. When scaling up your RL experiments, switch to **AWS Spot** or **Lambda Labs** to minimize interruptions.
- **For Serving**: **RunPod** or **Lambda Labs** offer the best cost-effective options. **AWS On-Demand** is ideal if you need higher availability and scalability.

--- 

### Documentation and Resources:

#### **LLaMA Documentation**:
- **Meta website**:
  - Meta LLaMA repo: [Meta LLaMA GitHub](https://github.com/meta-llama/llama-models/blob/main/README.md)
  - Thorough documentation: [LLaMA 3.1 Docs](https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1)
  - Download instructions: [LLaMA Download](https://github.com/meta-llama/llama-models/blob/main/README.md)
  
- **Hugging Face**:
  - Hugging Face LLaMA models: [LLaMA on Hugging Face](https://huggingface.co/meta-llama)
  - LLaMA 3.1 8B Instruct: [LLaMA 8B Instruct Model](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct)

#### **Reflection LLaMA 3.1 70B**:
- Currently the top open-source LLM, trained with Reflection-Tuning to help detect and correct reasoning errors.
  - [Reflection LLaMA 70B](https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B)

#### **Running LLaMA on macOS**:
- Use this guide to run Meta LLaMA on macOS, leveraging the Ollama library.
  - [Running LLaMA on macOS](https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-mac/)
  
- Example repo supporting LLaMA 1 and 2 (avoid for LLaMA 3.1):
  - [MLX Examples](https://github.com/ml-explore/mlx-examples?tab=readme-ov-file)

Based on the steps you've outlined and considering your focus on cost-effectiveness, experimentation, and the ability to serve and test models efficiently, here's a breakdown of the best platform for each step:

---