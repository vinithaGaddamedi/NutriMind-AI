import os
import sys
import argparse
from openai import OpenAI

class LLMTestGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("ERROR: GROQ_API_KEY environment variable is required.")
            sys.exit(1)
            
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )

    def generate_test(self, react_file_path):
        if not os.path.exists(react_file_path):
            return f"Error: File {react_file_path} not found."
            
        with open(react_file_path, 'r') as f:
            react_code = f.read()

        prompt = f"""
You are an expert SDET and QA Automation Architect. 
I will provide you with the source code for a React component. 
Your task is to write a complete, robust Playwright Python test script for this component.

Requirements:
1. Use `pytest` and `playwright` (the sync API).
2. Write locators using best practices (e.g., semantic locators like roles and text matching).
3. Include comments explaining the user journey.
4. Add robust assertions.

Here is the React Component:
```javascript
{react_code}
```

Please output ONLY the Python code block containing the complete test script. No extra explanations.
"""
        print(f"🤖 Generating Playwright test for {os.path.basename(react_file_path)} via Groq LLaMA3...")
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Generation failed: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Playwright tests from React components.")
    parser.add_argument("component_file", help="Path to the React component file (.jsx)")
    parser.add_argument("--out", help="Path to output test file (e.g., test_generated.py)", default="test_generated.py")
    
    args = parser.parse_args()
    
    generator = LLMTestGenerator()
    generated_code = generator.generate_test(args.component_file)
    
    # Strip markdown codeblocks if LLM returned them
    if generated_code.startswith("```python"):
        generated_code = generated_code.replace("```python\n", "", 1)
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
            
    with open(args.out, "w") as f:
        f.write(generated_code.strip())
        
    print(f"✅ Test script generated successfully at: {args.out}")
