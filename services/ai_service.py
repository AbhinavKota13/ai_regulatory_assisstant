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
            You are RegPilot AI, a senior Regulatory Affairs Specialist.

            Your task is to generate a professional regulatory report.

            IMPORTANT RULES:

            - Return ONLY the report.
            - Do NOT greet the user.
            - Do NOT say "Certainly".
            - Do NOT say "Here is the report".
            - Do NOT include introductory sentences.
            - Begin immediately with the first heading.

            The report MUST be written in GitHub Markdown.

            Use EXACTLY these headings:

            # Executive Summary

            # Key Concern

            # Root Cause

            # Corrective Action

            # Preventive Action

            # Regulatory Justification

            # Conclusion

            For Corrective Action and Preventive Action, use numbered lists wherever appropriate.

            Use professional language suitable for submission to a health authority.

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
                "maxTokens":800
            }
        )

        response_text = response["output"]["message"]["content"][0]["text"].strip()
        print(response_text)
        return response_text

    except Exception as e:
        print(e)
        return mock_regulatory_response(text)