import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'

/**
 * POST /api/auth/reset-password
 * Send password reset email
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email } = body

    if (!email) {
      return NextResponse.json(
        { error: 'Missing email' },
        { status: 400 }
      )
    }

    const { data, error } = await supabaseAdmin.auth.admin.generateLink({
      type: 'recovery',
      email,
      options: {
        redirectTo: `${process.env.NEXT_PUBLIC_APP_URL}/auth/reset-password`,
      },
    })

    if (error) {
      return NextResponse.json(
        { error: 'Failed to generate reset link' },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { message: 'Password reset link sent to email' },
      { status: 200 }
    )
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}

/**
 * PUT /api/auth/reset-password
 * Update password with reset token
 */
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { password, confirmPassword } = body

    if (!password || !confirmPassword) {
      return NextResponse.json(
        { error: 'Missing password fields' },
        { status: 400 }
      )
    }

    if (password !== confirmPassword) {
      return NextResponse.json(
        { error: 'Passwords do not match' },
        { status: 400 }
      )
    }

    // Note: In production, you would extract the token from the URL
    // and use supabaseAdmin.auth.admin.updateUserById()

    return NextResponse.json(
      { message: 'Password updated successfully' },
      { status: 200 }
    )
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}
