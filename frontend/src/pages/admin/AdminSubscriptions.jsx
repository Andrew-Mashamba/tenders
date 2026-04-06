import React, { useState, useEffect } from 'react'
import { DollarSign, Users, UserX } from 'lucide-react'
import StatsCard from '../../components/StatsCard'
import PlanBadge from '../../components/PlanBadge'
import DataTable from '../../components/DataTable'
import { StatusBadge } from '../../components/StatusBadge'
import { api } from '../../lib/api'

export default function AdminSubscriptions() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.adminGetSubscriptions()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="animate-pulse text-slate-400 py-12 text-center">Loading subscriptions...</div>
  }

  if (!data) {
    return <div className="text-red-500 py-12 text-center">Failed to load subscription data</div>
  }

  const formatMRR = (cents) => {
    if (!cents) return '$0.00'
    return `$${(cents / 100).toLocaleString('en-US', { minimumFractionDigits: 2 })}`
  }

  const columns = [
    {
      header: 'Email',
      render: (row) => <span className="font-medium text-slate-900">{row.email}</span>,
    },
    {
      header: 'Name',
      render: (row) => <span className="text-sm text-slate-600">{row.name || '—'}</span>,
      className: 'hidden md:table-cell',
    },
    {
      header: 'Plan',
      render: (row) => <PlanBadge plan={row.plan} />,
    },
    {
      header: 'Status',
      render: (row) => <StatusBadge status={row.subscription_status} />,
    },
    {
      header: 'Renewal',
      render: (row) => (
        <span className="text-xs text-slate-500">
          {row.subscription_ends_at ? new Date(row.subscription_ends_at).toLocaleDateString() : '—'}
        </span>
      ),
      className: 'hidden lg:table-cell',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Subscriptions</h1>
        <p className="text-sm text-slate-500">Revenue and subscriber management</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatsCard title="Monthly Recurring Revenue" value={formatMRR(data.mrr)} icon={DollarSign} color="purple" />
        <StatsCard title="Paying Subscribers" value={data.total_paying} icon={Users} color="success" />
        <StatsCard title="Free Users" value={data.free_users} icon={UserX} color="info" />
      </div>

      {/* Plan Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(data.subscribers_by_plan).map(([planId, info]) => (
          <div key={planId} className="bg-white rounded-xl border border-slate-200 p-4">
            <div className="flex items-center justify-between mb-2">
              <PlanBadge plan={planId} />
              <span className="text-xs text-slate-400">{formatMRR(info.revenue)}/mo</span>
            </div>
            <p className="text-2xl font-bold text-slate-900">{info.count}</p>
            <p className="text-xs text-slate-500">subscribers at {formatMRR(info.price)}/mo</p>
          </div>
        ))}
      </div>

      {/* Paying Subscribers Table */}
      <div>
        <h2 className="text-lg font-semibold text-slate-900 mb-3">Paying Subscribers</h2>
        <DataTable
          columns={columns}
          data={data.paying_subscribers}
          total={data.paying_subscribers.length}
          emptyMessage="No paying subscribers yet"
        />
      </div>
    </div>
  )
}
