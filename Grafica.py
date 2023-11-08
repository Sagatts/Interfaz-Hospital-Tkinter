from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from email.message import EmailMessage
import smtplib
import Gestion
import ConexionBD
import re

def validar_sesion(frame):              #Inicio de sesion
    dao=ConexionBD.conexionBD()

    validacion=dao.validar_entrada_de_sesion(Usuario_inicio.get(),Contrasena_inicio.get())

    if validacion is not None:
        frame.pack_forget()
        Usuario_inicio.set("")
        Contrasena_inicio.set("")                        
        ventana_principal(frame)
    else:
        messagebox.showerror("Inicio de sesión", "Usuario o contraseña incorrectos")

def regresar(frame1,frame2,frame3,frame4):          #Funcion para regresar
    frame1.pack_forget()
    frame4.pack_forget()
    frame3.pack_forget()
    frame2.pack()

def ventana_principal(frame_inicio):                            #Ventana inicial para acceder a las tablas
    frame_registro=LabelFrame(ventana,text='')          
    frame_registro.pack()

    label_bienvenida = tk.Label(frame_registro, text="¡Inicio de sesión exitoso!")
    label_bienvenida.pack()

    label_opcion = tk.Label(frame_registro, text="Tablas")
    label_opcion.pack()
    #command=lambda se crea una funcion anonima que se ejecutara cuando se active un evento
    btnMedico=Button(frame_registro, text="Tabla personal medico",width=40, height=1, command=lambda: mostrar_registros(1,frame_registro))
    btnMedico.pack()

    btnAdministrativo=Button(frame_registro, text="Tabla personal administrativo",width=40, height=1,command=lambda: mostrar_registros(2,frame_registro))
    btnAdministrativo.pack()

    btnPacientes=Button(frame_registro, text="Tabla pacientes",width=40, height=1, command=lambda: registro_pacientes(frame_registro))
    btnPacientes.pack()
    
    label_opcion = tk.Label(frame_registro, text="Pagos")
    label_opcion.pack()

    btnPagopersonal=Button(frame_registro,text="Pago del personal",width=40,height=1,command=lambda: mostrar_pago_personal(frame_registro))
    btnPagopersonal.pack()

    btnPagopacientes=Button(frame_registro,text="Pago de pacientes",width=40,height=1,command=lambda: mostrar_pago_pacientes(frame_registro))
    btnPagopacientes.pack()

    lregresar=Label(frame_registro,text="Regresar")
    lregresar.pack()

    btnRegresar_Inicio=Button(frame_registro,text="Regresar al inicio",width=40,height=1,command=lambda: regresar_inicio(frame_inicio,frame_registro))
    btnRegresar_Inicio.pack()

#Personal
def limpiar_datos_personal(op):                 #Limpiar los datos cuando se guarde un personal
    Documento_Id.set("")
    Nombre.set("")
    Fecha_ingreso.set("")
    Tipo_prevision.set("")
    Sueldo_bruto.set("")
    Afp.set("")
    if op == 1:
        Especialidad.set("")
        Rol.set("")
    elif op == 2:
        Unidad.set("")

# Validaciones

def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").lower()
    if not re.match(r"^\d{7,8}[k|0-9]$", rut):
        return False

    rut_numero, rut_verificador = rut[:-1], rut[-1]
    dv_calculado = calcular_digito_verificador(rut_numero)
    return dv_calculado == rut_verificador

def calcular_digito_verificador(rut_numero):
    multiplicador = 2
    suma = 0
    for digito in reversed(rut_numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    resto = suma % 11
    dv = 11 - resto
    return "k" if dv == 10 else str(dv)

def validar_letras(texto):
    return re.match(r'^[a-zA-Z\s]+$', texto) is not None

def validar_fecha(fecha):
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
        return False
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    # Convertir la fecha en una lista de valores enteros [año, mes, día]
    fecha_lista = [int(i) for i in fecha.split('-')]

    # Verificar que el año no sea mayor que el año actual
    if fecha_lista[0] > fecha_actual.year:
        return False

    # Verificar que el mes no sea mayor que 12
    if fecha_lista[1] > 12:
        return False

    # Verificar que el día no sea mayor que 30
    if fecha_lista[2] > 30:
        return False

    return True

def validar_sueldo(sueldo):
    # Verificar que el sueldo sea un número positivo
    try:
        sueldo_float = float(sueldo)
        return sueldo_float >= 0
    except ValueError:
        return False

def validar_datos(op,Personal: Gestion.Personas):
    if not validar_rut(Personal.get_documento_id()):
        messagebox.showerror("Error", "RUT inválido.")
        return False
    if not validar_letras(Personal.get_nombre()):
        messagebox.showerror("Error", "Nombre inválido, solo letras.")
        return False
    if not validar_fecha(Personal.get_fecha()):
        messagebox.showerror("Error", "Fecha de ingreso inválida formato yyyy-mm-dd.")
        return False
    if Personal.get_prevision()  is not None and Personal.get_prevision()=='':
        messagebox.showerror("Error", "El tipo de prevision no puede estar vacía.")
        return False
    if op==1 or op==2:
        if validar_sueldo_bruto(Personal)==False:
            return False
    if op==1:
        if validar_especialidad(Personal)==False:
            return False
    elif op==2:
        if validar_unidad(Personal)==False:
            return False
    if op==1 or op==2:
        if validar_afp(Personal)==False:
            return False
    if op==3:
        if validar_paciente(Personal)==False:
            return False

    return True

def validar_especialidad(Medico: Gestion.Medicos):
    if Medico.get_especialidad() is not None and Medico.get_especialidad() == '':
        messagebox.showerror("Error", "Especialidad no puede estar vacía.")
        return False
    
def validar_unidad(Administrativo: Gestion.Administrativos):
    if Administrativo.get_unidad() is not None and Administrativo.get_unidad()=='':
        messagebox.showerror("Error","Unidad no puede estar vacia")
        return False
    
def validar_sueldo_bruto(Personal: Gestion.Personal):
    if not validar_sueldo(Personal.get_sueldo()):
        messagebox.showerror("Error", "Sueldo bruto inválido, solo numeros.")
        return False
    
def validar_afp(Personal: Gestion.Personal):
    if Personal.get_afp() is not None and Personal.get_afp()=='':
        messagebox.showerror("Error", "Afp no puede estar vacía.")
        return False
    
def validar_paciente(Paciente: Gestion.Pacientes):
    if not validar_letras(Paciente.get_motivo()):
        messagebox.showerror("Error","Motivo invalido, solo letras.")
        return False
    if Paciente.get_derivacion() is not None and Paciente.get_derivacion()=='':
        messagebox.showerror("Error","La derivacion no tiene que estar vacia.")
        return False
    if Paciente.get_derivacion()=="Urgencia":
        if Paciente.get_box() is not None and Paciente.get_box()=='':
            messagebox.showerror("Error","El box no debe estar vacio.")
            return False
    elif Paciente.get_derivacion()=="Consulta medica":
        if Paciente.get_medico() is not None and Paciente.get_medico()=='':
            messagebox.showerror("Error","Medico no puede estar vacio.")
            return False
    if Paciente.get_hospitalizacion() is not None and Paciente.get_hospitalizacion()=='':
        messagebox.showerror("Error","Hospitalizacion no puede estar vacia.")
        return False
    elif Paciente.get_hospitalizacion()=="Si":
        if Paciente.get_dias() is not None and Paciente.get_dias()=='':
            messagebox.showerror("Error","Los dias no tienen que estar vacios")
            return False

#Mostrar los datos personal

def seleccionarDato(event,tree,documento,Nombre,Fecha,prevision,Sueldo,Rool,Spec,Afp_):
    item = tree.identify("item", event.x, event.y)
    documento.set(tree.item(item, "text"))
    Nombre.set(tree.item(item, "values")[0])
    Fecha.set(tree.item(item, "values")[1])
    prevision.set(tree.item(item, "values")[2])
    Sueldo.set(tree.item(item, "values")[3])
    Rool.set(tree.item(item, "values")[4])
    Spec.set(tree.item(item, "values")[5])
    Afp_.set(tree.item(item, "values")[6])

def cambio_de_rol(*args):                                   #Cambia el frame dependiendo si es Medico o Tens
    Especialidades = ['Pediatria', 'Anestesiologia', 'Cardiologia', 'Gastroenterologia', 'Medicina General', 'Ginecologia y obstetricia']
    opcion1_especialidades = tk.OptionMenu(frame_tabla, Especialidad, *Especialidades)
    lespecialidad = Label(frame_tabla, text="Especialidad :")

    Areas = ['Consultas externa', 'Emergencia', 'Pediatria', 'Quirofano', 'Hospitalizacion', 'Recuperacion UCI']
    opcion1_areas = tk.OptionMenu(frame_tabla, Especialidad, *Areas)
    larea = Label(frame_tabla, text="Area :")

    opcion1_especialidades.grid(row=6, column=2, sticky="ew")
    lespecialidad.grid(row=6, column=1, sticky="w")
    opcion1_areas.grid(row=6, column=2, sticky="ew")
    larea.grid(row=6, column=1, sticky="w")


    if Rol.get() == 'Medico':
        Especialidad.set("")
        opcion1_especialidades.grid(row=6, column=2, sticky="ew")
        lespecialidad.grid(row=6, column=1, sticky="ew")

        opcion1_areas.grid_remove()
        larea.grid_remove()

    if Rol.get() == 'Tens':
        Especialidad.set("")
        opcion1_areas.grid(row=6, column=2, sticky="ew")
        larea.grid(row=6, column=1, sticky="ew")
        
        opcion1_especialidades.grid_remove()
        lespecialidad.grid_remove()

def pago_personal(op,Sueldo_bru,Es_afp,fecha):              #Calcula el sueldo liquido para guardarlo en la BD
    Sueldo = float(Sueldo_bru)
    if op==1:
        Tiempo_sevicio=obtener_tiempo_servicio_mostrar(fecha)
    elif op==2:
        Tiempo_sevicio=obtener_tiempo_servicio_mostrar(fecha)

    if Es_afp=="Si":        #Afp descuento de 10%
        Sueldo=Sueldo*0.9
    if op==1:               #Area de salud descuento 7%
        Sueldo=Sueldo*0.93
    if Tiempo_sevicio>20:   #Lleva 20 años prestando servicios
        Sueldo=Sueldo*1.05
    if Tiempo_sevicio>30:   #Lleva 30 años prestando servicios
        Sueldo=Sueldo*1.07
    if op==1:               #Medico o Tens aumento 5%
        Sueldo=Sueldo*1.05
    if op == 2:             #Administrativo 3%
        Sueldo=Sueldo*1.03

    return Sueldo

def mostrar_resultado(op,Sueldo_bru,Es_afp,fecha):           #Muestra el sueldo_liquido calculado
    if validar_fecha(fecha)==False:
        messagebox.showinfo("Error","Rellene la casilla de fecha en el formato yyyy-mm-dd")
    elif Sueldo_bru=='' or validar_sueldo(Sueldo_bru)==False:
        messagebox.showinfo("Error","Rellene la casilla de Sueldo con numeros para el calculo")
    elif Es_afp=='':
        messagebox.showinfo("Error","Rellene la parte de Afp para el calculo")
    else:
        Sueldo = float(Sueldo_bru)
        Tiempo_servicio=obtener_tiempo_servicio_mostrar(fecha)

        if Es_afp=="Si":        #Afp descuento de 10%
            Sueldo=Sueldo*0.9
        if op==1:               #Area de salud descuento 7%
            Sueldo=Sueldo*0.93
        if Tiempo_servicio>20:   #Lleva 20 años prestando servicios
            Sueldo=Sueldo*1.05
        if Tiempo_servicio>30:   #Lleva 30 años prestando servicios
            Sueldo=Sueldo*1.07
        if op==1:               #Medico o Tens aumento 5%
            Sueldo=Sueldo*1.05
        if op == 2:             #Administrativo 3%
            Sueldo=Sueldo*1.03

        Sueldo=int(Sueldo)

        lmayor_de_20=Label(frame_tabla3,text="20 años prestando servicios Aumento 5%")
        lmayor_de_20.grid(row=4,column=0,sticky="w")
        if Tiempo_servicio>20:
            lmayor_de_20_cumple=Label(frame_tabla3,text="Si")
            lmayor_de_20_cumple.grid(row=4,column=1,sticky="ew")
        elif Tiempo_servicio<=20:
            lmayor_de_20_cumple=Label(frame_tabla3,text="No")
            lmayor_de_20_cumple.grid(row=4,column=1,sticky="ew")

        lmayor_de_30=Label(frame_tabla3,text="30 años prestando servicios Aumento 7%")
        lmayor_de_30.grid(row=5,column=0,sticky="ew")
        if Tiempo_servicio>30:
            lmayor_de_30_cumple=Label(frame_tabla3,text="Si")
            lmayor_de_30_cumple.grid(row=5,column=1,sticky="ew")
        elif Tiempo_servicio<=30:
            lmayor_de_30_cumple=Label(frame_tabla3,text="No")
            lmayor_de_30_cumple.grid(row=5,column=1,sticky="ew")

        lSueldo_liquido=Label(frame_tabla3,text=Sueldo)
        lSueldo_liquido.grid(row=10,column=1,sticky="ew")

def obtener_tiempo_servicio_mostrar(fecha):                 #Calcular el tiempo de servicio
    fecha_actual=datetime.now().date()
    fecha_ingresada=datetime.strptime(fecha,'%Y-%m-%d').date()

    diferencia=fecha_actual.year-fecha_ingresada.year
    if fecha_actual.month < fecha_ingresada.month or (fecha_actual.month == fecha_ingresada.month and fecha_actual.day < fecha_ingresada.day):
        diferencia-=1

    return diferencia

def mostrar_calculadora(op):                                #Muestra lo que cumple para calcular el sueldo_liquido
    lCumple=Label(frame_tabla3,text="Cumple?")
    lCumple.grid(row=0,column=1)

    lSalud=Label(frame_tabla3,text="Area Salud Descuento 10%:")
    lSalud.grid(row=2,column=0,sticky="w")
    if op==1:
        lrespuesta=Label(frame_tabla3,text="Si")
    else:
        lrespuesta=Label(frame_tabla3,text="No")
    lrespuesta.grid(row=2,column=1)
    
    lAdministrativo=Label(frame_tabla3,text="Administrativo Aumento 3%:")
    lAdministrativo.grid(row=3,column=0,sticky="w")
    if op==1:
        lrespuesta2=Label(frame_tabla3,text="No")
    else:
        lrespuesta2=Label(frame_tabla3,text="Si")
    lrespuesta2.grid(row=3,column=1)

    lMedico=Label(frame_tabla3,text="Medico o Tens Aumento 5%:")
    lMedico.grid(row=6,column=0,sticky="w")
    if op==1:
        lrespuesta2=Label(frame_tabla3,text="Si")
    else:
        lrespuesta2=Label(frame_tabla3,text="No")
    lrespuesta2.grid(row=6,column=1)
    
    btnCalcular=Button(frame_tabla3,text="Calcular Sueldo Liquido",command=lambda: mostrar_resultado(op,Sueldo_bruto.get(),Afp.get(),Fecha_ingreso.get()))
    btnCalcular.grid(row=10,column=0,sticky="ew")

def mostrar_registros(op,frame_registro):                  #Grafica del personal
    frame_registro.pack_forget()
    if op==1:
        texto='Personal Medico'
    elif op==2:
        texto='Personal Administrativa'

    global frame_tabla
    frame_tabla=LabelFrame(ventana, text=texto)
    frame_tabla.pack()

    global frame_tabla3
    frame_tabla3=LabelFrame(ventana,text='Calculadora')
    frame_tabla3.pack()

    frame_tabla2=LabelFrame(ventana, text=texto)
    frame_tabla2.pack()

    global Documento_Id,Nombre,Fecha_ingreso,Tipo_prevision,Afp,Especialidad

    Documento_Id = StringVar()
    Nombre = StringVar()
    Fecha_ingreso = StringVar()
    Tipo_prevision = StringVar()
    Afp=StringVar()
    Especialidad = StringVar()

    Tipos_de_prevision=['Fonasa','Isapre','Particular']
    Respuestas=['Si','No']

    tree = ttk.Treeview(frame_tabla2,height=15, columns=('#0','#1', '#2', '#3', '#4', '#5','#6','#7'))
    tree.grid(row=10, column=10)
    tree.column('#0', width=100)
    tree.heading('#0', text="Rut", anchor=CENTER)
    tree.column('#1', width=100)
    tree.heading('#1', text="Nombre", anchor=CENTER)
    tree.column('#2', width=100)
    tree.heading('#2', text="Fecha de ingreso", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Tipo de prevision", anchor=CENTER)
    tree.column('#5', width=75)
    tree.heading('#5', text="Rol", anchor=CENTER)

    ldocumento=Label(frame_tabla, text="RUT :")
    ldocumento.grid(row=0,column=1,sticky="w")
    etdocumento=Entry(frame_tabla, textvariable=Documento_Id, width=40)
    etdocumento.grid(row=0,column=2,sticky="w")

    lnombre=Label(frame_tabla, text="Nombre :")
    lnombre.grid(row=1,column=1,sticky="w")
    etNombre=Entry(frame_tabla, textvariable=Nombre, width=40)
    etNombre.grid(row=1,column=2,sticky="w")

    lFecha=Label(frame_tabla, text="Fecha de ingreso :")
    lFecha.grid(row=2,column=1,sticky="w")
    etFecha=Entry(frame_tabla, textvariable=Fecha_ingreso, width=40)
    etFecha.grid(row=2,column=2,sticky="w")

    lnombre=Label(frame_tabla, text="Tipo de prevision :")
    lnombre.grid(row=3,column=1,sticky="w")
    menuprevision=tk.OptionMenu(frame_tabla,Tipo_prevision,*Tipos_de_prevision)
    menuprevision.grid(row=3,column=2,sticky="ew")

    lAfp=Label(frame_tabla,text="Afp: ")
    lAfp.grid(row=8,column=1,sticky="w")
    menuAFP=tk.OptionMenu(frame_tabla,Afp,*Respuestas)
    menuAFP.grid(row=8,column=2,sticky="w")

    global Sueldo_bruto
    Sueldo_bruto=StringVar()

    lsueldo=Label(frame_tabla, text="Sueldo bruto :")
    lsueldo.grid(row=4,column=1,sticky="w")
    etsueldo=Entry(frame_tabla, textvariable=Sueldo_bruto, width=40)
    etsueldo.grid(row=4,column=2,sticky="w")

    if op==1:
        global Rol
        Rol=StringVar()
        Roles=['Medico','Tens']

        lroles=Label(frame_tabla,text="Rol :")
        lroles.grid(row=5,column=1,sticky="w")
        opcion_roles=tk.OptionMenu(frame_tabla,Rol,*Roles)
        opcion_roles.grid(row=5,column=2,sticky="w")

        tree.column('#4', width=100)
        tree.heading('#4', text="Sueldo Bruto", anchor=CENTER)
        tree.column('#6', width=200)
        tree.heading('#6', text="Especialidad o Area", anchor=CENTER)
        tree.column('#7', width=75)
        tree.heading('#7', text="Afp", anchor=CENTER)

        mostrar_calculadora(op)
        Rol.trace("w",cambio_de_rol)

        tabla="personal_medico"
        btnGuardar=Button(frame_tabla, text="Guardar", command=lambda: guardar(1,Documento_Id.get(),Nombre.get(),Fecha_ingreso.get(),Tipo_prevision.get(),Sueldo_bruto.get(),Rol.get(),Especialidad.get(),Afp.get()))
        btnBuscar=Button(frame_tabla, text="Buscar", command=lambda: buscar(1,tree))
        btnBorrar=Button(frame_tabla, text="Borrar", command=lambda: eliminar_personal_grafica(tabla))
        btnActualizar=Button(frame_tabla, text="Modificar", command=lambda: actualizar(tabla))
        tree.bind("<Double-1>", lambda event: seleccionarDato(event, tree, Documento_Id, Nombre, Fecha_ingreso, Tipo_prevision,Sueldo_bruto,Rol,Especialidad,Afp))

    elif op==2:
        global Unidad
        Unidad=StringVar()

        Unidades=['Unidad de servicios generales','Unidad de personal','Unidad de Jefatura']

        opcion2_unidades=tk.OptionMenu(frame_tabla,Unidad,*Unidades)
        opcion2_unidades.grid(row=5,column=2,sticky="ew")

        lsueldo=Label(frame_tabla, text="Sueldo bruto :")
        lsueldo.grid(row=4,column=1,sticky="w")
        etsueldo=Entry(frame_tabla, textvariable=Sueldo_bruto, width=40)
        etsueldo.grid(row=4,column=2,sticky="w")

        lUnidad=Label(frame_tabla, text="Unidad administrativa :")
        lUnidad.grid(row=5,column=1,sticky="w")
        
        mostrar_calculadora(op)

        tree.column('#4', width=100)
        tree.heading('#4', text="Sueldo Bruto", anchor=CENTER)
        tree.column('#6', width=200)
        tree.heading('#6', text="Unidad administrativa", anchor=CENTER)
        tree.column('#7', width=100)
        tree.heading('#7', text="Afp", anchor=CENTER)

        tabla="personal_administrativo"
        btnGuardar=Button(frame_tabla, text="Guardar", command=lambda: guardar(2,Documento_Id.get(),Nombre.get(),Fecha_ingreso.get(),Tipo_prevision.get(),Sueldo_bruto.get(),"Administrativo",Unidad.get(),Afp.get()))
        btnBuscar=Button(frame_tabla, text="Buscar", command=lambda: buscar(2,tree))
        btnBorrar=Button(frame_tabla, text="Borrar", command=lambda: eliminar_personal_grafica(tabla))
        btnActualizar=Button(frame_tabla, text="Modificar", command=lambda: actualizar(tabla))
        tree.bind("<Double-1>", lambda event: seleccionarDato(event, tree, Documento_Id, Nombre, Fecha_ingreso, Tipo_prevision,Sueldo_bruto,Unidad))

    btnGuardar.grid(row=0, column=4,sticky="ew")        #row=fila y column=columna y sticky="ew" hace que expanda el rectangulo del boton
    btnBuscar.grid(row=1, column=4,sticky="ew")
    btnBorrar.grid(row=2, column=4,sticky="ew")
    btnActualizar.grid(row=3, column=4,sticky="ew")

    btnAtras=Button(frame_tabla,text="Regresar",command=lambda: regresar(frame_tabla,frame_registro,frame_tabla2,frame_tabla3))
    btnAtras.grid(row=5,column=4,sticky="ew")

def guardar(op,id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp):         #Registra al personal
    dao=ConexionBD.conexionBD()
    if op==1:
        Medico=Gestion.Medicos(id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp)
        if validar_datos(op,Medico)==True:
            dao.validar_id(op,Medico)
            limpiar_datos_personal(op)
    elif op==2:
        Administrativo=Gestion.Administrativos(id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp)
        if validar_datos(op,Administrativo)==True:
            dao.validar_id(op,Administrativo)
            limpiar_datos_personal(op)

def buscar(op,treee):                       #Actualizar la tabla del personal
    dao=ConexionBD.conexionBD()
    if op==1:
        texto="personal_medico"
        dao.mostrar_tabla(texto,treee)
    elif op==2:
        texto="personal_administrativo"
        dao.mostrar_tabla(texto,treee)

def eliminar_personal_grafica(tabla_para_buscar):           #Grafica para eliminar un personal
    ventana_eliminar=tk.Toplevel()
    ventana_eliminar.title("Eliminar un personal")
    ventana_eliminar.geometry("400x300")

    ID_buscar=StringVar()
    dao=ConexionBD.conexionBD()

    frame_pedir_id=LabelFrame(ventana_eliminar,text="Ingresar el Rut para eliminar los datos")
    frame_pedir_id.pack()

    lPedir_ID=Label(frame_pedir_id, text="Ingrese el Rut :")
    lPedir_ID.grid(row=1,column=1)
    etPedir_ID=Entry(frame_pedir_id, textvariable=ID_buscar, width=40)
    etPedir_ID.grid(row=1,column=2)

    btnConfirmar=Button(frame_pedir_id,text="Confirmar",command=lambda: dao.eliminar_personal(tabla_para_buscar,ID_buscar.get(),ventana_eliminar))
    btnConfirmar.grid(row=2,column=2)

    ventana_eliminar.mainloop()
    
def modificar(op,id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp2,ventana_actu):             #Funcion modificar datos del personal
    dao=ConexionBD.conexionBD() 
    if op==1:
        Salud=Gestion.Medicos(id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp2)
        if validar_datos(op,Salud)==True:
            dao.modificar_medico(Salud)
            ventana_actu.destroy()
    elif op==2:
        Admin=Gestion.Administrativos(id,nombre,fecha,tipo_prevision,atributo1,roll,atributo2,afp2)
        if validar_datos(op,Admin)==True:
            dao.modificar_administrativo(Admin)
            ventana_actu.destroy()

def mostrar_datos_id(op,rut,frame_pedir,ventana_actualizar):    #Grafica para modificar el personal
    frame_pedir.pack_forget()
    global frame_cambio
    frame_cambio=LabelFrame(ventana_actualizar,text="Modificar")
    frame_cambio.pack(padx=20,pady=20)
    dao=ConexionBD.conexionBD()

    if op==1:
        resultado=dao.conseguir_datos_personal(rut)
    elif op==2:
        resultado=dao.conseguir_datos_personal_administrativo(rut)

    Nombre2 = StringVar()
    Fecha_ingreso2 = StringVar()
    Tipo_prevision2 = StringVar()
    Tipos_de_prevision2=['Fonasa','Isapre','Particular']
    Sueldo_bruto2=StringVar()
    Afp_cambio=StringVar()
    Respuestas=['Si','No']
    
    Nombre2.set(resultado[1])
    Fecha_ingreso2.set(resultado[2])
    Tipo_prevision2.set(resultado[3])
    Sueldo_bruto2.set(resultado[4])
    Afp_cambio.set(resultado[7])
    
    lnombre=Label(frame_cambio, text="Nombre :")
    lnombre.grid(row=2,column=1)
    etNombre=Entry(frame_cambio, textvariable=Nombre2, width=40)
    etNombre.grid(row=2,column=2)

    lnombre=Label(frame_cambio, text="Fecha de ingreso :")
    lnombre.grid(row=3,column=1)
    etNombre=Entry(frame_cambio, textvariable=Fecha_ingreso2, width=40)
    etNombre.grid(row=3,column=2)

    lnombre=Label(frame_cambio, text="Tipo de prevision :")
    lnombre.grid(row=4,column=1)
    menuprevision=tk.OptionMenu(frame_cambio,Tipo_prevision2,*Tipos_de_prevision2)
    menuprevision.grid(row=4,column=2,sticky="ew")

    lAfp=Label(frame_cambio,text="Afp: ")
    lAfp.grid(row=8,column=1,sticky="w")
    menuAFP=tk.OptionMenu(frame_cambio,Afp_cambio,*Respuestas)
    menuAFP.grid(row=8,column=2,sticky="w")

    lsueldo=Label(frame_cambio, text="Sueldo bruto :")
    lsueldo.grid(row=5,column=1)
    etsueldo=Entry(frame_cambio, textvariable=Sueldo_bruto2, width=40)
    etsueldo.grid(row=5,column=2)

    if op==1:
        global Rol2
        Rol2=StringVar()
        Roles=['Medico','Tens']

        Rol2.set(resultado[5])

        lroles=Label(frame_cambio,text="Rol :")
        lroles.grid(row=6,column=1)
        opcion_roles=tk.OptionMenu(frame_cambio,Rol2,*Roles)
        opcion_roles.grid(row=6,column=2,sticky="w")

        global Especialidad2
        Especialidad2 = StringVar()
        Especialidades = ['Pediatria', 'Anestesiologia', 'Cardiologia', 'Gastroenterologia', 'Medicina General', 'Ginecologia y obstetricia']
        opcion1_especialidades = tk.OptionMenu(frame_cambio, Especialidad2, *Especialidades)
        lespecialidad = Label(frame_cambio, text="Especialidad :")
        
        Areas = ['Consultas externa', 'Emergencia', 'Pediatria', 'Quirofano', 'Hospitalizacion', 'Recuperacion UCI']
        opcion1_areas = tk.OptionMenu(frame_cambio, Especialidad2, *Areas)
        larea = Label(frame_cambio, text="Area :")

        if Rol2.get()=="Medico":
            Especialidad2.set(resultado[6])
            opcion1_especialidades.grid(row=7, column=2, sticky="ew")
            lespecialidad.grid(row=7, column=1,sticky="ew")

            opcion1_areas.grid_remove()
            larea.grid_remove()

        elif Rol2.get()=="Tens":
            Especialidad2.set(resultado[6])
            opcion1_areas.grid(row=7, column=2, sticky="ew")
            larea.grid(row=7, column=1,sticky="ew")

            opcion1_especialidades.grid_remove()
            lespecialidad.grid_remove()

        Rol2.trace("w",cambio_de_rol2)

        btnAceptar=Button(frame_cambio, text="Aceptar", command=lambda: modificar(1,rut,Nombre2.get(),Fecha_ingreso2.get(),Tipo_prevision2.get(),Sueldo_bruto2.get(),Rol2.get(),Especialidad2.get(),Afp_cambio.get(),ventana_actualizar))

    elif op==2:
        Unidad=StringVar()
        Unidades=['Unidad de servicios generales','Unidad de personal','Unidad de Jefatura']

        Unidad.set(resultado[6])

        opcion2_unidades=tk.OptionMenu(frame_cambio,Unidad,*Unidades)
        opcion2_unidades.grid(row=6,column=2,sticky="ew")

        lUnidad=Label(frame_cambio, text="Unidad administrativa :")
        lUnidad.grid(row=6,column=1)

        btnAceptar=Button(frame_cambio, text="Aceptar", command=lambda: modificar(2,rut,Nombre2.get(),Fecha_ingreso2.get(),Tipo_prevision2.get(),Sueldo_bruto2.get(),"Administrativo",Unidad.get(),Afp_cambio.get(),ventana_actualizar))

    btnAceptar.grid(row=9,column=1)

def cambio_de_rol2(*args):              
    Especialidades = ['Pediatria', 'Anestesiologia', 'Cardiologia', 'Gastroenterologia', 'Medicina General', 'Ginecologia y obstetricia']
    opcion1_especialidades = tk.OptionMenu(frame_cambio, Especialidad2, *Especialidades)
    lespecialidad = Label(frame_cambio, text="Especialidad :")
    
    Areas = ['Consultas externa', 'Emergencia', 'Pediatria', 'Quirofano', 'Hospitalizacion', 'Recuperacion UCI']
    opcion1_areas = tk.OptionMenu(frame_cambio, Especialidad2, *Areas)
    larea = Label(frame_cambio, text="Area :")

    if Rol2.get()=="Medico":
        Especialidad2.set("")
        opcion1_especialidades.grid(row=7, column=2, sticky="ew")
        lespecialidad.grid(row=7, column=1,sticky="ew")

        opcion1_areas.grid_remove()
        larea.grid_remove()

    elif Rol2.get()=="Tens":
        Especialidad2.set("")
        opcion1_areas.grid(row=7, column=2, sticky="ew")
        larea.grid(row=7, column=1,sticky="ew")

        opcion1_especialidades.grid_remove()
        lespecialidad.grid_remove()

def mostrar_pago_personal(frame_registro):          #Interfaz para pagar el personal
    frame_registro.pack_forget()
    dao=ConexionBD.conexionBD()
    
    ID=StringVar()

    frame_pago2=LabelFrame(ventana,text='Pagar')
    frame_pago2.pack()

    frame_pago1=LabelFrame(ventana,text='Tabla del personal')
    frame_pago1.pack()

    dao.mostrar_fondos_hospital(frame_pago2,1)

    tree = ttk.Treeview(frame_pago1,height=30, columns=('#0','#1', '#2', '#3','#4'))
    tree.grid(row=10, column=10)
    tree.column('#0', width=100)
    tree.heading('#0', text="Rut", anchor=CENTER)
    tree.column('#1', width=100)
    tree.heading('#1', text="Nombre", anchor=CENTER)
    tree.column('#2', width=100)
    tree.heading('#2', text="Fecha de ingreso", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Sueldo liquido", anchor=CENTER)
    tree.column('#4', width=100)
    tree.heading('#4', text="Pagado", anchor=CENTER)

    lingresar_id=Label(frame_pago2,text='Ingresar Rut para pagar: ')
    lingresar_id.grid(row=0,column=0)

    etIngresar_id=Entry(frame_pago2,textvariable=ID)
    etIngresar_id.grid(row=0,column=1)

    btnatras=Button(frame_pago2,text='Regresar',command=lambda: regresar_pago(frame_registro,frame_pago1,frame_pago2))
    btnatras.grid(row=1,column=0,sticky="ew")

    lFondos=Label(frame_pago2,text="Fondos disponibles:")
    lFondos.grid(row=0,column=3,sticky="ew")


    lpagar=Button(frame_pago2,text='Pagar',command=lambda: dao.pagar_personal(ID.get(),frame_pago2))
    lpagar.grid(row=1,column=1,sticky="ew")

    btnActualizar=Button(frame_pago2,text='Actualizar tabla',command=lambda: dao.actualizar_tabla_personal(tree))
    btnActualizar.grid(row=1,column=2)

#Interfaz para modificar

def actualizar(tabla_buscar):
    ventana_actualizar=tk.Toplevel()                #crea una ventana secundaria
    ventana_actualizar.title("Modificar datos")
    ventana_actualizar.geometry("400x300")

    ID_buscar=StringVar()
    dao=ConexionBD.conexionBD()

    frame_pedir_id=LabelFrame(ventana_actualizar,text="Ingresar Rut para modificar los datos")
    frame_pedir_id.pack()

    lPedir_ID=Label(frame_pedir_id, text="Ingrese el Rut :")
    lPedir_ID.grid(row=1,column=1)
    etPedir_ID=Entry(frame_pedir_id, textvariable=ID_buscar, width=40)
    etPedir_ID.grid(row=1,column=2)

    btnConfirmar=Button(frame_pedir_id,text="Confirmar",command=lambda: dao.buscar_tabla(ID_buscar.get(),frame_pedir_id,ventana_actualizar,tabla_buscar))
    btnConfirmar.grid(row=2,column=2)

    ventana_actualizar.mainloop()

#PACIENTES-----------------------------------------------------------------------------------------------------------------------------

def seleccionarDatoPacientes(event,tree,documento,Nombre,Fecha,prevision,atributo1,atributo2):
    item = tree.identify("item", event.x, event.y)
    documento.set(tree.item(item, "text"))
    Nombre.set(tree.item(item, "values")[0])
    Fecha.set(tree.item(item, "values")[1])
    prevision.set(tree.item(item, "values")[2])
    atributo1.set(tree.item(item, "values")[3])
    atributo2.set(tree.item(item, "values")[4])

def tipo_de_derivacion(*arg):
    dao=ConexionBD.conexionBD()

    Lista_medicos=dao.obtener_medicos()
    N_box=['1','2','3','4','5']

    opcion_box=tk.OptionMenu(frame_tablaP,Box,*N_box)
    lBox=Label(frame_tablaP,text="Box:")
    
    opcion_medico=tk.OptionMenu(frame_tablaP,Medico_P,*Lista_medicos)
    lMedico=Label(frame_tablaP,text="Medico que atiende:")

    global Especialidad_P
    Especialidad_P=StringVar()

    def seleccionar_medico(event):
        # Obtener el índice seleccionado en el menú del médico
        index = Medico_P.get()

        # Obtener el nombre y la especialidad del médico seleccionado
        nombre_medico, especialidad_medico = Lista_medicos[index]

        # Actualizar la variable de control del médico y su especialidad
        Medico_P.set(nombre_medico)
        Especialidad_P.set(especialidad_medico)
    
    if Derivacion.get()=="Urgencia":
        lBox.grid(row=6,column=1,sticky="ew")
        opcion_box.grid(row=6,column=2,sticky="ew")
        Especialidad_P.set("")

        lMedico.grid_remove()
        opcion_medico.grid_remove()

    elif Derivacion.get()=="Consulta medica":
        Box.set("")
        opcion_medico.grid(row=6,column=2,sticky="ew")
        lMedico.grid(row=6,column=1,sticky="ew")

        lBox.grid_remove()
        opcion_box.grid_remove()

def Cuantos_dias(*arg):
    lDias=Label(frame_tablaP,text="Dias :")
    EtDias=Entry(frame_tablaP,textvariable=Dias,width=40)

    lNada=Label(frame_tablaP,text="")
    lNada2=Label(frame_tablaP,text="")

    if Hospitalizacion.get()=="Si":
        lDias.grid(row=8,column=1,sticky="ew")
        EtDias.grid(row=8,column=2,sticky="ew")

        lNada.grid_forget()

    elif Hospitalizacion.get()=="No":
        lNada.grid(row=8,column=1,sticky="ew")
        lNada2.grid(row=8,column=2,sticky="ew")

        lDias.grid_forget()
        EtDias.grid_forget()

def registro_pacientes(frame_registro):
    frame_registro.pack_forget()
    global frame_tablaP
    frame_tablaP=LabelFrame(ventana, text="Pacientes")
    frame_tablaP.pack()

    global frame_tabla3
    frame_tabla3=LabelFrame(ventana,text='Calculadora')
    frame_tabla3.pack()

    frame_tabla2=LabelFrame(ventana, text="Pacientes")
    frame_tabla2.pack()

    global Derivacion, Hospitalizacion, Dias, Box, Medico_P
    Box=StringVar()
    Medico_P=StringVar()
    Dias=StringVar()

    Documento_Id = StringVar()
    Nombre = StringVar()
    Fecha_ingreso = StringVar()
    Tipo_prevision = StringVar()
    Motivo_ingreso=StringVar()
    Derivacion=StringVar()
    Hospitalizacion=StringVar()
    
    Tipos_de_prevision=['Fonasa','Isapre','Particular']
    Derivaciones=['Consulta medica','Urgencia']
    Respuestas=['Si','No']

    tree = ttk.Treeview(frame_tabla2,height=15, columns=('#0','#1', '#2', '#3', '#4', '#5','#6','#7','#8'))
    tree.grid(row=10, column=10)
    tree.column('#0', width=100)
    tree.heading('#0', text="Rut", anchor=CENTER)
    tree.column('#1', width=100)
    tree.heading('#1', text="Nombre", anchor=CENTER)
    tree.column('#2', width=100)
    tree.heading('#2', text="Fecha de ingreso", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Tipo de prevision", anchor=CENTER)
    tree.column('#4', width=200)
    tree.heading('#4', text="Motivo de ingreso", anchor=CENTER)
    tree.column('#5', width=100)
    tree.heading('#5', text="Derivacion", anchor=CENTER)
    tree.column('#6',width=100)
    tree.heading('#6',text="Box",anchor=CENTER)
    tree.column('#7',width=200)
    tree.heading('#7',text='Medico y Especialidad',anchor=CENTER)

    ldocumento=Label(frame_tablaP, text="RUT :")
    ldocumento.grid(row=0,column=1,sticky="w")
    etdocumento=Entry(frame_tablaP, textvariable=Documento_Id, width=40)
    etdocumento.grid(row=0,column=2,sticky="w")

    lnombre=Label(frame_tablaP, text="Nombre :")
    lnombre.grid(row=1,column=1,sticky="w")
    etNombre=Entry(frame_tablaP, textvariable=Nombre, width=40)
    etNombre.grid(row=1,column=2,sticky="w")

    lnombre=Label(frame_tablaP, text="Fecha de ingreso :")
    lnombre.grid(row=2,column=1,sticky="w")
    etNombre=Entry(frame_tablaP, textvariable=Fecha_ingreso, width=40)
    etNombre.grid(row=2,column=2,sticky="w")

    lnombre=Label(frame_tablaP, text="Tipo de prevision :")
    lnombre.grid(row=3,column=1,sticky="w")
    menuprevision=tk.OptionMenu(frame_tablaP,Tipo_prevision,*Tipos_de_prevision)
    menuprevision.grid(row=3,column=2,sticky="ew")

    lMotivo_ingreso=Label(frame_tablaP, text="Motivo de ingreso :")
    lMotivo_ingreso.grid(row=4,column=1,sticky="w")
    etMotivo_ingreso=Entry(frame_tablaP, textvariable=Motivo_ingreso, width=40)
    etMotivo_ingreso.grid(row=4,column=2,sticky="w")
            
    opcion3_derivaciones=tk.OptionMenu(frame_tablaP,Derivacion,*Derivaciones)
    opcion3_derivaciones.grid(row=5,column=2,sticky="ew")
    lDerivacion=Label(frame_tablaP, text="Derivacion :")
    lDerivacion.grid(row=5,column=1,sticky="w")

    opcion_hospitalizacion=tk.OptionMenu(frame_tablaP,Hospitalizacion,*Respuestas)
    opcion_hospitalizacion.grid(row=7,column=2,sticky="ew")
    lHospitalizacion=Label(frame_tablaP,text="Hospitalizacion :")
    lHospitalizacion.grid(row=7,column=1,sticky="w")

    Derivacion.trace("w",tipo_de_derivacion)
    Hospitalizacion.trace("w",Cuantos_dias)

    tabla="pacientes"
    btnGuardar=Button(frame_tablaP, text="Guardar", command=lambda: guardar_pacientes(Documento_Id.get(),Nombre.get(),Fecha_ingreso.get(),Tipo_prevision.get(),Motivo_ingreso.get(),Derivacion.get(),Box.get(),Medico_P.get(),Hospitalizacion.get(),Dias.get(),Especialidad_P.get()))
    btnBuscar=Button(frame_tablaP, text="Buscar", command=lambda: buscar_pacientes(tree))
    btnBorrar=Button(frame_tablaP, text="Borrar", command=lambda: eliminar_paciente_grafica(tabla))
    btnActualizar=Button(frame_tablaP, text="Modificar", command=lambda: actualizar(tabla))
    tree.bind("<Double-1>", lambda event: seleccionarDatoPacientes(event, tree, Documento_Id, Nombre, Fecha_ingreso, Tipo_prevision,Motivo_ingreso,Derivacion,Box,Medico_P))

    btnGuardar.grid(row=0, column=4,sticky="ew")        #row=fila y column=columna y sticky="ew" hace que expanda el rectangulo del boton
    btnBuscar.grid(row=1, column=4,sticky="ew")
    btnBorrar.grid(row=2, column=4,sticky="ew")
    btnActualizar.grid(row=3, column=4,sticky="ew")

    btnAtras=Button(frame_tablaP,text="Regresar",command=lambda: regresar(frame_tablaP,frame_registro,frame_tabla2,frame_tabla3))
    btnAtras.grid(row=4,column=4,sticky="ew")

def guardar_pacientes(id,nombre,fecha,tipo_prevision,motivo,derivacion,_box,_medico,_hospitalizacion,dias,spec_p):
    dao=ConexionBD.conexionBD()
    if _hospitalizacion=="No":
        dias=0
    paciente=Gestion.Pacientes(id,nombre,fecha,tipo_prevision,motivo,derivacion,_box,_medico,_hospitalizacion,dias,spec_p)
    if validar_datos(3,paciente)==True:
        dao.validar_paciente(paciente)
        

def buscar_pacientes(treee):
    dao=ConexionBD.conexionBD()
    dao.mostrar_pacientes(treee)

def eliminar_paciente_grafica(tabla_para_buscar):
    ventana_eliminar=tk.Toplevel()
    ventana_eliminar.title("Eliminar un personal")
    ventana_eliminar.geometry("400x300")

    ID_buscar=StringVar()
    dao=ConexionBD.conexionBD()

    frame_pedir_id=LabelFrame(ventana_eliminar,text="Ingresar el Rut para eliminar los datos")
    frame_pedir_id.pack()

    lPedir_ID=Label(frame_pedir_id, text="Ingrese el Rut :")
    lPedir_ID.grid(row=1,column=1)
    etPedir_ID=Entry(frame_pedir_id, textvariable=ID_buscar, width=40)
    etPedir_ID.grid(row=1,column=2)

    btnConfirmar=Button(frame_pedir_id,text="Confirmar",command=lambda: dao.eliminar_paciente_bd(ID_buscar.get(),ventana_eliminar))
    btnConfirmar.grid(row=2,column=2)

    ventana_eliminar.mainloop()

def modificar_paciente(rut_p,nombre_p,fecha_p,prevision_p,motivo_p,derivacion_p,box_p,medico_p,hospita_p,Dias_p,ventana_actualizar):
    dao=ConexionBD.conexionBD()
    if Dias_p=="":
        Dias_p=0
    Actu_paciente=Gestion.Pacientes(rut_p,nombre_p,fecha_p,prevision_p,motivo_p,derivacion_p,box_p,medico_p,hospita_p,Dias_p)
    if validar_datos(3,Actu_paciente)==True:
        dao.modificar_paciente(Actu_paciente,Dias_p)
        ventana_actualizar.destroy()

def tipo_de_derivacion2(*arg):
    dao=ConexionBD.conexionBD()

    Lista_medicos=dao.obtener_medicos()
    N_box=['1','2','3','4','5']

    opcion_box=tk.OptionMenu(frame_cambio2,Box2,*N_box)
    lBox=Label(frame_cambio2,text="Box:")
    
    opcion_medico=tk.OptionMenu(frame_cambio2,Medico_P2,*Lista_medicos)
    lMedico=Label(frame_cambio2,text="Medico que atiende:")
    
    if Derivacion2.get()=="Urgencia":
        lBox.grid(row=7,column=1,sticky="ew")
        opcion_box.grid(row=7,column=2,sticky="ew")

        lMedico.grid_remove()
        opcion_medico.grid_remove()

    elif Derivacion2.get()=="Consulta medica":
        opcion_medico.grid(row=7,column=2,sticky="ew")
        lMedico.grid(row=7,column=1,sticky="ew")

        lBox.grid_remove()
        opcion_box.grid_remove()

def Cuantos_dias2(*arg):
    lDias=Label(frame_cambio2,text="Dias :")
    EtDias=Entry(frame_cambio2,textvariable=Dias2,width=40)

    lNada=Label(frame_cambio2,text="")
    lNada2=Label(frame_cambio2,text="")

    if Hospitalizacion2.get()=="Si":
        lDias.grid(row=9,column=1,sticky="w")
        EtDias.grid(row=9,column=2,sticky="w")

    elif Hospitalizacion2.get()=="No":
        lNada.grid(row=9,column=1,sticky="ew")
        lNada2.grid(row=9,column=2,sticky="ew")

        lDias.grid_forget()
        EtDias.grid_forget()

def mostrar_datos_id_pacientes(rut,frame_pedir,ventana_actualizar):    #Grafica para modificar el personal
    frame_pedir.pack_forget()
    global frame_cambio2
    frame_cambio2=LabelFrame(ventana_actualizar,text="Modificar")
    frame_cambio2.pack(padx=20,pady=20)
    dao=ConexionBD.conexionBD()

    global Derivacion2,Hospitalizacion2,Dias2,Box2, Medico_P2
    Box2=StringVar()
    Medico_P2=StringVar()
    Dias2=StringVar()

    resultado_paciente=dao.conseguir_datos_personal_paciente(rut)

    NombreP = StringVar()
    Fecha_ingresoP = StringVar()
    Tipo_previsionP = StringVar()
    Motivo_ingresoP=StringVar()
    Derivacion2=StringVar()
    Hospitalizacion2=StringVar()

    NombreP.set(resultado_paciente[1])
    Fecha_ingresoP.set(resultado_paciente[2])
    Tipo_previsionP.set(resultado_paciente[3])
    Motivo_ingresoP.set(resultado_paciente[4])
    Derivacion2.set(resultado_paciente[5])
    
    Tipos_de_prevision=['Fonasa','Isapre','Particular']
    Derivaciones=['Consulta medica','Urgencia']
    Respuestas=['Si','No']
    
    lnombre=Label(frame_cambio2, text="Nombre :")
    lnombre.grid(row=2,column=1)
    etNombre=Entry(frame_cambio2, textvariable=NombreP, width=40)
    etNombre.grid(row=2,column=2)

    lnombre=Label(frame_cambio2, text="Fecha de ingreso :")
    lnombre.grid(row=3,column=1)
    etNombre=Entry(frame_cambio2, textvariable=Fecha_ingresoP, width=40)
    etNombre.grid(row=3,column=2)

    lnombre=Label(frame_cambio2, text="Tipo de prevision :")
    lnombre.grid(row=4,column=1)
    menuprevision=tk.OptionMenu(frame_cambio2,Tipo_previsionP,*Tipos_de_prevision)
    menuprevision.grid(row=4,column=2,sticky="ew")

    lMotivo_ingreso=Label(frame_cambio2, text="Motivo de ingreso :")
    lMotivo_ingreso.grid(row=5,column=1,sticky="w")
    etMotivo_ingreso=Entry(frame_cambio2, textvariable=Motivo_ingresoP, width=40)
    etMotivo_ingreso.grid(row=5,column=2,sticky="w")
            
    opcion3_derivaciones=tk.OptionMenu(frame_cambio2,Derivacion2,*Derivaciones)
    opcion3_derivaciones.grid(row=6,column=2,sticky="ew")
    lDerivacion=Label(frame_cambio2, text="Derivacion :")
    lDerivacion.grid(row=6,column=1,sticky="w")

    opcion_hospitalizacion=tk.OptionMenu(frame_cambio2,Hospitalizacion2,*Respuestas)
    opcion_hospitalizacion.grid(row=8,column=2,sticky="ew")
    lHospitalizacion2=Label(frame_cambio2,text="Hospitalizacion :")
    lHospitalizacion2.grid(row=8,column=1,sticky="w")

    Lista_medicos=dao.obtener_medicos()
    N_box=['1','2','3','4','5']

    opcion_box=tk.OptionMenu(frame_cambio2,Box2,*N_box)
    lBox=Label(frame_cambio2,text="Box:")
    
    opcion_medico=tk.OptionMenu(frame_cambio2,Medico_P2,*Lista_medicos)
    lMedico=Label(frame_cambio2,text="Medico que atiende:")
    
    if Derivacion2.get()=="Urgencia":
        Box2.set(resultado_paciente[6])
        lBox.grid(row=7,column=1,sticky="ew")
        opcion_box.grid(row=7,column=2,sticky="ew")

        lMedico.grid_remove()
        opcion_medico.grid_remove()

    elif Derivacion2.get()=="Consulta medica":
        Medico_P2.set(resultado_paciente[7])
        opcion_medico.grid(row=7,column=2,sticky="ew")
        lMedico.grid(row=7,column=1,sticky="ew")

        lBox.grid_remove()
        opcion_box.grid_remove()

    lDias=Label(frame_cambio2,text="Dias :")
    EtDias=Entry(frame_cambio2,textvariable=Dias2,width=40)

    if Hospitalizacion2.get()=="Si":
        lDias.grid(row=9,column=1,sticky="w")
        EtDias.grid(row=9,column=2,sticky="w")

    elif Hospitalizacion2.get()=="No":
        lDias.grid_forget()
        EtDias.grid_forget()

    Derivacion2.trace("w",tipo_de_derivacion2)
    Hospitalizacion2.trace("w",Cuantos_dias2)

    btnAceptar=Button(frame_cambio2, text="Aceptar", command=lambda: modificar_paciente(rut,NombreP.get(),Fecha_ingresoP.get(),Tipo_previsionP.get(),Motivo_ingresoP.get(),Derivacion2.get(),Box2.get(),Medico_P2.get(),Hospitalizacion2.get(),Dias2.get(),ventana_actualizar))
    btnAceptar.grid(row=10,column=1)

def regresar_pago(frame1,frame2,frame3):
    frame2.pack_forget()
    frame3.pack_forget()
    frame1.pack()

def mostrar_pago_pacientes(frame_registro):
    frame_registro.pack_forget()
    dao=ConexionBD.conexionBD()
    
    ID=StringVar()

    frame_pago2=LabelFrame(ventana,text='Pagar')
    frame_pago2.pack()

    frame_pago1=LabelFrame(ventana,text='Tabla de los pacientes')
    frame_pago1.pack()

    tree = ttk.Treeview(frame_pago1,height=30, columns=('#0','#1', '#2', '#3','#4','#5','#6','#7'))
    tree.grid(row=10, column=10)
    tree.column('#0', width=100)
    tree.heading('#0', text="Rut", anchor=CENTER)
    tree.column('#1', width=100)
    tree.heading('#1', text="Nombre", anchor=CENTER)
    tree.column('#2', width=100)
    tree.heading('#2', text="Tipo_de_prevision", anchor=CENTER)
    tree.column('#3', width=100)
    tree.heading('#3', text="Derivacion", anchor=CENTER)
    tree.column('#4', width=100)
    tree.heading('#4', text="Hospitalizacion", anchor=CENTER)
    tree.column('#5', width=100)
    tree.heading('#5', text="Dias en cama", anchor=CENTER)
    tree.column('#6',width=100)
    tree.heading('#6',text="Dinero_a_pagar",anchor=CENTER)
    tree.column('#7',width=100)
    tree.heading('#7',text="Pagado",anchor=CENTER)

    lingresar_id=Label(frame_pago2,text='Ingresar ID para pagar: ')
    lingresar_id.grid(row=0,column=0)

    etIngresar_id=Entry(frame_pago2,textvariable=ID)
    etIngresar_id.grid(row=0,column=1)

    btnatras=Button(frame_pago2,text='Regresar',command=lambda: regresar_pago(frame_registro,frame_pago1,frame_pago2))
    btnatras.grid(row=1,column=0,sticky="ew")

    lpagar=Button(frame_pago2,text='Pagar',command=lambda: dao.pagar_pacientes(ID.get()))
    lpagar.grid(row=1,column=1,sticky="ew")

    btnActualizar=Button(frame_pago2,text='Actualizar tabla',command=lambda: dao.actualizar_tabla_pacientes(tree))
    btnActualizar.grid(row=1,column=2)

def obtener_dinero_a_pagar(Tipo_derivacion,Tipo_prevision,Hospitalizacion,Dias):
    Dinero_pagar=float()
    Dias_P=int(Dias)
    Dinero_pagar=0

    if Tipo_derivacion=="Consulta medica":
        Dinero_pagar=Dinero_pagar+20000
    if Tipo_derivacion=="Urgencia":
        Dinero_pagar=Dinero_pagar+35000
    if Hospitalizacion=="Si" and Dias_P>0:
        Dinero_pagar=Dinero_pagar+(Dias_P*25000)
    if Tipo_prevision=="Fonasa":
        Dinero_pagar=Dinero_pagar*0.75
    if Tipo_derivacion=="Isapre":
        Dinero_pagar=Dinero_pagar*0.8

    return Dinero_pagar

#Funcion principal
def validar_registro_usuario(U: Gestion.Usuarios):
    if U.get_usuario()=='':
        messagebox.showerror("Error","Rellene la casilla de usuario")
        return False
    elif U.get_contrasena()=='':
        messagebox.showerror("Error","Rellene la casilla de contraseña")
        return False
    elif U.get_corre()=="":
        messagebox.showerror("Error","Rellene la casilla del correo")
        return False
    return True

def registrar_usuario(User,contra,correo,frame_ini,frame_fini):
    dao=ConexionBD.conexionBD()
    Usuario=Gestion.Usuarios(User,contra,correo)
    if validar_registro_usuario(Usuario)==True:
        if enviar_correo_verificacion(Usuario.get_corre())==True:
            dao.validar_usuario(Usuario,frame_ini,frame_fini)
        else:
            pass

def enviar_correo_verificacion(correo):
    remitente="fernandotrujillo123455@gmail.com"
    mensaje = "Hola,\n\nGracias por registrarte en nuestro sitio. Tu cuenta ha sido creada exitosamente.\n\n¡Bienvenido!\n\nAtentamente,\nEl equipo del Hospital San Jose del Carmen"

    try:
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = correo
        email["Subject"] = "Validacion de correo"
        email.set_content(mensaje)

        # Conexión con el servidor SMTP de tu proveedor de correo electrónico
        smtp=smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(remitente,"gcnigmwyofbzzuen")
        smtp.sendmail(remitente,correo,email.as_string())
        messagebox.showinfo("Bienvenido","Se ha enviado un mensaje a tu correo.")
        smtp.quit()
        return True
    except Exception as e:
        messagebox.showinfo("Error",f"Error {e}")

def registro_de_cuentas(frame_inicion_s):
    frame_inicion_s.pack_forget()
    frame_registro_cuenta=LabelFrame(ventana,text='Registro de cuenta')
    frame_registro_cuenta.pack()

    Usuario=StringVar()
    Contrasena=StringVar()
    Correo=StringVar()

    lUsuario=Label(frame_registro_cuenta,text="Usuario")
    lUsuario.grid(row=0,column=0)
    etUsuario=Entry(frame_registro_cuenta,textvariable=Usuario,width=40)
    etUsuario.grid(row=0,column=1)

    lContrasena=Label(frame_registro_cuenta,text="Contraseña")
    lContrasena.grid(row=1,column=0)
    etContrasena=Entry(frame_registro_cuenta,textvariable=Contrasena,width=40)
    etContrasena.grid(row=1,column=1)

    lCorreo=Label(frame_registro_cuenta,text="Correo")
    lCorreo.grid(row=2,column=0)
    etCorreo=Entry(frame_registro_cuenta,textvariable=Correo,width=40)
    etCorreo.grid(row=2,column=1)

    btnConfirmar=Button(frame_registro_cuenta,text="Confirmar",command=lambda: registrar_usuario(Usuario.get(),Contrasena.get(),Correo.get(),frame_inicion_s,frame_registro_cuenta))
    btnConfirmar.grid(row=3,column=1)

    btnAtras=Button(frame_registro_cuenta,text="Atras",command=lambda: regresar_inicio(frame_inicion_s,frame_registro_cuenta))
    btnAtras.grid(row=3,column=0)

def regresar_inicio(frame_1,frame_2):
    frame_2.pack_forget()
    frame_1.pack()

def main():
    global ventana
    ventana = tk.Tk()
    ventana.title("Gestion de Hospital")
    ventana.geometry("1180x720")
    frame_inicio=LabelFrame(ventana,text='Bienvenido al Hospital San Jose del Carmen de Copiapo')
    frame_inicio.pack()

    global Usuario_inicio, Contrasena_inicio
    Usuario_inicio=StringVar()
    Contrasena_inicio=StringVar()

    # Etiqueta de usuario
    label_usuario = tk.Label(frame_inicio, text="Usuario:")
    label_usuario.pack()

    entry_usuario = tk.Entry(frame_inicio,textvariable=Usuario_inicio,width=30)
    entry_usuario.pack()

    # Etiqueta de contraseña
    label_contraseña = tk.Label(frame_inicio, text="Contraseña:")
    label_contraseña.pack()

    entry_contraseña = tk.Entry(frame_inicio, show="*",textvariable=Contrasena_inicio,width=30)
    entry_contraseña.pack()

    # Botón de inicio de sesión
    boton_iniciar_sesion = tk.Button(frame_inicio, text="Iniciar sesión", command=lambda: validar_sesion(frame_inicio))
    boton_iniciar_sesion.pack()

    boton_registrar = tk.Button(frame_inicio, text="Registrarse", command=lambda: registro_de_cuentas(frame_inicio))
    boton_registrar.pack()

    ventana.mainloop()

if __name__=="__main__":
    main()