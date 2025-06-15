import time
import json
import os
from dotenv import load_dotenv
import boto3 # Added for AWS Bedrock

load_dotenv() # Load .env file

# --- Configuration ---
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "anthropic": os.getenv("ANTHROPIC_API_KEY", ""), # Remains for completeness or other uses
    "google": os.getenv("GOOGLE_API_KEY", ""),
}

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:3000/api/generate")
AWS_REGION = os.getenv("AWS_REGION_NAME", "us-east-1") # Default AWS region if not in .env

MODELS_TO_EVALUATE = [
    # {"name": "GPT-4o", "type": "openai", "model_id": "gpt-4o"},
    {"name": "Claude Sonnet (Bedrock)", "type": "anthropic", "model_id": "anthropic.claude-3-sonnet-20240229-v1:0"},
    {"name": "Gemini Flash", "type": "google", "model_id": "gemini-1.5-flash-latest"},
    {"name": "DeepSeek R1 7b", "type": "ollama", "model_id": "deepseek-r1:7b"}
]

EVALUATION_PROMPTS = {
    "AppDev (Code Generation)": [
        {
            "id": "appdev_py_fizzbuzz",
            "task_description": "Python: FizzBuzz Implementation",
            "prompt": "Write a Python function that prints numbers from 1 to 100. For multiples of three print 'Fizz' instead of the number and for the multiples of five print 'Buzz'. For numbers which are multiples of both three and five print 'FizzBuzz'."
        },
        {
            "id": "appdev_js_api_fetch",
            "task_description": "JavaScript: Fetch API Data with Error Handling",
            "prompt": "Write a JavaScript asynchronous function that fetches JSON data from 'https://jsonplaceholder.typicode.com/todos/1'. The function should log the title of the todo to the console. Implement basic error handling for network issues or invalid JSON."
        },
        {
            "id": "appdev_python_class",
            "task_description": "Python: Simple Class for a 'Book'",
            "prompt": "Create a Python class named 'Book' with a constructor that accepts 'title', 'author', and 'isbn'. The class should have a method `get_details()` that returns a string with the book's information."
        }
    ],
    "Data (SQL Generation & Analysis)": [
        {
            "id": "data_sql_join",
            "task_description": "SQL: Select employees and department names",
            "prompt": "Given two tables, 'employees' (columns: id INT, name VARCHAR, department_id INT) and 'departments' (columns: id INT, name VARCHAR), write a SQL query to select the name of all employees and their respective department names."
        },
        {
            "id": "data_sql_aggregate_filter",
            "task_description": "SQL: Total sales per product last month, filtered",
            "prompt": "Write a SQL query for a 'sales' table (columns: sale_id INT, product_id INT, sale_date DATE, amount DECIMAL) to find the total sales amount for each product_id sold in the previous calendar month. Only include products where the total sales amount for that month was greater than $1000. Assume current date is 2025-06-14."
        }
    ],
    "DevOps (Infrastructure Automation)": [
        {
            "id": "devops_bash_file_check",
            "task_description": "Bash: Check for file existence",
            "prompt": "Write a Bash script that checks if a file named 'app.config' exists in the current directory. If it exists, the script should print 'app.config found.' to standard output. If it does not exist, it should print 'app.config not found.'."
        },
        {
            "id": "devops_terraform_s3",
            "task_description": "Terraform: Basic S3 Bucket Configuration",
            "prompt": "Provide a minimal Terraform HCL configuration snippet to declare an AWS S3 bucket resource named 'my-appdev-eval-bucket'. The bucket should have versioning enabled."
        }
    ]
}

# --- Model Interaction Functions ---

def query_openai_model(model_id, prompt_text):
    """Sends a prompt to the OpenAI API and returns the response."""
    # TODO: Implement using the openai Python library
    import openai
    client = openai.OpenAI(api_key=API_KEYS["openai"])
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_text}],
            model=model_id,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"OpenAI API Error: {str(e)}"
    print(f"    SIMULATING OpenAI call for {model_id}")
    return f"Simulated OpenAI response for: {prompt_text[:70]}..."

def query_anthropic_model(model_id, prompt_text):
    """Sends a prompt to an Anthropic model via AWS Bedrock."""
    # This function now uses AWS Bedrock for Anthropic models.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION_NAME
    # are available as environment variables (e.g., in .env file) or configured for boto3.
    # The model_id should be the Bedrock model identifier (e.g., "anthropic.claude-3-sonnet-20240229-v1:0")

    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_REGION
            # Credentials will be picked up from environment variables,
            # shared credentials file, or IAM role if not explicitly passed.
        )

        # Claude 3 models on Bedrock use a specific payload structure.
        # Refer to AWS Bedrock documentation for the exact payload for your model.
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31", # Required for Claude 3
            "max_tokens": 2048, # Adjust as needed
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt_text}]
                }
            ]
        })

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())

        # The response structure for Claude 3 messages API on Bedrock
        # is typically response_body['content'][0]['text']
        if response_body.get("content") and isinstance(response_body["content"], list) and len(response_body["content"]) > 0:
            return response_body["content"][0].get("text")
        else:
            # Log the actual response_body for debugging if parsing fails
            # print(f"    Bedrock response_body: {response_body}")
            return "Error: Could not parse response from Bedrock. Check response structure."

    except Exception as e:
        # Consider logging the full exception for easier debugging
        # import traceback
        # print(traceback.format_exc())
        return f"AWS Bedrock (Anthropic) API Error: {str(e)}"
    print(f"    SIMULATING Anthropic (Bedrock) call for {model_id}")
    return f"Simulated Anthropic (Bedrock) response for: {prompt_text[:70]}..."

def query_google_model(model_id, prompt_text):
    """Sends a prompt to the Google Generative AI API and returns the response."""
    # TODO: Implement using the google.generativeai Python library
    import google.generativeai as genai
    genai.configure(api_key=API_KEYS["google"])
    model = genai.GenerativeModel(model_id)
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Google API Error: {str(e)}"
    print(f"    SIMULATING Google call for {model_id}")
    return f"Simulated Google response for: {prompt_text[:70]}..."

def query_ollama_model(model_id, prompt_text):
    """Sends a prompt to a local Ollama API and returns the response."""
    # TODO: Implement using the requests library
    import requests
    payload = {"model": model_id, "prompt": prompt_text, "stream": False}
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "Error: 'response' key not found in Ollama output.")
    except requests.exceptions.RequestException as e:
        return f"Ollama API Error: {str(e)}"
    except KeyError:
         return "Ollama API Error: Malformed JSON response from Ollama."
    print(f"    SIMULATING Ollama call for {model_id}")
    return f"Simulated Ollama response for: {prompt_text[:70]}..."

# --- Evaluation Runner ---
def run_evaluation():
    evaluation_results = []
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    for model_config in MODELS_TO_EVALUATE:
        model_name = model_config["name"]
        model_type = model_config["type"]
        model_id = model_config["model_id"]

        print(f"\n--- Evaluating Model: {model_name} ({model_id}) ---")

        for category, prompts_in_category in EVALUATION_PROMPTS.items():
            print(f"  -- Category: {category} --")
            for prompt_item in prompts_in_category:
                prompt_id = prompt_item["id"]
                task_desc = prompt_item["task_description"]
                prompt_text = prompt_item["prompt"]

                print(f"    Running Task: {task_desc} (ID: {prompt_id})")

                start_time = time.time()
                response_text = ""
                error_message = None

                try:
                    if model_type == "openai":
                        response_text = query_openai_model(model_id, prompt_text)
                    elif model_type == "anthropic": # This will now call the Bedrock version
                        response_text = query_anthropic_model(model_id, prompt_text)
                    elif model_type == "google":
                        response_text = query_google_model(model_id, prompt_text)
                    elif model_type == "ollama":
                        response_text = query_ollama_model(model_id, prompt_text)
                    else:
                        raise ValueError(f"Unknown model type: {model_type}")
                except Exception as e:
                    error_message = str(e)
                    response_text = f"ERROR DURING API CALL: {e}"
                    print(f"      ERROR: {e}")

                end_time = time.time()
                latency_seconds = end_time - start_time

                result_entry = {
                    "model_name": model_name,
                    "model_id": model_id,
                    "category": category,
                    "prompt_id": prompt_id,
                    "task_description": task_desc,
                    "prompt_text": prompt_text,
                    "response_text": response_text,
                    "latency_seconds": round(latency_seconds, 3),
                    "error": error_message,
                    "rating": "",
                    "comments": ""
                }
                evaluation_results.append(result_entry)
                print(f"      Latency: {latency_seconds:.3f}s")

    raw_results_filename = f"ai_evaluation_raw_results_{timestamp}.json"
    with open(raw_results_filename, "w") as f:
        json.dump(evaluation_results, f, indent=2)
    print(f"\n--- Evaluation Collection Complete ---")
    print(f"Collected {len(evaluation_results)} results.")
    print(f"Raw results saved to: {raw_results_filename}")
    print("\nNext Steps:")
    print(f"1. Review the responses in '{raw_results_filename}'.")
    print("2. For each entry, fill in the 'rating' and 'comments' fields.")
    print("3. Use the annotated JSON data to generate your final Markdown comparison table.")

    return raw_results_filename, evaluation_results

# --- Helper for Markdown Generation (Example) ---
def generate_markdown_from_annotated_results(annotated_results_file):
    try:
        with open(annotated_results_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: Annotated results file '{annotated_results_file}' not found.")
        return

    markdown_lines = ["# AI Model Comparison Results", ""]
    from collections import defaultdict
    grouped_results = defaultdict(lambda: defaultdict(list))
    for res in results:
        grouped_results[res['category']][res['model_name']].append(res)

    for category, models_data in grouped_results.items():
        markdown_lines.append(f"## {category}")
        markdown_lines.append("")
        markdown_lines.append("| Model Evaluated | Task Description | Rating | Latency (s) | Comments |")
        markdown_lines.append("|-----------------|--------------------|--------|---------------|----------|")
        for model_name, tasks in models_data.items():
            for task in tasks:
                markdown_lines.append(
                    f"| {model_name} | {task['task_description']} | {task.get('rating', 'N/A')} | {task.get('latency_seconds', 'N/A')} | {task.get('comments', '')} |"
                )
        markdown_lines.append("")

    output_md_filename = annotated_results_file.replace(".json", "_report.md")
    with open(output_md_filename, 'w') as f:
        f.write("\n".join(markdown_lines))
    print(f"\nMarkdown report generated: {output_md_filename}")
    print("Please review and customize the Markdown file as needed.")


if __name__ == "__main__":
    print("Starting AI Model Evaluation Script...")
    raw_file, _ = run_evaluation()

    print(f"\nIMPORTANT: Now, please open '{raw_file}', review each response,")
    print("and fill in the 'rating' and 'comments' fields for each entry.")
    input("Press Enter after you have manually annotated the JSON file to generate the Markdown report...")

    generate_markdown_from_annotated_results(raw_file)