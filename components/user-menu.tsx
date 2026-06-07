'use client'

import { useState } from 'react'
import { useAuth } from '@/lib/auth-context'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ChevronDown, LogOut, User, Settings } from 'lucide-react'

export function UserMenu() {
  const [isOpen, setIsOpen] = useState(false)
  const { user, signOut } = useAuth()
  const router = useRouter()

  const handleSignOut = async () => {
    await signOut()
    router.push('/auth/login')
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-slate-100 transition"
      >
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
          {user?.name?.charAt(0).toUpperCase()}
        </div>
        <div className="hidden sm:block text-sm">
          <div className="font-medium text-slate-900">{user?.name}</div>
          <div className="text-xs text-slate-500">{user?.email}</div>
        </div>
        <ChevronDown className="w-4 h-4 text-slate-400" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 z-50">
          <Link
            href="/dashboard/profile"
            onClick={() => setIsOpen(false)}
            className="flex items-center space-x-2 px-4 py-2 hover:bg-slate-50 transition border-b border-slate-100"
          >
            <User className="w-4 h-4 text-slate-600" />
            <span className="text-sm text-slate-700">Profile</span>
          </Link>
          <Link
            href="/dashboard/settings"
            onClick={() => setIsOpen(false)}
            className="flex items-center space-x-2 px-4 py-2 hover:bg-slate-50 transition border-b border-slate-100"
          >
            <Settings className="w-4 h-4 text-slate-600" />
            <span className="text-sm text-slate-700">Settings</span>
          </Link>
          <button
            onClick={handleSignOut}
            className="w-full flex items-center space-x-2 px-4 py-2 hover:bg-red-50 transition text-red-600"
          >
            <LogOut className="w-4 h-4" />
            <span className="text-sm font-medium">Sign Out</span>
          </button>
        </div>
      )}
    </div>
  )
}
