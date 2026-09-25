import os


def generate_gemini_text(model: str, prompt: str) -> str:
	from google import genai

	client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
	response = client.models.generate_content(model=model, contents=prompt)
	text = getattr(response, "text", None)
	if not text:
		raise RuntimeError("Gemini returned an empty response")
	return text.strip()