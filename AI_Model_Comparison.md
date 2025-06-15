
# AI Model Comparison Table

### Legend:
- ✅ Excellent  
- 👍 Good  
- ⚠️ Basic / Limited Support  
- ❌ Not Supported  

---

### 📌 Use Case: **Code Quality (Python, JS, Classes)**
| Model              | FizzBuzz | JS Fetch API | Python Class | Comments |
|-------------------|----------|--------------|---------------|----------|
| **Claude Sonnet** | ✅       | ✅           | ✅            | Accurate and well-explained responses; verbose but solid. |
| **Gemini Flash**  | ✅       | ✅           | ✅            | Efficient, concise code; excellent formatting and examples. |
| **DeepSeek-R1:7B**| 👍       | 👍           | 👍            | Adds meta-thinking steps; slower but logically clear. |

---

### 📌 Use Case: **SQL Generation**
| Model              | Join Query | Aggregated Sales Filter | Comments |
|-------------------|------------|--------------------------|----------|
| **Claude Sonnet** | ✅         | ✅                       | High-quality, production-ready SQL. |
| **Gemini Flash**  | ✅         | ✅                       | Clean and concise with date range precision. |
| **DeepSeek-R1:7B**| ✅         | ❌                       | Join is good; timed out on aggregation filter query. |

---

### 📌 Use Case: **Infrastructure Automation (Scripts)**
| Model              | Bash File Check | Terraform S3 | Comments |
|-------------------|------------------|--------------|----------|
| **Claude Sonnet** | ✅               | ✅           | Canonical Terraform and Bash responses. |
| **Gemini Flash**  | ✅               | ✅           | Clear and minimal with best practices. |
| **DeepSeek-R1:7B**| ✅               | ⚠️           | Bash OK; Terraform syntax incorrect, likely hallucinated. |

---

### 📌 Use Case: **Ease of Use**
| Model              | Ease of Use | Comments |
|-------------------|-------------|----------|
| **Claude Sonnet** | 👍          | Helpful, detailed, but verbose for simple tasks. |
| **Gemini Flash**  | ✅          | Direct, fast, and minimalistic — great for copy-paste usage. |
| **DeepSeek-R1:7B**| ⚠️          | Provides logical steps, but too verbose and slower response. |

---

### 📌 Use Case: **Speed / Latency**
| Model              | Average Latency | Comments |
|-------------------|------------------|----------|
| **Claude Sonnet** | ~9–13 sec       | Slower than Gemini; acceptable for depth. |
| **Gemini Flash**  | ~3–5 sec        | Fastest across all tasks. |
| **DeepSeek-R1:7B**| ~26–49 sec      | Significantly slower; timed out on some prompts. |
