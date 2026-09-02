# Generated manually for Dashboard model

from django.db import migrations, models


def seed_dashboard(apps, schema_editor):
    Dashboard = apps.get_model('core', 'Dashboard')
    Dashboard.objects.update_or_create(
        id=1,
        defaults={
            'titulo': 'Dashboard de Dados Demográficos',
            'slug': 'dashboard-de-dados-demograficos',
            'descricao': 'Indicadores socioambientais e dados demográficos do município de Porto Velho/RO embutido via Apache Superset.',
            'link': 'https://painel.provaconceito.tech/superset/dashboard/6e1ba906-05c6-4b95-a3d0-ee50fe1734c9/?permalink_key=xOY1wMmwkZP&standalone=2',
            'icone': 'bi-people',
            'ordem': 1,
            'destaque': True,
            'ativo': True,
        }
    )


def remove_dashboard(apps, schema_editor):
    Dashboard = apps.get_model('core', 'Dashboard')
    Dashboard.objects.filter(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_regiao_distrito'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('titulo', models.CharField(max_length=150, verbose_name='título')),
                ('slug', models.SlugField(blank=True, max_length=160, unique=True, verbose_name='slug')),
                ('descricao', models.TextField(blank=True, verbose_name='descrição')),
                ('link', models.URLField(help_text='URL pública do dashboard, ex: http://painel.provaconceito.tech/superset/dashboard/p/xOY1wMmwkZP/?standalone=2', max_length=500, verbose_name='link / URL do iframe')),
                ('icone', models.CharField(blank=True, default='bi-bar-chart-line', max_length=40, verbose_name='ícone (Bootstrap Icons)')),
                ('ordem', models.PositiveIntegerField(default=0, verbose_name='ordem de exibição')),
                ('destaque', models.BooleanField(default=False, verbose_name='destaque')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
            ],
            options={
                'verbose_name': 'Dashboard',
                'verbose_name_plural': 'Dashboards',
                'ordering': ['ordem', '-criado_em'],
            },
        ),
        migrations.RunPython(seed_dashboard, remove_dashboard),
    ]
