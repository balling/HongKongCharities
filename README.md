This scraper is running periodically on [Morph](https://morph.io/balling/HongKongCharities).  Visit the page to download the data set.

# Source
The current complete list of charitable Institutions & trusts of a public character, which are exempt from tax under section 88 of the Inland Revenue Ordinance is available on [IRD website](https://www.ird.gov.hk/eng/tax/ach_index.htm) as:
* [search page](https://www.ird.gov.hk/charity/view_detail.php)
  - no unique identifier for each charity for change tracking
  - no subsidiaries information
* [pdf](https://www.ird.gov.hk/eng/pdf/s88list_emb.pdf)
  - no unique identifier for each charity for change tracking
  - non machine readable (pdftotxt.py attempts to convert the pdf into txt, however the formatting of the pdf is too irregular for extracting structured information reliably)

# Todos
- [ ] obtain identifier for each subsidiary (e.g. S000002 for Ricci Hall (H.K.U.))
- [ ] add last update time for subsidiaries
- [ ] add status (active/inactive) for each charity based on last update time
