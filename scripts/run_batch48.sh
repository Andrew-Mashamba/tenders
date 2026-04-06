#!/bin/bash
# Run batch 48 - scrape 25 institutions
PROJECT="/Volumes/DATA/PROJECTS/TENDERS"
RUN_ID="run_20260315_060430_batch48"
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

slugs="hsh hssrf hubnet huca hudhud huga huheso humanrights humanrightsinstitute humor hunkydory hurumahospital husseini hyperionconsultants hypermed iaa iae iamorganic ibes ibmtelecenter ibn-tv ibunjazar icare ice icealion"

for slug in $slugs; do
  readme="$PROJECT/institutions/$slug/README.md"
  [ ! -f "$readme" ] && echo "RESULT|$slug|error|0|0" && continue
  
  url=$(grep "tender_url:" "$readme" | grep -oE 'https?://[^"]+' | head -1)
  [ -z "$url" ] && url=$(grep "homepage:" "$readme" | grep -oE 'https?://[^"]+' | head -1)
  [ -z "$url" ] && echo "RESULT|$slug|error|0|0" && continue
  
  if echo "$url" | grep -q "facebook"; then
    echo "RESULT|$slug|skipped|0|0"
    status="skipped"
    tenders=0
    docs=0
    err="Facebook URL"
  else
    html=$(curl -sL -m 12 -A "TendersBot/1.0" "$url" 2>/dev/null)
    if [ -z "$html" ]; then
      echo "RESULT|$slug|error|0|0"
      status="error"
      tenders=0
      docs=0
      err="Fetch failed"
    else
      if echo "$html" | grep -qiE "tender|tenders|procurement|rfi|rfp|rfq|eoi|bid|bids|manunuzi"; then
        echo "RESULT|$slug|success|1|0"
        status="success"
        tenders=1
        docs=0
        err=""
      else
        echo "RESULT|$slug|success|0|0"
        status="success"
        tenders=0
        docs=0
        err=""
      fi
    fi
  fi
  
  inst="$PROJECT/institutions/$slug"
  mkdir -p "$inst"
  python3 -c "
import json
p='$PROJECT'
s='$slug'
r='$RUN_ID'
t='$NOW'
st='$status'
te=$tenders
d=$docs
err='$err'
last={'institution':s,'last_scrape':t,'next_scrape':t,'active_tenders_count':te,'status':st,'error':err if err else None}
open(p+'/institutions/'+s+'/last_scrape.json','w').write(json.dumps(last,indent=2))
logf=p+'/institutions/'+s+'/scrape_log.json'
try: data=json.load(open(logf))
except: data={'runs':[]}
data['runs'].insert(0,{'run_id':r,'timestamp':t,'duration_seconds':0,'status':st,'tenders_found':te,'new_tenders':te,'updated_tenders':0,'documents_downloaded':d,'errors':[err] if err else []})
open(logf,'w').write(json.dumps(data,indent=2))
" 2>/dev/null
  
  sleep 2
done

python3 "$PROJECT/scripts/sync_leads_csv.py" 2>/dev/null || true
echo "Done."
