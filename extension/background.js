const API_BASE = "http://localhost:8000";

chrome.runtime.onMessage.addListener(
  (message, sender, sendResponse) => {

    async function handleRequest() {
      try {

        switch (message.type) {

          case "GENERATE": {
            const response = await fetch(
              `${API_BASE}/generate`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify(
                  message.payload
                )
              }
            );

            const data =
              await response.json();

            sendResponse(data);
            break;
          }

          case "SAVE_PROFILE": {
            const response = await fetch(
              `${API_BASE}/save-profile`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify(
                  message.payload
                )
              }
            );

            const data =
              await response.json();

            sendResponse(data);
            break;
          }

          case "GET_STATUS": {
            const response = await fetch(
              `${API_BASE}/status`
            );

            const data =
              await response.json();

            sendResponse(data);
            break;
          }

          default:
            sendResponse({
              error:
                "Unknown message type"
            });
        }

      } catch (error) {

        console.error(error);

        sendResponse({
          error:
            "Backend not running. Start the FastAPI server."
        });
      }
    }

    handleRequest();

    return true;
  }
);