const form = document.getElementById("complaintForm");

const platformWrapper =
    document.getElementById("platformWrapper");

const formError =
    document.getElementById("formError");

const successPanel =
    document.getElementById("successPanel");

const referenceNumber =
    document.getElementById("referenceNumber");

const submitButton =
    document.getElementById("submitButton");


/*
    Show delivery platform only when
    the user selected online delivery.
*/

document
    .querySelectorAll('input[name="order_channel"]')
    .forEach(radio => {

        radio.addEventListener("change", () => {

            if (radio.value === "DELIVERY_PLATFORM") {

                platformWrapper.classList.remove("hidden");

            } else if (radio.checked) {

                platformWrapper.classList.add("hidden");

                document.getElementById("platform").value = "";
            }
        });

    });


/*
    Submit complaint.
*/

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    formError.classList.add("hidden");

    submitButton.disabled = true;

    submitButton.textContent = "Submitting...";


    const selectedChannel =
        document.querySelector(
            'input[name="order_channel"]:checked'
        );


    const symptoms =
        Array.from(
            document.querySelectorAll(
                ".symptom-grid input:checked"
            )
        ).map(
            checkbox => checkbox.value
        );


    const payload = {

        description:
            document
                .getElementById("description")
                .value
                .trim(),

        business_name:
            document
                .getElementById("business_name")
                .value
                .trim(),

        food_product:
            document
                .getElementById("food_product")
                .value
                .trim(),

        order_channel:
            selectedChannel
                ? selectedChannel.value
                : null,

        platform:
            document
                .getElementById("platform")
                .value || null,

        order_date:
            document
                .getElementById("order_date")
                .value,

        people_affected:
            Number(
                document
                    .getElementById("people_affected")
                    .value
            ) || 0,

        reported_symptoms:
            symptoms
    };


    try {

        const result =
            await createComplaint(payload);


        /*
            Python backend has successfully
            created the complaint.
        */

        referenceNumber.textContent =
            result.complaint_number;


        form.classList.add("hidden");

        document
            .querySelector(".report-intro")
            .classList.add("hidden");

        successPanel.classList.remove("hidden");


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });


    } catch (error) {

        console.error(error);

       let errorMessage = "We could not submit your report.";

if (error && error.message) {
    errorMessage = error.message;
}

if (typeof errorMessage === "object") {
    errorMessage =
        errorMessage.msg ||
        errorMessage.message ||
        JSON.stringify(errorMessage);
}

formError.textContent = errorMessage;

        formError.classList.remove("hidden");


        submitButton.disabled = false;

        submitButton.textContent = "Submit report";
    }

});
