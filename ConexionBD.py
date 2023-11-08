import pymysql
import Gestion
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import Grafica

class conexionBD():
    def __init__(self):
        self.connection=None
        self.cursor=None

    def conectar(self):
        try:
            self.connection=pymysql.connect(
                host='localhost',
			    user='root',
			    password='Fernandomike123',
			    db='hospital'
            )
            self.cursor=self.connection.cursor()
            print("Conexion exitosa")
        except pymysql.Error as e:
            print(f"Error al conectar:{e}")

    def cerrar(self):
        self.connection.commit()
        self.connection.close()

    def validar_id(self,op, objeto_persona: Gestion.Personal):
        self.conectar()
        valor=objeto_persona.get_documento_id()
        self.cursor.execute("SELECT * FROM personal_medico WHERE Rut=%s",(valor,))
        resultado=self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM personal_administrativo WHERE Rut=%s",(valor,))
        resultado2=self.cursor.fetchone()
        if resultado is None and resultado2 is None:
            if op==1:
                self.registrar_medico(objeto_persona)
            elif op==2:
                self.registrar_administrativo(objeto_persona)
        else:
            messagebox.showwarning("Error","Ya esta registrado")
    
    def insertar_pago(self,op, b: Gestion.Personal):
        Sueldo_liquido=Grafica.pago_personal(op,b.get_sueldo(),b.get_afp(),b.get_fecha())
        sql="INSERT INTO pago_personal (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Sueldo_liquido`,`Pagado`) VALUES(%s,%s,%s,%s,%s)"
        values=(b.get_documento_id(),b.get_nombre(),b.get_fecha(),Sueldo_liquido,"No")
        self.cursor.execute(sql,values)
        messagebox.showinfo("Exito","Se registro con exito!")
        self.cerrar()

    def registrar_medico(self, a: Gestion.Medicos):
        self.conectar()
        sql = "INSERT INTO personal_medico (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Sueldo_bruto`,`Rol`, `Especialidad_o_Area`,`Afp`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (a.get_documento_id(),a.get_nombre(),a.get_fecha(),a.get_prevision(),a.get_sueldo(),a.get_rol(),a.get_especialidad(),a.get_afp())
        self.cursor.execute(sql,values)
        self.connection.commit()
        self.insertar_pago(1,a)

    def registrar_administrativo(self, a: Gestion.Administrativos):
        self.conectar()
        sql = "INSERT INTO personal_administrativo (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Sueldo_bruto`,`Rol`, `Unidad_administrativa`,`Afp`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (a.get_documento_id(),a.get_nombre(),a.get_fecha(),a.get_prevision(),a.get_sueldo(),a.get_rol(),a.get_unidad(),a.get_afp())
        self.cursor.execute(sql,values)
        self.insertar_pago(2,a)

    def buscar_tabla(self,id,frame,ventana,tabla):
        self.conectar()
        self.cursor.execute("SELECT * FROM "+tabla+" WHERE Rut=%s",(id,))
        resultado=self.cursor.fetchone()
        if resultado is None:
            messagebox.showwarning("Error","No se encontro ese Rut")
        else:
            if tabla=="personal_medico":
                Grafica.mostrar_datos_id(1,id,frame,ventana)
            elif tabla=="personal_administrativo":
                Grafica.mostrar_datos_id(2,id,frame,ventana)
            elif tabla=="pacientes":
                Grafica.mostrar_datos_id_pacientes(id,frame,ventana)

    def mostrar_tabla(self,tabla,tree):
        self.conectar()
        registros=tree.get_children() 
        for elemento in registros: 
            tree.delete(elemento)
        try:
            sql='SELECT * FROM '+tabla
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        except Exception as e:
            pass

    def actualizar_tabla_personal(self,treee):
        self.conectar()
        registros=treee.get_children() 
        for elemento in registros: 
            treee.delete(elemento)
        try:
            sql='SELECT * FROM pago_personal'
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                treee.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4]))
        except Exception as e:
            pass

    def mostrar_fondos_hospital(self,frame,id):
        self.conectar()
        self.cursor.execute("SELECT Fondos FROM fondos WHERE id=%s",(id,))
        Fondos=self.cursor.fetchone()[0]
        ldinero=Label(frame,text=Fondos)
        ldinero.grid(row=1,column=3,sticky="ew")
        self.cerrar()

    def pagar_personal(self,ID,frame_pago2):
        self.conectar()
        self.cursor.execute("SELECT * FROM pago_personal WHERE Rut=%s",(ID,))
        resultado=self.cursor.fetchone()
        if resultado is None:
            messagebox.showwarning("Error","No se encontro ese Rut")
        else:
            self.cursor.execute("SELECT Pagado FROM pago_personal WHERE Rut=%s",(ID,))
            Pagado=self.cursor.fetchone()[0]
            if Pagado=="Si":
                messagebox.showinfo("Pagado","Al personal ya se le pago")
            else:
                self.cursor.execute("SELECT Sueldo_liquido FROM pago_personal WHERE Rut=%s",(ID,))
                sueldo_liquido=self.cursor.fetchone()[0]
                self.cursor.execute("UPDATE `pago_personal` SET `Pagado` = 'Si' WHERE `pago_personal`.`Rut`=%s",(ID,))
                self.cursor.execute("SELECT Fondos FROM fondos WHERE id=%s",(1,))
                Fondos=self.cursor.fetchone()[0]
                if sueldo_liquido>Fondos:
                    messagebox.showinfo("Insuficiente","Los fondos son insuficientes")
                else:
                    Fondos=Fondos-sueldo_liquido
                    ldinero=Label(frame_pago2,text=Fondos)
                    ldinero.grid(row=1,column=3,sticky="ew")
                    self.cursor.execute("UPDATE `fondos` SET `Fondos`=%s WHERE `fondos`.`id`=%s",(Fondos,1,))
                    self.cerrar()

    def eliminar_personal(self, tabla, rut ,ventana):
        self.conectar()
        try:
            if messagebox.askyesno(message="¿Esta seguro que desea ELIMINAR...?", title="Precaución"):
                sql = "DELETE FROM " + tabla + " WHERE Rut=%s"
                self.cursor.execute(sql, (rut,))
                self.connection.commit()
                if self.cursor.rowcount > 0:  # Verificar si se eliminaron filas
                    self.cursor.execute("DELETE FROM pago_personal WHERE Rut=%s", (rut,))
                    self.connection.commit()
                    messagebox.showinfo("Exito", "Se eliminó con éxito!")
                    ventana.destroy()
                else:
                    messagebox.showinfo("Error", "No se encontró el Rut")
        except Exception as e:
            messagebox.showwarning("Error", "No se eliminaron datos...")
            pass
        
    def modificar_medico(self, Medico: Gestion.Medicos):
        self.conectar()
        try:
            values = (Medico.get_nombre(),Medico.get_fecha(),Medico.get_prevision(),Medico.get_sueldo(),Medico.get_rol(),Medico.get_especialidad(),Medico.get_afp(),Medico.get_documento_id())
            sql = "UPDATE personal_medico SET Nombre=%s, `Fecha_de_ingreso`=%s, `Tipo_de_prevision`=%s, `Sueldo_bruto`=%s, `Rol`=%s, `Especialidad_o_Area`=%s, `Afp`=%s WHERE Rut=%s"
            self.cursor.execute(sql,values)
            self.actualizar_pago(1,Medico)
        except Exception as e:
            messagebox.showwarning("Error", "No se actualizaron los datos...")
            pass

    def modificar_administrativo(self, Admin: Gestion.Administrativos):
        self.conectar()
        try:
            values = (Admin.get_nombre(),Admin.get_fecha(),Admin.get_prevision(),Admin.get_sueldo(),Admin.get_rol(),Admin.get_unidad(),Admin.get_afp(),Admin.get_documento_id())
            sql = "UPDATE personal_administrativo SET Nombre=%s, `Fecha_de_ingreso`=%s, `Tipo_de_prevision`=%s, `Sueldo_bruto`=%s, `Rol`=%s, `Unidad_administrativa`=%s, `Afp`=%s WHERE Rut=%s"
            self.cursor.execute(sql,values)
            self.connection.commit()
            self.actualizar_pago(2,Admin)
        except Exception as e:
            messagebox.showwarning("Error", "No se actualizaron los datos...")
            pass

    def actualizar_pago(self,op, b: Gestion.Personal):
        try:
            Sueldo_liquido=Grafica.pago_personal(op,b.get_sueldo(),b.get_afp(),b.get_fecha())
            sql="UPDATE pago_personal SET `Nombre` = %s, `Fecha_de_ingreso` = %s, `Sueldo_liquido` = %s, `Pagado` = %s WHERE `Rut` = %s"
            values=(b.get_nombre(),b.get_fecha(),Sueldo_liquido,"No",b.get_documento_id())
            self.cursor.execute(sql,values)
            messagebox.showinfo("Exito","Se hizo la modificacion con exito!")
            self.cerrar()
        except Exception as e:
            messagebox.showwarning("Error", "No se actualizaron los datos...")
            pass

    def conseguir_datos_personal(self,id):
        self.conectar()
        self.cursor.execute("SELECT * FROM personal_medico WHERE Rut=%s",(id,))
        return self.cursor.fetchone()
    
    def conseguir_datos_personal_administrativo(self,id):
        self.conectar()
        self.cursor.execute("SELECT * FROM personal_administrativo WHERE Rut=%s",(id,))
        return self.cursor.fetchone()

    #Pacientes
        
    def validar_paciente(self, paciente: Gestion.Pacientes): 
        self.conectar()
        Rut=paciente.get_documento_id()
        self.cursor.execute("SELECT * FROM pacientes WHERE Rut=%s",(Rut,))
        resultado=self.cursor.fetchone()
        if resultado is None:
            self.registrar_pacientes(paciente)
        else:
            messagebox.showwarning("Error","Ya esta registrado")

    def insertar_pago_pacientes(self, b: Gestion.Pacientes):
        Dinero_a_pagar=Grafica.obtener_dinero_a_pagar(b.get_derivacion(),b.get_prevision(),b.get_hospitalizacion(),b.get_dias())
        sql="INSERT INTO pago_pacientes (`Rut`,`Nombre`,`Tipo_de_prevision`,`Derivacion`,`Hospitalizacion`,`Dias_en_cama`,`Dinero_a_pagar`,`Pagado`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(b.get_documento_id(),b.get_nombre(),b.get_prevision(),b.get_derivacion(),b.get_hospitalizacion(),b.get_dias(),Dinero_a_pagar,"No")
        self.cursor.execute(sql,values)
        messagebox.showinfo("Exito","Se registro con exito!")
        self.cerrar()

    def registrar_pacientes(self, a: Gestion.Pacientes):        #comillas invertidas para variables con espacios o caracteres especiales
        self.conectar()
        sql = "INSERT INTO pacientes (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Motivo_de_ingreso`, `Derivacion`,`Box`,`Medico_y_Especialidad`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (a.get_documento_id(),a.get_nombre(),a.get_fecha(),a.get_prevision(),a.get_motivo(),a.get_derivacion(),a.get_box(),a.get_medico())
        self.cursor.execute(sql,values)
        self.insertar_pago_pacientes(a)
        
    def eliminar_paciente_bd(self,rut,ventana):
        self.conectar()
        try:
            if messagebox.askyesno(message="¿Esta seguro que desea ELIMINAR...?",title="Precaución"):
                sql="DELETE FROM pacientes WHERE Rut=%s"
                self.cursor.execute(sql,(rut,))
                self.connection.commit()
                if self.cursor.rowcount > 0:
                    self.cursor.execute("DELETE FROM pago_pacientes WHERE Rut=%s",(rut,))
                    self.connection.commit()
                    messagebox.showinfo("Exito","Se elimino con exito!")
                    ventana.destroy()
        except Exception as e:
                messagebox.showwarning("Error", "No se eliminaron de datos...")
                pass

    def modificar_paciente(self, a: Gestion.Pacientes,Dias_p):
        self.conectar()
        try:
            values=(a.get_nombre(),a.get_fecha(),a.get_prevision(),a.get_motivo(),a.get_derivacion(),a.get_box(),a.get_medico(),a.get_documento_id())
            sql = "UPDATE pacientes SET Nombre=%s, `Fecha_de_ingreso`=%s, `Tipo_de_prevision`=%s, `Motivo_de_ingreso`=%s, `Derivacion`=%s, `Box`=%s,`Medico_y_Especialidad`=%s WHERE Rut=%s"
            self.cursor.execute(sql,values)
            self.actualizar_pago_pacientes(a)
        except Exception as e:
            messagebox.showwarning("Error", "No se actualizaron los datos...")
            pass

    def actualizar_pago_pacientes(self,b: Gestion.Pacientes):
        Dinero_a_pagar=Grafica.obtener_dinero_a_pagar(b.get_derivacion(),b.get_prevision(),b.get_hospitalizacion(),b.get_dias())
        sql="UPDATE pago_pacientes SET `Nombre`=%s,`Tipo_de_prevision`=%s, `Derivacion`=%s ,`Hospitalizacion`=%s, `Dias_en_cama`=%s, `Dinero_a_pagar`=%s, `Pagado`=%s WHERE `Rut` = %s"
        values=(b.get_nombre(),b.get_prevision(),b.get_derivacion(),b.get_hospitalizacion(),b.get_dias(),Dinero_a_pagar,"No",b.get_documento_id())
        self.cursor.execute(sql,values)
        messagebox.showinfo("Exito","Se hizo la modificacion con exito!")
        self.cerrar()

    def actualizar_tabla_pacientes(self,treee):
        self.conectar()
        registros=treee.get_children() 
        for elemento in registros: 
            treee.delete(elemento)
        try:
            sql='SELECT * FROM pago_pacientes'
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                treee.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        except Exception as e:
            pass

    def mostrar_pacientes(self,treee):
        self.conectar()
        registros=treee.get_children() 
        for elemento in registros: 
            treee.delete(elemento)
        try:
            sql='SELECT * FROM pacientes'
            self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                treee.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        except Exception as e:
            pass

    def pagar_pacientes(self,ID):
        self.conectar()
        self.cursor.execute("SELECT * FROM pago_pacientes WHERE Rut=%s",(ID,))
        resultado=self.cursor.fetchone()
        if resultado is None:
            messagebox.showwarning("Error","No se encontro ese Rut")
        else:
            self.cursor.execute("SELECT Pagado FROM pago_pacientes WHERE Rut=%s",(ID,))
            Pagado=self.cursor.fetchone()[0]
            if Pagado=="Si":
                messagebox.showinfo("Pagado","Al pacientes ya pago")
            else:
                self.cursor.execute("SELECT Dinero_a_pagar FROM pago_pacientes WHERE Rut=%s",(ID,))
                dinero_pagar=self.cursor.fetchone()[0]
                self.cursor.execute("UPDATE `pago_pacientes` SET `Pagado` = 'Si' WHERE `pago_pacientes`.`Rut`=%s",(ID,))
                self.cursor.execute("SELECT Fondos FROM fondos WHERE id=%s",(1,))
                Fondos=self.cursor.fetchone()[0]
                Fondos=Fondos+dinero_pagar
                self.cursor.execute("UPDATE `fondos` SET `Fondos`=%s WHERE `fondos`.`id`=%s",(Fondos,1,))
                messagebox.showinfo("Exito","Se realizo la transferencia con exito")
                self.cerrar()

    def obtener_medicos(self):
        self.conectar()
        self.cursor.execute('SELECT Nombre, Especialidad_o_Area FROM personal_medico WHERE Rol=%s',("Medico"))
        datos=self.cursor.fetchall()
        self.cerrar()
        return datos
    
    def conseguir_datos_personal_paciente(self,id):
        self.conectar()
        self.cursor.execute("SELECT * FROM pacientes WHERE Rut=%s",(id,))
        return self.cursor.fetchone()
    
    #Usuarios
    
    def validar_usuario(self, C: Gestion.Usuarios,frame_ini,frame_fin):
        self.conectar()
        User=C.get_usuario()
        self.cursor.execute("SELECT * FROM cuentas WHERE Usuario=%s",(User,))
        resultado=self.cursor.fetchone()
        if resultado is None:
            self.registrar_usuario(C,frame_ini,frame_fin)
        else:
            messagebox.showwarning("Error","El usuario ya esta ocupado")
            return False
    
    def registrar_usuario(self, C: Gestion.Usuarios,frame_ini,frame_fin):
        sql="INSERT INTO cuentas (`Usuario`,`Contraseña`,`Correo`)VALUES(%s,%s,%s)"
        values=(C.get_usuario(),C.get_contrasena(),C.get_corre())
        self.cursor.execute(sql,values)
        messagebox.showinfo("Exito","Registro hecho con exito!")
        Grafica.regresar_inicio(frame_ini,frame_fin)
        self.cerrar()

    def validar_entrada_de_sesion(self,user,password):
        self.conectar()
        self.cursor.execute("SELECT * FROM cuentas WHERE Usuario=%s AND Contraseña=%s",(user,password,))
        return self.cursor.fetchone()

        