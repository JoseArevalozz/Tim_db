from io import StringIO,BytesIO
import xlsxwriter
from .models import Rejected

def WriteToExcel(check):
    headers = ['Pn', 'Description', 'Commodity', 'Product', 'Fail Description', 'Sn', 'Sn System', 'Station', 'Folio', 'Qty', 'Ubicacion Logica']
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)

    # Here we will adding the code to add data
    worksheet_s = workbook.add_worksheet("Summary")
    row_num = 0
    
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    acum_h = 0
    for header_f in headers:
        worksheet_s.write(0, acum_h, header_f, header)
        acum_h+=1
        
    worksheet_s.set_column('A:A', 20)
    worksheet_s.set_column('B:B', 20)
    worksheet_s.set_column('C:C', 11)
    worksheet_s.set_column('D:D', 13)
    worksheet_s.set_column('E:E', 18)
    worksheet_s.set_column('G:G', 20)
    worksheet_s.set_column('H:H', 12)
    worksheet_s.set_column('K:K', 14)
    
    for checked in check:
        reject = Rejected.objects.get(id=checked)
        
        sn = str(reject.id_f.sn_f)
        model = str(reject.id_f.sn_f.pn_b.product)
        message = str(reject.id_f.id_er.message)
        pn = str(reject.pn_b.pn)
        snDamaged = str(reject.snDamaged)
        description = str(reject.pn_b.description)
        commodity = str(reject.pn_b.commodity)
        # station = '' if str(reject.id_f.id_s.stationName) == None else str(reject.id_f.id_s.stationName)
        station = str(reject.id_f.id_s.stationName)
        folio = str(reject.folio)
        ubi = str(reject.pn_b.ubiLogic)
        
        row_num = row_num + 1
        worksheet_s.write(row_num, 0, pn, )
        worksheet_s.write(row_num, 1, description,)
        worksheet_s.write(row_num, 2, commodity,)
        worksheet_s.write(row_num, 3, model,)
        worksheet_s.write(row_num, 4, message,)
        worksheet_s.write(row_num, 5, snDamaged,)
        worksheet_s.write(row_num, 6, sn,)
        worksheet_s.write(row_num, 7, station,)
        worksheet_s.write(row_num, 8, folio,)
        worksheet_s.write(row_num, 9, str(1), )
        worksheet_s.write(row_num, 10, ubi, )
    # the rest of the data
    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data