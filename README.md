# AWS Smart Inbox Sentiment Analyzer

A serverless application that automatically analyzes message sentiment and routes them to priority queues.

## Architecture
```
S3 (Email Upload)
   ↓
Lambda: sentiment_processor
   ↓
AWS Comprehend
   ↓
DynamoDB (store results)
   ↓
SQS
   ├── HighPriorityQueue (NEGATIVE)
   ├── NormalQueue (POSITIVE / NEUTRAL)
   └── DLQ (Failures)

```

## Features

- 📧 Automatic message ingestion via S3
- 🧠 Real-time sentiment analysis using AWS Comprehend
- 🚦 Smart routing based on negative sentiment threshold
- 💾 Processed message storage with metadata
- 📊 Separate queues for priority handling

## Cost

- S3: ~$0.05/month (for 1000 messages)
- Lambda: ~$0.10/month
- Comprehend: ~$0.10/month
- SQS: Free tier covers most usage
- **Total: ~$0.20-$1/month**

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for step-by-step instructions.

## Testing
```bash
# Upload a test message
aws s3 cp sample-messages/negative.txt s3://$BUCKET_NAME/incoming/test.txt

# Monitor queues
python monitor_queues.py
```

## Cleanup
```bash
./cleanup.sh
```

## Author

Built following Zero To Cloud's AWS ML project guide.
