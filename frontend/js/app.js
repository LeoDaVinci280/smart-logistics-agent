console.log("app.js loaded");

/**
 * Last extracted shipment.
 *
 * Stores the latest result returned by
 * the PDF analysis endpoint.
 */
let currentShipment = null;

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

    if (!userMessage.trim()) {
        return;
    }

    const history =
        document.getElementById(
            "chat-history"
        );

    try {

        history.innerHTML += `

            <div class="chat-role">

                👤 You

            </div>

            <div class="user-message">

                ${userMessage}

            </div>
        `;

        history.innerHTML += `

            <div
                id="thinking-message"
                class="agent-message">

                🤖 Thinking...

            </div>
        `;

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

        const thinking =
            document.getElementById(
                "thinking-message"
            );

        if (thinking) {

            thinking.remove();
        }

        history.innerHTML += `

            <div class="chat-role">

                🤖 Smart Logistics Agent

            </div>

            <div class="agent-message">

                ${result.response}

            </div>
        `;

    history.scrollTop = history.scrollHeight;
        document.getElementById(
        "user-message"
    ).value = "";

    } catch (error) {

        history.innerHTML += `

            <div class="chat-role">

                🤖 Smart Logistics Agent

            </div>

            <div class="agent-message">

                Unable to contact the AI agent.

            </div>
        `;
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

    document.getElementById(
        "pdf-loading"
    ).style.display =
        "block";

    document.getElementById(
        "pdf-result"
    ).innerHTML = "";

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
            "pdf-loading"
        ).style.display =
            "none";

        currentShipment = result.result;
        if (currentShipment) {
            document.getElementById(
                "save-shipment-button"
            ).style.display = "inline-block";
        }

        const shipment =
            result.result;

        document.getElementById(
            "pdf-result"
        ).innerHTML = `

            <h3>
                ✅ Shipment Successfully Analysed
            </h3>

            <div class="pdf-summary">

                <div class="pdf-field">

                    <div class="pdf-label">
                        Tracking Number
                    </div>

                    <div class="pdf-value">
                        ${shipment.tracking_number}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Sender
                    </div>

                    <div class="pdf-value">
                        ${shipment.sender}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Recipient
                    </div>

                    <div class="pdf-value">
                        ${shipment.recipient}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Destination Country
                    </div>

                    <div class="pdf-value">
                        ${shipment.destination_country}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Transport Mode
                    </div>

                    <div class="pdf-value">
                        ${shipment.transport_mode}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Incoterm
                    </div>

                    <div class="pdf-value">
                        ${shipment.incoterm}
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Weight
                    </div>

                    <div class="pdf-value">
                        ${shipment.weight_kg} kg
                    </div>

                </div>

                <div class="pdf-field">

                    <div class="pdf-label">
                        Shipping Cost
                    </div>

                    <div class="pdf-value">
                        ${shipment.shipping_cost} ${shipment.currency}
                    </div>

                </div>

            </div>
        `;

    } catch (error) {

        document.getElementById(
            "pdf-result"
        ).innerHTML =
            "PDF analysis failed.";

        document.getElementById(
            "pdf-loading"
        ).style.display =
            "none";
    }
}

/**
 * Save analyzed shipment into database.
 */
async function saveShipment() {

    if (!currentShipment) {
        alert("No shipment available.");
        return;
    }

    try {
        const response =
            await fetch(
                `${API_BASE_URL}/save-shipment`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(
                        currentShipment
                    )
                }
            );

        const result = await response.json();

        if (result.status === "already_exists") {
            alert(result.message);
            return;
        }

        document.getElementById(
            "save-shipment-button"
        ).style.display =
            "none";

        alert(`Shipment saved (ID ${result.shipment_id})`);
        //
        // Refresh dashboard
        //
        loadDashboard();
        //
        // Refresh table
        //
        loadShipments();

    } catch (error) {
        alert("Unable to save shipment.");
    }
}


loadDashboard();
loadShipments();