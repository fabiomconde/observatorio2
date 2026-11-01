from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_publicacaoredesocial_alter_dashboard_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="membro",
            name="inicio_participacao",
            field=models.DateField(
                blank=True,
                help_text=(
                    "Data em que a pessoa passou a integrar o Observatório. "
                    "Pode ficar em branco para registros legados."
                ),
                null=True,
                verbose_name="início da participação",
            ),
        ),
        migrations.AddField(
            model_name="membro",
            name="fim_participacao",
            field=models.DateField(
                blank=True,
                help_text=(
                    "Deixe em branco enquanto a participação estiver vigente. "
                    "Ao preencher, o membro passa ao histórico após essa data."
                ),
                null=True,
                verbose_name="fim da participação",
            ),
        ),
        migrations.AlterField(
            model_name="membro",
            name="ativo",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Controla apenas a visibilidade pública do registro; "
                    "não representa o encerramento da participação."
                ),
                verbose_name="publicado",
            ),
        ),
        migrations.AddConstraint(
            model_name="membro",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(("inicio_participacao__isnull", True))
                    | models.Q(("fim_participacao__isnull", True))
                    | models.Q(
                        ("fim_participacao__gte", models.F("inicio_participacao"))
                    )
                ),
                name="membro_fim_nao_anterior_inicio",
            ),
        ),
    ]
