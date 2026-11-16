"""
Seed script to populate initial plant library data for common indoor and outdoor plants.
"""
from models import db, PlantLibrary

PLANT_LIBRARY_DATA = [
    {
        "name": "Snake Plant",
        "scientific_name": "Sansevieria trifasciata / Dracaena trifasciata",
        "category": "Succulent",
        "description": "Hardy evergreen perennial with striking upright sword-like green and yellow foliage. Excellent for beginners and air purification.",
        "watering_requirements": "Low. Water only when soil is completely dry throughout the pot, approximately every 14 days.",
        "fertilizer_requirements": "Light feeder. Apply balanced liquid fertilizer once a month during spring and summer only.",
        "sunlight_requirements": "Adaptable to low, medium, or bright indirect light.",
        "soil_requirements": "Well-draining cactus or succulent potting mix with perlite.",
        "care_instructions": "Avoid overwatering to prevent root rot. Wipe leaves periodically to remove dust.",
        "default_watering_frequency_days": 14,
        "default_fertilizer_frequency_days": 30
    },
    {
        "name": "Monstera Deliciosa",
        "scientific_name": "Monstera deliciosa",
        "category": "Indoor",
        "description": "Known as the Swiss Cheese Plant, famous for its large glossy leaves with natural perforations and fenestrations.",
        "watering_requirements": "Moderate. Water thoroughly when top 2-3 inches of soil feel dry, roughly every 7 days.",
        "fertilizer_requirements": "Fertilize once a month with balanced 20-20-20 houseplant fertilizer in spring and summer.",
        "sunlight_requirements": "Bright indirect sunlight. Avoid harsh direct sun which scorches leaves.",
        "soil_requirements": "Rich, peat-based, chunky potting mix with orchid bark and perlite.",
        "care_instructions": "Provide a moss pole or trellis for support as it climbs. Mist occasionally for humidity.",
        "default_watering_frequency_days": 7,
        "default_fertilizer_frequency_days": 30
    },
    {
        "name": "Peace Lily",
        "scientific_name": "Spathiphyllum wallisii",
        "category": "Flowering",
        "description": "Elegant indoor plant with dark glossy leaves and pristine white spathes. It visibly droops when thirsty, making it expressive.",
        "watering_requirements": "Consistent moisture. Water when the top inch of soil feels dry, approximately every 5-7 days.",
        "fertilizer_requirements": "Feed every 6 weeks during spring and summer with a balanced organic houseplant fertilizer.",
        "sunlight_requirements": "Thrives in medium to low indirect light.",
        "soil_requirements": "Moist, rich, well-aerated potting mix containing peat moss.",
        "care_instructions": "Sensitive to tap water chlorine and fluoride; use filtered or distilled water if leaf tips turn brown.",
        "default_watering_frequency_days": 5,
        "default_fertilizer_frequency_days": 42
    },
    {
        "name": "Golden Pothos",
        "scientific_name": "Epipremnum aureum",
        "category": "Indoor",
        "description": "Popular, fast-growing trailing vine with heart-shaped variegation. Highly resilient and forgiving of occasional neglect.",
        "watering_requirements": "Water when the top half of the soil has dried out, usually every 7 to 10 days.",
        "fertilizer_requirements": "Apply half-strength liquid fertilizer once a month during active growth.",
        "sunlight_requirements": "Tolerates low light, but thrives and maintains vibrant variegation in bright indirect light.",
        "soil_requirements": "Standard standard well-draining indoor potting mix.",
        "care_instructions": "Trim long vines to encourage bushier growth. Propagates easily in water from stem cuttings.",
        "default_watering_frequency_days": 7,
        "default_fertilizer_frequency_days": 30
    },
    {
        "name": "Spider Plant",
        "scientific_name": "Chlorophytum comosum",
        "category": "Indoor",
        "description": "Graceful arching green and white striped leaves that produce hanging offshoots or 'spiderettes'.",
        "watering_requirements": "Moderate watering. Keep soil lightly moist in summer, allowing top inch to dry between waterings (every 6-8 days).",
        "fertilizer_requirements": "Feed twice monthly during spring and summer with weak liquid houseplant food.",
        "sunlight_requirements": "Bright to moderate indirect light.",
        "soil_requirements": "Loose, well-draining loam potting soil with good drainage.",
        "care_instructions": "Prune brown tips and propagate baby plantlets directly in soil or water.",
        "default_watering_frequency_days": 7,
        "default_fertilizer_frequency_days": 21
    },
    {
        "name": "Aloe Vera",
        "scientific_name": "Aloe barbadensis Miller",
        "category": "Succulent",
        "description": "Stemless succulent with thick, fleshy serrated leaves filled with soothing medicinal gel.",
        "watering_requirements": "Infrequent and deep watering. Allow soil to dry out completely between waterings, roughly every 14-21 days.",
        "fertilizer_requirements": "Light feeder; fertilize once or twice during spring with phosphorus-heavy succulent food.",
        "sunlight_requirements": "Prefers 6 hours of bright indirect sunlight or direct morning sun.",
        "soil_requirements": "Porous sandy soil with excellent drainage or specialized cactus potting mix.",
        "care_instructions": "Ensure pots have drainage holes. Never let roots sit in standing water.",
        "default_watering_frequency_days": 14,
        "default_fertilizer_frequency_days": 60
    },
    {
        "name": "ZZ Plant",
        "scientific_name": "Zamioculcas zamiifolia",
        "category": "Indoor",
        "description": "Stunning architectural plant with waxy, dark-green feathered foliage. Stores water in tuberous rhizomes.",
        "watering_requirements": "Extremely drought tolerant. Water only when the potting mix is 100% dry, roughly every 14-20 days.",
        "fertilizer_requirements": "Balanced liquid fertilizer diluted to half strength once every 2 months in spring/summer.",
        "sunlight_requirements": "Thrives in low, moderate, or fluorescent office light.",
        "soil_requirements": "Fast-draining potting soil with added perlite or coarse sand.",
        "care_instructions": "Overwatering is the primary danger. When in doubt, wait a few more days before watering.",
        "default_watering_frequency_days": 18,
        "default_fertilizer_frequency_days": 60
    },
    {
        "name": "Holy Basil (Tulsi)",
        "scientific_name": "Ocimum tenuiflorum",
        "category": "Herb",
        "description": "Revered aromatic medicinal herb with clove-scented foliage and delicate purple flowers.",
        "watering_requirements": "Requires regular moisture. Water deeply when top layer feels dry, approximately every 2-3 days in warm weather.",
        "fertilizer_requirements": "Feed organic seaweed or vermicompost every 3-4 weeks to boost leafy vigor.",
        "sunlight_requirements": "At least 4 to 6 hours of direct sunlight daily (balcony or sunny window).",
        "soil_requirements": "Rich, moist, fertile, and well-draining garden soil mix.",
        "care_instructions": "Pinch back flower buds and terminal tips to stimulate lush branching and healthy foliage.",
        "default_watering_frequency_days": 3,
        "default_fertilizer_frequency_days": 21
    },
    {
        "name": "Jade Plant",
        "scientific_name": "Crassula ovata",
        "category": "Succulent",
        "description": "Miniature tree-like succulent with thick fleshy oval leaves and woody brown stems, symbolizing luck and prosperity.",
        "watering_requirements": "Water thoroughly once the soil has dried out completely, roughly every 10-14 days.",
        "fertilizer_requirements": "Feed every 30-45 days with diluted succulent fertilizer during spring and summer.",
        "sunlight_requirements": "Needs 4+ hours of direct sunlight or very bright sunny spots to maintain compact shape.",
        "soil_requirements": "Sandy, gritty soil mix with optimal drainage.",
        "care_instructions": "Do not let leaves sit wet. Dropping leaves indicate under- or over-watering.",
        "default_watering_frequency_days": 12,
        "default_fertilizer_frequency_days": 40
    },
    {
        "name": "Rubber Plant",
        "scientific_name": "Ficus elastica",
        "category": "Indoor",
        "description": "Bold indoor tree with oversized thick leathery leaves in deep emerald green or burgundy hues.",
        "watering_requirements": "Keep soil moderately moist in summer, allowing top 1-2 inches to dry between waterings, around every 7-10 days.",
        "fertilizer_requirements": "Apply high-nitrogen houseplant fertilizer once monthly in growing season.",
        "sunlight_requirements": "Medium to bright indirect light. Avoid sudden temperature changes or cold drafts.",
        "soil_requirements": "Well-aerated potting mix containing pine bark and perlite.",
        "care_instructions": "Gently clean dust off the glossy leaves with a damp cloth to encourage photosynthesis.",
        "default_watering_frequency_days": 7,
        "default_fertilizer_frequency_days": 30
    },
    {
        "name": "Rose Plant",
        "scientific_name": "Rosa",
        "category": "Outdoor",
        "description": "Classic woody perennial flowering shrub renowned for its fragrant blooms and vivid colors.",
        "watering_requirements": "Deep watering 2-3 times per week. Soil should remain consistently moist but never waterlogged.",
        "fertilizer_requirements": "Feed rich balanced rose food or compost every 2 weeks during peak blooming season.",
        "sunlight_requirements": "Full sun: minimum 6 hours of direct sunlight per day.",
        "soil_requirements": "Rich, loamy, slightly acidic, well-draining garden soil.",
        "care_instructions": "Prune dead or diseased stems and deadhead spent blooms to encourage continuous flowering.",
        "default_watering_frequency_days": 3,
        "default_fertilizer_frequency_days": 14
    },
    {
        "name": "Fiddle Leaf Fig",
        "scientific_name": "Ficus lyrata",
        "category": "Indoor",
        "description": "Show-stopping interior design favorite with enormous violin-shaped leaves and an upright columnar profile.",
        "watering_requirements": "Water thoroughly when the top 2 inches of soil feel dry, usually every 7-9 days.",
        "fertilizer_requirements": "Fertilize once a month during spring and summer with a balanced 3-1-2 ratio fertilizer.",
        "sunlight_requirements": "Bright, filtered indirect light. Sensitive to being moved once settled.",
        "soil_requirements": "Rich, fast-draining potting soil with excellent drainage.",
        "care_instructions": "Rotate pot every few weeks so all sides receive balanced light. Protect from drafts.",
        "default_watering_frequency_days": 8,
        "default_fertilizer_frequency_days": 30
    }
]

def seed_plant_library():
    """Insert default plant library entries if table is empty."""
    count = PlantLibrary.query.count()
    if count == 0:
        for item in PLANT_LIBRARY_DATA:
            plant_entry = PlantLibrary(**item)
            db.session.add(plant_entry)
        db.session.commit()
        print(f"Successfully seeded {len(PLANT_LIBRARY_DATA)} plants into PlantLibrary.")
    else:
        print(f"PlantLibrary already contains {count} entries. Skipping seeding.")
