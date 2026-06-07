import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'
import { prisma } from '@/lib/prisma'
import { getUserFromHeaders } from '@/lib/auth-middleware'

/**
 * GET /api/auth/me
 * Get current authenticated user
 */
export async function GET(request: NextRequest) {
  try {
    const user = getUserFromHeaders(request)

    if (!user) {
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    // Fetch full user details from database
    const userDetails = await prisma.user.findUnique({
      where: { id: user.id },
      include: {
        subscriptions: true,
        projects: { take: 5 },
      },
    })

    if (!userDetails) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    }

    return NextResponse.json(
      {
        user: userDetails,
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

/**
 * PUT /api/auth/me
 * Update current user profile
 */
export async function PUT(request: NextRequest) {
  try {
    const user = getUserFromHeaders(request)

    if (!user) {
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    const body = await request.json()
    const { name, avatar, walletAddress } = body

    const updatedUser = await prisma.user.update({
      where: { id: user.id },
      data: {
        ...(name && { name }),
        ...(avatar && { avatar }),
        ...(walletAddress && { walletAddress }),
        updatedAt: new Date(),
      },
    })

    return NextResponse.json(
      {
        message: 'Profile updated successfully',
        user: updatedUser,
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
