from datetime import date
from models import db, WateringDecision, Plant

def evaluate_watering_decision(user_id, plant_id, soil_condition):
    """
    Evaluates plant care schedule combined with manually reported soil condition.
    Returns (recommendation, explanation).
    Recommendations: 'Water Now' | 'Wait and Check Later' | 'Avoid Watering Now'
    """
    plant = Plant.query.filter_by(id=plant_id, user_id=user_id).first_or_404()
    soil_condition = (soil_condition or '').strip().title()
    if soil_condition not in ['Dry', 'Slightly Moist', 'Wet']:
        raise ValueError("Invalid soil condition. Must be 'Dry', 'Slightly Moist', or 'Wet'.")

    days_until = plant.days_until_watering
    category = (plant.category or 'Indoor').lower()
    
    # Logic Engine:
    if soil_condition == 'Wet':
        recommendation = "Avoid Watering Now"
        explanation = (
            f"The soil around {plant.name} is currently wet. Adding more water now risks "
            f"suffocating roots and causing root rot, even if scheduled for watering soon. "
            f"Allow the top soil layer to dry before adding more water."
        )
    elif soil_condition == 'Slightly Moist':
        if 'succulent' in category or plant.watering_frequency_days >= 14:
            recommendation = "Avoid Watering Now"
            explanation = (
                f"{plant.name} is a drought-tolerant variety that prefers completely dry soil between waterings. "
                f"Since the soil is still slightly moist, hold off until it is fully dry throughout."
            )
        elif days_until <= 0 and ('herb' in category or 'flowering' in category):
            recommendation = "Water Now"
            explanation = (
                f"{plant.name} is a moisture-loving variety and scheduled for water today. "
                f"A light watering is appropriate to maintain consistent moisture without waterlogging."
            )
        else:
            recommendation = "Wait and Check Later"
            explanation = (
                f"The soil is still slightly moist. {plant.name} does not urgently require water today. "
                f"Re-check soil moisture in 1 to 2 days before giving water."
            )
    else:  # Dry
        if days_until <= 1:
            recommendation = "Water Now"
            explanation = (
                f"The soil is dry and {plant.name} is scheduled for watering. "
                f"Give it a deep, thorough watering until water drains freely from the drainage holes."
            )
        elif days_until > 3:
            recommendation = "Water Now"
            explanation = (
                f"Although the routine schedule was in {days_until} days, the soil has already dried out completely. "
                f"Environmental factors (heat, sunlight, or low humidity) may have increased water loss. Water thoroughly now."
            )
        else:
            recommendation = "Water Now"
            explanation = (
                f"The soil feels dry to the touch. It is safe and beneficial to water {plant.name} now."
            )

    # Save decision in database
    decision = WateringDecision(
        user_id=user_id,
        plant_id=plant.id,
        soil_condition=soil_condition,
        recommendation=recommendation,
        explanation=explanation
    )
    db.session.add(decision)
    db.session.commit()

    return decision
