def build_city_request_with_params_by_city_name(city_name, start_date, end_date):
    params = city_request_params.get(city_name).copy()
    """
    String (yyyy-mm-dd)
    """
    if params is None:
        raise ValueError(f"Unknown city with name = {city_name}")
    params["start_date"] = start_date
    params["end_date"] = end_date
    params["hourly"] = "temperature_2m"
    return params
