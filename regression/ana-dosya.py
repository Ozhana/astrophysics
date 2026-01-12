import cv2  # Resim analizi için gerekli modül
import numpy as np  # Matematiksel işlemler için gereli modül
import pandas as pd  # Tablo işlemleri için gerekli modül
from tkinter import *  # Arayüz Modülü
from tkinter import filedialog  # Dosya açmak ve kaydetmek için gerekli müdül
import tkinter as tk  # Arayüz Modülü
from tkinter import ttk  # Arayüz Modülü
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Grafik için alan hazırlayan modül
from matplotlib.figure import Figure  # Grafik Modülü
import os

regression_list = ['Hiçbiri', 'Linear', 'Polynomial', 'Sinusoidal']  # Regression yöntemleri listesi
scatter_k = 0  # Dağılım grafiğini temizlemek için sayaç
formula_k = 0  # Formül alanı için Dağılım grafiğini temizlemek için sayaç
box_k = 0  # Box plot grafiğini temizlemek için gerekli sayaç

X = []  # Ana grafik X koordinatları
y = []  # Ana grafik Y koordinatları
X_reg = []  # Regression X koordinatları
y_reg = []  # Regression Y koordinatları

root = Tk()  # Arayüz açılıyor
root.geometry("1201x641")  # Arayüz geometrisi
root['bg'] = 'grey'  # Arayüz arkaplan rengi
root.title("Pınar Akdağ Grafik analizi")
root.propagate(False)  # Arayüzün geometrisinin içindekiler tarafından değiştirilmesini engeller
root.resizable(False, False)  # Arayüz geometrisinin değişmesini engeller

# Arayüz içinde alanlar oluşturuluyor ve her bir alanın adı yazılıyor
file_opening_area = tk.LabelFrame(root, text="Dosya Acma Alanı")
file_opening_area.place(height=50, width=180, relx=0, rely=0)
file_opening_info_area = tk.LabelFrame(root, text="Açılan Dosya")
file_opening_info_area.place(height=100, width=180, relx=0, rely=50/640)
file_saving_area = tk.LabelFrame(root, text="Dosya Saklama Alanı")
file_saving_area.place(height=50, width=180, relx=0, rely=150/640)
file_saving_info_area = tk.LabelFrame(root, text="Saklanan Dosya")
file_saving_info_area.place(height=100, width=180, relx=0, rely=200/640)
slider_area = tk.LabelFrame(root, text="Hassaslik Ayar Alanı")
slider_area.place(height=107, width=180, relx=0, rely=300/640)
control_area = tk.LabelFrame(root, text="control Alanı")
control_area.place(height=153, width=180, relx=0, rely=407/640)
analysis_area = tk.LabelFrame(root, text="Grafik ve Analiz Alanı")
analysis_area.place(height=560, width=600, relx=180/1200, rely=0)
Coordinate_area = tk.LabelFrame(root, text="Koordinatlar")
Coordinate_area.place(height=560, width=130, relx=780/1200, rely=0)
regression_Coordinate_area = tk.LabelFrame(root, text="Regression")
regression_Coordinate_area.place(height=560, width=130, relx=910/1200, rely=0)
formula_area = tk.LabelFrame(root, text="Formül Katsayıları")
formula_area.place(height=230, width=180, relx=1040/1200, rely=0)
main_data_analysis_area = tk.LabelFrame(root, text="Ana Data Analizleri")
main_data_analysis_area.place(height=165, width=160, relx=1040/1200, rely=230/640)
regression_data_analysis_area = tk.LabelFrame(root, text="Regresyon Data Analizleri")
regression_data_analysis_area.place(height=165, width=160, relx=1040/1200, rely=395/640)
formula_printing_area = tk.LabelFrame(root, text="Tam Regresyon Formülü")
formula_printing_area.place(height=80, width=1200, relx=0/1200, rely=560/640)

# Gerekli değişkenler
regresion_option = StringVar()
filename_open = StringVar()
filename_save = StringVar()
max_power = IntVar()
slider_value = IntVar()
regresion_option.set(regression_list[0])  # Regression listesi ilk elemana sabitlendi (Hiçbiri)

# Masaustü yerini "desktop" adlı değişkene atar.
# Masaüstü yerini dosya açmak ve kaydetmek için kullanacağız
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Çıkarılan koordinatlar arayüz içine yazılması için alan hazırlığı
# Ana grafik koordinatları
tree_coordinates = ttk.Treeview(Coordinate_area)
tree_coordinates.place(relheight=1, relwidth=1)
tree_scroll1y = tk.Scrollbar(tree_coordinates, orient="vertical", command=tree_coordinates.yview)
tree_scroll1x = tk.Scrollbar(tree_coordinates, orient="horizontal", command=tree_coordinates.xview)
tree_coordinates.configure(xscrollcommand=tree_scroll1x.set, yscrollcommand=tree_scroll1y.set)
tree_scroll1x.pack(side="bottom", fill="x")
tree_scroll1y.pack(side="right", fill="y")

# Regression grafiği koordinatları
tree_regression = ttk.Treeview(regression_Coordinate_area)
tree_regression.place(relheight=1, relwidth=1)
tree_scroll2y = tk.Scrollbar(tree_regression, orient="vertical", command=tree_regression.yview)
tree_scroll2x = tk.Scrollbar(tree_regression, orient="horizontal", command=tree_regression.xview)
tree_regression.configure(xscrollcommand=tree_scroll2x.set, yscrollcommand=tree_scroll2y.set)
tree_scroll2x.pack(side="bottom", fill="x")
tree_scroll2y.pack(side="right", fill="y")

# Regression alanına küçük bir bilgi notu gerekli
if regresion_option.get() == "Hiçbiri":
    info = Label(formula_area, text="Lütfen bir regresyon yöntemi seçin", width=200,
                 wraplength=150, fg="red", font=('Arial', 14))
    info.pack()

    label_alert = Label(analysis_area, text="")
    label_main_describe = Label(main_data_analysis_area, text="")
    label_reg_describe = Label(regression_data_analysis_area, text="")
    # Dosya açılması için gerekli fonksiyon tanımlanmalı


def browse_files():
    global filename_open
    global label_alert
    global X_reg
    global y_reg
    global label_main_describe
    global label_reg_describe
    X_reg = []
    y_reg = []
    # açılacak dosyanın yerini belirleyip sisteme ileten dialog penceresi
    filename_open = filedialog.askopenfilename(initialdir=desktop,
                                               title="Select a File",
                                               filetypes=(("Resim Dosyaları", "*.jpg*"),
                                                          ("Resim Dosyaları", "*.JPEG*"),
                                                          ("Resim Dosyaları", "*.gif"),
                                                          ("Resim Dosyaları", "*.jpeg*"),
                                                          ("Resim Dosyaları", "*.png*"),
                                                          ("Excel Dosyaları", "*.xls*"),
                                                          ("Text Dosyaları", "*.txt*"),
                                                          ("Tüm Dosyalar", "*.*")))

    # filename_open = filename_open.replace("/", "\\")
    # Eğer dosya adı boş ise yada diyalog penceresi iyi çalışmamışsa diye kontrol etmek gerek
    if not filename_open:
        label_alert.destroy()
        # Eğer resim okunanamışsa yada arıza vermişse Patates Oldu Yazsın
        label_alert = Label(analysis_area, text="Patates oldu", font=('Arial', 30), wraplength=300,
                            fg="red", anchor=CENTER)
    else:
        # Herşey yolunda ise Kaydedilecek alaın seçmesi için uyarı ver
        label_alert.destroy()
        label_alert = Label(analysis_area, text="Lütfen Kaydedilecek yeri seçin", font=('Arial', 30), wraplength=300,
                            fg="red", anchor=CENTER)

    label_file_explorer.configure(text="Açılan Dosya: " + "\n" + filename_open)
    label_alert.pack(side=TOP)
    # save_files()

# Hangi dosyanın ve nereden alındığını ekrana yazmakta fayda var
label_file_explorer = Label(file_opening_info_area, text="Analiz için Lütfen resim Seçin", width=200,
                            wraplength=190, height=10, fg="blue")
label_file_explorer.pack()

# Kayıt fonksiyonu oluşturulmalı
# eğer kayıt yerini biz seçmezsek otomatik olarak kaydetme ayarlanmalı ama bize bir uyarı da vermeli
# Tam otomtik kayıt sıkıntılı olabilir


def save_files():
    global filename_save
    # Kaydedilecek alanın açılması gerekli
    filename_save = filedialog.asksaveasfilename(initialdir=desktop, title="Select a File",
                                                 filetypes=(("Excel Dosyaları", "*.xls*"),
                                                            ("Tüm Dosyalar", "*.*")))
    # Kaydedilece yer ve isim otomatik seçmek in aşağıdaki kod kullanıldı
    if not filename_save:
        filename_save = filename_open
        if filename_save[-4::] == ".jpg":
            filename_save = filename_open[:-4]
        if filename_save[-5::] != ".xlsx":
            filename_save = filename_save + ".xlsx"

    # Eğer kayıt isminde ".xlsx" yoksa ekler varsa tekrarlamaz
    if filename_save[-5::] != ".xlsx":
        filename_save = filename_save + ".xlsx"
    # Kaydedilecek yer yazılırken sağa yatık çizgiyi sola yatık hale getirmek gerek
    # Çünki bazı bilgisayarlada arıa verebiliyor
    filename_save = filename_save.replace("/", "\\")
    label_file_saver.configure(text="Kayıt Yeri: " + "\n" + filename_save)
    label_alert.destroy()
    analyze()


# Dosyanın kaydedildiği yeri ekrana yazdırır
label_file_saver = Label(file_saving_info_area, text="Dosyanın kaydedildiği Yer", width=200,
                         wraplength=175, height=10, fg="blue")
label_file_saver.pack()
# Dağılım grafiği çizmek için bir bir grafik fonksiyonu gerekli


def draw_scatter_graph():
    global scatter_k  # Dağılım grafiğini temizleyebilmek için gerekli olan sayaç
    global X_reg  # Regression için gerekli olan x koordinatları (ana fonksiyon X koordinatları)
    global y_reg  # Regresyondan sonra üretilen Y koordinatları
    global X  # Ana fonksiyon X Koordinatları
    global y  # Ana fonksiyon Y Koordinatları
    global scatter_canvas  # Kanvas açılmalı ki dağılım grafiği içine çizilebilsin
    figure_scatter = Figure(figsize=(4, 2), dpi=100)  # Kanvas ve figür geometrisi
    subplot_scatter = figure_scatter.add_subplot(111)  # Grafik ve yeri

    # Eğer regresiyon yapılmamışsa Y_reg boştur ve eğer y_reg boş ise sadece ana dağılım grafiği çizilie
    # Eğer regresiyon yapılmışsa hem ana dağılım grafiği hem de regresyn grafiği çizilir
    if len(y_reg) != 0:
        subplot_scatter.scatter(X, y, color="#db1d9f", marker=".", s=3)
        subplot_scatter.scatter(X, y_reg, color="#6fb830", marker=".", s=2)
    else:
        subplot_scatter.scatter(X, y, color="#db1d9f", marker=".", s=3)

    scatter_canvas = FigureCanvasTkAgg(figure_scatter, analysis_area)
    scatter_canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)
    scatter_k = scatter_k + 1

    return
# Hem önceki grafiği silmek hem de birden fazzla işlem yapabilmek için bir fonksiyon gerekli


def multi_work_scatter():
    global scatter_k  # Grafiği silmek için gerekli sayaç
    if scatter_k != 0:
        scatter_canvas.get_tk_widget().destroy()  # Grafiği siler
    draw_scatter_graph()
    data_analysis()

# Ana Analiz fonksiyonu


def analyze():
    global filename_open  # Analiz yapıldıktan sonra dataların kayıt edilmesi için gerekli
    global filename_save  # Analiz yapıldıktan sonra dataların kayıt edilmesi için gerekli
    global power_entry  # Gerekli olan x kuvvetini alan değişken
    global X
    global y
    global y_reg
    global dataFrame
    X = []  # Her analiz öncesi mutlaka tüm koordinatlar temizlenmeli aksi halde dağılım grafiği çizilemiyor
    y = []
    y_reg = []

    # Analizi Yapilacak olan resim okunur ve GRİ degeri ayarlanır
    # image = cv2.imread(r'C:\Users\ozhan\Desktop\Pinar Projeler\Star Classification\Tek resim\Resimler\resim1.jpg')
    image = cv2.imread(filename_open)
    # img = io.imread(filename_open)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Eşik değeri ayarlandıç
    # Eşik değero artınca daha hassah olur ve etrafındaki çerçeveyi de alabilir
    # Uygun eşik değeri (Bence) 50 ila 100 arası
    # threshold_level = 200
    threshold_level = slider_value.get()  # Eşik değeri slider dan alınıyor

    # Eşik değerinin altında kalan bölgeler işaretlenir ve koordınatları çıkarılır
    coords = np.column_stack(np.where(gray < threshold_level))

    # X ve Y koordınatlrını excel2e doğru şekilde taşımak için bir dizi gerekli
    for_df = []

    # Koorddınatlardan gelen x ve y değerleri dizilerin içlerine aktarılır
    for i in range(len(coords)):
        X.append(coords[i][1])
        y.append(400 - coords[i][0])
        for_df.append([coords[i][1], 400 - coords[i][0]])

    # Çıkarılan koordinatlar excel'e aktarılmak için tablo halinede düzenlenir
    dataFrame = pd.DataFrame(for_df, columns=["X Values", "Y Values"])

    # Çıkarılan X ve Y koordinatları ekrana aktarılıyor
    
    tree_coordinates["column"] = list(dataFrame.columns)
    tree_coordinates["show"] = "headings"
    for column in tree_coordinates["columns"]:
        tree_coordinates.heading(column, text=column)
        tree_coordinates.column(column, anchor=CENTER)
        tree_coordinates.column(column, minwidth=0, width=10)
    df_rows = dataFrame.to_numpy().tolist()
    for row in df_rows:
        tree_coordinates.insert("", "end", values=row)
    
    # Düzenlenen tablo Excel'e aktarılır
    with pd.ExcelWriter(filename_save) as writer:
        dataFrame.to_excel(writer, sheet_name='Ana datalar')

    # Bu noktadan sonrasi sadece grafiği çizdirip doğru yapıp yapmadığımızın kontrolü içindir
    # Excel'e aktırıldıktan sonra çok da gerekli değil

    # Eşikten altta kalan bölgelerın boyanması için bir maskeleme hazırlanmalı
    mask = gray < threshold_level

    # Maske rengine bu geğerlerle karar verildi ama değişik renkler de güzel durdu (Mesela Turuncu)
    image[mask] = (204, 119, 0)

    multi_work_scatter()

    return


def regression():
    global max_power
    global X
    global y
    global y_reg
    global formula_k
    global formula_coefficients
    global full_formula_coefficients
    global scatter_k
    global dataFrameReg

    y_reg = []
    for_reg_df = []

    info.destroy()
    max_us = 0
    # Eğer regresiyon yöntemi seçilmediyse y=a grafiği çizilmeli
    if regresion_option.get() == "Hiçbiri":
        max_us = 1
    # Linear regresiyon da maximum x kuvveti 1 dir
    elif regresion_option.get() == "Linear":
        max_us = 2
    # Polinomlar için maximum x kuvveti girdiden alınmalı
    elif regresion_option.get() == "Polynomial":
        max_us = max_power.get() + 1
    else:
        # Sinüsoidal grafik sürekli olarak arıza verdiği için bu projede kullanılamadı
        pass

    # max_us = max_power.get() + 1
    cumulative = np.ones((len(y), max_us))  # Sadece 1 lerden oluşan mxk boyutunda bir matriz oluşturuldu

    # Matrix'in elemanları x^n ile değistirildi ki LSM ile katsayılar hesaplanabisin
    # LSM = Least Square Method
    for i in range(len(y)):
        for us in range(max_us):
            if us != 0:
                cumulative[i][us] = X[i] ** us

    # LSM katsayı çözüm yöntemim
    cumulative = np.matrix(np.asarray(cumulative))
    x_mat = np.linalg.inv(cumulative.transpose() @ cumulative) @ cumulative.transpose()
    coefficients = x_mat @ y
    coefficients_array = np.squeeze(np.asarray(coefficients))
    coefficients_array2 = coefficients_array.flatten()
    coefficients_array3 = []
    coefficients_array4 = []  # Ekranın altındaki formül alanı için
    coefficients_array5 = []  # Katsayıların Excel dosyasına kayıtları için

    # Hesaplanan katsayılar hem ekrana yazılması hem de excel e kaydedilmesi için bir fonksiyon gerekli
    for i in range(len(coefficients_array2)):
        coefficients_array3.append("{:.20f}".format(coefficients_array2[i]))
        # Ekrana yazılacaksayılar virgülden sonra 20 basamaklı
        coefficients_array4.append("+"+"("+"{:.20f}".format(coefficients_array2[i])+"x"+str(i)+")")
        # Excel e kayıt edilecek sayılar virgülden sonra 50 basamaklı
        coefficients_array5.append("+" + "(" + "{:.50f}".format(coefficients_array2[i]) + "x^" + str(i) + ")")

    # Her regresiyon sonrası bir önceki formülü ekrandan temizlemek için bir temizleme foksiyonu
    if formula_k != 0:
        formula_coefficients.destroy()
        full_formula_coefficients.destroy()

    formula_coefficients = Label(formula_area, text=coefficients_array3, width=200,
                                 wraplength=150, fg="blue")
    full_formula_coefficients = Label(formula_printing_area, text=coefficients_array4, width=200,
                                      wraplength=1150, fg="red")
    formula_coefficients.pack()
    full_formula_coefficients.pack()
    scatter_k = scatter_k + 1
    formula_k = formula_k + 1

    for i in range(len(X)):
        p = 0
        for us in range(max_us):
            p = p + coefficients_array2[us] * (X[i] ** us)

        y_reg.append(p)

    # Koorddınatlardan gelen x ve y değerleri dizilerin içlerine aktarılır
    for i in range(len(y_reg)):
        for_reg_df.append([X[i], y_reg[i]])
        if i >= len(coefficients_array5):
            coefficients_array5.append(0)

    # Çıkarılan koordinatlar excel'e aktarılmak için tablo halinede düzenlenir
    dataFrameReg = pd.DataFrame(for_reg_df, columns=["X Reg Val", "Y Reg Val"])

    for item in tree_regression.get_children():
        tree_regression.delete(item)

    # Tahmini X ve Y koordinatları ekrana aktarılıyor
    tree_regression["column"] = list(dataFrameReg.columns)
    tree_regression["show"] = "headings"
    for column in tree_regression["columns"]:
        tree_regression.heading(column, text=column)
        tree_regression.column(column, anchor=CENTER)
        tree_regression.column(column, minwidth=0, width=10)
    df_rows_reg = dataFrameReg.to_numpy().tolist()
    for row in df_rows_reg:
        tree_regression.insert("", "end", values=row)

    dataFrameReg['Katsayılar'] = coefficients_array5
    # Oluşturulan herşey excel e kaydedilir
    with pd.ExcelWriter(filename_save, mode='a', if_sheet_exists='replace') as writer:
        dataFrameReg.to_excel(writer, sheet_name=('tahmini datalar' + ' us= ' + str(max_power.get())))

    multi_work_scatter()
    return

# Eğer regresiyon yöntemi polinom ise girdi alanı açılı aksi halde girdi alanı herzaman kapalı kalmalı
# Bu nedenle aşağıdaki fonksiyon yazıldı


def mp(widget):
    if regresion_option.get() == "Polynomial":
        power_entry.pack()
        power_entry.place(x=95, y=35)
        label_max_power.pack()
        label_max_power.place(x=5, y=37)

    else:
        power_entry.pack_forget()
        power_entry.place_forget()
        label_max_power.pack_forget()
        label_max_power.place_forget()


def regression_sinusoidal():
    global max_power
    global X
    global y
    global y_reg
    global formula_k
    global formula_coefficients
    global full_formula_coefficients
    global scatter_k
    global dataFrameReg
    y_reg = []
    for_reg_df = []

    info.destroy()
    cumulative = np.ones((len(X), 3))  # Sadece 1 lerden oluşan mxk boyutunda bir matriks oluşturuldu

    # Matrix'in elemanları x^n ile değistirildi ki LSM ile katsayılar hesaplanabisin
    # LSM = Least Square Method
    for i in range(len(X)):
        cumulative[i][0] = np.sin(np.degrees((2*np.pi/len(X))*X[i]))
        cumulative[i][1] = np.cos(np.degrees((2*np.pi/len(X))*X[i]))

    # LSM katsayı çözüm yöntemim
    cumulative = np.matrix(np.asarray(cumulative))
    x_mat = np.linalg.inv(cumulative.transpose() @ cumulative) @ cumulative.transpose()
    coefficients = x_mat @ y
    coefficients_array = np.squeeze(np.asarray(coefficients))
    coefficients_array = np.asarray(coefficients_array)
    coefficients_array2 = coefficients_array.flatten()
    coefficients_array3 = []
    coefficients_array4 = []  # Ekranın altındaki formül alanı için
    coefficients_array5 = []  # Katsayıların Excel dosyasına kayıtları için

    # Hesaplanan katsayılar hem ekrana yazılması hem de excel e kaydedilmesi için bir fonksiyon gerekli
    for i in range(len(coefficients_array2)):
        # Ekranin sağ tarafındaki katsayı alanı için gerekli kod
        coefficients_array3.append("{:.20f}".format(coefficients_array2[i]))
        # Ekrana yazılacaksayılar virgülden sonra 20 basamaklı
        # coefficients_array4.append("+" + "(" + "{:.20f}".format(coefficients_array2[i]) + "x" + str(i) + ")")
        # Excel e kayıt edilecek sayılar virgülden sonra 50 basamaklı
        coefficients_array5.append("+" + "(" + "{:.50f}".format(coefficients_array2[i]) + "x^" + str(i) + ")")

    # Her regresiyon sonrası bir önceki formülü ekrandan temizlemek için bir temizleme foksiyonu
    if formula_k != 0:
        formula_coefficients.destroy()
        full_formula_coefficients.destroy()

    formula_coefficients = Label(formula_area, text=coefficients_array3, width=200,
                                 wraplength=150, fg="blue")
    sincoef = ("(" + str(coefficients_array2[0]) + "*" + "sin(x)" + ")" + "+" +
               "(" + str(coefficients_array2[1]) + "*" + "cos(x)" + ")" + "+" +
               "(" + str(coefficients_array2[2]) + ")")
    full_formula_coefficients = Label(formula_printing_area, text=sincoef, width=200,
                                      wraplength=1150, fg="red")
    formula_coefficients.pack()
    full_formula_coefficients.pack()
    scatter_k = scatter_k + 1
    formula_k = formula_k + 1

    a = np.sqrt(coefficients_array2[0])**2+(coefficients_array2[1]**2)
    c = np.arcsin(coefficients_array2[0]/a)
    b = (2 * np.pi / len(X))
    d = coefficients_array2[2]

    for i in range(len(X)):
        p = a*np.sin(np.degrees(b*X[i]) + c) + d
        y_reg.append(p)

    # Koorddınatlardan gelen x ve y değerleri dizilerin içlerine aktarılır
    for i in range(len(y_reg)):
        for_reg_df.append([X[i], y_reg[i]])
        if i >= len(coefficients_array5):
            coefficients_array5.append(0)

    # Çıkarılan koordinatlar excel'e aktarılmak için tablo halinede düzenlenir
    dataFrameReg = pd.DataFrame(for_reg_df, columns=["X Reg Val", "Y Reg Val"])
    dataFrameReg['Katsayılar'] = coefficients_array5

    # Oluşturulan herşey excel e kaydedilir
    with pd.ExcelWriter(filename_save, mode='a', if_sheet_exists='replace') as writer:
        dataFrameReg.to_excel(writer, sheet_name=('tahmini datalar' + ' us= ' + str(max_power.get())))

    for item in tree_regression.get_children():
        tree_regression.delete(item)

    # Tahmini X ve Y koordinatları ekrana aktarılıyor

    tree_regression["column"] = list(dataFrameReg.columns)
    tree_regression["show"] = "headings"
    for column in tree_regression["columns"]:
        tree_regression.heading(column, text=column)
        tree_regression.column(column, anchor=CENTER)
        tree_regression.column(column, minwidth=0, width=10)
    df_rows_reg = dataFrameReg.to_numpy().tolist()
    for row in df_rows_reg:
        tree_regression.insert("", "end", values=row)

    multi_work_scatter()
    return


def regression_dir():
    if regresion_option.get() == "Sinusoidal":
        regression_sinusoidal()
    else:
        regression()
    return


def data_analysis():
    global dataFrame
    global dataFrameReg
    global label_main_describe
    global label_reg_describe

    if len(y_reg) == 0:
        label_main_describe.destroy()
        label_main_describe = Label(main_data_analysis_area, text=dataFrame.describe().round(decimals=3))
        label_main_describe.pack()
    else:
        # label_main_describe.destroy()
        label_reg_describe.destroy()
        # label_main_describe = Label(main_data_analysis_area, text=dataFrame.describe().round(decimals=3))
        label_reg_describe = Label(regression_data_analysis_area, text=dataFrameReg.describe().round(decimals=3))
        # label_main_describe.pack()
        label_reg_describe.pack()

    return


file_chooser = Button(file_opening_area, text="Resim Aç", command=browse_files)
file_chooser.place(relx=10, rely=20)
file_chooser.pack()
file_saver = Button(file_saving_area, text="Dataları Kaydet", command=save_files)
file_saver .pack()
analyze_button = Button(control_area, text="Analiz Et", width=15, command=regression_dir, bg="light blue", fg="red",
                        font=('Arial', 12))
analyze_button.pack()
analyze_button.place(x=10, y=65)
exit_button = Button(control_area, text="ÇIKIŞ", width=15, command=root.destroy,
                     bg="RED", fg="white", font=('Arial', 12))
exit_button.pack()
exit_button.place(x=10, y=100)

label_regression = Label(control_area, text="Yöntem :", fg="blue")
label_regression.pack()
label_regression.place(x=5, y=5)
label_max_power = Label(control_area, text="Maximum Üs :", fg="blue")
label_max_power.pack()
label_max_power.place(x=5, y=37)

power_entry = Entry(control_area, textvariable=max_power, bd=5, width=5)
power_entry.pack()

drop_regresion = OptionMenu(control_area, regresion_option, *regression_list, command=mp)
drop_regresion.pack()
drop_regresion.place(x=60, y=0)

Slider = Scale(slider_area, from_=0, to=250, orient=HORIZONTAL, tickinterval=50, variable=slider_value,
               length=170)
Slider.set(175)
Slider.pack()
Slider.place(x=0, y=0)
slider_button = Button(slider_area, text="TAMAM", width=15, command=analyze,
                       bg="blue", fg="white", font=('Arial', 9))
slider_button.pack()
slider_button.place(x=25, y=60)

mp(power_entry)

root.mainloop()
