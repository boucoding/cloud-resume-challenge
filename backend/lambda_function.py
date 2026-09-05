import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "cloud-resume-visitor-counter")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def build_response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """
    Handles visitor counter requests.
    - Query parameter '?action=get' performs a read-only fetch without incrementing.
    - Default behavior atomically increments the counter and returns the new count.
    """
    logger.info(f"Incoming event: {json.dumps(event)}")

    http_method = (
        event.get("requestContext", {}).get("http", {}).get("method")
        or event.get("httpMethod", "GET")
    )
    if http_method == "OPTIONS":
        return build_response(200, {"message": "Preflight OK"})

    query_params = event.get("queryStringParameters") or {}
    action = query_params.get("action", "increment")

    try:
        if action == "get":
            response = table.get_item(Key={"id": "visitors"})
            item = response.get("Item", {})
            current_count = int(item.get("count", 0))
            return build_response(200, {"count": current_count, "action": "get"})

        # Atomic increment using DynamoDB ADD expression (avoids race conditions)
        response = table.update_item(
            Key={"id": "visitors"},
            UpdateExpression="ADD #count :incr",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="UPDATED_NEW",
        )

        new_count = int(response["Attributes"]["count"])
        logger.info(f"Visitor count updated to: {new_count}")

        return build_response(200, {"count": new_count, "action": "increment"})

    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return build_response(500, {"error": "Database error", "details": e.response["Error"]["Message"]})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return build_response(500, {"error": "Internal server error", "details": str(e)})
