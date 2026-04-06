import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Check, Building2 } from 'lucide-react'
import { useAuth } from '../lib/auth'
import { api } from '../lib/api'
import PlanBadge from '../components/PlanBadge'

export default function Onboarding() {
  const { user, refreshUser } = useAuth()
  const navigate = useNavigate()
  const [institutions, setInstitutions] = useState([])
  const [selected, setSelected] = useState(new Set())
  const [search, setSearch] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const maxInstitutions = user?.max_institutions || 10

  useEffect(() => {
    api.getInstitutions({ limit: 1000, enabled: true })
      .then(d => {
        setInstitutions(d.institutions)
        setLoading(false)
      })
      .catch(console.error)
  }, [])

  const categories = [...new Set(institutions.map(i => i.category).filter(Boolean))].sort()

  const filtered = institutions.filter(inst => {
    if (search && !`${inst.name} ${inst.slug} ${inst.category}`.toLowerCase().includes(search.toLowerCase())) return false
    if (categoryFilter && inst.category !== categoryFilter) return false
    return true
  })

  const toggle = (slug) => {
    const next = new Set(selected)
    if (next.has(slug)) {
      next.delete(slug)
    } else if (next.size < maxInstitutions) {
      next.add(slug)
    }
    setSelected(next)
  }

  const handleContinue = async () => {
    setSaving(true)
    try {
      for (const slug of selected) {
        await api.followInstitution(slug)
      }
      await refreshUser()
      navigate('/', { replace: true })
    } catch (err) {
      alert(err.message)
    }
    setSaving(false)
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-slate-900">Welcome to TENDERS</h1>
        <p className="text-sm text-slate-500 mt-1">
          Choose institutions to follow. You'll see tenders from these institutions on your dashboard.
        </p>
        <div className="mt-2 inline-flex items-center gap-2">
          <PlanBadge plan={user?.plan} />
          <span className="text-sm text-slate-500">
            {selected.size} / {maxInstitutions} selected
          </span>
        </div>
      </div>

      {/* Search + filter */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text" placeholder="Search institutions..."
            value={search} onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"
          />
        </div>
        <select
          value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)}
          className="px-3 py-2 text-sm border border-slate-300 rounded-lg"
        >
          <option value="">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      {/* Institution grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-400">Loading institutions...</div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {filtered.map(inst => {
            const isSelected = selected.has(inst.slug)
            const atLimit = selected.size >= maxInstitutions && !isSelected

            return (
              <button
                key={inst.slug}
                onClick={() => toggle(inst.slug)}
                disabled={atLimit}
                className={`
                  text-left p-4 rounded-xl border-2 transition-all
                  ${isSelected
                    ? 'border-blue-500 bg-blue-50'
                    : atLimit
                    ? 'border-slate-200 bg-slate-50 opacity-50 cursor-not-allowed'
                    : 'border-slate-200 hover:border-blue-300 hover:bg-blue-50/50'}
                `}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2 min-w-0">
                    <Building2 size={16} className="text-slate-400 shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-900 truncate">{inst.name || inst.slug}</p>
                      <p className="text-xs text-slate-400">{inst.category || 'Uncategorized'}</p>
                    </div>
                  </div>
                  {isSelected && (
                    <Check size={18} className="text-blue-600 shrink-0" />
                  )}
                </div>
                {inst.active_tenders > 0 && (
                  <p className="text-xs text-blue-600 mt-1">{inst.active_tenders} active tenders</p>
                )}
              </button>
            )
          })}
        </div>
      )}

      {/* Continue button */}
      <div className="sticky bottom-4 flex justify-center">
        <button
          onClick={handleContinue}
          disabled={selected.size === 0 || saving}
          className="px-8 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 disabled:opacity-50 shadow-lg transition-colors"
        >
          {saving ? 'Setting up...' : `Continue with ${selected.size} institution${selected.size !== 1 ? 's' : ''}`}
        </button>
      </div>
    </div>
  )
}
