# Azure-AI-Phishing-Detector
A cloud-native phishing detection app using a RAG architecture on Microsoft Azure



<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/336d832c-4ecb-4f0f-9434-c1bd038ce6a6" />




This repository documents the successful development and deployment of an AI-powered Phishing Detector. The project serves as a practical demonstration of building a modern, cloud-native AI solution using a Retrieval-Augmented Generation (RAG) architecture on Microsoft Azure.

---

### **▶️ Video Demo**



https://github.com/user-attachments/assets/0d65c298-f273-4281-b751-abd3281707a6




## 1. Project Overview

The goal of this project was to build an intelligent application that can analyze user-submitted text or URLs and determine if they are a phishing attempt. Unlike simple blocklists, this solution provides a real-time classification ("Safe," "Suspicious," or "Malicious") along with a clear, context-aware explanation for its conclusion, powered by a Large Language Model.

This application uses a Retrieval-Augmented Generation (RAG) architecture to analyze URLs and text for phishing threats in real-time, providing not just a classification, but a clear, AI-generated explanation for its reasoning.

Key Technologies Implemented:

AI Engine: Azure OpenAI (gpt-3.5-turbo)

Knowledge Base: Azure AI Search (with Semantic Search enabled)

Data Storage: Azure Blob Storage

Hosting: Azure Web Apps on an App Service Plan

<img width="600" height="600" alt="Gemini_Generated_Image_qzlj17qzlj17qzlj" src="https://github.com/user-attachments/assets/a04e0775-845f-4728-9fd9-844ee054b683" />



## 2. Core Architecture: Retrieval-Augmented Generation (RAG)

This project implements a RAG architecture to ensure the AI's responses are accurate and grounded in factual, domain-specific data. This approach is like giving the AI an "open-book exam."

-   **The "Brain":** An **Azure OpenAI `gpt-3.5-turbo`** model acts as the core reasoning engine.
-   **The "Textbook":** An **Azure AI Search** index, populated with a real-world list of verified phishing URLs from PhishTank, serves as the specialized knowledge base.

**Architecture:**

<img width="600" height="600" alt="Gemini_Generated_Image_8zdogf8zdogf8zdo" src="https://github.com/user-attachments/assets/651b2ecd-fdee-48d9-93ba-5c9fff5619be" />

---

**Raw Data To Indexed data**

<img width="600" height="600" alt="Gemini_Generated_Image_u9zd81u9zd81u9zd" src="https://github.com/user-attachments/assets/580a59ff-4585-4a38-888c-977e24147c8c" />

---


## 3. Technology Stack

| Service                | Tier / SKU     | Purpose in Project                                                               |
| :--------------------- | :------------- | :------------------------------------------------------------------------------- |
| **Azure OpenAI** | Pay-as-you-go  | Hosts the `gpt-3.5-turbo` model for reasoning and text generation.                 |
| **Azure AI Search** | **Basic Tier** | Hosts the indexed phishing data and provides the crucial **Semantic Search** capability. |
| **Azure Blob Storage** | Standard       | Stores the initial `verified_online.csv` dataset from PhishTank.                   |
| **Azure App Service Plan**| **Free (F1)** | Provides the compute resources to host the final web application.               |
| **Azure Web App** | -              | The pre-built, secure chatbot interface deployed from the Azure AI Studio.         |
| **Azure AI Studio** | -              | The central hub for configuring the RAG pipeline and managing deployment.        |

---

## 4. Challenges & Key Learnings

A major part of this project was navigating and overcoming real-world cloud deployment challenges.

-   **Initial Architecture:** The first plan was to deploy a custom Python backend using a serverless **Azure Function**.
-   **Troubleshooting:** I encountered persistent platform-level deployment failures, which I diagnosed as an unreachable Kudu (`.scm.`) management endpoint for my Azure for Students subscription.
-   **Strategic Pivot:** After extensive troubleshooting, I successfully pivoted my strategy to use the integrated **"Deploy a web app"** feature from Azure AI Studio. This required upgrading the AI Search service to a paid tier to meet compatibility requirements.
-   **Fine-Tuning:** Final debugging involved correctly configuring the AI Search **Semantic Configuration**, **Data Field Mappings**, and the Azure OpenAI **Content Filter** to get the application working perfectly.

This journey provided invaluable experience in advanced cloud diagnostics, problem-solving, and adapting an architecture to platform constraints.

---

## 5. Final Result

The project culminated in a fully functional, publicly accessible web application that correctly identifies phishing attempts using the RAG pattern.

<img width="600" height="600" alt="Screenshot 2025-09-29 110458" src="https://github.com/user-attachments/assets/85b5faaa-7e11-4c99-adda-9c196d033749" />
<img width="600" height="600" alt="Screenshot 2025-09-29 105611" src="https://github.com/user-attachments/assets/f4dc3131-e70d-4214-a351-e49cf2e430bb" />
