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
 * Load shipment database.
 */
async function loadShipments() {
    try {

        const response =
            await fetch(
                `${API_BASE_URL}/shipments`
            );

        const shipments =
            await response.json();

        const body =
            document.getElementById(
                "shipment-table-body"
            );

        body.innerHTML = "";

        shipments.forEach(
            shipment => {

            body.innerHTML += `
                <tr>

                    <td>
                        ${shipment.tracking_number}
                    </td>

                    <td>
                        ${shipment.destination_country}
                    </td>

                    <td>
                        ${shipment.transport_mode}
                    </td>

                    <td>
                        ${shipment.incoterm}
                    </td>

                    <td>
                        ${shipment.weight_kg}
                    </td>

                    <td>
                        ${shipment.shipping_cost}
                    </td>

                    <td>
                        ${shipment.currency}
                    </td>

                </tr>
            `;
        }
        );

    } catch (error) {

        console.error(
            "Unable to load shipments",
            error
        );
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

        const history =
            document.getElementById(
                "chat-history"
            );

        history.innerHTML += `
            <div class="user-message">
                ${userMessage}
            </div>
        `;

        history.innerHTML += `
            <div class="agent-message">
                ${result.response}
            </div>
        `;

    } catch (error) {

        document.getElementById(
            "response"
        ).textContent =
            "Unable to contact the AI agent.";
    }
}

async function analyzePdf() {

    const fileInput =
        document.getElementById(
            "pdf-file"
        );

    const file =
        fileInput.files[0];

    if (!file) {

        alert(
            "Please select a PDF file."
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/upload-pdf`,
                {
                    method: "POST",
                    body: formData
                }
            );

        const result =
            await response.json();

        document.getElementById(
            "pdf-result"
        ).innerHTML =
            `<pre>${JSON.stringify(
                result,
                null,
                2
            )}</pre>`;

    } catch (error) {

        document.getElementById(
            "pdf-result"
        ).innerHTML =
            "PDF analysis failed.";
    }
}


loadDashboard();
loadShipments();