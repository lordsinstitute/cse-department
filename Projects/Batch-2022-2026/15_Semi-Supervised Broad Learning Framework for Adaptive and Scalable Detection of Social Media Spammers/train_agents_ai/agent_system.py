from train_agents_ai.agents.content_agent import analyze_content
from train_agents_ai.agents.behavior_agent import analyze_behavior
from train_agents_ai.agents.link_agent import analyze_links
from train_agents_ai.agents.decision_agent import final_decision


def detect_spam(tweet, followers, following, actions):

    content_result = analyze_content(tweet)

    behavior_result = analyze_behavior(
        followers,
        following,
        actions
    )

    link_result = analyze_links(tweet)

    decision = final_decision(
        content_result,
        behavior_result,
        link_result
    )

    return {
        "content_agent": content_result,
        "behavior_agent": behavior_result,
        "link_agent": link_result,
        "decision": decision
    }