import docx
from docx.shared import Inches, Pt, Mm
import win32com.client
import pythoncom
import fitz

doc = docx.Document(r"C:\Users\note\vf\vf21_pdf_clone_농업전망\result\[036]_농업전망_제1원본_템플릿_골격_레이아웃.docx")

# Table 18 is the header table
tbl18 = doc.tables[18]
print("Table 18 text:", " ".join(c.text.strip() for row in tbl18.rows for c in row.cells))

# Remove Table 18 from its parent
tbl18._element.getparent().remove(tbl18._element)
print("Removed Table 18!")

test_docx = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\process\test_no_table18.docx"
test_pdf = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\process\test_no_table18.pdf"
doc.save(test_docx)

pythoncom.CoInitialize()
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
try:
    wdoc = word.Documents.Open(test_docx)
    wdoc.SaveAs(test_pdf, FileFormat=17)
    wdoc.Close(False)
finally:
    word.Quit()
    pythoncom.CoUninitialize()

pdoc = fitz.open(test_pdf)
print("Page count:", len(pdoc))
pix = pdoc[25].get_pixmap(dpi=150)
out_img = r"C:\Users\note\vf\vf21_pdf_clone_농업전망\process\test_p26_fixed.png"
pix.save(out_img)
print("Saved test_p26_fixed.png")
