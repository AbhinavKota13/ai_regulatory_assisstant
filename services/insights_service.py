def generate_insights(risk):

    if risk["level"] == "HIGH":

        return {

            "priority": "High",

            "impact": "Potential Compliance Risk",

            "recommended_action": (
                "Immediate review and corrective action are recommended "
                "before regulatory submission."
            ),

            "complexity": "High"

        }

    return {

        "priority": "Normal",

        "impact": "Low Regulatory Impact",

        "recommended_action": (
            "Proceed with the standard regulatory review process."
        ),

        "complexity": "Low"

    }