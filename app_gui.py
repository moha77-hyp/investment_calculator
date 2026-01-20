from tkinter import *
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import io
from datetime import datetime
import helpers

win = None
e1 = None
e2 = None
e3 = None
e4 = None
res_lbl = None
fig = None
ax = None
cvs = None
btn_pdf = None

g_years = []
g_vals = []
g_invs = []
last_data = {}

def run_prog():
    global win, e1, e2, e3, e4, res_lbl, fig, ax, cvs, btn_pdf
    
    win = Tk()
    win.geometry("1100x700")
    win.title(helpers.a("حاسبة الاستثمار الاحترافية"))
    win.configure(bg="#f0f0f0")

    f1 = Frame(win)
    f1.pack(fill=BOTH, expand=True, padx=20, pady=20)

    lf = LabelFrame(f1, text=helpers.a("بيانات الاستثمار"))
    lf.pack(side=LEFT, fill=Y, padx=(0, 20), ipadx=10, ipady=10)

    l1 = Label(lf, text=helpers.a("المبلغ الأولي ($):"), font=("Arial", 11))
    l1.grid(row=0, column=0, padx=10, pady=10)
    e1 = Entry(lf, font=("Arial", 11))
    e1.grid(row=0, column=1, padx=10, pady=10)

    l2 = Label(lf, text=helpers.a("الإيداع الشهري ($):"), font=("Arial", 11))
    l2.grid(row=1, column=0, padx=10, pady=10)
    e2 = Entry(lf, font=("Arial", 11))
    e2.grid(row=1, column=1, padx=10, pady=10)

    l3 = Label(lf, text=helpers.a("العائد السنوي (%):"), font=("Arial", 11))
    l3.grid(row=2, column=0, padx=10, pady=10)
    e3 = Entry(lf, font=("Arial", 11))
    e3.grid(row=2, column=1, padx=10, pady=10)

    l4 = Label(lf, text=helpers.a("مدة الاستثمار (سنة):"), font=("Arial", 11))
    l4.grid(row=3, column=0, padx=10, pady=10)
    e4 = Entry(lf, font=("Arial", 11))
    e4.grid(row=3, column=1, padx=10, pady=10)

    b_fr = Frame(lf)
    b_fr.grid(row=4, column=0, columnspan=2, pady=20)

    b1 = Button(b_fr, text=helpers.a("حساب وعرض الرسم"), command=do_calc, bg="#dddddd")
    b1.pack(side=TOP, fill=X, pady=5)

    btn_pdf = Button(b_fr, text=helpers.a("تصدير تقرير PDF"), command=make_pdf, state=DISABLED, bg="#dddddd")
    btn_pdf.pack(side=TOP, fill=X, pady=5)

    res_lbl = Label(lf, text="", font=("Arial", 12, "bold"), fg="#2c3e50", justify=RIGHT)
    res_lbl.grid(row=5, column=0, columnspan=2, pady=20)

    fr_ch = Frame(f1)
    fr_ch.pack(side=RIGHT, fill=BOTH, expand=True)

    fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
    ax.set_title(helpers.a("نمو الاستثمار عبر السنوات"))
    ax.grid(True, linestyle='--', alpha=0.6)

    cvs = FigureCanvasTkAgg(fig, fr_ch)
    cvs.get_tk_widget().pack(fill=BOTH, expand=True)

    win.mainloop()

def do_calc():
    global g_years, g_vals, g_invs, last_data
    
    v = helpers.check_vals(e1.get(), e2.get(), e3.get(), e4.get())
    if v is None:
        messagebox.showerror("Error", helpers.a("الرجاء إدخال أرقام صحيحة وموجبة"))
        return

    ini, mon, rat, yrs = v
    r = rat / 100
    
    g_years = list(range(yrs + 1))
    g_vals = [ini]
    g_invs = [ini]

    cur = ini
    tot = ini

    for i in range(1, yrs + 1):
        for _ in range(12):
            cur += mon
            cur *= (1 + r / 12)
            tot += mon
        g_vals.append(cur)
        g_invs.append(tot)

    ax.clear()
    ax.plot(g_years, g_vals, label='Total Value', color='#2ecc71', linewidth=2)
    ax.fill_between(g_years, g_vals, color='#2ecc71', alpha=0.1)
    ax.plot(g_years, g_invs, label='Principal Invested', color='#3498db', linestyle='--')
    ax.set_title("Investment Growth")
    ax.legend(loc='upper left')
    ax.grid(True)
    fig.tight_layout()
    cvs.draw()

    prof = cur - tot
    txt = f"""
    {helpers.a('ملخص النتائج:')}
    ---------------------------
    {helpers.a('القيمة النهائية:')} ${cur:,.2f}
    {helpers.a('إجمالي المستثمر:')} ${tot:,.2f}
    {helpers.a('إجمالي الأرباح:')} ${prof:,.2f}
    """
    res_lbl.config(text=txt)
    btn_pdf.config(state=NORMAL)
    
    last_data = {
        "y": yrs, "r": rat, "i": tot, "p": prof, "f": cur
    }

def make_pdf():
    p = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not p: return

    try:
        c = canvas.Canvas(p, pagesize=A4)
        w, h = A4

        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.darkblue)
        c.drawString(50, h - 50, "Investment Report")

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.gray)
        c.drawString(50, h - 70, f"Date: {datetime.now()}")
        c.line(50, h - 80, w - 50, h - 80)

        yp = h - 120
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.black)
        c.drawString(50, yp, "Financial Summary:")
        yp -= 30
        
        c.setFont("Helvetica", 12)
        L = [
            f"Duration: {last_data['y']} Years",
            f"Rate: {last_data['r']}%",
            f"Invested: ${last_data['i']:,.2f}",
            f"Interest: ${last_data['p']:,.2f}",
            f"Final: ${last_data['f']:,.2f}"
        ]
        
        for x in L:
            c.drawString(70, yp, f"- {x}")
            yp -= 20

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150)
        buf.seek(0)
        img = ImageReader(buf)
        c.drawImage(img, 50, h - 500, width=500, height=300)

        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.darkgray)
        c.drawString(w/2 - 50, 30, "Generated by Python")
        c.save()
        messagebox.showinfo("OK", helpers.a("تم حفظ ملف PDF بنجاح"))

    except:
        messagebox.showerror("Error", "PDF Error")
