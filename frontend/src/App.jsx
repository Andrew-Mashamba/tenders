import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './lib/auth'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Tenders from './pages/Tenders'
import TenderDetail from './pages/TenderDetail'
import Applications from './pages/Applications'
import Opportunities from './pages/Opportunities'
import Institutions from './pages/Institutions'
import InstitutionDetail from './pages/InstitutionDetail'
import ScraperControl from './pages/ScraperControl'
import Login from './pages/Login'
import Register from './pages/Register'
import Pricing from './pages/Pricing'
import Settings from './pages/Settings'
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminUsers from './pages/admin/AdminUsers'
import AdminUserDetail from './pages/admin/AdminUserDetail'
import AdminInstitutions from './pages/admin/AdminInstitutions'
import AdminSubscriptions from './pages/admin/AdminSubscriptions'

function ProtectedLayout({ children }) {
  return (
    <ProtectedRoute>
      <Layout>{children}</Layout>
    </ProtectedRoute>
  )
}

function AdminLayout({ children }) {
  return (
    <ProtectedRoute adminOnly>
      <Layout>{children}</Layout>
    </ProtectedRoute>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes with layout */}
        <Route path="/" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
        <Route path="/tenders" element={<ProtectedLayout><Tenders /></ProtectedLayout>} />
        <Route path="/tenders/:tenderId" element={<ProtectedLayout><TenderDetail /></ProtectedLayout>} />
        <Route path="/applications" element={<ProtectedLayout><Applications /></ProtectedLayout>} />
        <Route path="/opportunities" element={<AdminLayout><Opportunities /></AdminLayout>} />
        <Route path="/institutions" element={<ProtectedLayout><Institutions /></ProtectedLayout>} />
        <Route path="/institutions/:slug" element={<ProtectedLayout><InstitutionDetail /></ProtectedLayout>} />
        <Route path="/scraper" element={<AdminLayout><ScraperControl /></AdminLayout>} />
        <Route path="/pricing" element={<ProtectedLayout><Pricing /></ProtectedLayout>} />
        <Route path="/settings" element={<ProtectedLayout><Settings /></ProtectedLayout>} />

        {/* Admin routes */}
        <Route path="/admin" element={<AdminLayout><AdminDashboard /></AdminLayout>} />
        <Route path="/admin/users" element={<AdminLayout><AdminUsers /></AdminLayout>} />
        <Route path="/admin/users/:id" element={<AdminLayout><AdminUserDetail /></AdminLayout>} />
        <Route path="/admin/institutions" element={<AdminLayout><AdminInstitutions /></AdminLayout>} />
        <Route path="/admin/subscriptions" element={<AdminLayout><AdminSubscriptions /></AdminLayout>} />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthProvider>
  )
}
