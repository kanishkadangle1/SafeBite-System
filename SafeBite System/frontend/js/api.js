const API_BASE_URL = "http://127.0.0.1:8000";


async function apiRequest(endpoint, options = {}) {

    let response;

    try {

        response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                ...options,

                headers: {
                    "Content-Type": "application/json",

                    ...(options.headers || {})
                }
            }
        );

    } catch (error) {

        throw new Error(
            "SafeBite could not connect to the server. Make sure the FastAPI server is running."
        );
    }


    /*
        Try to read JSON response.
    */

    let data = null;

    try {

        data = await response.json();

    } catch {

        data = null;
    }


    /*
        Handle HTTP errors.
    */

    if (!response.ok) {

        /*
            FastAPI:

            {
                "detail": "message"
            }
        */

        if (data?.detail) {

            if (typeof data.detail === "string") {

                throw new Error(data.detail);

            }


            /*
                FastAPI validation:

                {
                    "detail": [
                        {
                            "loc": [...],
                            "msg": "...",
                            "type": "..."
                        }
                    ]
                }
            */

            if (Array.isArray(data.detail)) {

                const messages =
                    data.detail.map((item) => {

                        if (typeof item === "string") {
                            return item;
                        }

                        if (item?.msg) {

                            const location =
                                Array.isArray(item.loc)
                                    ? item.loc
                                        .filter(
                                            part =>
                                                part !== "body"
                                        )
                                        .join(" → ")
                                    : "";

                            return location
                                ? `${location}: ${item.msg}`
                                : item.msg;
                        }

                        return JSON.stringify(item);

                    });


                throw new Error(
                    messages.join("\n")
                );
            }


            /*
                Detail is another object.
            */

            throw new Error(
                JSON.stringify(data.detail)
            );
        }


        if (data?.message) {

            throw new Error(
                typeof data.message === "string"
                    ? data.message
                    : JSON.stringify(data.message)
            );
        }


        throw new Error(
            `Server returned HTTP ${response.status}.`
        );
    }


    return data;
}


/* ---------------------------------
   COMPLAINT API
---------------------------------- */

async function createComplaint(payload) {

    return apiRequest(
        "/complaints",
        {
            method: "POST",

            body: JSON.stringify(payload)
        }
    );
}


/* ---------------------------------
   SINGLE COMPLAINT
---------------------------------- */

async function getComplaint(id) {

    return apiRequest(
        `/complaints/${encodeURIComponent(id)}`
    );
}


/* ---------------------------------
   ALL COMPLAINTS
---------------------------------- */

async function getComplaints() {

    return apiRequest(
        "/complaints"
    );
}
