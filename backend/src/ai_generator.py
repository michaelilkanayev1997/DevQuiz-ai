import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import uuid

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fallback challenge if AI fails
FALLBACK_CHALLENGE: Dict[str, Any] = {
    "title": "Basic Python List Operation",
    "options": [
        "my_list.append(5)",
        "my_list.add(5)",
        "my_list.push(5)",
        "my_list.insert(5)",
    ],
    "correct_answer_id": 0,
    "explanation": "In Python, append() is the correct method to add an element to the end of a list.",
}

# Centralized system prompt for generating challenges
SYSTEM_PROMPT = (
    "Avoid repeating questions or topics. Each question must be unique and not similar to previous questions.\n"
    "If you've already generated a similar question, choose a different topic or angle within the same difficulty.\n"
    "You are an expert coding challenge creator.\n"
    "Your task is to generate a coding question with multiple choice answers.\n"
    "The question should be appropriate for the specified difficulty level.\n\n"
    "For easy questions: Focus on basic syntax, simple operations, or common programming concepts.\n"
    "For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.\n"
    "For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.\n\n"
    "Return the challenge in the following JSON structure:\n"
    "{\n"
    '  "title": "The question title",\n'
    '  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],\n'
    '  "correct_answer_id": 0,\n'
    '  "explanation": "Detailed explanation of why the correct answer is right"\n'
    "}\n\n"
    "Make sure the options are plausible but with only one clearly correct answer."
)


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    print(f"[INFO] Generating challenge for difficulty: {difficulty}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge. ID: {uuid.uuid4()}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        content = response.choices[0].message.content
        print("[DEBUG] Raw response content:", content)

        challenge_data = json.loads(content)

        # Validate required structure
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        missing = [field for field in required_fields if field not in challenge_data]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        print("[SUCCESS] Challenge generated successfully.")
        return challenge_data

    except (OpenAIError, ValueError, json.JSONDecodeError) as e:
        print(f"[ERROR] Challenge generation failed: {e}")
        return FALLBACK_CHALLENGE
