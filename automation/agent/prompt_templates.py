def generate_test_prompt(feature_description):
    return f"""
    You are a senior QA engineer.

    Generate:
    1. Positive test cases
    2. Negative test cases
    3. Edge cases
    4. API test cases

    Feature:
    {feature_description}

    Output JSON:
    {{
      "positive": [],
      "negative": [],
      "edge": [],
      "api": []
    }}
    """
