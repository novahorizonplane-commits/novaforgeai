import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'
import { prisma } from '@/lib/prisma'

/**
 * POST /api/auth/signup
 * Create new user account with email and password
 * Automatically creates free subscription
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, password, name } = body

    // Validate inputs
    if (!email || !password || !name) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    })

    if (existingUser) {
      return NextResponse.json(
        { error: 'Email already registered' },
        { status: 409 }
      )
    }

    // Create auth user in Supabase
    const { data: authData, error: authError } = await supabaseAdmin.auth.admin.createUser({
      email,
      password,
      email_confirm: false,
    })

    if (authError) {
      return NextResponse.json(
        { error: authError.message || 'Failed to create user' },
        { status: 400 }
      )
    }

    // Create user record in database
    const user = await prisma.user.create({
      data: {
        id: authData.user.id,
        email,
        name,
      },
    })

    // Create free subscription
    const subscription = await prisma.subscription.create({
      data: {
        userId: user.id,
        plan: 'FREE',
        status: 'ACTIVE',
        startDate: new Date(),
        renewalDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
      },
    })

    // Send verification email
    await supabaseAdmin.auth.admin.sendUserInvitationEmail(authData.user.id)

    return NextResponse.json(
      {
        message: 'Account created successfully. Please verify your email.',
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
        },
        subscription: {
          id: subscription.id,
          plan: subscription.plan,
          status: subscription.status,
        },
      },
      { status: 201 }
    )
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}
