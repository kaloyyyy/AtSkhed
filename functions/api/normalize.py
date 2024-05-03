def normalize(data: list, constraint_max, setting_name) -> list:
    min_value = 0
    max_value = max(data)

    if min_value == max_value:  # Handle identical values (avoid division by zero)
        return [1] * len(data)  # Return a list of ones
    return [round(100 - ((x - 0) / (max_value - 0)) * 100, 8) for x in data]

