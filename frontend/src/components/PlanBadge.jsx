import React from 'react'

const PLAN_STYLES = {
  free: 'bg-slate-100 text-slate-600',
  pro: 'bg-blue-100 text-blue-700',
  enterprise: 'bg-purple-100 text-purple-700',
}

export default function PlanBadge({ plan }) {
  const style = PLAN_STYLES[plan] || PLAN_STYLES.free
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold uppercase ${style}`}>
      {plan || 'free'}
    </span>
  )
}
