/**
 * SETUP GUIDE: Authentication Configuration
 * 
 * Phase 1 Step 2: Authentication - Supabase Integration
 */

# Authentication Setup Guide

## Prerequisites

Before proceeding, ensure you have:
- A Supabase project (https://supabase.com)
- Supabase credentials (Project URL and Anon Key)
- PostgreSQL database connected to Supabase

## Step 1: Supabase Configuration

### Create Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Copy your Project URL and Anon Key
4. Store them in `.env` as:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   ```

### Enable Authentication Providers

In Supabase Dashboard → Authentication → Providers:

- **Email/Password**: Enabled by default
- **Google OAuth**: 
  1. Go to Google Cloud Console
  2. Create OAuth 2.0 credentials
  3. Add redirect URI: `https://your-project.supabase.co/auth/v1/callback`
  4. Copy Client ID and Secret
  5. Paste in Supabase → Authentication → Google

## Step 2: Database Sync

### Link Supabase to Prisma

1. Update `prisma/schema.prisma`:
   ```prisma
   datasource db {
     provider = "postgresql"
     url      = env("DATABASE_URL")
   }
   ```

2. Set `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL="postgresql://[user]:[password]@db.xxx.supabase.co:5432/postgres"
   ```

### Push Prisma Schema

```bash
npm run db:push
```

This creates all tables and relationships in Supabase PostgreSQL.

## Step 3: Authentication Flow

### User Registration

```
1. User submits email/password/name
2. POST /api/auth/signup
3. Supabase creates auth user
4. Prisma creates user record
5. Free subscription created
6. Email verification sent
```

### User Login

```
1. User submits email/password
2. POST /api/auth/signin
3. Supabase verifies credentials
4. Session tokens returned
5. User redirected to dashboard
```

### Protected Routes

```
1. Middleware checks authentication
2. If no session → redirect to /auth/login
3. If authenticated → allow access
```

## Step 4: Environment Variables

Copy all required vars to `.env.local`:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Database
DATABASE_URL=postgresql://[user]:[password]@db.xxx.supabase.co:5432/postgres

# Application
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

## Step 5: Testing

### Test Sign Up

```bash
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  }'
```

### Test Sign In

```bash
curl -X POST http://localhost:3000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

## Step 6: Frontend Integration

### Use Auth Context

```typescript
import { useAuth } from '@/lib/auth-context'

export function MyComponent() {
  const { user, signIn, signOut } = useAuth()
  
  return (
    <div>
      {user && <p>Welcome, {user.email}</p>}
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  )
}
```

### Protect Routes

```typescript
import { useProtectedRoute } from '@/lib/auth-hooks'

export default function DashboardPage() {
  const { isLoading, isAuthenticated } = useProtectedRoute()
  
  if (isLoading) return <div>Loading...</div>
  if (!isAuthenticated) return null
  
  return <div>Dashboard Content</div>
}
```

## Troubleshooting

### Email Verification Issues
- Check Supabase email templates: Authentication → Email Templates
- Ensure SMTP is configured in Supabase settings
- Check spam folder for verification emails

### OAuth Login Issues
- Verify redirect URI matches exactly
- Check Google OAuth credentials
- Ensure `NEXT_PUBLIC_SUPABASE_URL` is correct

### Session Persistence Issues
- Check browser cookies are enabled
- Verify JWT tokens are valid
- Check auth middleware configuration

### Database Connection Issues
- Verify `DATABASE_URL` format
- Test connection: `psql <DATABASE_URL>`
- Check IP whitelist in Supabase

## Security Best Practices

✅ **DO:**
- Use HTTPS in production
- Rotate API keys regularly
- Enable 2FA for Supabase dashboard
- Use Row Level Security (RLS) for sensitive data
- Validate all user inputs
- Store sensitive data server-side

❌ **DON'T:**
- Commit `.env` files
- Use anon key for sensitive operations
- Expose service role key to frontend
- Store passwords in plain text
- Trust client-side validation alone

## Next Steps

Phase 1 Step 3: Dashboard
- Create main dashboard layout
- Add navigation and sidebar
- Implement user profile page
- Add project listing

---

**Status**: Phase 1 Step 2 Complete ✅
**Auth System**: Fully functional and tested
**Next**: Phase 1 Step 3 - Dashboard
