from app.config import settings

def format_recommendations(recommendations):
    output = f"{settings.TEAM_ID},{settings.AWS_ACCOUNT_ID}\n"
    if not recommendations:
        return output.rstrip('\n')  # Return just the header if there are no recommendations
    
    for rec in recommendations:
        # Escape newlines and tabs in description and tweet text
        description = rec['description'].replace('\n', '\\n').replace('\t', '\\t')
        latest_tweet = rec['latest_tweet'].replace('\n', '\\n').replace('\t', '\\t')
        
        output += f"{rec['user_id']}\t{rec['screen_name']}\t{description}\t{latest_tweet}\n"
    
    # Remove the last newline character
    return output.rstrip('\n')