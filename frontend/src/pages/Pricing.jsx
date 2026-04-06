import React, { useState, useEffect } from 'react'
import { Check, X } from 'lucide-react'
import { useAuth } from '../lib/auth'
import { api } from '../lib/api'

const FEATURES = [
  { label: 'Follow institutions', key: 'max_institutions' },
  { label: 'Applications / month', key: 'max_applications_per_month' },
  { label: 'Document downloads', key: 'can_download_documents', bool: true },
  { label: 'Email alerts', key: 'has_email_alerts', bool: true },
  { label: 'Scraper control', key: 'can_control_scraper', bool: true },
  { label: 'API access', key: 'has_api_access', bool: true },
]

function formatLimit(v) {
  if (v >= 999999) return 'Unlimited'
  return v.toLocaleString()
}

export default function Pricing() {
  const { user } = useAuth()
  const [plans, setPlans] = useState([])
  const [upgrading, setUpgrading] = useState(null)

  useEffect(() => {
    api.getPlans().then(d => setPlans(d.plans)).catch(console.error)
  }, [])

  const handleUpgrade = async (planId) => {
    if (planId === 'free' || planId === user?.plan) return
    setUpgrading(planId)
    try {
      const { checkout_url } = await api.createCheckout(planId)
      if (checkout_url) window.location.href = checkout_url
    } catch (err) {
      alert(err.message)
    }
    setUpgrading(null)
  }

  const colors = { free: 'slate', pro: 'blue', enterprise: 'purple' }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-slate-900">Plans & Pricing</h1>
        <p className="text-sm text-slate-500 mt-1">Choose the right plan for your tender tracking needs</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {plans.map(plan => {
          const color = colors[plan.id] || 'slate'
          const isCurrent = user?.plan === plan.id
          const popular = plan.id === 'pro'

          return (
            <div key={plan.id} className={`
              relative bg-white rounded-xl border-2 p-6 flex flex-col
              ${popular ? 'border-blue-500 shadow-lg' : 'border-slate-200'}
            `}>
              {popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                  POPULAR
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-lg font-bold text-slate-900">{plan.name}</h3>
                <div className="mt-2">
                  <span className="text-3xl font-bold text-slate-900">
                    ${(plan.price_monthly / 100).toFixed(0)}
                  </span>
                  <span className="text-sm text-slate-500">/mo</span>
                </div>
              </div>

              <ul className="space-y-3 flex-1">
                {FEATURES.map(f => {
                  const val = plan[f.key]
                  return (
                    <li key={f.key} className="flex items-center gap-2 text-sm">
                      {f.bool ? (
                        val ? <Check size={16} className="text-green-500" /> : <X size={16} className="text-slate-300" />
                      ) : (
                        <Check size={16} className="text-green-500" />
                      )}
                      <span className={f.bool && !val ? 'text-slate-400' : 'text-slate-700'}>
                        {f.bool ? f.label : `${formatLimit(val)} ${f.label.toLowerCase()}`}
                      </span>
                    </li>
                  )
                })}
              </ul>

              <button
                onClick={() => handleUpgrade(plan.id)}
                disabled={isCurrent || plan.id === 'free' || upgrading === plan.id}
                className={`
                  mt-6 w-full py-2.5 text-sm font-medium rounded-lg transition-colors
                  ${isCurrent
                    ? 'bg-slate-100 text-slate-500 cursor-default'
                    : plan.id === 'free'
                    ? 'bg-slate-100 text-slate-500 cursor-default'
                    : `bg-${color}-600 text-white hover:bg-${color}-700 disabled:opacity-50`
                  }
                `}
              >
                {isCurrent ? 'Current Plan' : plan.id === 'free' ? 'Free' : upgrading === plan.id ? 'Redirecting...' : 'Upgrade'}
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}
