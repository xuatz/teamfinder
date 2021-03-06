from common.models import Position, Region, SkillBracket, TeamMember
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from teams.models import Team
from tf_auth.models import TFUser
from . import permissions, serializers, views
from .serializers import MembershipSerializer, PositionSerializer, RegionSerializer, SkillBracketSerializer

User = get_user_model()


# Some of these are defined by DRF
ALLOWED_LIST_METHODS = ('head', 'options', 'get', 'post', )
ALLOWED_DETAIL_METHODS = ('head', 'options', 'get', 'put', 'patch', 'delete', )
AUTHORIZED_LIST_METHODS = ('head', 'options', 'get', )
AUTHORIZED_DETAIL_METHODS = ('head', 'options' 'get', )


class CommonApiSerializerTests(APITestCase):
    """
    Serializer tests.
    """
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_RegionSerializer(self):
        name = 'Test Region'
        region = Region.objects.create(name=name)
        url = reverse('region-detail', (region.id, ))
        request = self.factory.get(url)
        absolute_url = request.build_absolute_uri()
        serializer = RegionSerializer(instance=region, context={'request': request})
        self.assertEqual(serializer.data, {'id': str(region.id),
                                           'name': name,
                                           'url': absolute_url})

    def test_PositionSerializer(self):
        name = 'Test Position'
        position = Position.objects.create(name=name)
        url = reverse('position-detail', (position.id, ))
        request = self.factory.get(url)
        absolute_url = request.build_absolute_uri()
        serializer = PositionSerializer(instance=position, context={'request': request})
        self.assertEqual(serializer.data, {'id': str(position.id),
                                           'name': name,
                                           'secondary': False,
                                           'url': absolute_url})

    def test_SkillBracketSerializer(self):
        name = 'Test Skill Bracket'
        skill_bracket = SkillBracket.objects.create(name=name)
        url = reverse('skillbracket-detail', (skill_bracket.id, ))
        request = self.factory.get(url)
        absolute_url = request.build_absolute_uri()
        serializer = SkillBracketSerializer(instance=skill_bracket, context={'request': request})
        self.assertEqual(serializer.data, {'id': str(skill_bracket.id),
                                           'name': name,
                                           'url': absolute_url})

    def test_MembershipSerializer(self):
        user = TFUser.objects.create_user('lenny+tftests@prattdev.net', '12345678')
        player = user.player
        team = Team.objects.create(name='team')
        member = TeamMember.objects.create(player=player, team=team)
        url = reverse('teammember-detail', (member.id, ))
        request = self.factory.get(url)
        absolute_url = request.build_absolute_uri()
        serializer = MembershipSerializer(instance=member, context={'request': request})
        expected_data = {
            'id': str(member.id),
            'player': member.player.id,
            'team': member.team.id,
            'position': None,
            'url': absolute_url
        }
        self.assertLessEqual(expected_data.items(), serializer.data.items())


class BaseTestCases:

    class AuthenticatedTests(APITestCase):
        """
        Base test case for an authenticated user.
        """
        @classmethod
        def setUpTestData(cls):
            super(BaseTestCases.AuthenticatedTests, cls).setUpTestData()
            cls.user = User.objects.create_user('lenny+tftests@prattdev.net', '01234567')
            token, _ = Token.objects.get_or_create(user=cls.user)
            cls.token = token

        def setUp(self):
            # Authenticate user
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class CommonModelTests:
    """
    Test cases for HTTP methods against the common models (Position, Region, and SkillBracket)
    """
    class UnauthenticatedListViewTests(APITestCase):
        url = ''

        def test_head(self):
            response = self.client.head(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_options(self):
            response = self.client.options(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_get(self):
            response = self.client.get(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_post(self):
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_put(self):
            response = self.client.put(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_patch(self):
            response = self.client.patch(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_delete(self):
            response = self.client.delete(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_trace(self):
            response = self.client.trace(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    class UnauthenticatedDetailViewTests(APITestCase):
        url = ''

        def test_head(self):
            response = self.client.head(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_options(self):
            response = self.client.options(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_get(self):
            response = self.client.get(self.url)
            self.assertTrue(200 <= response.status_code < 300)

        def test_post(self):
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_put(self):
            response = self.client.put(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_patch(self):
            response = self.client.patch(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_delete(self):
            response = self.client.delete(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        def test_trace(self):
            response = self.client.trace(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UnauthenticatedPositionListViewTests(CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('position-list')


class UnauthenticatedPositionDetailViewTests(CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('position-detail', (Position.objects.first().pk, ))


class UnauthenticatedRegionListViewTests(CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('region-list')


class UnauthenticatedRegionDetailViewTests(CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('region-detail', (Region.objects.first().pk, ))


class UnauthenticatedSkillBracketListViewTests(CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('skillbracket-list')


class UnauthenticatedSkillBracketDetailViewTests(CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('skillbracket-detail', (SkillBracket.objects.first().pk, ))


class AuthenticatedPositionListViewTests(BaseTestCases.AuthenticatedTests,
                                         CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('position-list')


class AuthenticatedPositionDetailViewTests(BaseTestCases.AuthenticatedTests,
                                           CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('position-detail', (Position.objects.first().pk, ))


class AuthenticatedRegionListViewTests(BaseTestCases.AuthenticatedTests,
                                       CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('region-list')


class AuthenticatedRegionDetailViewTests(BaseTestCases.AuthenticatedTests,
                                         CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('region-detail', (Region.objects.first().pk, ))


class AuthenticatedSkillBracketListViewTests(BaseTestCases.AuthenticatedTests,
                                             CommonModelTests.UnauthenticatedListViewTests):
    url = reverse('skillbracket-list')


class AuthenticatedSkillBracketDetailViewTests(BaseTestCases.AuthenticatedTests,
                                               CommonModelTests.UnauthenticatedDetailViewTests):
    url = reverse('skillbracket-detail', (SkillBracket.objects.first().pk, ))


# Viewset test cases
class UnauthenticatedSkillBracketListViewSetTests(APITestCase):
    url = reverse('skillbracket-list')

    def test_head(self):
        response = self.client.head(self.url)
        self.assertEqual(response.data['count'], SkillBracket.objects.count())

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Skill Bracket List')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], SkillBracket.objects.count())


class UnauthenticatedSkillBracketDetailViewSetTests(APITestCase):
    skill_bracket = SkillBracket.objects.first()
    url = reverse('skillbracket-detail', (skill_bracket.pk, ))

    def assertDataEqualsInstance(self, data):
        self.assertEqual(data['id'], str(self.skill_bracket.id))
        self.assertEqual(data['name'], str(self.skill_bracket.name))

    def test_head(self):
        response = self.client.head(self.url)
        self.assertDataEqualsInstance(response.data)

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Skill Bracket Instance')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertDataEqualsInstance(response.data)


class UnauthenticatedRegionListViewSetTests(APITestCase):
    url = reverse('region-list')

    def test_head(self):
        response = self.client.head(self.url)
        self.assertEqual(response.data['count'], Region.objects.count())

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Region List')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], Region.objects.count())


class UnauthenticatedRegionDetailViewSetTests(APITestCase):
    region = Region.objects.first()
    url = reverse('region-detail', (region.pk, ))

    def assertDataEqualsInstance(self, data):
        self.assertEqual(data['id'], str(self.region.id))
        self.assertEqual(data['name'], str(self.region.name))

    def test_head(self):
        response = self.client.head(self.url)
        self.assertDataEqualsInstance(response.data)

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Region Instance')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertDataEqualsInstance(response.data)


class UnauthenticatedPositionListViewSetTests(APITestCase):
    url = reverse('position-list')

    def test_head(self):
        response = self.client.head(self.url)
        self.assertEqual(response.data['count'], Position.objects.count())

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Position List')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], Position.objects.count())


class UnauthenticatedPositionDetailViewSetTests(APITestCase):
    position = Position.objects.first()
    url = reverse('position-detail', (position.pk, ))

    def assertDataEqualsInstance(self, data):
        self.assertEqual(data['id'], str(self.position.id))
        self.assertEqual(data['name'], str(self.position.name))

    def test_head(self):
        response = self.client.head(self.url)
        self.assertDataEqualsInstance(response.data)

    def test_options(self):
        response = self.client.options(self.url)
        self.assertEqual(response.data['name'], 'Position Instance')
        self.assertTrue('application/json' in response.data['renders'])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertDataEqualsInstance(response.data)


class AuthenticatedSkillBracketListViewSetTests(BaseTestCases.AuthenticatedTests,
                                                UnauthenticatedSkillBracketListViewSetTests):
    pass


class AuthenticatedSkillBracketDetailViewSetTests(BaseTestCases.AuthenticatedTests,
                                                  UnauthenticatedSkillBracketDetailViewSetTests):
    pass


class AuthenticatedRegionListViewSetTests(BaseTestCases.AuthenticatedTests,
                                          UnauthenticatedRegionListViewSetTests):
    pass


class AuthenticatedRegionDetailViewSetTests(BaseTestCases.AuthenticatedTests,
                                            UnauthenticatedRegionDetailViewSetTests):
    pass


class AuthenticatedPositionListViewSetTests(BaseTestCases.AuthenticatedTests,
                                            UnauthenticatedPositionListViewSetTests):
    pass


class AuthenticatedPositionDetailViewSetTests(BaseTestCases.AuthenticatedTests,
                                              UnauthenticatedPositionDetailViewSetTests):
    pass
