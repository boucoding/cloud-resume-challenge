# DynamoDB Table for visitor counter
resource "aws_dynamodb_table" "visitor_counter" {
  name         = "${var.project_name}-visitor-counter"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name = "${var.project_name}-visitor-counter"
  }
}

# Initial seed item for the visitor counter
resource "aws_dynamodb_table_item" "initial_counter" {
  table_name = aws_dynamodb_table.visitor_counter.name
  hash_key   = aws_dynamodb_table.visitor_counter.hash_key

  # Notice we seed with 0 if not present, lifecycle ignores subsequent updates
  item = jsonencode({
    id    = { S = "visitors" }
    count = { N = "0" }
  })

  lifecycle {
    ignore_changes = [item]
  }
}
