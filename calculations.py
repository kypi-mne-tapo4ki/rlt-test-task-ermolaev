# Description: This module contains the function that performs the aggregation of the salary data.
from datetime import datetime, timedelta
from enum import Enum

import motor.motor_asyncio


class TimePattern(Enum):
    HOUR = "%Y-%m-%dT%H:00:00"
    DAY = "%Y-%m-%dT00:00:00"
    MONTH = "%Y-%m-01T00:00:00"


async def aggregate_salary_data(dt_from, dt_upto, group_type):
    # Create a connection to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["RLT_test_task_db"]
    collection = db["sample_collection"]

    # Prepare the data
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)
    group_type_value = f"${group_type}"
    aggregator = []

    # This match stage filters the data by the specified date range.
    aggregator.append({"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}})

    # This projection stage prepares the data that we will group and aggregate in the subsequent stages of the pipeline.
    aggregator.append(
        {
            "$project": {
                "hour": {
                    "$dateToString": {"format": TimePattern.HOUR.value, "date": "$dt"}
                },
                "day": {
                    "$dateToString": {"format": TimePattern.DAY.value, "date": "$dt"}
                },
                "month": {
                    "$dateToString": {"format": TimePattern.MONTH.value, "date": "$dt"}
                },
                "value": 1,
            }
        }
    )
    # This group stage groups the data by the specified group_type and calculates the sum of the values.
    aggregator.append(
        {"$group": {"_id": group_type_value, "sum_value": {"$sum": "$value"}}}
    )
    # This sort stage sorts the data by the specified group_type.
    aggregator.append({"$sort": {"_id": 1}})

    result = await collection.aggregate(aggregator).to_list(None)
    result = {entry["_id"]: entry["sum_value"] for entry in result}

    # Prepare the data for the chart.

    labels = [entry for entry in result.keys()]
    dataset = [entry for entry in result.values()]

    preliminary_result = {"dataset": dataset, "labels": labels}

    return preliminary_result

