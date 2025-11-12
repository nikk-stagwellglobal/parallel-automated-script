from parallel_ai_testing.query_parser import parse_search_term_to_text


async def boolean_to_natural_language(boolean_query: str) -> str:
    return await parse_search_term_to_text(boolean_query)


async def create_prompt(brand: str) -> str:
    prompt = (
        f'Generate a detailed report for the brand "{brand}" focusing on the following components (widgets): '
        f'Leaderboard - list the top 5 influencers or key figures impacting sentiment or market trends. '
        f'Sentiment Summary - provide a summary of the current sentiment (positive, neutral, negative) with explanations. '
        f'Volume Alerts - highlight any significant volume spikes or drops in mentions or discussions about the brand. '
        f'Root Causes - identify main factors or events causing changes in sentiment or volume. '
        f'Heatmap - describe geographic or demographic areas with notable activity or sentiment changes. '
        f'Please return the entire report in the strict JSON format below (do not add extra text outside JSON): '
        f'{{"brand": "{brand}", "leaderboard": [], "sentiment_summary": {{}}, "volume_alerts": [], '
        f'"root_causes": [], "heatmap": {{}}}}'
    )
    return prompt


def create_brand_query(brand: str) -> str:
    return f'(brand:"{brand}" OR company:"{brand}") AND (news OR announcement OR press)'
