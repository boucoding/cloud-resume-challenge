import json
import os
import sys
from pathlib import Path
import boto3
import pytest
from moto import mock_aws

# Ensure backend root is on sys.path
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure environment variable points to test table before importing lambda_function
os.environ["DYNAMODB_TABLE"] = "test-visitor-counter"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "mock_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret"


@pytest.fixture
def dynamodb_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="test-visitor-counter",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
        yield table


def test_lambda_increment_first_visitor(dynamodb_table):
    import lambda_function as app

    app.table = dynamodb_table

    event = {
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": None,
    }
    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 1
    assert body["action"] == "increment"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"


def test_lambda_increment_subsequent_visitors(dynamodb_table):
    import lambda_function as app

    app.table = dynamodb_table

    # Seed count to 10
    dynamodb_table.put_item(Item={"id": "visitors", "count": 10})

    event = {
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": {"action": "increment"},
    }
    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 11


def test_lambda_read_only_action(dynamodb_table):
    import lambda_function as app

    app.table = dynamodb_table

    # Seed count to 42
    dynamodb_table.put_item(Item={"id": "visitors", "count": 42})

    event = {
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": {"action": "get"},
    }
    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 42
    assert body["action"] == "get"

    # Verify count did NOT increment in the database
    item = dynamodb_table.get_item(Key={"id": "visitors"}).get("Item")
    assert item["count"] == 42


def test_lambda_options_preflight(dynamodb_table):
    import lambda_function as app

    event = {
        "requestContext": {"http": {"method": "OPTIONS"}},
    }
    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Preflight OK"
