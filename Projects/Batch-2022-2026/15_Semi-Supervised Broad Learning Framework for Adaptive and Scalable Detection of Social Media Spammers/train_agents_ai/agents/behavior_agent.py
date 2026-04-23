def analyze_behavior(followers, following, actions):

    ratio = followers / (following + 1)

    spam_score = 0
    reasons = []

    if followers < 20 and following > 500:
        spam_score += 0.4
        reasons.append("Suspicious follower ratio")

    if actions > 1000:
        spam_score += 0.3
        reasons.append("Excessive activity")

    if ratio < 0.05:
        spam_score += 0.3
        reasons.append("Low follower credibility")

    return {
        "spam_score": min(spam_score,1),
        "reason": ", ".join(reasons)
    }