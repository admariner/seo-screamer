import pandas
import csv
import sys

from tqdm import tqdm


class color:
    PURPLE = '33[95m'
    CYAN = '33[96m'
    DARKCYAN = '33[36m'
    BLUE = '33[94m'
    GREEN = '33[92m'
    YELLOW = '33[93m'
    RED = '33[91m'
    BOLD = '33[1m'
    UNDERLINE = '33[4m'
    END = '33[0m'


def main(argv):
    if len(argv) != 4:
        print('Usage: programname.py crawl_overview1.csv crawl_overview2.csv output.csv')
        sys.exit()

    headerrows = 5
    endline = 191

    fileone = get_csv(argv[1])
    filetwo = get_csv(argv[2])

    fileone = fileone[0:endline]
    filetwo = filetwo[0:endline]

    fileonesite = fileone[1][1]
    filetwosite = filetwo[1][1]

    fileone = fileone[headerrows:]
    filetwo = filetwo[headerrows:]

    fileonedata = []
    filetwodata = []
    combineddata = []
    firstcolumn = []

    firstcolumn.extend(get_column(fileone, 0))
    fileonedata.extend(get_column(fileone, 1))
    filetwodata.extend(get_column(filetwo, 1))
    combineddata.extend(zip(firstcolumn, fileonedata, filetwodata))

    outFile = csv.writer(open(argv[3], 'w'))
    outFile.writerow(["", fileonesite, filetwosite])
    for i in tqdm(combineddata):
        outFile.writerow(i)

    if fileonedata == filetwodata:
        print(color.BOLD + color.RED + "Crawl files are identical" + color.END)
    else:
        print(color.BOLD + color.GREEN + "Crawl files are NOT identical" + color.END)


def get_csv(thefile):
    datafile = open(thefile, 'r')
    datareader = csv.reader(datafile, delimiter=",")
    data = []
    for row in tqdm(datareader):
        data.append(row)
    datafile.close()
    return data


def get_column(thelist, thecolumn):
    newlist = []
    for row in tqdm(thelist):
        if len(row) >= thecolumn + 1:
            newlist.append(row[thecolumn])
        else:
            newlist.append("")
    return newlist


if __name__ == '__main__':
    main(sys.argv)