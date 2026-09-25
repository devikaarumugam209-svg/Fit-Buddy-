import json

from .ai_common import generate_gemini_text
from .config import TIP_MODEL


def generate_nutrition(profile: dict) -> dict:
	raw_response = generate_gemini_text(
		TIP_MODEL,
		f"Create concise, actionable nutrition tips for this fitness profile: {profile}. "
		"Return only valid JSON with string keys guidance, daily_habits (array of three "
		"strings), and meal_ideas (object with breakfast, lunch, snack, dinner strings). "
		"Avoid medical claims.",
	)
	clean_response = raw_response.removeprefix("```json").removesuffix("```").strip()
	generated = json.loads(clean_response)
	if not isinstance(generated, dict) or not generated.get("daily_habits") or not generated.get("meal_ideas"):
		raise ValueError("Gemini returned invalid nutrition data")
	return generated