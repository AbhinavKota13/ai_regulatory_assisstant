import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId="add_mode_id",
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