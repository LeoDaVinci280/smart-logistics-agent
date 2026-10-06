console.log("app.js loaded");

const API_BASE_URL =
    "http://127.0.0.1:8000";


/**
 * Load dashboard analytics.
 */
async function loadDashboard() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/analytics`
            );

        const data =
            await response.json();

        document.getElementById(
            "total-shipments"
        ).textContent =
            data.total_shipments.total_shipments;

        document.getElementById(
            "average-cost"
        ).textContent =
            `${data.average_cost.average_shipping_cost} USD`;

        document.getElementById(
            "countries"
        ).innerHTML =
            data.countries.countries
                .map(
                    country =>
                        `<span class="badge">
                            ${country}
                        </span>`
                )
                .join("");

        document.getElementById(
            "transport-modes"
        ).innerHTML =
            data.transport_modes.transport_modes
                .map(
                    mode =>
                        `<span class="badge">
                            ${mode}
                        </span>`
                )
                .join("");
                
    } catch (error) {

        document.getElementById(
            "dashboard"
        ).innerHTML =
            "Unable to load analytics.";
    }
}


/**
 * Send a message to the AI agent.
 */
async function sendMessage() {

    const userMessage =
        document.getElementById(
            "user-message"
        ).value;

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/agent/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            message:
                                userMessage
                        }
                    )
                }
            );

        const result =
            await response.json();

        document.getElementById(
            "response"
        ).textContent =
            result.response;

    } catch (error) {

        document.getElementById(
            "response"
        ).textContent =
            "Unable to contact the AI agent.";
    }
}


loadDashboard();