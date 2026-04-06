import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Shield, ShieldOff, Key, UserCheck, UserX } from 'lucide-react'
import PlanBadge from '../../components/PlanBadge'
import { StatusBadge } from '../../components/StatusBadge'
import DataTable from '../../components/DataTable'
import { api } from '../../lib/api'

export default function AdminUserDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)
  const [tempPassword, setTempPassword] = useState(null)

  const fetchUser = () => {
    setLoading(true)
    api.adminGetUser(id)
      .then(setUser)
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchUser() }, [id])

  const handleChangePlan = async (plan) => {
    setActionLoading('plan')
    try {
      const updated = await api.adminUpdateUser(id, { plan })
      setUser(updated)
    } catch (e) { console.error(e) }
    setActionLoading(null)
  }

  const handleToggleAdmin = async () => {
    setActionLoading('admin')
    try {
      const updated = await api.adminUpdateUser(id, { is_admin: !user.is_admin })
      setUser(updated)
    } catch (e) { console.error(e) }
    setActionLoading(null)
  }

  const handleToggleStatus = async () => {
    setActionLoading('status')
    const newStatus = user.subscription_status === 'active' ? 'cancelled' : 'active'
    try {
      const updated = await api.adminUpdateUser(id, { subscription_status: newStatus })
      setUser(updated)
    } catch (e) { console.error(e) }
    setActionLoading(null)
  }

  const handleResetPassword = async () => {
    setActionLoading('password')
    setTempPassword(null)
    try {
      const result = await api.adminResetPassword(id)
      setTempPassword(result.temp_password)
    } catch (e) { console.error(e) }
    setActionLoading(null)
  }

  if (loading) {
    return <div className="animate-pulse text-slate-400 py-12 text-center">Loading user...</div>
  }

  if (!user) {
    return <div className="text-red-500 py-12 text-center">User not found</div>
  }

  const appColumns = [
    { header: 'Tender', key: 'tender_id' },
    { header: 'Institution', key: 'institution_slug' },
    { header: 'Status', render: (row) => <StatusBadge status={row.status} /> },
    {
      header: 'Created',
      render: (row) => <span className="text-xs text-slate-500">{row.created_at ? new Date(row.created_at).toLocaleDateString() : '—'}</span>,
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/admin/users')} className="p-2 rounded-lg hover:bg-slate-100">
          <ArrowLeft size={18} />
        </button>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">{user.email}</h1>
            {user.is_admin && <Shield size={18} className="text-purple-500" />}
          </div>
          <p className="text-sm text-slate-500">{user.name || 'No name'} {user.company ? `— ${user.company}` : ''}</p>
        </div>
      </div>

      {/* Actions */}
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <h2 className="text-sm font-semibold text-slate-700 mb-3">Actions</h2>
        <div className="flex flex-wrap gap-3">
          {/* Plan selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">Plan:</span>
            <select
              value={user.plan}
              onChange={(e) => handleChangePlan(e.target.value)}
              disabled={actionLoading === 'plan'}
              className="px-3 py-1.5 text-sm border border-slate-300 rounded-lg"
            >
              <option value="free">Free</option>
              <option value="pro">Pro</option>
              <option value="enterprise">Enterprise</option>
            </select>
          </div>

          <button
            onClick={handleToggleAdmin}
            disabled={actionLoading === 'admin'}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border ${
              user.is_admin
                ? 'border-purple-200 bg-purple-50 text-purple-700 hover:bg-purple-100'
                : 'border-slate-300 text-slate-600 hover:bg-slate-50'
            }`}
          >
            {user.is_admin ? <ShieldOff size={14} /> : <Shield size={14} />}
            {user.is_admin ? 'Remove Admin' : 'Make Admin'}
          </button>

          <button
            onClick={handleToggleStatus}
            disabled={actionLoading === 'status'}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border ${
              user.subscription_status === 'active'
                ? 'border-red-200 bg-red-50 text-red-700 hover:bg-red-100'
                : 'border-green-200 bg-green-50 text-green-700 hover:bg-green-100'
            }`}
          >
            {user.subscription_status === 'active' ? <UserX size={14} /> : <UserCheck size={14} />}
            {user.subscription_status === 'active' ? 'Deactivate' : 'Activate'}
          </button>

          <button
            onClick={handleResetPassword}
            disabled={actionLoading === 'password'}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-lg border border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100"
          >
            <Key size={14} />
            Reset Password
          </button>
        </div>

        {tempPassword && (
          <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              Temporary password: <code className="font-mono font-bold bg-green-100 px-2 py-0.5 rounded">{tempPassword}</code>
            </p>
            <p className="text-xs text-green-600 mt-1">Share this with the user securely. They should change it on next login.</p>
          </div>
        )}
      </div>

      {/* Profile Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">Profile</h2>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-slate-500">Email</dt>
              <dd className="text-slate-900">{user.email}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Name</dt>
              <dd className="text-slate-900">{user.name || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Company</dt>
              <dd className="text-slate-900">{user.company || '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Verified</dt>
              <dd>{user.email_verified ? <span className="text-green-600">Yes</span> : <span className="text-slate-400">No</span>}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Signed Up</dt>
              <dd className="text-slate-900">{user.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</dd>
            </div>
          </dl>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">Subscription</h2>
          <dl className="space-y-2 text-sm">
            <div className="flex justify-between">
              <dt className="text-slate-500">Plan</dt>
              <dd><PlanBadge plan={user.plan} /></dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Status</dt>
              <dd><StatusBadge status={user.subscription_status || 'active'} /></dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Renewal</dt>
              <dd className="text-slate-900">{user.subscription_ends_at ? new Date(user.subscription_ends_at).toLocaleDateString() : '—'}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Apps This Month</dt>
              <dd className="text-slate-900">{user.applications_this_month}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-slate-500">Institutions</dt>
              <dd className="text-slate-900">{user.followed_institutions} / {user.max_institutions}</dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Followed Institutions */}
      {user.followed_institutions_list?.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">
            Followed Institutions ({user.followed_institutions_list.length})
          </h2>
          <div className="flex flex-wrap gap-2">
            {user.followed_institutions_list.map((inst) => (
              <span key={inst.slug}
                    className="inline-flex items-center px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-xs font-medium">
                {inst.slug}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Applications */}
      {user.applications_list?.length > 0 && (
        <div>
          <h2 className="text-sm font-semibold text-slate-700 mb-2">
            Applications ({user.applications_list.length})
          </h2>
          <DataTable
            columns={appColumns}
            data={user.applications_list}
            total={user.applications_list.length}
            emptyMessage="No applications"
          />
        </div>
      )}
    </div>
  )
}
