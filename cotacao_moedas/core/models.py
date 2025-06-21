from django.db import models

class Cotacao(models.Model):
    moeda = models.CharField(max_length=3)
    valor = models.DecimalField(max_digits=10, decimal_places=4)
    data_atualizacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.moeda} - {self.valor}"

    class Meta:
        verbose_name = "Cotação"
        verbose_name_plural = "Cotações"