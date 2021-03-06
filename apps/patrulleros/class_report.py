# -*- coding: utf-8 -*-
from fpdf import FPDF
import time


class PDF(FPDF):

    def header(self):

        self.set_font('Arial', 'B', 12)
        self.set_fill_color(217, 237, 247)
        self.cell(260, 5, 'SISTEMA DE REGISTRO Y CONSULTA DE CLP/UBCH/1x10', '', 1, 'C', 1)
        self.ln(10)

    def footer(self):
        #Posición a 1.5 cm desde abajo
        self.set_y(-15)
        #Arial italic 8
        self.set_font('Arial', 'I', 7)
        #Color de texto en gris
        self.set_text_color(0, 0, 0)
        #Numero de pagina
        self.cell(0, 10, 'Fecha- '+str(time.strftime("%d/%m/%Y")+', '+time.strftime("%I:%M %p") ), 0, 0, 'L')
        self.cell(0, 10, 'http://www.registro1x10.org.ve', 0, 0, 'R')
        self.set_y(-10)
        self.cell(0, 10, 'Pagina '+str(self.page_no()), 0, 0, 'R')

    def chapter_title(self, num, label):
        #Arial 12
        self.set_font('Arial', '', 12)
        #Color de fondo
        self.set_fill_color(200, 220, 255)
        #Titulo
        self.cell(0, 6, "Chapter %d : %s" % (num, label), 0, 1, 'L', 1)
        #Salto de línea
        self.ln(4)

    def chapter_body(self, name):
        #Leer archivo de texto
        txt = file(name).read()
        #Times 12
        self.set_font('Times', '', 12)
        #Emitir texto justificado
        self.multi_cell(0, 5, txt)
        #Salto de línea
        self.ln()
        #Mención en italic -cursiva-
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    # CONSTRUCCTOR DEL DOCUMENTO
    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)
