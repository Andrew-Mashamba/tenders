import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Shield } from 'lucide-react'
import DataTable from '../../components/DataTable'
import PlanBadge from '../../components/PlanBadge'
import { StatusBadge } from '../../components/StatusBadge'
import { api } from '../../lib/api'

export default function AdminUsers() {
  const navigate = useNavigate()
  const [data, setData] = useState({ users: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [planFilter, setPlanFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [offset, setOffset] = useState(0)

  const fetchData = useCallback(() => {
    setLoading(true)
    const params = { limit: 50, offset }
    if (search) params.search = search
    if (planFilter) params.plan = planFilter
    if (statusFilter) params.status = statusFilter

    api.adminGetUsers(params)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [search, planFilter, statusFilter, offset])

  useEffect(() => { fetchData() }, [fetchData])

  const columns = [
    {
      header: 'User',
      render: (row) => (
        <div>
          <div className="flex items-center gap-1.5">
            <p className="font-medium text-slate-900">{row.email}</p>
            {row.is_admin && <Shield size={14} className="text-purple-500" />}
          </div>
          {row.name && <p className="text-xs text-slate-400">{row.name}</p>}
        </div>
      ),
    },
    {
      header: 'Company',
      render: (row) => <span className="text-xs text-slate-600">{row.company || '—'}</span>,
      className: 'hidden md:table-cell',
    },
    {
      header: 'Plan',
      render: (row) => <PlanBadge plan={row.plan} />,
    },
    {
      header: 'Status',
      render: (row) => <StatusBadge status={row.subscription_status || 'active'} />,
    },
    {
      header: 'Institutions',
      render: (row) => <span className="text-sm text-slate-600">{row.institutions_count}</span>,
      className: 'hidden lg:table-cell',
    },
    {
      header: 'Apps',
      render: (row) => <span className="text-sm text-slate-600">{row.applications_count}</span>,
      className: 'hidden lg:table-cell',
    },
    {
      header: 'Signed Up',
      render: (row) => (
        <span className="text-xs text-slate-500">
          {row.created_at ? new Date(row.created_at).toLocaleDateString() : '—'}
        </span>
      ),
      className: 'hidden md:table-cell',
    },
  ]

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Users</h1>
        <p className="text-sm text-slate-500">{data.total} registered users</p>
      </div>

      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text" placeholder="Search users..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setOffset(0) }}
            className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
          />
        </div>

        <select value={planFilter} onChange={(e) => { setPlanFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All Plans</option>
          <option value="free">Free</option>
          <option value="pro">Pro</option>
          <option value="enterprise">Enterprise</option>
        </select>

        <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="cancelled">Cancelled</option>
          <option value="past_due">Past Due</option>
        </select>
      </div>

      <DataTable
        columns={columns}
        data={data.users}
        total={data.total}
        offset={offset}
        limit={50}
        loading={loading}
        onRowClick={(row) => navigate(`/admin/users/${row.id}`)}
        onPageChange={setOffset}
        emptyMessage="No users found"
      />
    </div>
  )
}
