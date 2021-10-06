import { CSRF_TOKEN } from "./csrf_token.js";

async function getJSON(response) {
  /*
    Get json response.
  */

  if (response.status === 204) return '';
  return response.json();
};

function apiService(endpoint, method, data, contentType='application/json') {
  /*
    Generic function to make requests to an endpoint and
    process the response received in json format.

    * The default method is GET if no method is specified.
  */

  let body = data;
  if (contentType === 'application/json') {
    body = data !== undefined ? JSON.stringify(data) : null;
  }
  const config = {
    method: method || 'GET',
    body: body,
    headers: {
      'Content-Type': contentType,
      'X-CSRFToken': CSRF_TOKEN
    }
  };
  return fetch(endpoint, config)
          .then(getJSON)
          .catch(error => {
            console.log(error);
          });
};

function apiServicev2(endpoint, method, data) {
  /*
    Generic function to make requests to an endpoint and
    process the response received in json format.

    * The default method is GET if no method is specified.
  */

  const config = {
    method: method,
    body: data,
    headers: {
      'X-CSRFToken': CSRF_TOKEN
    }
  };
  return fetch(endpoint, config)
          .then(getJSON)
          .catch(error => {
            console.log(error);
          });
};

export { apiService, apiServicev2 };
