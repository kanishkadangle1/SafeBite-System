const trackForm =
    document.getElementById("trackForm");

const complaintIdInput =
    document.getElementById("complaintId");

const trackError =
    document.getElementById("trackError");

const statusResult =
    document.getElementById("statusResult");


trackForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    trackError.classList.add("hidden");

    statusResult.classList.add("hidden");


    const complaintId =
        complaintIdInput.value.trim();


    if (!complaintId) {
        return;
    }


    const button =
        trackForm.querySelector("button");

    button.disabled = true;

    button.textContent = "Checking...";


    try {

        const result =
            await getComplaint(complaintId);


        document.getElementById(
            "resultNumber"
        ).textContent =
            result.complaint_number || complaintId;


        document.getElementById(
            "statusBadge"
        ).textContent =
            formatStatus(result.status);


        document.getElementById(
            "resultBusiness"
        ).textContent =
            result.business_name || "Not provided";


        document.getElementById(
            "resultFood"
        ).textContent =
            result.food_product || "Not provided";


        document.getElementById(
            "resultChannel"
        ).textContent =
            formatChannel(result.order_channel);


        document.getElementById(
            "resultPeople"
        ).textContent =
            result.people_affected ?? "0";


        document.getElementById(
            "resultMessage"
        ).textContent =
            getStatusMessage(result.status);


        statusResult.classList.remove("hidden");


    } catch (error) {

        trackError.textContent =
            "We couldn't find a report with that reference number.";

        trackError.classList.remove("hidden");

    } finally {

        button.disabled = false;

        button.textContent = "Check status";
    }

});


function formatStatus(status) {

    if (!status) {
        return "Received";
    }

    return status
        .replaceAll("_", " ")
        .replace(
            /\w\S*/g,
            word =>
                word.charAt(0).toUpperCase() +
                word.substring(1).toLowerCase()
        );
}


function formatChannel(channel) {

    if (!channel) {
        return "Not provided";
    }

    return channel
        .replaceAll("_", " ")
        .replace(
            /\w\S*/g,
            word =>
                word.charAt(0).toUpperCase() +
                word.substring(1).toLowerCase()
        );
}


function getStatusMessage(status) {

    switch (status) {

        case "UNDER_REVIEW":
            return "Your report is currently being reviewed by an authorized officer.";

        case "INVESTIGATION":
            return "Your report has moved into the investigation workflow.";

        case "RESOLVED":
            return "The review process for this report has been completed.";

        default:
            return "Your report has been received and is waiting for review.";
    }
}
