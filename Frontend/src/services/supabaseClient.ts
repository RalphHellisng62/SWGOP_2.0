
import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://orchzfygjitiaoqigljhy.supabase.co'
const SUPABASE_ANON_KEY = 'sb_publishable_fWFtY2BeeetX3HinMMUboQ_gmWar9z0' //

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)