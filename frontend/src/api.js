import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ── Emails ─────────────────────────────────────────────────────────

export async function uploadEmail(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/emails/analyze', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function listEmails(skip = 0, limit = 50) {
  const { data } = await api.get('/emails', { params: { skip, limit } })
  return data
}

export async function getEmail(id) {
  const { data } = await api.get(`/emails/${id}`)
  return data
}

// ── Analysis ───────────────────────────────────────────────────────

export async function runFullAnalysis(emailId) {
  const { data } = await api.post(`/emails/${emailId}/analyze-full`)
  return data
}

export async function getFullAnalysis(emailId) {
  const { data } = await api.get(`/emails/${emailId}/analyze-full`)
  return data
}

// ── Classification ─────────────────────────────────────────────────

export async function classifyEmail(emailId) {
  const { data } = await api.post(`/emails/${emailId}/classify`)
  return data
}

// ── Risk Engine ────────────────────────────────────────────────────

export async function computeRisk(emailId) {
  const { data } = await api.post(`/emails/${emailId}/risk`)
  return data
}

export async function getRisk(emailId) {
  const { data } = await api.get(`/emails/${emailId}/risk`)
  return data
}

// ── Health ─────────────────────────────────────────────────────────

export async function checkHealth() {
  const { data } = await axios.get('/health')
  return data
}
