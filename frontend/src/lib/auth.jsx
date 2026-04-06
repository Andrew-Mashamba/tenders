import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'

const AuthContext = createContext(null)

const TOKEN_KEY = 'tenders_access_token'
const REFRESH_KEY = 'tenders_refresh_token'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const saveTokens = (access, refresh) => {
    localStorage.setItem(TOKEN_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
  }

  const clearTokens = () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
  }

  const getAccessToken = () => localStorage.getItem(TOKEN_KEY)
  const getRefreshToken = () => localStorage.getItem(REFRESH_KEY)

  const fetchWithAuth = useCallback(async (url, opts = {}) => {
    const token = getAccessToken()
    const headers = { ...opts.headers }
    if (token) headers['Authorization'] = `Bearer ${token}`
    if (opts.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json'

    let res = await fetch(url, { ...opts, headers })

    // Try refresh on 401
    if (res.status === 401 && getRefreshToken()) {
      const refreshRes = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: getRefreshToken() }),
      })

      if (refreshRes.ok) {
        const data = await refreshRes.json()
        saveTokens(data.access_token, data.refresh_token)
        setUser(data.user)
        headers['Authorization'] = `Bearer ${data.access_token}`
        res = await fetch(url, { ...opts, headers })
      } else {
        clearTokens()
        setUser(null)
        throw new Error('Session expired')
      }
    }

    return res
  }, [])

  const login = async (email, password) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Login failed' }))
      throw new Error(err.detail || 'Login failed')
    }
    const data = await res.json()
    saveTokens(data.access_token, data.refresh_token)
    setUser(data.user)
    return data
  }

  const register = async (email, password, name, company) => {
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name, company }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Registration failed' }))
      throw new Error(err.detail || 'Registration failed')
    }
    const data = await res.json()
    saveTokens(data.access_token, data.refresh_token)
    setUser(data.user)
    return data
  }

  const logout = async () => {
    const rt = getRefreshToken()
    if (rt) {
      try {
        await fetchWithAuth('/api/auth/logout', {
          method: 'POST',
          body: JSON.stringify({ refresh_token: rt }),
        })
      } catch {}
    }
    clearTokens()
    setUser(null)
  }

  const refreshUser = useCallback(async () => {
    const token = getAccessToken()
    if (!token) { setLoading(false); return }
    try {
      const res = await fetchWithAuth('/api/auth/me')
      if (res.ok) {
        setUser(await res.json())
      } else {
        clearTokens()
        setUser(null)
      }
    } catch {
      clearTokens()
      setUser(null)
    }
    setLoading(false)
  }, [fetchWithAuth])

  useEffect(() => { refreshUser() }, [refreshUser])

  return (
    <AuthContext.Provider value={{
      user, loading, login, register, logout, refreshUser,
      fetchWithAuth, getAccessToken, isAuthenticated: !!user,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
