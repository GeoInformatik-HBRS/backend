import pytest
from processor.src.use_cases.category_routing import CategoryRoutingUseCase

@pytest.fixture
def category_routing_case_instance():
    return CategoryRoutingUseCase()

@pytest.mark.parametrize("input_data,expected", [("street_damage", "technical_department"), ("illegal_waste", "waste_department")])
def test_category_routing(category_routing_case_instance, input_data, expected):
    assert category_routing_case_instance.execute(input_data) == expected

def test_category_routing_with_invalid_category_throws_value_error(category_routing_case_instance):
    pytest.raises(ValueError, category_routing_case_instance.execute, "invalid_category")