# AI Model Evaluation Script

This script automates the process of evaluating various AI language models based on a predefined set of prompts. It queries different AI APIs (OpenAI, Anthropic via AWS Bedrock, Google, and local Ollama instances), records their responses and latencies, and facilitates the generation of a comparative report.

## Features

*   Supports multiple AI model providers:
    *   OpenAI (e.g., GPT-4, GPT-3.5-turbo)
    *   Anthropic via AWS Bedrock (e.g., Claude 3 Sonnet, Claude 3 Haiku)
    *   Google (e.g., Gemini Pro, Gemini Flash)
    *   Ollama (for locally hosted models like Llama, Mistral, etc.)
*   Customizable list of models to evaluate.
*   Customizable set of prompts categorized for evaluation.
*   Records latency for each API call.
*   Generates a raw JSON file with all evaluation data.
*   Prompts the user to manually annotate (rate and comment) the raw results.
*   Generates a Markdown report from the annotated results for easy comparison.

## Prerequisites

1.  **Python 3.7+**
2.  **Required Python Packages**: Install them using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
3.  **API Keys and Configuration**:
    *   Create a `.env` file in the root directory of the project. You can copy `.env.example` (if provided) or create it from scratch.
    *   Populate the `.env` file with your API keys:
        ```dotenv
        OPENAI_API_KEY="your_openai_api_key"
        # ANTHROPIC_API_KEY is not directly used if using Bedrock, but good to have if you plan to use Anthropic's direct API elsewhere.
        # ANTHROPIC_API_KEY="your_anthropic_api_key"
        GOOGLE_API_KEY="your_google_ai_studio_api_key"

        # For AWS Bedrock (used for Anthropic models in this script)
        AWS_ACCESS_KEY_ID="your_aws_access_key_id"
        AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
        AWS_REGION_NAME="your_aws_region" # e.g., us-east-1

        # For Ollama (if testing local models)
        OLLAMA_API_URL="http://localhost:11434/api/generate" # Default Ollama API URL
        ```
4.  **AWS CLI (Optional but Recommended for Bedrock)**:
    *   If using AWS Bedrock, ensure your AWS CLI is configured with the necessary credentials and permissions to invoke Bedrock models. The script uses `boto3`, which can pick up credentials from shared AWS credential files (`~/.aws/credentials`), environment variables, or IAM roles.
5.  **Ollama (Optional)**:
    *   If you plan to evaluate models using Ollama, ensure Ollama is installed and running locally.
    *   Pull the models you want to test using the Ollama CLI (e.g., `ollama pull llama3`).
    *   Make sure the `OLLAMA_API_URL` in your `.env` file points to your running Ollama instance. The default is usually `http://localhost:11434/api/generate`.

## Setup

1.  **Clone the repository** (if applicable) or ensure you have the script (`ai_model_evaluation.py`) and `requirements.txt` in your project directory.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys**: Create and populate the `.env` file as described in the "Prerequisites" section.

## Configuration

Open the `ai_model_evaluation.py` script and modify the following sections as needed:

1.  **`API_KEYS` Dictionary (Loaded from `.env`)**:
    *   The script loads keys from the `.env` file. Ensure the keys in `.env` match what the script expects.

2.  **`MODELS_TO_EVALUATE` List**:
    *   This list defines which models will be queried. Each entry is a dictionary:
        ```python
        MODELS_TO_EVALUATE = [
            {
                "name": "GPT-4o (OpenAI)", # User-friendly name for reports
                "type": "openai",         # 'openai', 'anthropic', 'google', or 'ollama'
                "model_id": "gpt-4o"      # Actual model ID for the API
            },
            {
                "name": "Claude 3 Sonnet (Bedrock)",
                "type": "anthropic", # This uses the Bedrock client for Anthropic
                "model_id": "anthropic.claude-3-sonnet-20240229-v1:0"
            },
            {
                "name": "Gemini 1.5 Flash (Google)",
                "type": "google",
                "model_id": "gemini-1.5-flash-latest"
            },
            {
                "name": "Llama3 8b (Ollama)",
                "type": "ollama",
                "model_id": "llama3:8b" # Ensure this model is pulled in Ollama
            },
            # Add more models as needed
        ]
        ```
    *   **`name`**: A descriptive name for the model that will appear in reports.
    *   **`type`**: Must be one of `"openai"`, `"anthropic"` (for Bedrock-hosted Anthropic models), `"google"`, or `"ollama"`. This determines which query function is called.
    *   **`model_id`**: The specific model identifier required by the respective API.

3.  **`EVALUATION_PROMPTS` Dictionary**:
    *   This dictionary organizes prompts by category. Each category contains a list of prompt items:
        ```python
        EVALUATION_PROMPTS = {
            "AppDev (Code Generation)": [
                {
                    "id": "appdev_py_fizzbuzz", # Unique ID for the prompt
                    "task_description": "Python: FizzBuzz Implementation",
                    "prompt": "Write a Python function that prints numbers from 1 to 100..."
                },
                # Add more prompts in this category
            ],
            "Data (SQL Generation & Analysis)": [
                # Add prompts for this category
            ],
            # Add more categories and prompts
        }
        ```
    *   **`id`**: A unique identifier for the prompt.
    *   **`task_description`**: A brief description of what the prompt is asking the AI to do.
    *   **`prompt`**: The actual text of the prompt to be sent to the AI model.

## Running the Script

1.  Execute the script from your terminal:
    ```bash
    python ai_model_evaluation.py
    ```

2.  **Evaluation Process**:
    *   The script will iterate through each model defined in `MODELS_TO_EVALUATE`.
    *   For each model, it will iterate through all prompts in `EVALUATION_PROMPTS`.
    *   It will send the prompt to the model's API, record the response, and measure the latency.
    *   Progress will be printed to the console.

3.  **Raw Results**:
    *   Once all models and prompts have been processed, the script will save the raw results to a JSON file named `ai_evaluation_raw_results_YYYYMMDD-HHMMSS.json` (timestamped).

4.  **Manual Annotation**:
    *   The script will then pause and prompt you:
        ```
        IMPORTANT: Now, please open 'ai_evaluation_raw_results_YYYYMMDD-HHMMSS.json', review each response,
        and fill in the 'rating' and 'comments' fields for each entry.
        Press Enter after you have manually annotated the JSON file to generate the Markdown report...
        ```
    *   Open the generated JSON file. For each entry, you will find empty `"rating": ""` and `"comments": ""` fields.
    *   Review the `"response_text"` and fill in your subjective `rating` (e.g., "Good", "Poor", "5/5", "Needs Improvement") and any `comments`.
    *   Save the JSON file after annotating.

5.  **Generate Markdown Report**:
    *   Return to the terminal where the script is paused and press `Enter`.
    *   The script will read the annotated JSON file and generate a Markdown report named `ai_evaluation_raw_results_YYYYMMDD-HHMMSS_report.md`.

## Output Files

*   **`ai_evaluation_raw_results_YYYYMMDD-HHMMSS.json`**:
    *   Contains the detailed raw output from each model for every prompt, including the prompt text, response text, latency, and placeholders for your ratings and comments.
*   **`ai_evaluation_raw_results_YYYYMMDD-HHMMSS_report.md`**:
    *   A Markdown file summarizing the evaluation, structured by category and including the task description, your rating, latency, and comments for each model and prompt. This file is suitable for sharing or further analysis.

## Troubleshooting

*   **API Errors**:
    *   Ensure your API keys in `.env` are correct and have the necessary permissions.
    *   Check for rate limits if you are sending many requests.
    *   Verify the `model_id` is correct for the specified API and that you have access to it.
*   **AWS Bedrock Errors**:
    *   Confirm your AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME`) are correctly set up and have permissions for Bedrock.
    *   Ensure the Bedrock model ID is accurate and available in your specified AWS region.
*   **Ollama Errors**:
    *   Make sure the Ollama service is running locally.
    *   Verify the `OLLAMA_API_URL` in `.env` is correct (default: `http://localhost:11434/api/generate`).
    *   Ensure the Ollama model specified by `model_id` (e.g., `llama3:8b`) has been pulled and is available in your Ollama instance (`ollama list`).
*   **`FileNotFoundError` for `.env`**: Make sure the `.env` file exists in the same directory as the script.
*   **Module Not Found Errors**: Ensure you have installed all packages from `requirements.txt`.

This script provides a flexible framework for systematically evaluating and comparing AI models. Customize the models and prompts to suit your specific evaluation needs.