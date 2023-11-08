class Personas():
    def __init__(self,Documento_id,nombre,fecha_ingreso,tipo_prevision):
        self.documento_id=Documento_id
        self.nombre=nombre
        self.fecha_ingreso=fecha_ingreso
        self.tipo_prevision=tipo_prevision

    def get_documento_id(self):
        return self.documento_id
    
    def get_nombre(self):
        return self.nombre
    
    def get_fecha(self):
        return self.fecha_ingreso
    
    def get_prevision(self):
        return self.tipo_prevision
    
    
class Personal(Personas):
    def __init__(self, Documento_id, nombre, fecha_ingreso, tipo_prevision,sueldo_bruto,rol,afp):
        super().__init__(Documento_id, nombre, fecha_ingreso, tipo_prevision)
        self.sueldo_bruto=sueldo_bruto
        self.afp=afp
        self.rol=rol

    def get_sueldo(self):
        return self.sueldo_bruto
    
    def get_afp(self):
        return self.afp
    
    def get_rol(self):
        return self.rol

class Medicos(Personal):
    def __init__(self, Documento_id, nombre, fecha_ingreso, tipo_prevision, sueldo_bruto,rol,especialidad,afp):
        super().__init__(Documento_id, nombre, fecha_ingreso, tipo_prevision,sueldo_bruto,rol,afp)
        self.especialidad=especialidad
    
    def get_especialidad(self):
        return self.especialidad

class Tens(Personal):
    def __init__(self, Documento_id, nombre, fecha_ingreso, tipo_prevision, sueldo_bruto,rol,area,afp):
        super().__init__(Documento_id, nombre, fecha_ingreso, tipo_prevision,sueldo_bruto,rol,afp)
        self.area=area
    
    def get_area(self):
        return self.area

class Administrativos(Personal):
    def __init__(self, Documento_id, nombre, fecha_ingreso, tipo_prevision, sueldo_bruto,rol,Unidad_administrativa,afp):
        super().__init__(Documento_id, nombre, fecha_ingreso, tipo_prevision, sueldo_bruto,rol,afp)
        self.sueldo_bruto=sueldo_bruto
        self.unidad_administrativa=Unidad_administrativa
    
    def get_unidad(self):
        return self.unidad_administrativa

# Gestion de ingreso de pacientes
class Pacientes(Personas):
    def __init__(self, Documento_id, nombre, fecha_ingreso, tipo_prevision,motivo_ingreso,derivacion,box,medico,hospitalizacion,dias,especialidad_p):
        super().__init__(Documento_id, nombre, fecha_ingreso, tipo_prevision)
        self.motivo_ingreso=motivo_ingreso
        self.derivacion=derivacion
        self.box=box
        self.medico=medico
        self.hospitalizacion=hospitalizacion
        self.dias=dias
        self.especialidad_p=especialidad_p

    def get_motivo(self):
        return self.motivo_ingreso
    
    def get_derivacion(self):
        return self.derivacion
    
    def get_box(self):
        return self.box
    
    def get_medico(self):
        return self.medico
    
    def get_hospitalizacion(self):
        return self.hospitalizacion
    
    def get_dias(self):
        return self.dias
    
    def get_especialidad_medico(self):
        return self.especialidad_p
    
class Usuarios():
    def __init__(self,usuario,contrasena,correo):
        self.usuario=usuario
        self.contrasena=contrasena
        self.correo=correo
    
    def get_usuario(self):
        return self.usuario
    
    def get_contrasena(self):
        return self.contrasena
    
    def get_corre(self):
        return self.correo