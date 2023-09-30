from customtkinter import *


def Entry(master, holder, largura, altura):
    return CTkEntry(master, placeholder_text=holder, width=largura, height=altura)

def Frame(master, largura, altura):
    return CTkFrame(master, width=largura, height=altura)

def Label(master, texto, fonte, tamanho, weight):
    return CTkLabel(master, text=texto, font=(fonte,tamanho, weight),)

def fao(sex, idade, peso):
    if sex in 'Mm':
        if idade < 3:
            return 60.9 * peso - 54
        elif 3 <= idade < 10:
            return 22.7 * peso + 495
        elif 10 <= idade < 18:
            return 17.5 * peso + 651
        elif 18 <= idade < 30:
            return 15.3 * peso + 679
        elif 30 <= idade < 60:
            return 11.6 * peso + 879
        elif idade >= 60:
            return 13.5 * peso + 487
    elif sex in 'Ff':
        if idade < 3:
            return 61.0 * peso - 51
        elif 3 <= idade < 10:
            return 22.5 * peso + 499
        elif 10 <= idade < 18:
            return 12.2 * peso + 746
        elif 18 <= idade < 30:
            return 14.7 * peso + 496
        elif 30 <= idade < 60:
            return 8.7 * peso + 829
        elif idade >= 60:
            return 10.5 * peso + 596

def harris(sex, idade, peso, alturacm):
    if sex in 'Mm':
        return 66.47 + (13.75 * peso) + (5.0 * alturacm) - (6.76 * idade)
    elif sex in 'Ff':
        return 655.1 + (9.56 * peso) + (1.85 * alturacm) - (4.68 * idade)


window = CTk()
window.geometry("600x450")
window.title('Calculadora Dietética')
window._apply_appearance_mode('dark')

h1 = Label(window, 'Calculadora Dietética', 'arial bold', 22, 'bold')
h1.pack(padx=15, pady=15)

inputs = Frame(window, 550, 320)
inputs.pack()

#sexo
sex_lab = Label(inputs, 'Sexo:', 'arial bold', 16, 'normal')
sex_lab.place(x=160, y=40)

radio_var = IntVar(value=0)

def radio_event():
    global sex
    v = radio_var.get()

    if v == 1:
        sex = 'M'
    else:
        sex = 'F'
    pass

radio1 = CTkRadioButton(inputs, text='Maculino', command=radio_event, variable=radio_var, value=1)
radio2 = CTkRadioButton(inputs, text='Feminino', command=radio_event, variable=radio_var, value=2)
radio1.place(x=230, y=40)
radio2.place(x=330, y=40)

#idade
age_lab = Label(inputs, 'Idade do paciente:', 'arial bold', 16, 'normal')
age_lab.place(x=135, y=90)

age_entry = Entry(inputs, 'só os números', 110, 30)
age_entry.place(x=270, y=90)

age_anos = Label(inputs, 'anos', 'arial bold', 12, 'normal')
age_anos.place(x=385, y=95)

#altura
altura_lab = Label(inputs, 'Altura do paciente:', 'arial bold', 16, 'normal')
altura_lab.place(x=135, y=140)

altura_entry = Entry(inputs, 'em metros', 110, 30)
altura_entry.place(x=270, y=140)

metro_lab = Label(inputs, 'metros', 'arial bold', 12, 'normal')
metro_lab.place(x=385, y=145)

#peso
peso_lab = Label(inputs, 'Peso do paciente:', 'arial bold', 16, 'normal')
peso_lab.place(x=137, y=190)

peso_entry = Entry(inputs,'em kg', 110, 30)
peso_entry.place(x=270, y=190)

kg_lab = Label(inputs, 'kg', 'arial bold', 12, 'normal')
kg_lab.place(x=385, y=195)

#fator atividade
fa_lab = Label(inputs, 'Fator atividade:', 'arial bold', 16, 'normal')
fa_lab.place(x=155, y=240)

fa_entry = Entry(inputs, 'FA do paciente', 110, 30)
fa_entry.place(x=270, y=240)


#calculo
def bt_onclick():
    global idade_str, altura_str, peso_str, fa_str, alturacm, peso, fa, get_fao, get_harris, resultados

    idade_str = age_entry.get()
    altura_str = altura_entry.get()
    peso_str = peso_entry.get()
    fa_str = fa_entry.get()

    #idade
    idade = int(idade_str)

    #alturaM e alturacm
    if ',' in altura_str:
        altura_str = altura_str.replace(',', '.')
    alturaM = float(altura_str)
    alturacm = alturaM * 100

    #peso
    if ',' in peso_str:
        peso_str = peso_str.replace(',', '.')
    peso = float(peso_str)

    #fator atividade
    if ',' in fa_str:
        fa_str = fa_str.replace(',', '.')
    fa = float(fa_str)
    
    #imc
    imc = peso / (alturaM**2)

    #Taxa de Metabolismo Basal
    if imc >= 27:
        if sex == 'M':
            pi = 22
        elif sex == 'F':
            pi = 21
        pa = (peso - pi) * 0.25 + pi
        
        tmb_fao = fao(sex, idade, pa)
        tmb_harris = harris(sex, idade, pa, alturacm)

    elif imc < 18:
        if sex == 'M':
            pi = 22
        elif sex == 'F':
            pi = 21
        pa = (pi - peso) * 0.25 + peso
        
        tmb_fao = fao(sex, idade, pa)
        tmb_harris = harris(sex, idade, pa, alturacm)

    else:
        pa = peso
        tmb_fao = fao(sex, idade, peso)
        tmb_harris = harris(sex, idade, peso, alturacm)

    #Gasto energético total
    get_fao = tmb_fao * fa
    get_harris = tmb_harris * fa

    #Janela de Resultados
    resultados = CTkToplevel(window)
    resultados.geometry('400x550')
    resultados.title('Resultados')

    #FAO resultados
    fao_output = Frame(resultados, 550, 320)
    fao_output.pack(padx=10, pady=10)

    fao_titulo = Label(fao_output, 'Segundo a FAO/OMS', 'arial bold', 18, 'bold')
    fao_titulo.pack(padx=10, pady=10)

    imc_output = Label(fao_output, f'Índice de Massa Corporal: {imc:.1f}', 'arial bold', 15, 'normal')
    imc_output.pack(padx=10, pady=10)

    tmb_fao_output = Label(fao_output, f'Taxa de Metabolismo Basal: {tmb_fao}', 'arial bold', 15, 'normal')
    tmb_fao_output.pack(padx=10, pady=10)

    get_fao_output = Label(fao_output, f'Gasto energético total: {get_fao}', 'arial bold', 15, 'normal')
    get_fao_output.pack(padx=10, pady=10)

    #Harris Resultados
    harris_output = Frame(resultados, 550, 320)
    harris_output.pack(padx=10, pady=10)

    harris_titulo = Label(harris_output, 'Segundo Harris Bennedict', 'arial bold', 18, 'bold')
    harris_titulo.pack(padx=10, pady=10)

    imc_harris_output = Label(harris_output, f'Índice de Massa Corporal: {imc:.1f}', 'arial bold', 15, 'normal')
    imc_harris_output.pack(padx=10, pady=10)

    tmb_harris_output = Label(harris_output, f'Taxa de Metabolismo Basal: {tmb_harris}', 'arial bold', 15, 'normal')
    tmb_harris_output.pack(padx=10, pady=10)

    get_harris_output = Label(harris_output, f'Gasto Energético Total: {get_harris}', 'arial bold', 15, 'normal')
    get_harris_output.pack(padx=10, pady=10)
    
CTkButton(window, text='CALCULAR', command=bt_onclick, width=95, height=40).pack(padx=15, pady=15)


window.mainloop()

