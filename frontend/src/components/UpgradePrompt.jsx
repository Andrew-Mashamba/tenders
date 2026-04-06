import React from 'react'
import { Link } from 'react-router-dom'
import { Lock } from 'lucide-react'

export default function UpgradePrompt({ message, feature }) {
  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6 text-center">
      <Lock size={24} className="mx-auto text-blue-500 mb-2" />
      <p className="text-sm font-medium text-slate-700 mb-1">
        {message || 'This feature requires an upgrade.'}
      </p>
      <p className="text-xs text-slate-500 mb-4">
        Upgrade your plan to unlock {feature || 'this feature'}.
      </p>
      <Link
        to="/pricing"
        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
      >
        View Plans
      </Link>
    </div>
  )
}
