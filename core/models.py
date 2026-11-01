from django.db import models

class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=30) 
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre 

class LugarPatrimoniales(models.Model):
    id = models.CharField(max_length=4, primary_key=True) 
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=20)
    anio_construccion = models.IntegerField()
    imagen= models.URLField(max_length=500)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='lugares')

    def __str__(self):
        return self.nombre