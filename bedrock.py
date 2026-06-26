import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId="amazon.nova-pro-v1:0",
    messages=[
        {
            "role": "user",
            "content": [{"text": "Write a 3-line regulatory response."}]
        }
    ],
    inferenceConfig={
        "temperature": 0.2,
        "maxTokens": 200
    }
)

print(response["output"]["message"]["content"][0]["text"])