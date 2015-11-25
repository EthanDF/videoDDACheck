# videoDDACheck
checks the titles of our PDA collection against an incoming set of video titles for any matches

FAU Libraries puts PDA titles into a database that is not easy to search in our catalog. However, we can capture those titles by querying the oracle tables. The following query will capture all of the PDA titles that are in video format:

select b.Z13U_REC_KEY, a.Z13_TITLE, a.Z13_IMPRINT, b.Z13U_USER_DEFINED_4 AS Control_Number, a.Z13_UPDATE_DATE, a.*
from PDA01.Z13 a
join PDA01.z13u b on a.Z13_REC_KEY = b.Z13U_REC_KEY
where 1=1
and Z13U_USER_DEFINED_5 = 'FA'
and b.Z13U_USER_DEFINED_1 = 'VM'

Once those are exported into a CSV, we can compare the titles of videos of an incoming MARC file.

Titles are:
- stripped of all spaces and the following characters: ":", "-", ".", ","
- made all caps

Results are printed to a log (which is launched at the end of the script).

Results should be considered for removal from the PDA database so that patrons use our licensed titles instead of triggering PDA loans
