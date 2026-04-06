import React from 'react'

const URGENCY_STYLES = {
  CRITICAL: 'bg-red-100 text-red-800 border-red-200',
  URGENT: 'bg-orange-100 text-orange-800 border-orange-200',
  HIGH: 'bg-amber-100 text-amber-800 border-amber-200',
  MEDIUM: 'bg-blue-100 text-blue-800 border-blue-200',
  LOW: 'bg-slate-100 text-slate-600 border-slate-200',
  UNKNOWN: 'bg-gray-100 text-gray-600 border-gray-200',
  EXPIRED: 'bg-gray-100 text-gray-400 border-gray-200 line-through',
}

const STATUS_STYLES = {
  active: 'bg-green-100 text-green-800 border-green-200',
  closed: 'bg-gray-100 text-gray-600 border-gray-200',
  archived: 'bg-gray-50 text-gray-400 border-gray-100',
  Submitted: 'bg-blue-100 text-blue-800 border-blue-200',
  Sent: 'bg-green-100 text-green-800 border-green-200',
  Draft: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Pending: 'bg-orange-100 text-orange-800 border-orange-200',
  sent: 'bg-green-100 text-green-800 border-green-200',
  failed: 'bg-red-100 text-red-800 border-red-200',
  pending: 'bg-yellow-100 text-yellow-800 border-yellow-200',
}

export function UrgencyBadge({ urgency }) {
  const style = URGENCY_STYLES[urgency] || URGENCY_STYLES.UNKNOWN
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${style}`}>
      {urgency}
    </span>
  )
}

export function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || 'bg-gray-100 text-gray-600 border-gray-200'
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${style}`}>
      {status}
    </span>
  )
}

export function DaysRemainingBadge({ days }) {
  if (days === null || days === undefined) {
    return <span className="text-xs text-gray-400">No date</span>
  }
  if (days < 0) {
    return <span className="text-xs text-gray-400 line-through">Expired</span>
  }
  if (days === 0) {
    return <span className="text-xs font-bold text-red-600">TODAY</span>
  }
  if (days <= 3) {
    return <span className="text-xs font-bold text-red-600">{days}d left</span>
  }
  if (days <= 7) {
    return <span className="text-xs font-semibold text-orange-600">{days}d left</span>
  }
  return <span className="text-xs text-slate-500">{days}d left</span>
}
