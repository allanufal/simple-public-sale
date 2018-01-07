from django.db import models, IntegrityError
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

from channels_core.models import GrupoEvento
from core.utils import send_to_evento


class Doador(models.Model):
    nome_doador = models.CharField(max_length=100)
    apelido_doador = models.CharField(max_length=100)
    cpf_cnpj_doador = models.CharField(max_length=14)
    def __str__(self):
        return self.nome_doador
class Evento(models.Model):
    nome_evento = models.CharField(max_length=100)
    data_evento = models.DateTimeField(null=True,blank=True)
    url_image = models.ImageField(upload_to='imagens')
    grupo = models.OneToOneField(GrupoEvento, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome_evento
    def is_online(self):
        return self.grupo.online
    
class TipoPrenda(models.Model):
    nome = models.CharField(max_length=100,default='',null=True,blank=True)
    descricao = models.CharField(max_length=100)
    url_image = models.ImageField(upload_to='tipos/imagens',null=True,blank=True)
    def __str__(self):
        return self.nome

class Caracteristica(models.Model):
    caracteristica = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)
    def __str__(self):
        return self.caracteristica
class Prenda(models.Model):
    doador_fk = models.ForeignKey(Doador, on_delete=models.CASCADE)
    valor_inicial = models.DecimalField(decimal_places=2, max_digits=8)
    tipo_prenda_fk = models.ForeignKey(TipoPrenda, on_delete=models.CASCADE)
    evento_fk = models.ForeignKey(Evento, on_delete=models.CASCADE)
    arrematada = models.BooleanField(default=False)
    url_image = models.ImageField(upload_to='prendas/imagens', null=True, blank=True)
    caracteristicas = models.ManyToManyField(Caracteristica,through='CaracteristicaPrenda')
    def __str__(self):
        return self.tipo_prenda_fk.nome
    def last_three_movements(self):
        return self.movimento_set.all().order_by("-data_movimento")[0:3]

class CaracteristicaPrenda(models.Model):
    prenda = models.ForeignKey(Prenda,on_delete=models.CASCADE)
    caracteristica = models.ForeignKey(Caracteristica,on_delete=models.CASCADE)
    valor = models.CharField(max_length=100)
    class Meta:
        unique_together=('prenda','caracteristica')
    def __str__(self):
        return "%s - %s"%(self.caracteristica.caracteristica, self.prenda.tipo_prenda_fk.nome)

class ArrematadorManager(models.Manager):
    def get_by_natural_key(self, nome_arrematador):
        return self.get(nome_arrematador=nome_arrematador)

class Arrematador(models.Model):
    nome_arrematador = models.CharField(max_length=100,unique=True,db_index=True)
    cpf_cnpj_arrematador = models.CharField(max_length=14,null=True,blank=True)
    rg_arrematador = models.CharField(max_length=50,null=True,blank=True)
    endereco_arrematador = models.CharField(max_length=200,null=True,blank=True)

    objects=ArrematadorManager()
    def __str__(self):
        return self.nome_arrematador

    def natural_key(self):
        return (self.nome_arrematador)
    
class Movimento(models.Model):
    data_movimento = models.DateField(auto_now=True,editable=False)
    arrematador_fk = models.ForeignKey(Arrematador, on_delete=models.CASCADE)
    valor_arremate = models.DecimalField(decimal_places=2, max_digits=8)
    prenda_fk = models.ForeignKey('Prenda', on_delete=models.CASCADE)
    def __str__(self):
        return "%s - %s : R$ %s"%(self.arrematador_fk.nome_arrematador,self.prenda_fk.tipo_prenda_fk.nome,self.valor_arremate)
    def send_to_stream(self):
        if self.prenda_fk.evento_fk.is_online():
            prenda = self.prenda_fk
            send_to_evento(prenda=prenda)
            print("Stream Atualizada")
        else:
            print("Stream Offline")
        return False


@receiver(post_save, sender=Movimento)
def post_save_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)

    instance.send_to_stream()


@receiver(pre_delete, sender=Movimento)
def pre_delete_movimento(sender,instance, **kwargs):
    assert isinstance(instance, Movimento)
    instance.send_to_stream()

@receiver(pre_save, sender=Arrematador)
def pre_save_arrematador(sender,instance, **kwargs):
    assert isinstance(instance, Arrematador)
    instance.nome_arrematador=instance.nome_arrematador.upper()

@receiver(pre_save, sender=CaracteristicaPrenda)
def pre_save_caracteristica_prenda(sender,instance, **kwargs):
    assert isinstance(instance, CaracteristicaPrenda)
    if(instance.prenda.caracteristicaprenda_set.count()>=3):
        raise IntegrityError("Cada prenda tem um limite de 3 caracteristicas.")
