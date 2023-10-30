import pytest
import test_data

from calculations import aggregate_salary_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data,expected_len,expected_result",
    [
        (test_data.input_data_1, 4, test_data.expected_result_1),
        (test_data.input_data_2, 61, test_data.expected_result_2),
        (test_data.input_data_3, 25, test_data.expected_result_3),
    ],
)
async def test_aggregate_salary_data(input_data, expected_len, expected_result):
    result = await aggregate_salary_data(**input_data)

    assert len(result["dataset"]) == expected_len
    assert result == expected_result
