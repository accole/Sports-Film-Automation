# Sports-Film-Automation
Automating repetitive spreadsheet work for tags in Sports Film in Python3

After tagging a filmed game using Dartfish, excel sheets containing the timestamped tags must be edited.

All tags containing the 'Dark' keyword must be replaced with the home team and all tags containing the
'White' keywords must be replaced with the away team.

After editing, the file must be saved as a tab delimited .txt file.

# Usage

***-d tag*** indicates the home team

***-w tag*** indicates the away team

***-l tag*** indicates the excel tags were tagged in Dartfish and not on the mobile app
             (switches the encodings, mobile app = UTF-8, Dartfish = UTF-16)


Example for UCLA (D) vs USC (W) tagged on mobile app:

***$ python3 replace.py -d UCLA -w USC 'PATH_TO_FOLDER'

Example for Stanford (D) vs UCSB (W) tagged in dartfish:

***$ python3 replace.py -d Stanford -w UCSB -l 'PATH_TO_FOLDER'
  
   *All CSV files in FOLDER must have same encoding, if they differ replace.py will only replace some of the tags
