function getCsrfToken() {
  const cookie = document.cookie
    .split(';')
    .find((c) => c.trim().startsWith('csrftoken='))
  return cookie ? decodeURIComponent(cookie.split('=')[1]) : ''
}

export async function apiFetch(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCsrfToken(),
    ...options.headers,
  }
  const res = await fetch(url, {
    credentials: 'same-origin',
    ...options,
    headers,
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw { status: res.status, data }
  }
  return res.json()
}

export { getCsrfToken }
