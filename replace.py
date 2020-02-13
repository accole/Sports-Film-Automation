
import os
import sys
import csv
import pandas as pd
from optparse import OptionParser


def main():

    #output version message and how to use it
    version_msg = "%prog 1.0"
    usage_msg = """%prog -d [TEAM] -w [TEAM] -l [OPTIONAL] DIR
       Replaces d/w with team names for all csv files in DIR.
       (include -l if live tagged in DartFish)"""

    #create parser
    parser = OptionParser(version=version_msg, usage=usage_msg)

    #implement options
    parser.add_option("-w", "--white", action="store", dest="team_w", default="", 
                    help="White Team")
    parser.add_option("-d", "--dark", action="store", dest="team_d", default="", 
                    help="Dark Team")
    parser.add_option("-l", "--live", action="store_true", dest="livetag", default=False, 
                    help="Live Tagged?")

    #read the input line and store options
    options, args = parser.parse_args(sys.argv[1:])

    #error handling for dark and white team
    if options.team_d == "":
        parser.error("Must specify dark team")
    if options.team_w == "":
        parser.error("Must specify white team")

    utflag = options.livetag

    #error handling for input file
    try:
        folder = args[0]
    except:
        parser.error("invalid DIR")

    #format the directory name
    folder = "../" + folder + "/"

    #read in the folder contents
    csv_files = []
    names = []
    print("Loading CSV files from %s..." % folder)
    with os.scandir(folder) as entries:
        for entry in entries:
            s_entry = str(entry)
            if s_entry[-6:] == ".csv'>":
                print("\t%s" % entry.name)
                names.append(entry.name)
                csv_files.append(folder + entry.name)
        
    print(" ")

    #test for CSV files
    if len(csv_files) == 0:
        parser.error("No CSV Files found in DIR")
        
    #open each of the csv files with pandas
    i = 0
    for f in csv_files:
         
        print("Replacing %s" % f)

        #open the csv file with pandas
        if utflag:
            sheet = pd.read_csv(f, encoding = "utf-16")
            sheet.replace(to_replace = '"', value = "", inplace = True, regex = True)
        else :
            sheet = pd.read_csv(f)

        #replace Dark with team_d
        sheet.replace(to_replace = "Dark", value = options.team_d, inplace = True, regex = True)
        sheet.replace(to_replace = "White", value = options.team_w, inplace = True, regex = True)

        #create save name with i
        savename = names[i][:-4] + " tags replaced"
        if utflag:
            print("Saving as unicode to: %s\n" % (folder + savename + ".txt"))
            savename = folder + savename + "LIVE.txt"
        else:
            savename = folder + savename + ".txt"
            print("Saving as unicode to: %s\n" % savename)

        i = i + 1
        #save as unicode text to folder
        sheet.to_csv(savename, index = False, sep = '\t')
        
        #if live tagged, quotes must be removed
        if utflag:
            final = savename[:-8] + ".txt"
            with open(savename, 'rb') as infile:
                with open(final, 'wb') as outfile:
                    temp = infile.read().replace(b'"', b'')
                    outfile.write(temp)

    #cleanup
    with os.scandir(folder) as entries:
        for entry in entries:
            s_entry = str(entry)
            if s_entry[-10:] == "LIVE.txt'>":
                os.unlink(os.path.abspath(folder + entry.name))
    
    #done
    print("Done.")
    

if __name__ == "__main__":
    main()