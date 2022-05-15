from ursina import Entity

class ObjetoGiratorio(object):
    def __init__(self, x0, y0, z0, textura_asociada, velocidad_angular_rotacion, velocidad_angular_traslacion) -> None:
        self.entidad=Entity(model="sphere", texture=textura_asociada)
        self.x=x0
        self.y=y0
