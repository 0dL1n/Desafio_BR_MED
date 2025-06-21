# cotacao_moedas/core/models.py
from django.db import models

class Cotacao(models.Model):
    data = models.DateField(unique=True, help_text="Data da cotação (formato YYYY-MM-DD)")
    valor_brl = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Valor do Dólar em Real (USD/BRL)")
    valor_eur = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Valor do Dólar em Euro (USD/EUR)")
    valor_jpy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Valor do Dólar em Iene (USD/JPY)")
    data_registro = models.DateTimeField(auto_now_add=True, help_text="Data e hora do registro/última atualização no banco de dados")

    class Meta:
        verbose_name = "Cotação"
        verbose_name_plural = "Cotações"
        ordering = ['-data'] # Ordena por data (mais recente primeiro)

    def __str__(self):
        return f"Cotações de USD para {self.data.strftime('%Y-%m-%d')}"