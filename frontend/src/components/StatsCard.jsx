import React from 'react'

export default function StatsCard({ title, value, subtitle, icon: Icon, color = 'primary', trend }) {
  const colors = {
    primary: 'bg-blue-50 text-blue-700 border-blue-200',
    success: 'bg-green-50 text-green-700 border-green-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    danger: 'bg-red-50 text-red-700 border-red-200',
    info: 'bg-cyan-50 text-cyan-700 border-cyan-200',
    purple: 'bg-purple-50 text-purple-700 border-purple-200',
  }

  const iconColors = {
    primary: 'text-blue-500',
    success: 'text-green-500',
    warning: 'text-amber-500',
    danger: 'text-red-500',
    info: 'text-cyan-500',
    purple: 'text-purple-500',
  }

  return (
    <div className={`rounded-xl border p-4 ${colors[color]}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium opacity-75 uppercase tracking-wide">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {subtitle && <p className="text-xs mt-1 opacity-60">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-2 rounded-lg bg-white/60 ${iconColors[color]}`}>
            <Icon size={20} />
          </div>
        )}
      </div>
    </div>
  )
}
