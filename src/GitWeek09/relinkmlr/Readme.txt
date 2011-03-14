Application: URL cataloging tool
Running on Google App Engine at: http://relinkmlr.appspot.com
Admin interface at: http://relinkmlr.appspot.com/admin
Author: Melissa Rice (mlrice)

Configuration: app.yaml

Handlers:  relink.py

CSS: static/CSS/base.css is the css file for this site.
  
Templates:  
  /            ---> index.html (landing page)
  /links       ---> links.html (links page for displaying all the links)
  /tags        ---> tags.html  (tags page for displaying all the tags)
  /tag/tagname ---> tagged.html (displays all links tagged with the requested tag
  /link/id     ---> linkEdit.html (displays the link properties for editing)
  /admin       ---> admin.html > for the main admin page (working)
  /admin/export/csv  ---> export-csv.txt CSV exporter (partially working)
  /admin/export/json ---> export-json.txt (working)
  /admin/tasks ---> tasks.html (informal task list for site development - stale)

Fragilities and broken things:
1. Currently there is no real authorization going on.... At least the data is backed up.
2. Tagnames should not contain whitespace. In fact, they are currently only tested 
   with alphabetical characters.
3. Virtually nothing is sanitized. The json import, in particular, is very sensitive 
   to non-ascii and non-printing characters. 
4. I wrote the json export by hand (to understand the wheel better) and used json.loads
   for the import. The import is broken by the slightest irregularity so I will have to
   try json.dumps for export and/or carefully sanitize. I feel like I know enough about
   wheels for now.
5. The csv output is partially complete - I didn't fix the linktag output yet but I know
   what is broken. The csv import is not written yet.
6. Initially I was not querying foreign keys correctly. That is now fixed in the update links
   but the initial addLink page is still broken so it is only adding the first tag, even if
   you select many tags. I know how to fix but have not done it yet.
7. The tag list should be alphabetized and the display improved.
8. I plan to add taglists on the tagged page, for refining the search; not done yet clearly.
9. It should be more convenient to add new tags while adding a new link - I just have to
   provide the form support but have not done so yet.

   