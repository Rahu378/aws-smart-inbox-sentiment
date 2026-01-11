import boto3
import json
import os
from datetime import datetime
from urllib.parse import unquote

# Load your environment variables
try:
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    print("❌ .env file not found! Create it first.")
    exit(1)

sqs = boto3.client('sqs', region_name=os.environ.get('REGION', 'us-east-1'))
s3 = boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']
HIGH_PRIORITY_URL = os.environ['HIGH_PRIORITY_URL']
NORMAL_PRIORITY_URL = os.environ['NORMAL_PRIORITY_URL']

def check_queue(queue_url, queue_name):
    print(f"\n{'='*70}")
    print(f"📬 {queue_name} QUEUE")
    print('='*70)
    
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
            MessageAttributeNames=['All']
        )
        
        messages = response.get('Messages', [])
        
        if not messages:
            print("  ✅ Queue is empty")
            return
        
        print(f"  📨 Found {len(messages)} messages:")
        for i, msg in enumerate(messages, 1):
            try:
                body = json.loads(msg['Body'])
                key = body.get('original_key', 'unknown')
                # Make clickable S3 link
                s3_link = f"https://{BUCKET_NAME}.s3.amazonaws.com/{unquote(key)}"
                
                print(f"\n    📄 Message {i}:")
                print(f"       🔗 S3: {s3_link}")
                print(f"       📝 File: {key}")
                print(f"       😊 Sentiment: {body.get('sentiment', 'N/A')}")
                print(f"       ❌ Negative: {body.get('negative_score', 0):.1%}")
                print(f"       👀 Preview: {body.get('message', '')[:120]}...")
            except json.JSONDecodeError:
                print(f"    ❌ Message {i}: Invalid JSON")
                
    except Exception as e:
        print(f"  ❌ Error checking queue: {e}")

if __name__ == '__main__':
    print("\n�� AWS SMART INBOX - LIVE QUEUE MONITOR")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Bucket: {BUCKET_NAME}")
    print(f"🌎 Region: {os.environ.get('REGION', 'us-east-1')}")
    print("-" * 70)
    
    check_queue(HIGH_PRIORITY_URL, "🔴 HIGH PRIORITY")
    check_queue(NORMAL_PRIORITY_URL, "🟢 NORMAL PRIORITY")
    
    print("\n💡 Tip: Upload files to s3://smart-inbox-messages-1768095982/incoming/")
    print("    Watch messages appear live here! 👇")
    print("="*70)

