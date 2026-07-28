
import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://orchzfygjtiayqjgljhy.supabase.co' 
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9yY2h6ZnlnanRpYXlxamdsamh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUxOTI5OTksImV4cCI6MjEwMDc2ODk5OX0.qE7jVoMziYZAwG2DYcWNmBVt5ayluj1L7ItUZUXRd8s' //

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)