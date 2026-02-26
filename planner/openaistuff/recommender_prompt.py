from openai import OpenAI
import json
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def build_prompt(stay_length, location, favorite_cuisine, activity_level, budget, social_context, dislikes, radius):
    return f"""You are an expert Chicago travel planner. Build a personalized, day-by-day itinerary for a visitor based strictly on their survey preferences below.

USER SURVEY:
- Trip length: {stay_length} days
- Staying in: {location}, Chicago  ← BASE LOCATION. Prioritize places here and in immediately adjacent neighborhoods.
- Search radius: {radius} miles from {location}. All itinerary items MUST be within {radius} miles of {location}.
- Favorite cuisine: {favorite_cuisine}
- Activity level: {activity_level}  (Low = relaxed/seated, Moderate = some walking, High = physically active)
- Budget: ${budget}
- Travelling with: {social_context}
- Wants to avoid: {dislikes}

RULES:
1. Only recommend places that genuinely exist in Chicago. Do not make up places.
2. The user is staying in {location}. Every recommended place MUST be within {radius} miles of {location}. Do not suggest places outside this radius.
3. You MUST generate exactly {stay_length} days of activities. Each day MUST have exactly 4 items: at least 2 activities/attractions AND at least 1 restaurant. That means {stay_length * 4} total itinerary items with "day" values from 1 to {stay_length}. Do NOT stop at Day 1.
4. Match recommendations to the user's cuisine preference, activity level, budget, and social context.
5. Add 8-12 alternative places (not used in the itinerary) into recommendations for the user to swap in, also within {radius} miles of {location}.
6. Never repeat a place between itinerary and recommendations.
7. CRITICAL: The itinerary array MUST contain items for ALL {stay_length} days. If the trip is 3 days, return 12 items (4 for day 1, 4 for day 2, 4 for day 3). Stopping early is unacceptable.
8. Output MUST be valid JSON in exactly this format — no extra text:

{{
    "itinerary": [
        {{
            "neighborhood": "Lincoln Park",
            "name": "Lincoln Park Zoo",
            "explanation": "Free admission makes it perfect for your budget, and the outdoor walks suit your moderate activity level.",
            "day": 1,
            "order": 1,
            "category": "activity"
        }}
    ],
    "recommendations": [
        {{
            "neighborhood": "River North",
            "name": "Frontera Grill",
            "explanation": "Award-winning Mexican cuisine that matches your taste preference.",
            "category": "restaurant"
        }}
    ]
}}"""


def activity_recommendation(stay_length, location, favorite_cuisine, activity_level, budget, social_context, dislikes, radius):
    prompt = build_prompt(stay_length, location, favorite_cuisine, activity_level, budget, social_context, dislikes, radius)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=4000,
        temperature=0,
        timeout=120,
        messages=[
            {"role": "system", "content": "You are a JSON-only response generator. Do not include any text outside the JSON object."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        content = response.choices[0].message.content.strip()

        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        parsed = json.loads(content)
        print(f"[DEBUG] GPT itinerary:\n{json.dumps(parsed, indent=4)}")
        return parsed
    except json.JSONDecodeError:
        print("[ERROR] Could not parse GPT response as JSON.")
        print("[RAW RESPONSE]", response.choices[0].message.content)
        return None


def get_recommendations(stay_length, location, favorite_cuisine, activity_level, budget, social_context, dislikes, radius=5):
    """
    Returns:
    {
        "itinerary": [ { neighborhood, name, explanation, day, order, category }, ... ],
        "recommendations": [ { neighborhood, name, explanation, category }, ... ]
    }
    """
    result = activity_recommendation(stay_length, location, favorite_cuisine, activity_level, budget, social_context, dislikes, radius)

    if result is None:
        raise ValueError("GPT response could not be parsed as JSON.")

    return result
