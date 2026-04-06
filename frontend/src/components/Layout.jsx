import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard, FileText, Send, Lightbulb, Building2,
  Bot, Menu, X, Settings, CreditCard, LogOut, Shield, Users, DollarSign
} from 'lucide-react'
import { useAuth } from '../lib/auth'
import PlanBadge from './PlanBadge'

const NAV = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/tenders', label: 'Tenders', icon: FileText },
  { path: '/applications', label: 'Applications', icon: Send },
  { path: '/institutions', label: 'Institutions', icon: Building2 },
  { path: '/pricing', label: 'Pricing', icon: CreditCard },
  { path: '/settings', label: 'Settings', icon: Settings },
]

const ADMIN_NAV = [
  { path: '/admin', label: 'Overview', icon: Shield },
  { path: '/admin/users', label: 'Users', icon: Users },
  { path: '/admin/institutions', label: 'Manage Institutions', icon: Building2 },
  { path: '/admin/subscriptions', label: 'Subscriptions', icon: DollarSign },
  { path: '/opportunities', label: 'Opportunities', icon: Lightbulb },
  { path: '/scraper', label: 'Scraper', icon: Bot },
]

export default function Layout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const currentPage = [...NAV, ...ADMIN_NAV].find(n => {
    if (n.path === '/') return location.pathname === '/'
    return location.pathname.startsWith(n.path)
  })

  const navLink = ({ path, label, icon: Icon }) => {
    const active = path === '/'
      ? location.pathname === '/'
      : location.pathname.startsWith(path)

    return (
      <Link key={path} to={path}
            onClick={() => setSidebarOpen(false)}
            className={`
              flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
              transition-colors duration-150
              ${active
                ? 'bg-primary text-white'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'}
            `}>
        <Icon size={18} />
        {label}
      </Link>
    )
  }

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 lg:hidden"
             onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 bg-slate-900 text-white flex flex-col
        transition-transform duration-200
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-5 border-b border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-bold tracking-tight">TENDERS</h1>
              <p className="text-xs text-slate-400 mt-0.5">ZIMA Solutions Ltd</p>
            </div>
            <button className="lg:hidden text-slate-400 hover:text-white"
                    onClick={() => setSidebarOpen(false)}>
              <X size={20} />
            </button>
          </div>
        </div>

        <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
          {NAV.map(navLink)}

          {user?.is_admin && (
            <>
              <div className="pt-3 pb-1 px-3">
                <div className="border-t border-slate-700 pt-3">
                  <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500">Admin</span>
                </div>
              </div>
              {ADMIN_NAV.map(navLink)}
            </>
          )}
        </nav>

        {/* User section */}
        <div className="p-4 border-t border-slate-700">
          {user && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center text-xs font-bold">
                  {(user.name || user.email || '?')[0].toUpperCase()}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium truncate">{user.name || user.email}</p>
                  <PlanBadge plan={user.plan} />
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 text-xs text-slate-400 hover:text-white transition-colors w-full"
              >
                <LogOut size={14} />
                Sign out
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-14 bg-white border-b border-slate-200 flex items-center px-4 gap-4 shrink-0">
          <button className="lg:hidden text-slate-600 hover:text-slate-900"
                  onClick={() => setSidebarOpen(true)}>
            <Menu size={20} />
          </button>

          <div className="flex items-center gap-2 text-sm text-slate-500">
            <span>{currentPage?.label || 'Dashboard'}</span>
          </div>

          <div className="ml-auto flex items-center gap-3">
            {user && (
              <span className="text-xs text-slate-400 hidden sm:inline">
                {user.email}
              </span>
            )}
            <span className="text-xs text-slate-400">
              {new Date().toLocaleDateString('en-GB', {
                weekday: 'short', day: 'numeric', month: 'short', year: 'numeric'
              })}
            </span>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
