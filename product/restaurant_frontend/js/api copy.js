function apiFetch(url, options = {}) {
  const token = localStorage.getItem("access");

  const headers = options.headers || {};
  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  return fetch(url, {
    ...options,
    headers
  });
}

function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  location.reload();
}
