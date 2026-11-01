from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Membro


class MembroDomainTests(TestCase):
    def setUp(self):
        self.hoje = timezone.localdate()

    def test_registro_legado_sem_datas_permanece_atual(self):
        membro = Membro.objects.create(nome="Legado")
        self.assertTrue(membro.participacao_atual)
        self.assertEqual(list(Membro.objects.atuais()), [membro])

    def test_membro_encerrado_vai_para_historico(self):
        membro = Membro.objects.create(
            nome="Histórico",
            inicio_participacao=self.hoje - timedelta(days=365),
            fim_participacao=self.hoje - timedelta(days=1),
        )
        self.assertTrue(membro.participacao_historica)
        self.assertIn(membro, Membro.objects.historicos())
        self.assertNotIn(membro, Membro.objects.atuais())

    def test_fim_futuro_ainda_e_participacao_atual(self):
        membro = Membro.objects.create(
            nome="Vigente",
            inicio_participacao=self.hoje - timedelta(days=30),
            fim_participacao=self.hoje + timedelta(days=30),
        )
        self.assertIn(membro, Membro.objects.atuais())

    def test_inicio_futuro_nao_aparece_como_atual(self):
        membro = Membro.objects.create(
            nome="Previsto",
            inicio_participacao=self.hoje + timedelta(days=30),
        )
        self.assertEqual(membro.status_participacao, "Previsto")
        self.assertNotIn(membro, Membro.objects.atuais())
        self.assertNotIn(membro, Membro.objects.historicos())

    def test_registro_nao_publicado_nao_aparece(self):
        membro = Membro.objects.create(nome="Oculto", ativo=False)
        self.assertNotIn(membro, Membro.objects.atuais())
        self.assertNotIn(membro, Membro.objects.historicos())

    def test_modelo_rejeita_fim_anterior_ao_inicio(self):
        membro = Membro(
            nome="Inválido",
            inicio_participacao=self.hoje,
            fim_participacao=self.hoje - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            membro.full_clean()


class MembrosPageTests(TestCase):
    def setUp(self):
        hoje = timezone.localdate()
        self.atual = Membro.objects.create(nome="Pessoa Atual")
        self.historico = Membro.objects.create(
            nome="Pessoa Histórica",
            inicio_participacao=hoje - timedelta(days=365),
            fim_participacao=hoje - timedelta(days=1),
        )
        self.oculto = Membro.objects.create(nome="Pessoa Oculta", ativo=False)

    def test_pagina_separa_atuais_e_historicos(self):
        response = self.client.get(reverse("core:membros"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Membros atuais")
        self.assertContains(response, "Histórico de participação")
        self.assertContains(response, self.atual.nome)
        self.assertContains(response, self.historico.nome)
        self.assertNotContains(response, self.oculto.nome)


class MembrosPageEmptyTests(TestCase):
    def test_sem_atuais(self):
        Membro.objects.create(nome="Somente Histórico", fim_participacao=timezone.localdate() - timedelta(days=1))
        response = self.client.get(reverse("core:membros"))
        self.assertContains(response, "Nenhum membro atual cadastrado.")
        self.assertContains(response, "Somente Histórico")

    def test_sem_historico(self):
        Membro.objects.create(nome="Somente Atual")
        response = self.client.get(reverse("core:membros"))
        self.assertContains(response, "Somente Atual")
        self.assertContains(response, "Ainda não há participações encerradas registradas.")

    def test_pagina_totalmente_vazia(self):
        response = self.client.get(reverse("core:membros"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum membro atual cadastrado.")
        self.assertContains(response, "Ainda não há participações encerradas registradas.")

    def test_periodos_sao_mes_e_ano(self):
        inicio = timezone.localdate().replace(year=2020, month=3, day=1)
        fim = inicio.replace(year=2022, month=4)
        Membro.objects.create(nome="Participação Finalizada", inicio_participacao=inicio, fim_participacao=fim)
        response = self.client.get(reverse("core:membros"))
        self.assertContains(response, "03/2020")
        self.assertContains(response, "04/2022")


class MembroAdminTests(TestCase):
    def test_admin_permite_edicao_das_datas(self):
        user = get_user_model().objects.create_superuser(
            username="admin_test", email="admin@exemplo.test", password="senha-teste-segura"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:core_membro_add"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="inicio_participacao"')
        self.assertContains(response, 'name="fim_participacao"')

    def test_constraint_banco_rejeita_intervalo_invalido(self):
        hoje = timezone.localdate()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Membro.objects.create(nome="Inconsistente", inicio_participacao=hoje, fim_participacao=hoje - timedelta(days=1))

    def test_membro_legado_mantem_visibilidade_sem_datas(self):
        membro = Membro.objects.create(nome="Antigo Visível", ativo=True)
        response = self.client.get(reverse("core:membros"))
        self.assertContains(response, membro.nome)
        self.assertEqual(Membro.objects.get(pk=membro.pk).inicio_participacao, None)
