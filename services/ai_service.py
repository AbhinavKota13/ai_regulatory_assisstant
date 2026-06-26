import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

USE_REAL_AI = True


def mock_regulatory_response(text):

    return """
REGULATORY RESPONSE (Mock Output)

Query Summary:
...

Conclusion:
...
"""


def generate_response(text, risk, query_type=None):

    if not USE_REAL_AI:
        return mock_regulatory_response(text)

    try:

        text = text[:12000]

        prompt = f"""
            You are an experienced Regulatory Affairs Specialist.

            Document Risk Level:
            {risk["level"]}

            Detected Risk Keywords:
            {", ".join(risk["keywords"]) if risk["keywords"] else "None"}

            Prepare a professional response suitable for submission to a regulatory authority.
            The response must contain:
            1. Executive Summary
            2. Key Concern
            3. Root Cause
            4. Corrective Action
            5. Preventive Action
            6. Regulatory Justification
            7. Conclusion
            Document:
            {text}
        """

        response = client.converse(
            modelId="amazon.nova-pro-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            inferenceConfig={
                "temperature":0.2,
                "maxTokens":400
            }
        )

        return response["output"]["message"]["content"][0]["text"]

    except Exception as e:
        print(e)
        return mock_regulatory_response(text)