import { CSRF_TOKEN } from "./csrf_token.js";

async function getJSON(response) {
  /*
    Get json response.
  */

  if (response.status === 204) return '';
  return response.json();
};

function apiService(endpoint, method, data, imageData=false) {
  /*
    Generic function to make requests to an endpoint and
    process the response received in json format.

    * The default method is GET if no method is specified.
    * Set "imageData" true in order to send images.
  */

  let body = data;
  let headers = { 'X-CSRFToken': CSRF_TOKEN };
  if (!imageData) {
    body = data !== undefined ? JSON.stringify(data) : null;
    headers['Content-Type'] = 'application/json';
  }
  const config = {
    method: method || 'GET',
    body: body,
    headers: headers
  };
  return fetch(endpoint, config)
          .then(getJSON)
          .catch(error => {
            console.log(error);
          });
};

export { apiService };
