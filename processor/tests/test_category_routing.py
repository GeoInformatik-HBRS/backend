import pytest
from src.use_cases.category_routing import CategoryRoutingUseCase

@pytest.fixture
def category_routing_case_instance():
    return CategoryRoutingUseCase()

@pytest.mark.parametrize("input_data,expected", [
    ("street_damage", "technical_department"),
    ("illegal_waste", "waste_department"),
    ("fallen_tree_in_park", "parks_department"),
    ("damaged_traffic_sign", "traffic_department"),
    ("blocked_storm_drain", "water_department"),
    ("damaged_bus_stop", "public_facilities_department"),
])
def test_department_routing(category_routing_case_instance, input_data, expected):
    assert category_routing_case_instance.execute(input_data) == expected

def test_multiple_categories_per_department(category_routing_case_instance):
    assert category_routing_case_instance.execute("street_damage") == "technical_department"
    assert category_routing_case_instance.execute("broken_streetlight") == "technical_department"
    assert category_routing_case_instance.execute("damaged_sidewalk") == "technical_department"

@pytest.mark.parametrize("input_data,expected", [
    ("street_damage", "technical_department"),
    ("broken_streetlight", "technical_department"),
    ("damaged_sidewalk", "technical_department"),
    ("illegal_waste", "waste_department"),
    ("overflowing_public_bin", "waste_department"),
    ("litter_in_public_area", "waste_department"),
    ("fallen_tree_in_park", "parks_department"),
    ("damaged_park_bench", "parks_department"),
    ("overgrown_park_path", "parks_department"),
    ("damaged_traffic_sign", "traffic_department"),
    ("broken_traffic_light", "traffic_department"),
    ("faded_road_markings", "traffic_department"),
    ("blocked_storm_drain", "water_department"),
    ("leaking_public_pipe", "water_department"),
    ("street_flooding", "water_department"),
    ("broken_playground_equipment", "public_facilities_department"),
    ("damaged_bus_stop", "public_facilities_department"),
    ("broken_public_toilet", "public_facilities_department"),
])
def test_all_supported_categories(category_routing_case_instance, input_data, expected):
    assert category_routing_case_instance.execute(input_data) == expected

@pytest.mark.parametrize("input_data", ["unknown_problem", "invalid_category"])
def test_unknown_categories(category_routing_case_instance, input_data):
    pytest.raises(ValueError, category_routing_case_instance.execute, input_data)

@pytest.mark.parametrize("input_data", ["", "Street_Damage"])
def test_invalid_category_ids(category_routing_case_instance, input_data):
    pytest.raises(ValueError, category_routing_case_instance.execute, input_data)
