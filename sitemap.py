#Generate Sitemap
import os
import datetime

def modificationDate(filename):
    t = os.path.getmtime(filename)
    return datetime.date.fromtimestamp(t)

f = open("sitemap.xml","w")

f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

currentDirectory = os.getcwd()
for subdir, dirs, files in os.walk(currentDirectory):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".html") and not '\\components\\' in filepath and not '\\templates\\' in filepath:
            f.write('\t<url>\n')
            websitepath = filepath.replace("D:\Git\debatebroshow.github.io\\", "https://debatebroshow.com\\")
            f.write('\t\t<loc>' + websitepath +'</loc>\n')
            f.write('\t\t<lastmod>' + str(modificationDate(filepath)) +'</lastmod>\n')
            f.write("\t</url>\n")
f.write('</urlset>')
f.close()
