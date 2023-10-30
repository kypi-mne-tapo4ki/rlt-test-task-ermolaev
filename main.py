import asyncio
from datetime import datetime

import motor.motor_asyncio


async def aggregate_salary_data(dt_from, dt_upto, group_type):
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["RLT_test_task_db"]
    collection = db["sample_collection"]

    pipeline = []
    if group_type == "month":
        pipeline.append({"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}})

    result = await collection.aggregate(pipeline).to_list(None)

    dataset = [entry["value"] for entry in result]
    labels = [entry["dt"] for entry in result]

    return {"dataset": dataset, "labels": labels}


async def main():
    dt_from = datetime.fromisoformat("2022-09-01T00:00:00")
    dt_upto = datetime.fromisoformat("2022-12-31T23:59:00")
    group_type = "month"

    result = await aggregate_salary_data(dt_from, dt_upto, group_type)
    print(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())