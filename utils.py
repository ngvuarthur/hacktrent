def validate_portions(adult_portions, child_portions):
    if adult_portions < 0 or child_portions < 0:
        raise ValueError("Portions cannot be negative.")
    return True
