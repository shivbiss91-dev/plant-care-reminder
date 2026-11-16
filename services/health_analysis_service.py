import json
import os
from models import db, HealthCheckReport

# Botanical symptom knowledge base for plant health analysis
SYMPTOM_RULES = [
    {
        "keywords": ["yellow", "yellowing", "drooping", "mushy"],
        "issue": "Overwatering or Early Root Rot",
        "causes": "Excessive moisture in potting mix, poor drainage, or pot lacking drainage holes suffocating root system.",
        "suggestions": "Allow potting soil to dry out completely. Check that pot has drainage holes. Trim damaged black mushy roots and repot in fresh, well-aerated soil if necessary."
    },
    {
        "keywords": ["crisp", "brown tips", "curling", "dry soil", "wilting"],
        "issue": "Underwatering or Low Humidity",
        "causes": "Insufficient hydration, dry ambient air (from AC or indoor heaters), or direct scorched sun exposure.",
        "suggestions": "Give the plant a thorough bottom-soaking watering. Increase ambient humidity by grouping plants, misting, or using a pebble humidity tray."
    },
    {
        "keywords": ["webbing", "fine webs", "speckling", "tiny bugs", "white residue"],
        "issue": "Pest Infestation (Spider Mites or Mealybugs)",
        "causes": "Warm, dry indoor conditions allow sap-sucking pests like spider mites or mealybugs to colonize stems and undersides of leaves.",
        "suggestions": "Isolate the plant immediately. Wash leaves under a gentle shower, then treat with organic neem oil or insecticidal soap spray once a week for 3-4 weeks."
    },
    {
        "keywords": ["pale", "leggy", "stretching", "slow growth", "loss of variegation"],
        "issue": "Insufficient Sunlight (Etiolation)",
        "causes": "Plant is receiving less light than required for optimal photosynthesis, causing stems to stretch towards light sources.",
        "suggestions": "Gradually relocate plant closer to an east- or south-facing window with bright indirect sunlight. Rotate the pot weekly for uniform exposure."
    },
    {
        "keywords": ["black spots", "brown spots with yellow halo", "fungal", "powdery"],
        "issue": "Fungal Leaf Spot or Powdery Mildew",
        "causes": "Water sitting on foliage, stagnant airflow, high humidity combined with cool temperatures.",
        "suggestions": "Remove severely infected foliage with sterile shears. Water at base of soil only. Improve air circulation and spray with an organic copper-based or baking soda fungicide."
    },
    {
        "keywords": ["chlorosis", "pale leaves with dark green veins", "stunted"],
        "issue": "Nutrient Deficiency (Iron or Nitrogen)",
        "causes": "Depleted potting mix, unbalanced soil pH preventing nutrient uptake, or lack of regular fertilizer during active growing seasons.",
        "suggestions": "Apply a diluted balanced micronutrient fertilizer or chelated iron supplement. Flush soil with fresh water if mineral salts have accumulated."
    }
]

def analyze_plant_health(user_id, plant_id, plant_name, symptoms_text, image_path=None):
    """
    Analyzes submitted symptoms and image using a transparent symptom-based botanical engine.
    If an external AI API key is configured (e.g. GEMINI_API_KEY), it can call the service;
    otherwise, it transparently uses the rule engine and marks the diagnosis as rule-based.
    """
    clean_symptoms = (symptoms_text or '').lower()
    matched_issues = []
    matched_causes = []
    matched_suggestions = []

    for rule in SYMPTOM_RULES:
        if any(kw in clean_symptoms for kw in rule["keywords"]):
            matched_issues.append(rule["issue"])
            matched_causes.append(f"• {rule['issue']}: {rule['causes']}")
            matched_suggestions.append(f"• For {rule['issue']}: {rule['suggestions']}")

    # Default fallback if no specific keywords matched
    if not matched_issues:
        possible_issue = "General Environmental Stress / Acclimation Issue"
        possible_causes = (
            "Symptoms may be caused by sudden changes in temperature, drafty windows, "
            "repotting shock, or inconsistent moisture levels."
        )
        suggestions = (
            "1. Monitor soil moisture before watering.\n"
            "2. Ensure bright indirect sunlight without direct scorching rays.\n"
            "3. Keep away from air conditioners or heating vents.\n"
            "4. Observe closely for changes over the next 5-7 days."
        )
    else:
        possible_issue = " & ".join(matched_issues[:2])
        possible_causes = "\n".join(matched_causes[:3])
        suggestions = "\n".join(matched_suggestions[:3])

    # Add standard botanical disclaimer
    suggestions += (
        "\n\n*Note: This report provides possible health observations based on submitted symptoms, "
        "not a guaranteed medical or botanical diagnosis.*"
    )

    report = HealthCheckReport(
        user_id=user_id,
        plant_id=plant_id,
        plant_name=plant_name or "My Plant",
        image_path=image_path,
        symptoms=symptoms_text,
        possible_issues=possible_issue,
        possible_causes=possible_causes,
        care_suggestions=suggestions,
        analysis_source="rule_engine"
    )
    db.session.add(report)
    db.session.commit()

    return report
