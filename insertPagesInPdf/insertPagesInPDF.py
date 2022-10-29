# !/usr/bin/python

import fitz
import sys
import os

import re

from os import listdir
from os.path import isfile, join

def main():
    if sys.argv.len != 3:
        print("Uso: insertPagesInPDF.py archivo.pdf n [n es la pagina después de la que insertará 0.pdf, 1.pdf, etc. en este directorio]")
    else:
        paginaInsertar = sys.argv[2]
        archivoOriginal = sys.argv[1]
        archivo_salida = f"{archivoOriginal}_Inserted.pdf"

        carpetaPDFs = "C:\\\\Users\\nsole\\Desktop\\Scraping\\insertPagesInPdf\\"
        archivosAInsertar = []

        onlyfiles = [f for f in listdir(carpetaPDFs) if isfile(join(carpetaPDFs, f))]
        for filePDF in onlyfiles:
            soloNombrePDF = filePDF.split('insertPagesInPDF\\')[1]
            if soloNombrePDF == re.match('[0-9]+\.pdf',soloNombrePDF):
                archivosAInsertar.append(filePDF)
        #Insertar
        
        archivosAInsertar.sort()
        numeroArchivos = len(archivosAInsertar)

        for i in range(numeroArchivos):
            
            original_pdf = fitz.open(archivoOriginal)
            extra_page = fitz.open(archivosAInsertar[i])

            original_pdf.insertPDF(extra_page, paginaInsertar)
            original_pdf.save(archivo_salida)



if __name__ == "__main__":
    main()