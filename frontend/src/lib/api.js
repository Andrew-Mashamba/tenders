const BASE = '/api'

function getToken() {
  return localStorage.getItem('tenders_access_token')
}

async function fetchJSON(url, opts = {}) {
  const headers = { ...opts.headers }
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (opts.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json'

  let res = await fetch(`${BASE}${url}`, { ...opts, headers })

  // Auto-refresh on 401
  if (res.status === 401) {
    const refreshToken = localStorage.getItem('tenders_refresh_token')
    if (refreshToken) {
      const refreshRes = await fetch(`${BASE}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })
      if (refreshRes.ok) {
        const data = await refreshRes.json()
        localStorage.setItem('tenders_access_token', data.access_token)
        localStorage.setItem('tenders_refresh_token', data.refresh_token)
        headers['Authorization'] = `Bearer ${data.access_token}`
        res = await fetch(`${BASE}${url}`, { ...opts, headers })
      } else {
        localStorage.removeItem('tenders_access_token')
        localStorage.removeItem('tenders_refresh_token')
        window.location.href = '/login'
        throw new Error('Session expired')
      }
    } else {
      window.location.href = '/login'
      throw new Error('Not authenticated')
    }
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    const error = new Error(err.detail || err.message || 'Request failed')
    error.status = res.status
    error.data = err
    throw error
  }
  return res.json()
}

export const api = {
  // Stats
  getStats: () => fetchJSON('/stats'),

  // Tenders
  getTenders: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/tenders?${qs}`)
  },
  getTender: (id) => fetchJSON(`/tenders/${id}`),

  // Applications (user-scoped)
  getApplications: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/me/applications?${qs}`)
  },
  createApplication: (data) =>
    fetchJSON('/me/applications', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  updateApplication: (id, data) =>
    fetchJSON(`/me/applications/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  deleteApplication: (id) =>
    fetchJSON(`/me/applications/${id}`, { method: 'DELETE' }),

  // Legacy application endpoints
  getApplication: (id) => fetchJSON(`/applications/${id}`),
  getSentLog: (limit = 50) => fetchJSON(`/sent-log?limit=${limit}`),

  // Opportunities
  getOpportunities: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/opportunities?${qs}`)
  },

  // Institutions
  getInstitutions: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/institutions?${qs}`)
  },
  getInstitution: (slug) => fetchJSON(`/institutions/${slug}`),

  // Institution following
  getMyInstitutions: () => fetchJSON('/me/institutions'),
  followInstitution: (slug) =>
    fetchJSON('/me/institutions', {
      method: 'POST',
      body: JSON.stringify({ slug }),
    }),
  unfollowInstitution: (slug) =>
    fetchJSON(`/me/institutions/${slug}`, { method: 'DELETE' }),

  // Company documents
  getCompanyDocs: () => fetchJSON('/me/company-docs'),
  uploadCompanyDoc: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const headers = {}
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await fetch(`${BASE}/me/company-docs`, {
      method: 'POST',
      headers,
      body: formData,
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }))
      throw new Error(err.detail || 'Upload failed')
    }
    return res.json()
  },
  deleteCompanyDoc: (filename) =>
    fetchJSON(`/me/company-docs/${encodeURIComponent(filename)}`, { method: 'DELETE' }),
  getCompanyDocUrl: (filename) => `${BASE}/me/company-docs/${encodeURIComponent(filename)}`,

  // Application actions
  prepareApplications: (tender_ids) =>
    fetchJSON('/applications/prepare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tender_ids }),
    }),
  applyToTenders: (tender_ids, dry_run = false) =>
    fetchJSON('/applications/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tender_ids, dry_run }),
    }),
  getJobs: () => fetchJSON('/applications/jobs'),
  getJob: (jobId) => fetchJSON(`/applications/jobs/${jobId}`),
  checkPdfExists: (tenderId) => fetchJSON(`/applications/pdf-exists/${tenderId}`),
  getApplicationPdfUrl: (tenderId) => `${BASE}/applications/pdfs/${tenderId}`,
  openAuthenticatedUrl: async (url) => {
    const headers = {}
    const token = getToken()
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await fetch(url.startsWith('/') ? url : `${BASE}/${url}`, { headers })
    if (!res.ok) throw new Error('Failed to fetch file')
    const blob = await res.blob()
    const blobUrl = URL.createObjectURL(blob)
    window.open(blobUrl, '_blank')
    setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
  },

  // Scraper
  getScrapeStatus: () => fetchJSON('/scrape/status'),
  startScrape: (data = {}) =>
    fetchJSON('/scrape/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),
  stopScrape: () =>
    fetchJSON('/scrape/stop', { method: 'POST' }),

  // Notifications
  getNotifications: (limit = 20) => fetchJSON(`/notifications?limit=${limit}`),

  // Documents
  getDocumentText: (slug, tenderId, filename) =>
    fetchJSON(`/documents/${slug}/${tenderId}/${filename}/text`),

  // Plans & Billing
  getPlans: () => fetchJSON('/plans'),
  createCheckout: (planId) =>
    fetchJSON('/billing/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan_id: planId }),
    }),
  createPortal: () =>
    fetchJSON('/billing/portal', { method: 'POST' }),
  getBillingStatus: () => fetchJSON('/billing/status'),

  // Profile
  updateProfile: (data) =>
    fetchJSON('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  // Admin
  adminGetStats: () => fetchJSON('/admin/stats'),
  adminGetUsers: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/admin/users?${qs}`)
  },
  adminGetUser: (id) => fetchJSON(`/admin/users/${id}`),
  adminUpdateUser: (id, data) =>
    fetchJSON(`/admin/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
  adminResetPassword: (id) =>
    fetchJSON(`/admin/users/${id}/reset-password`, { method: 'POST' }),
  adminCreateInstitution: (data) =>
    fetchJSON('/admin/institutions', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  adminGetCreateJob: (jobId) => fetchJSON(`/admin/institutions/jobs/${jobId}`),
  adminGetInstitutions: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/admin/institutions?${qs}`)
  },
  adminToggleInstitution: (slug) =>
    fetchJSON(`/admin/institutions/${slug}/toggle`, { method: 'PUT' }),
  adminTriggerScrape: (slug) =>
    fetchJSON(`/admin/institutions/${slug}/scrape`, { method: 'POST' }),
  adminGetInstitutionLogs: (slug) =>
    fetchJSON(`/admin/institutions/${slug}/logs`),
  adminGetSubscriptions: () => fetchJSON('/admin/subscriptions'),
  adminGetTenders: (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return fetchJSON(`/admin/tenders?${qs}`)
  },
}
