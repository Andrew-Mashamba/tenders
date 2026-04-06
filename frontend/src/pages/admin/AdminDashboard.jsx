import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Users, CreditCard, DollarSign, FileText, Building2, Bot, ArrowRight } from 'lucide-react'
import StatsCard from '../../components/StatsCard'
import PlanBadge from '../../components/PlanBadge'
import { api } from '../../lib/api'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.adminGetStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="animate-pulse text-slate-400 py-12 text-center">Loading admin dashboard...</div>
  }

  if (!stats) {
    return <div className="text-red-500 py-12 text-center">Failed to load stats</div>
  }

  const formatMRR = (cents) => {
    if (!cents) return '$0'
    return `$${(cents / 100).toLocaleString('en-US', { minimumFractionDigits: 2 })}`
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Admin Dashboard</h1>
        <p className="text-sm text-slate-500">System overview and management</p>
      </div>

      {/* Stats Row 1 */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <StatsCard title="Total Users" value={stats.total_users} icon={Users} color="primary" />
        <StatsCard title="Active Subscriptions" value={stats.active_subscriptions} icon={CreditCard} color="success" />
        <StatsCard title="MRR" value={formatMRR(stats.mrr)} icon={DollarSign} color="purple" />
      </div>

      {/* Stats Row 2 */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <StatsCard title="Active Tenders" value={stats.total_active_tenders} icon={FileText} color="info" />
        <StatsCard
          title="Institutions"
          value={`${stats.enabled_institutions} / ${stats.total_institutions}`}
          subtitle="enabled / total"
          icon={Building2}
          color="warning"
        />
        <StatsCard
          title="Scraper"
          value={stats.scraper_running ? 'Running' : 'Idle'}
          subtitle={stats.last_scrape ? `Last: ${new Date(stats.last_scrape).toLocaleDateString()}` : 'Never run'}
          icon={Bot}
          color={stats.scraper_running ? 'success' : 'danger'}
        />
      </div>

      {/* Users by Plan */}
      {stats.users_by_plan && Object.keys(stats.users_by_plan).length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-4">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">Users by Plan</h2>
          <div className="flex gap-4">
            {Object.entries(stats.users_by_plan).map(([plan, count]) => (
              <div key={plan} className="flex items-center gap-2">
                <PlanBadge plan={plan} />
                <span className="text-sm font-bold text-slate-700">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Signups */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200 bg-slate-50">
          <h2 className="text-sm font-semibold text-slate-700">Recent Signups</h2>
          <Link to="/admin/users" className="text-xs text-primary hover:underline flex items-center gap-1">
            View all <ArrowRight size={12} />
          </Link>
        </div>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100">
              <th className="px-4 py-2 text-left text-xs font-medium text-slate-500">Email</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-slate-500 hidden sm:table-cell">Name</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-slate-500">Plan</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-slate-500 hidden md:table-cell">Signed Up</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50">
            {stats.recent_signups.map((u) => (
              <tr key={u.id} className="hover:bg-slate-50">
                <td className="px-4 py-2">
                  <Link to={`/admin/users/${u.id}`} className="text-primary hover:underline">{u.email}</Link>
                </td>
                <td className="px-4 py-2 text-slate-600 hidden sm:table-cell">{u.name || '—'}</td>
                <td className="px-4 py-2"><PlanBadge plan={u.plan} /></td>
                <td className="px-4 py-2 text-xs text-slate-400 hidden md:table-cell">
                  {u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[
          { to: '/admin/users', label: 'Manage Users', icon: Users },
          { to: '/admin/institutions', label: 'Manage Institutions', icon: Building2 },
          { to: '/admin/subscriptions', label: 'Subscriptions', icon: DollarSign },
          { to: '/scraper', label: 'Scraper Control', icon: Bot },
        ].map(({ to, label, icon: Icon }) => (
          <Link key={to} to={to}
                className="flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-200 hover:border-primary hover:shadow-sm transition-all">
            <Icon size={18} className="text-slate-400" />
            <span className="text-sm font-medium text-slate-700">{label}</span>
            <ArrowRight size={14} className="text-slate-300 ml-auto" />
          </Link>
        ))}
      </div>
    </div>
  )
}
