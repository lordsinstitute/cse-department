// Agentic AI step-by-step animation

document.addEventListener("DOMContentLoaded", function () {

    const runBtn = document.getElementById("runAgents");

    if (!runBtn) return;

    runBtn.addEventListener("click", function () {

        startAgentAnimation();

    });

});


function startAgentAnimation() {

    hideAllAgents();

    runAgent("content_agent", 1000);
    runAgent("behavior_agent", 3000);
    runAgent("link_agent", 5000);
    runAgent("decision_agent", 7000);

}


// Hide results initially

function hideAllAgents() {

    const agents = [
        "content_agent",
        "behavior_agent",
        "link_agent",
        "decision_agent"
    ];

    agents.forEach(function (agent) {

        document.getElementById(agent + "_spinner").style.display = "block";

        document.getElementById(agent + "_result").style.display = "none";

    });

}


// Run each agent with delay

function runAgent(agentId, delay) {

    setTimeout(function () {

        const spinner = document.getElementById(agentId + "_spinner");

        const result = document.getElementById(agentId + "_result");

        if (spinner) spinner.style.display = "none";

        if (result) result.style.display = "block";

    }, delay);

}