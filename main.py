#bem vindo ao código do programa de Assistência de Estudos
  
import wolframalpha as wa
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import scrolledtext
import wikipedia as wiki
import wikipediaapi


#inicializando Wolfram e a wikipedia   
client = wa.Client("98WG5H-758TVWLYXX")
wikiapi=wikipediaapi.Wikipedia('en')

  
#inicializando o tk
gui=tk.Tk()
gui.title("Assistente de Estudo") #título
gui.iconbitmap("ufrj.ico") #icone
gui.geometry("700x700") #dimensões


#aplicando o tema pra ficar bonito (tkinter feio demais)
tema=ttk.Style(gui)
gui.tk.call('source','azure-dark.tcl')
tema.theme_use("azure-dark")
tema.configure("TRadiobutton", font=("Terminal",12))


#Criando o frame principal
frame1 = ttk.Frame(gui)
frame1.pack(fill=tk.BOTH, expand=1)


#label com o nome do programa
titulo=ttk.Label(frame1, text="Assistente de Estudo", font=("Javanese Text", 30)).pack(pady=10,padx=140)


#colocando os botões radio na tela
x=tk.IntVar()
x.set("1")
wolframRadio=ttk.Radiobutton(frame1, text="Wolfram Alpha", variable=x, value=1,style="TRadiobutton").pack()
wikiRadio=ttk.Radiobutton(frame1, text="Wikipedia", variable=x, value=2, style="TRadiobutton").pack(pady=10)


#caixa para pegar e armazenar o input
caixa=ttk.Entry(frame1, font=("Consolas", 17), justify=tk.CENTER)
caixa.pack()
caixa.insert(0,"Pergunte Aqui!")


#label com a resposta
respostaAqui=scrolledtext.ScrolledText(frame1, font=12, width=73, wrap="word", bd=0, undo=True)


#função pra pegar a resposta do wolfram ou da wikipedia com o input e colocar na tela
def responder(x):
    if x==1:
        pergunta=client.query(caixa.get())
        resposta = next(pergunta.results).text
        respostaAqui.insert("end", " \n"+resposta)
        
    if x==2:
        resposta= wikiapi.page(wiki.search(caixa.get(), results=1)[0])
        respostaAqui.insert("end",resposta.summary)
        respostaAqui.yview(tk.END)


#botão pra perguntar que executa a função
botao=ttk.Button(frame1,text="Perguntar", command=lambda: responder(x.get())).pack(pady=10)
respostaAqui.pack(anchor="center",padx=(10,0),pady=5)


#código para o menu
menu=tk.Menu(gui)
gui.config(menu=menu)


#funções para o menu, o nome é autoexplicativo
def novo(e):
    respostaAqui.delete("1.0","end")

def abrir(e):
    respostaAqui.delete("1.0","end")
    arquivo=filedialog.askopenfilename(title="Abrir", filetypes=(("Arquivos de Texto","*.txt"), ("Python", "*.py"), ("Todos os Arquivos","*.*")))
    arquivo=open(arquivo,"r")
    texto=arquivo.read()
    respostaAqui.insert("end",texto)
    arquivo.close()

def salvar(e):
    arquivo=filedialog.asksaveasfilename(title="Salvar", defaultextension=".*", filetypes=(("Arquivos de Texto","*.txt"), ("Python", "*.py"), ("Todos os Arquivos","*.*")))
    if arquivo:
        arquivo=open(arquivo,"w")
        arquivo.write(respostaAqui.get(1.0,"end"))
        arquivo.close()

def cortar(e):
    global selecionado
    if e:
        selecionado=gui.clipboard_get()
    else:
        if respostaAqui.selection_get():
            selecionado=respostaAqui.selection_get()
            respostaAqui.delete("sel.first","sel.last")
            gui.clipboard_clear()
            gui.clipboard_append(selecionado)
        
def copiar(e):
    global selecionado
    if e:
        selecionado=gui.clipboard_get()
        
    if respostaAqui.selection_get():
        selecionado=respostaAqui.selection_get()
        gui.clipboard_clear()
        gui.clipboard_append(selecionado)

def colar(e):
    global selecionado
    if e:
        selecionado=gui.clipboard_get()

    else:    
        if selecionado:
            cursor=respostaAqui.index("insert")
            respostaAqui.insert(cursor, selecionado)

def negrito():
    negrito=font.Font(respostaAqui, respostaAqui.cget("font"))
    negrito.configure(weight="bold")
    respostaAqui.tag_configure("negrito", font=negrito)

    fontes=respostaAqui.tag_names("sel.first")

    if "negrito" in fontes:
        respostaAqui.tag_remove("negrito", "sel.first", "sel.last")
    else:
        respostaAqui.tag_add("negrito", "sel.first", "sel.last")

def italico():
    italico=font.Font(respostaAqui, respostaAqui.cget("font"))
    italico.configure(slant="italic")
    respostaAqui.tag_configure("italico", font=italico)

    fontes=respostaAqui.tag_names("sel.first")

    if "italico" in fontes:
        respostaAqui.tag_remove("italico", "sel.first", "sel.last")
    else:
        respostaAqui.tag_add("italico", "sel.first", "sel.last")

def corTexto():
    corEscolhida=colorchooser.askcolor()[1]
    if corEscolhida:
        corFonte=font.Font(respostaAqui, respostaAqui.cget("font"))
        respostaAqui.tag_configure("cor", font=corFonte, foreground=corEscolhida)
        fontes=respostaAqui.tag_names("sel.first")

        if "cor" in fontes:
            respostaAqui.tag_remove("cor", "sel.first", "sel.last")
        else:
            respostaAqui.tag_add("cor", "sel.first", "sel.last")

def corFundo():
    corEscolhida=colorchooser.askcolor()[1]
    if corEscolhida:
        respostaAqui.config(bg=corEscolhida)
    
def mudaIdioma(idioma):
    global wikiapi 
    wikiapi=wikipediaapi.Wikipedia(idioma)
    wiki.set_lang(idioma)
               
#Menu de Arquivos
arquivoMenu=tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Arquivo", menu=arquivoMenu)
arquivoMenu.add_command(label="Novo", command=lambda: novo(False), accelerator="Ctrl+N")
arquivoMenu.add_command(label="Abrir", command=lambda: abrir(False), accelerator="Ctrl+O")
arquivoMenu.add_command(label="Salvar", command=lambda: salvar(False), accelerator="Ctrl+S")
arquivoMenu.add_separator()
arquivoMenu.add_command(label="Sair", command=gui.destroy)


#Menu de Editar
editarMenu=tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Editar", menu=editarMenu)
editarMenu.add_command(label="Recortar", command=lambda: cortar(False), accelerator="Ctrl+X")
editarMenu.add_command(label="Copiar", command=lambda: copiar(False), accelerator="Ctrl+C")
editarMenu.add_command(label="Colar", command=lambda: colar(False), accelerator="Ctrl+V")
editarMenu.add_separator()
editarMenu.add_command(label="Desfazer", command=respostaAqui.edit_undo, accelerator="Ctrl+Z")
editarMenu.add_command(label="Refazer", command=respostaAqui.edit_redo, accelerator="Ctrl+Y")


#Menu Formatar
formatarMenu=tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Formatar", menu=formatarMenu)
formatarMenu.add_command(label="Negrito", command=negrito)
formatarMenu.add_command(label="Itálico", command=italico)
formatarMenu.add_separator()
formatarMenu.add_command(label="Cor do Texto", command=corTexto)
formatarMenu.add_command(label="Cor do Fundo", command=corFundo)

#Menu idioma Wikipedia
idiomaMenu=tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Idioma Wiki", menu=idiomaMenu)
idiomaMenu.add_command(label="Inglês", command=lambda: mudaIdioma('en'))
idiomaMenu.add_command(label="Português", command=lambda: mudaIdioma('pt'))
idiomaMenu.add_command(label="Italiano", command=lambda: mudaIdioma('it'))


#bindings do teclado pro programa
gui.bind("<Control-Key-x>", cortar)
gui.bind("<Control-Key-c>", copiar)
gui.bind("<Control-Key-v>", colar)
gui.bind("<Control-Key-n>", novo)
gui.bind("<Control-Key-o>", abrir)
gui.bind("<Control-Key-s>", salvar)

#loop
gui.mainloop()
