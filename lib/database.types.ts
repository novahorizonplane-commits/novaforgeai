export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          name: string | null
          avatar: string | null
          wallet_address: string | null
          email_verified: string | null
          created_at: string
          updated_at: string
          deleted_at: string | null
        }
        Insert: {
          id?: string
          email: string
          name?: string | null
          avatar?: string | null
          wallet_address?: string | null
          email_verified?: string | null
          created_at?: string
          updated_at?: string
          deleted_at?: string | null
        }
        Update: {
          id?: string
          email?: string
          name?: string | null
          avatar?: string | null
          wallet_address?: string | null
          email_verified?: string | null
          created_at?: string
          updated_at?: string
          deleted_at?: string | null
        }
      }
    }
    Views: {}
    Functions: {}
    Enums: {}
  }
}
