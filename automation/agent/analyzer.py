import os
from openai import OpenAI

class AIFailureAnalyzer:
    def __init__(self):
        # We will use the groq API as previously requested by the user
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found. AI Failure Analysis will return a generic message.")
            self.client = None
        else:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )

    def analyze_failure(self, error_message, stack_trace, page_dom=None):
        if not self.client:
            return "AI Analysis skipped. Please set GROQ_API_KEY environment variable to enable AI Failure Analyzer."

        prompt = f"""
You are an expert QA Automation Engineer and AI Failure Analyzer.
A Playwright E2E test has failed. Please analyze the failure.

Error Message:
{error_message}

Stack Trace:
{stack_trace}
"""

        if page_dom:
            # truncate DOM to avoid token limits
            truncated_dom = page_dom[:10000]
            prompt += f"\nHere is a snippet of the page DOM at the time of failure:\n```html\n{truncated_dom}\n```"

        prompt += "\n\nPlease analyze why the test failed and provide a clear, actionable solution to fix the automation script or the UI bug. Format your output in clean Markdown."

        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Analysis failed to run: {str(e)}"
