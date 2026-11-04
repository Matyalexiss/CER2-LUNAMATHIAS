from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, LugarPatrimoniales


class LugarViewTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Histórico',
            descripcion='Lugares de valor histórico.',
        )
        self.lugar = LugarPatrimoniales.objects.create(
            id='A001',
            nombre='Casa Patrimonial',
            descripcion='Edificación histórica.',
            ubicacion='Valparaíso',
            anio_construccion=1900,
            imagen='https://example.com/casa.jpg',
            categoria=self.categoria,
        )
        self.user = get_user_model().objects.create_user(
            username='editor',
            password='test-password',
        )

    def test_detail_accepts_text_id_and_shows_complete_information(self):
        response = self.client.get(
            reverse('detalle_lugar', args=[self.lugar.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/detalle.html')
        self.assertContains(response, self.lugar.nombre)
        self.assertContains(response, self.lugar.descripcion)
        self.assertContains(response, self.lugar.ubicacion)
        self.assertContains(response, str(self.lugar.anio_construccion))
        self.assertContains(response, self.categoria.nombre)

    def test_authorized_user_can_edit_place_with_text_id(self):
        permission = Permission.objects.get(
            content_type__app_label='core',
            codename='change_lugarpatrimoniales',
        )
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('lugar_editar', args=[self.lugar.id]),
            {
                'nombre': 'Casa Restaurada',
                'descripcion': self.lugar.descripcion,
                'ubicacion': self.lugar.ubicacion,
                'anio_construccion': self.lugar.anio_construccion,
                'imagen': self.lugar.imagen,
                'categoria': self.categoria.id,
            },
        )

        self.assertRedirects(response, reverse('catalogo'))
        self.lugar.refresh_from_db()
        self.assertEqual(self.lugar.nombre, 'Casa Restaurada')

    def test_edit_rejects_authenticated_user_without_permission(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('lugar_editar', args=[self.lugar.id]),
            {'nombre': 'Cambio no autorizado'},
        )

        self.assertEqual(response.status_code, 403)
        self.lugar.refresh_from_db()
        self.assertEqual(self.lugar.nombre, 'Casa Patrimonial')

    def test_create_rejects_authenticated_user_without_permission(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('lugar_crear'), {})

        self.assertEqual(response.status_code, 403)

    def test_authorized_user_can_create_place(self):
        permission = Permission.objects.get(
            content_type__app_label='core',
            codename='add_lugarpatrimoniales',
        )
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('lugar_crear'),
            {
                'id': 'B002',
                'nombre': 'Museo Local',
                'descripcion': 'Espacio dedicado a la historia local.',
                'ubicacion': 'Santiago',
                'anio_construccion': 1950,
                'imagen': 'https://example.com/museo.jpg',
                'categoria': self.categoria.id,
            },
        )

        self.assertRedirects(response, reverse('catalogo'))
        self.assertTrue(LugarPatrimoniales.objects.filter(id='B002').exists())
