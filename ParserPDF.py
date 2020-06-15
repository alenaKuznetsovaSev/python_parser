from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO

url = "http://www.silicontao.com/ProgrammingGuide/other/beejnet.pdf"
writer = PdfFileWriter()

remoteFile = urlopen(Request(url)).read()
memoryFile = StringIO(remoteFile)
pdfFile = PdfFileReader(memoryFile)

for pageNum in xrange(pdfFile.getNumPages()):
        currentPage = pdfFile.getPage(pageNum)
        #currentPage.mergePage(watermark.getPage(0))
        writer.addPage(currentPage)


outputStream = open("output.pdf","wb")
writer.write(outputStream)
outputStream.close()