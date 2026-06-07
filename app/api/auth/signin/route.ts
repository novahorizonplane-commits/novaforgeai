import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'
import { prisma } from '@/lib/prisma'

/**
 * POST /api/auth/signin
 * Sign in user with email and password
 * Returns session tokens
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, password } = body

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Missing email or password' },
        { status: 400 }
      )
    }

    // Verify credentials
    const { data, error } = await supabaseAdmin.auth.admin.listUsers()

    if (error) {
      return NextResponse.json({ error: 'Authentication failed' }, { status: 401 })
    }

    // Get user tokens
    const { data: sessionData, error: sessionError } =
      await supabaseAdmin.auth.signInWithPassword({
        email,
        password,
      })

    if (sessionError) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      )
    }

    // Fetch user from database
    const user = await prisma.user.findUnique({
      where: { email },
    })

    return NextResponse.json(
      {
        message: 'Sign in successful',
        user: {
          id: user?.id,
          email: user?.email,
          name: user?.name,
        },
        session: {
          accessToken: sessionData.session?.access_token,
          refreshToken: sessionData.session?.refresh_token,
        },
      },
      { status: 200 }
    )
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}
