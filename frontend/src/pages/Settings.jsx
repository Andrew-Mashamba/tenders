import React, { useState, useEffect, useRef } from 'react'
import { useAuth } from '../lib/auth'
import { api } from '../lib/api'
import PlanBadge from '../components/PlanBadge'
import { Building2, Plus, X, Upload, FileText, Trash2, Download, FolderOpen } from 'lucide-react'

const PROFILE_FIELDS = [
  { key: 'company_name', label: 'Company Name', required: true },
  { key: 'contact_person', label: 'Contact Person', placeholder: 'Name used on cover letters' },
  { key: 'contact_title', label: 'Title', placeholder: 'e.g., Managing Director, CEO' },
  { key: 'phone', label: 'Phone' },
  { key: 'contact_email', label: 'Email', placeholder: 'e.g., info@company.co.tz' },
  { key: 'address', label: 'Office Address' },
  { key: 'website', label: 'Website', placeholder: 'e.g., www.company.co.tz' },
]

const EMPTY_PROFILE = PROFILE_FIELDS.reduce((acc, f) => ({ ...acc, [f.key]: '' }), {
  capabilities: [],
  key_facts: [],
  partnership_model: '',
})

export default function Settings() {
  const { user, refreshUser } = useAuth()
  const [name, setName] = useState(user?.name || '')
  const [company, setCompany] = useState(user?.company || '')
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  // Company profile state
  const [profile, setProfile] = useState(() => {
    const p = user?.company_profile || {}
    return { ...EMPTY_PROFILE, ...p }
  })
  const [newCapability, setNewCapability] = useState('')
  const [newFact, setNewFact] = useState('')
  const [savingProfile, setSavingProfile] = useState(false)
  const [profileMessage, setProfileMessage] = useState('')

  // Company documents state
  const [companyDocs, setCompanyDocs] = useState([])
  const [docsLoading, setDocsLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [docsMessage, setDocsMessage] = useState('')
  const fileInputRef = useRef(null)

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await api.updateProfile({ name, company })
      await refreshUser()
      setMessage('Profile updated')
      setTimeout(() => setMessage(''), 3000)
    } catch (err) {
      setMessage(err.message)
    }
    setSaving(false)
  }

  const handleSaveProfile = async (e) => {
    e.preventDefault()
    setSavingProfile(true)
    try {
      // Clean empty strings
      const cleaned = { ...profile }
      if (!cleaned.capabilities?.length) delete cleaned.capabilities
      if (!cleaned.key_facts?.length) delete cleaned.key_facts
      if (!cleaned.partnership_model) delete cleaned.partnership_model

      await api.updateProfile({ company_profile: cleaned })
      await refreshUser()
      setProfileMessage('Company profile saved. This will be used for all future tender applications.')
      setTimeout(() => setProfileMessage(''), 5000)
    } catch (err) {
      setProfileMessage(err.message)
    }
    setSavingProfile(false)
  }

  const updateField = (key, value) => {
    setProfile(prev => ({ ...prev, [key]: value }))
  }

  const addCapability = () => {
    if (!newCapability.trim()) return
    setProfile(prev => ({ ...prev, capabilities: [...(prev.capabilities || []), newCapability.trim()] }))
    setNewCapability('')
  }

  const removeCapability = (index) => {
    setProfile(prev => ({
      ...prev,
      capabilities: prev.capabilities.filter((_, i) => i !== index)
    }))
  }

  const addFact = () => {
    if (!newFact.trim()) return
    setProfile(prev => ({ ...prev, key_facts: [...(prev.key_facts || []), newFact.trim()] }))
    setNewFact('')
  }

  const removeFact = (index) => {
    setProfile(prev => ({
      ...prev,
      key_facts: prev.key_facts.filter((_, i) => i !== index)
    }))
  }

  // Fetch company documents
  const fetchDocs = async () => {
    try {
      const data = await api.getCompanyDocs()
      setCompanyDocs(data.files || [])
    } catch { setCompanyDocs([]) }
    setDocsLoading(false)
  }
  useEffect(() => { fetchDocs() }, [])

  const handleUploadDoc = async (e) => {
    const files = e.target.files
    if (!files?.length) return
    setUploading(true)
    setDocsMessage('')
    let uploaded = 0
    for (const file of files) {
      try {
        await api.uploadCompanyDoc(file)
        uploaded++
      } catch (err) {
        setDocsMessage(`Failed to upload ${file.name}: ${err.message}`)
      }
    }
    if (uploaded > 0) {
      setDocsMessage(`${uploaded} file(s) uploaded`)
      setTimeout(() => setDocsMessage(''), 3000)
    }
    await fetchDocs()
    setUploading(false)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleDeleteDoc = async (filename) => {
    if (!confirm(`Delete "${filename}"?`)) return
    try {
      await api.deleteCompanyDoc(filename)
      await fetchDocs()
    } catch (err) {
      setDocsMessage(`Failed to delete: ${err.message}`)
    }
  }

  const handleManageBilling = async () => {
    try {
      const { portal_url } = await api.createPortal()
      if (portal_url) window.location.href = portal_url
    } catch (err) {
      alert(err.message)
    }
  }

  const inputClass = "w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Settings</h1>

      {/* Top row: Profile + Subscription side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile */}
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">Profile</h2>
          <form onSubmit={handleSave} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input
                type="email" disabled value={user?.email || ''}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-lg text-slate-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
              <input
                type="text" value={name} onChange={(e) => setName(e.target.value)}
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Company</label>
              <input
                type="text" value={company} onChange={(e) => setCompany(e.target.value)}
                className={inputClass}
              />
            </div>
            <div className="flex items-center gap-3">
              <button
                type="submit" disabled={saving}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              {message && <span className="text-sm text-green-600">{message}</span>}
            </div>
          </form>
        </div>

        {/* Subscription + Account */}
        <div className="space-y-6">
          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Subscription</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">Current plan</span>
                <PlanBadge plan={user?.plan} />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">Institutions followed</span>
                <span className="text-sm font-medium">{user?.followed_institutions || 0} / {user?.max_institutions || 10}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-600">Applications this month</span>
                <span className="text-sm font-medium">{user?.applications_this_month || 0} / {user?.max_applications_per_month || 5}</span>
              </div>
              {user?.subscription_ends_at && (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Renews</span>
                  <span className="text-sm">{new Date(user.subscription_ends_at).toLocaleDateString()}</span>
                </div>
              )}
            </div>
            <div className="mt-4 flex gap-3">
              {user?.plan !== 'enterprise' && (
                <a href="/pricing" className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
                  Upgrade Plan
                </a>
              )}
              {user?.plan !== 'free' && (
                <button
                  onClick={handleManageBilling}
                  className="px-4 py-2 border border-slate-300 text-sm font-medium rounded-lg hover:bg-slate-50"
                >
                  Manage Billing
                </button>
              )}
            </div>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Account</h2>
            <div className="space-y-2 text-sm text-slate-500">
              <p>Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</p>
              <p>Status: {user?.subscription_status || 'active'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom row: Documents + Company Details side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Company Documents */}
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <div className="flex items-center gap-2 mb-1">
            <FolderOpen size={20} className="text-green-600" />
            <h2 className="text-lg font-semibold text-slate-900">Company Documents</h2>
          </div>
          <p className="text-sm text-slate-500 mb-2">
            Upload your company documents. The AI reads these when preparing tender applications.
          </p>
          <div className="mb-5 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
            <p className="text-xs font-medium text-amber-800 mb-1">Required documents:</p>
            <ul className="text-xs text-amber-700 space-y-0.5 list-disc list-inside">
              <li>Company Profile (PDF)</li>
              <li>TIN Certificate</li>
              <li>Business License</li>
              <li>Audited Financial Statements</li>
              <li>Certificate of Incorporation / MEMART</li>
            </ul>
          </div>

          {/* Upload button */}
          <div className="flex items-center gap-3 mb-4">
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.txt,.md,.jpg,.jpeg,.png,.xlsx,.xls"
              onChange={handleUploadDoc}
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              className="inline-flex items-center gap-2 px-4 py-2.5 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              <Upload size={16} />
              {uploading ? 'Uploading...' : 'Upload Documents'}
            </button>
            <span className="text-xs text-slate-400">Max 20MB each</span>
          </div>

          {docsMessage && (
            <p className={`text-sm mb-3 ${docsMessage.includes('Failed') ? 'text-red-600' : 'text-green-600'}`}>
              {docsMessage}
            </p>
          )}

          {/* Document list */}
          {docsLoading ? (
            <p className="text-sm text-slate-400">Loading...</p>
          ) : companyDocs.length === 0 ? (
            <div className="text-center py-8 bg-slate-50 rounded-lg border-2 border-dashed border-slate-200">
              <FileText size={28} className="text-slate-300 mx-auto mb-2" />
              <p className="text-sm text-slate-400">No documents uploaded yet</p>
              <p className="text-xs text-slate-400 mt-1">Upload your company profile, TIN, license, financials, etc.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {companyDocs.map((doc) => (
                <div key={doc.filename}
                     className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                  <div className="flex items-center gap-3 min-w-0">
                    <FileText size={16} className="text-green-600 shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-700 truncate">{doc.filename}</p>
                      <p className="text-xs text-slate-400">
                        {(doc.size / 1024).toFixed(0)} KB
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <a href={api.getCompanyDocUrl(doc.filename)}
                       target="_blank" rel="noopener"
                       className="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
                       title="Download">
                      <Download size={15} />
                    </a>
                    <button
                      onClick={() => handleDeleteDoc(doc.filename)}
                      className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                      title="Delete">
                      <Trash2 size={15} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Company Details */}
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <div className="flex items-center gap-2 mb-1">
            <Building2 size={20} className="text-blue-600" />
            <h2 className="text-lg font-semibold text-slate-900">Company Details</h2>
          </div>
          <p className="text-sm text-slate-500 mb-5">
            Contact details for cover letters. TIN, registration, and credentials are
            extracted from your uploaded documents.
          </p>

          <form onSubmit={handleSaveProfile} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {PROFILE_FIELDS.map(({ key, label, required, placeholder }) => (
                <div key={key} className={key === 'company_name' || key === 'address' ? 'col-span-2' : ''}>
                  <label className="block text-sm font-medium text-slate-700 mb-1">
                    {label}{required && <span className="text-red-500 ml-0.5">*</span>}
                  </label>
                  <input
                    type="text"
                    value={profile[key] || ''}
                    onChange={(e) => updateField(key, e.target.value)}
                    placeholder={placeholder}
                    required={required}
                    className={inputClass}
                  />
                </div>
              ))}
            </div>

            {/* Capabilities */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Core Capabilities
              </label>
              <p className="text-xs text-slate-400 mb-2">What your company does. Used as bullet points in applications.</p>
              {(profile.capabilities || []).map((cap, i) => (
                <div key={i} className="flex items-center gap-2 mb-1.5">
                  <span className="text-xs text-slate-400 shrink-0 w-4">{i + 1}.</span>
                  <span className="flex-1 text-sm text-slate-700 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">{cap}</span>
                  <button type="button" onClick={() => removeCapability(i)}
                          className="p-1 text-slate-400 hover:text-red-500 shrink-0">
                    <X size={14} />
                  </button>
                </div>
              ))}
              <div className="flex gap-2 mt-2">
                <input
                  type="text"
                  value={newCapability}
                  onChange={(e) => setNewCapability(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addCapability() } }}
                  placeholder="e.g., Software development for banks and SACCOs"
                  className={`flex-1 ${inputClass}`}
                />
                <button type="button" onClick={addCapability}
                        className="px-3 py-2 text-sm border border-slate-300 rounded-lg hover:bg-slate-50 shrink-0">
                  <Plus size={14} />
                </button>
              </div>
            </div>

            {/* Key Facts */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Key Facts
              </label>
              <p className="text-xs text-slate-400 mb-2">Notable achievements, metrics, or certifications.</p>
              {(profile.key_facts || []).map((fact, i) => (
                <div key={i} className="flex items-center gap-2 mb-1.5">
                  <span className="flex-1 text-sm text-slate-700 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200">{fact}</span>
                  <button type="button" onClick={() => removeFact(i)}
                          className="p-1 text-slate-400 hover:text-red-500 shrink-0">
                    <X size={14} />
                  </button>
                </div>
              ))}
              <div className="flex gap-2 mt-2">
                <input
                  type="text"
                  value={newFact}
                  onChange={(e) => setNewFact(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addFact() } }}
                  placeholder="e.g., 20+ projects delivered, ISO 9001 certified"
                  className={`flex-1 ${inputClass}`}
                />
                <button type="button" onClick={addFact}
                        className="px-3 py-2 text-sm border border-slate-300 rounded-lg hover:bg-slate-50 shrink-0">
                  <Plus size={14} />
                </button>
              </div>
            </div>

            {/* Partnership model */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Partnership Model (optional)
              </label>
              <p className="text-xs text-slate-400 mb-2">How your company handles tenders outside its core expertise.</p>
              <textarea
                value={profile.partnership_model || ''}
                onChange={(e) => updateField('partnership_model', e.target.value)}
                rows={3}
                placeholder="e.g., For construction tenders, we partner with licensed contractors..."
                className={`${inputClass} resize-y`}
              />
            </div>

            <div className="flex items-center gap-3 pt-2">
              <button
                type="submit" disabled={savingProfile}
                className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {savingProfile ? 'Saving...' : 'Save Company Details'}
              </button>
              {profileMessage && (
                <span className="text-sm text-green-600">{profileMessage}</span>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
