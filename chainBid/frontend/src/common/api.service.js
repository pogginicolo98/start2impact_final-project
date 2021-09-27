import { CSRF_TOKEN } from "./csrf_token.js";

async function getJSON(response) {
  /*
    Get json response.
  */

  if (response.status === 204) return '';
  return response.json();
};

function apiService(endpoint, method, data) {
  /*
    Generic function to make requests to an endpoint and
    process the response received in json format.

    * The default method is GET if no method is specified.
  */

  const config = {
    method: method || 'GET',
    body: data !== undefined ? JSON.stringify(data) : null,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN
    }
  };
  return fetch(endpoint, config)
          .then(getJSON)
          .catch(error => {
            console.log(error);
          });
};

export { apiService };
