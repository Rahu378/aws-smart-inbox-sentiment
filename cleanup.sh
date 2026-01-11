#!/bin/bash

source .env

echo "🧹 Cleaning up AWS Smart Inbox resources..."

# Delete S3 buckets
echo "Deleting S3 buckets..."
aws s3 rb s3://$BUCKET_NAME --force
aws s3 rb s3://$PROCESSED_BUCKET --force

# Delete SQS queues
echo "Deleting SQS queues..."
aws sqs delete-queue --queue-url $HIGH_PRIORITY_URL
aws sqs delete-queue --queue-url $NORMAL_PRIORITY_URL

# Delete Lambda function
echo "Deleting Lambda function..."
aws lambda delete-function --function-name smart-inbox-sentiment-analyzer

# Delete IAM role
echo "Deleting IAM role..."
aws iam delete-role-policy --role-name SmartInboxLambdaRole --policy-name SmartInboxPolicy
aws iam delete-role --role-name SmartInboxLambdaRole

echo "✅ Cleanup complete!"
