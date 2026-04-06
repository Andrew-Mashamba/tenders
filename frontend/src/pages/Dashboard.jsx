import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  FileText, Send, Building2, Lightbulb, AlertTriangle,
  Clock, TrendingUp, CheckCircle2
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import StatsCard from '../components/StatsCard'
import { DaysRemainingBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

const PIE_COLORS = ['#1565C0', '#2E7D32', '#F57F17', '#C62828', '#7B1FA2', '#00838F', '#4E342E', '#546E7A']

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-slate-400">Loading dashboard...</div>
      </div>
    )
  }

  if (!stats) {
    return <div className="text-red-500 p-4">Failed to load dashboard data. Is the API running?</div>
  }

  // Prepare chart data
  const categoryData = Object.entries(stats.categories || {})
    .slice(0, 8)
    .map(([name, value]) => ({ name: name.length > 15 ? name.slice(0, 15) + '...' : name, value }))

  const summaryData = [
    { name: 'Active', value: stats.active_tenders },
    { name: 'Submitted', value: stats.applications_submitted },
    { name: 'Pending', value: stats.applications_pending },
    { name: 'Leads', value: stats.pending_leads },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">
          Tender tracking overview
          {stats.last_scrape_date && ` — Last scrape: ${stats.last_scrape_date}`}
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Active Tenders"
          value={stats.active_tenders}
          subtitle={`${stats.institutions_with_tenders} institutions`}
          icon={FileText}
          color="primary"
        />
        <StatsCard
          title="Applications Sent"
          value={stats.applications_submitted}
          subtitle={`${stats.applications_pending} pending`}
          icon={Send}
          color="success"
        />
        <StatsCard
          title="Closing Soon"
          value={stats.closing_soon}
          subtitle="Within 7 days"
          icon={AlertTriangle}
          color={stats.closing_soon > 0 ? 'warning' : 'info'}
        />
        <StatsCard
          title="Opportunities"
          value={stats.pending_leads}
          subtitle={`${stats.total_leads} total leads`}
          icon={Lightbulb}
          color="purple"
        />
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Institutions"
          value={stats.total_institutions}
          subtitle={`${stats.enabled_institutions} enabled`}
          icon={Building2}
          color="info"
        />
        <StatsCard
          title="With Tenders"
          value={stats.institutions_with_tenders}
          subtitle={`${((stats.institutions_with_tenders / stats.enabled_institutions) * 100).toFixed(0)}% hit rate`}
          icon={TrendingUp}
          color="success"
        />
        <StatsCard
          title="Submitted"
          value={stats.applications_submitted}
          icon={CheckCircle2}
          color="success"
        />
        <StatsCard
          title="Pending Apps"
          value={stats.applications_pending}
          icon={Clock}
          color="warning"
        />
      </div>

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Category breakdown */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-4">Tenders by Category</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={categoryData} layout="vertical" margin={{ left: 10 }}>
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="value" fill="#1565C0" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pipeline */}
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-4">Pipeline Summary</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={summaryData}
                cx="50%" cy="50%"
                innerRadius={60} outerRadius={90}
                paddingAngle={3}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {summaryData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Closing soon */}
      {stats.closing_soon_tenders?.length > 0 && (
        <div className="bg-white rounded-xl border border-amber-200 p-5">
          <h3 className="text-sm font-semibold text-amber-700 mb-3 flex items-center gap-2">
            <AlertTriangle size={16} />
            Closing Soon
          </h3>
          <div className="space-y-2">
            {stats.closing_soon_tenders.map((t, i) => (
              <Link key={i} to={`/tenders/${t.tender_id}`}
                    className="flex items-center justify-between p-3 rounded-lg hover:bg-amber-50 transition-colors">
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-900 truncate">{t.title}</p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {t.institution_slug || t.institution} — {t.closing_date}
                  </p>
                </div>
                <DaysRemainingBadge days={t.days_remaining} />
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
