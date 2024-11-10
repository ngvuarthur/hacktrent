class Recipe:
    def __init__(self, name, ingredients, instructions, dietary_restrictions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.dietary_restrictions = dietary_restrictions
        self.environmental_impact_score = {"carbon_footprint": None, "water_usage": None}
    
    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "dietary_restrictions": self.dietary_restrictions,
            "environmental_impact_score": self.environmental_impact_score
        }
