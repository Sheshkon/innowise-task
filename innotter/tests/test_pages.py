import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from pages.serializers import page_serializers, tag_serializers
from pages.models import Tag
User = get_user_model()


class TestTags:

    @pytest.mark.django_db
    def test_user_create_tag(self, auth_user_client):
        url = reverse('tags-list')
        payload = {
            'name': 'new_tag'
        }
        response = auth_user_client.post(url, payload, format('json'))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_admin_create_tag(self, auth_admin_client):
        url = reverse('tags-list')
        payload = {
            'name': 'new_tag'
        }
        response = auth_admin_client.post(url, payload, format('json'))

        assert response.status_code == status.HTTP_201_CREATED
        assert Tag.objects.filter(name='new_tag').exists()

    @pytest.mark.django_db
    def test_admin_delete_tag(self, auth_admin_client, tags_list):
        url = reverse('tags-detail', args=(tags_list[2].pk,))
        response = auth_admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_tags_list(self, auth_user_client, tags_list):
        url = reverse('tags-list')
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(tags_list)

    @pytest.mark.django_db
    def test_tag_retrieve(self, auth_user_client, tags_list):
        url = reverse('tags-detail', args=(tags_list[3].pk,))

        expected_data = tag_serializers.TagSerializer(tags_list[3]).data
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    @pytest.mark.django_db
    def test_admin_update_tag(self, auth_admin_client, tags_list):
        url = reverse('tags-detail', args=(tags_list[3].pk,))
        payload = {
            'name': 'new_tag'
        }

        response = auth_admin_client.put(url, payload, format('json'))

        assert response.status_code == status.HTTP_200_OK


class TestLikes:

    @pytest.mark.django_db
    def test_create_like(self, auth_admin_client, user_post):
        url = reverse('likes-list')
        payload = {
            'post': user_post.pk
        }
        response = auth_admin_client.post(url, payload, format('json'))

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_admin_list_like(self, auth_admin_client, user_post, likes):
        url = reverse('likes-list')
        response = auth_admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(likes) == len(response.data)

    @pytest.mark.django_db
    def test_user_list_like(self, auth_user_client, user_post, likes):
        url = reverse('likes-list')
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_delete_not_own_like(self, auth_user_client, user_post, likes):
        url = reverse('likes-detail', args=(likes[1].pk,))

        response = auth_user_client.delete(url, {}, format('json'))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_own_like(self, auth_user_client, user_post, likes):
        url = reverse('likes-detail', args=(likes[0].pk,))

        response = auth_user_client.delete(url, {}, format('json'))

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestPosts:
    @pytest.mark.django_db
    def test_create_post(self, auth_user_client, user_page):
        url = reverse('posts-list', )
        payload = {
            'page': user_page.pk,
            'content': 'test content',
        }

        response = auth_user_client.post(url, payload, format('json'))

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_delete_post(self, auth_user_client, user_post):
        url = reverse('posts-detail', args=(user_post.pk,))

        response = auth_user_client.delete(url, {}, format('json'))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_admin_delete_post(self, auth_admin_client, user_post):
        url = reverse('posts-detail', args=(user_post.pk,))

        response = auth_admin_client.delete(url, {}, format('json'))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_post_list(self, auth_user_client, user_post, admin_post):
        url = reverse('posts-list')
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_post_retrieve(self, auth_user_client, user_post, admin_post):
        url = reverse('posts-detail', args=(user_post.pk,))
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_post_admin_list(self, auth_admin_client, user_post, admin_post):
        url = reverse('posts-list')
        response = auth_admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_post_update(self, auth_user_client, user_post, admin_post):
        url = reverse('posts-detail', args=(user_post.pk,))
        payload = {
            'content': 'new content'
        }
        response = auth_user_client.put(url, payload, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == 'new content'

    @pytest.mark.django_db
    def test_post_news_with_followers(self, auth_user_client, user_page_with_follower, user_post, admin_post, admin_page_with_follower):
        url = reverse('posts-news')
        response = auth_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_post_news_without_followers(self, auth_user_client, user_page, user_post, admin_post,):
        url = reverse('posts-news')
        response = auth_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


class TestPages:

    @pytest.mark.django_db
    def test_user_list_pages(self, auth_user_client, user_page, admin_page):
        url = reverse('pages-list')
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_admin_list_pages(self, auth_admin_client, user_page, admin_page):
        url = reverse('pages-list')
        response = auth_admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_user_retrieve_page(self, auth_user_client, user_page, admin_page):
        url = reverse('pages-detail', args=(user_page.pk,))
        response = auth_user_client.get(url)
        expected_data = page_serializers.RetrievePageSerializer(user_page).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    @pytest.mark.django_db
    def test_user_retrieve_private_page(self, auth_user_client, user_page, private_admin_page):
        url = reverse('pages-detail', args=(private_admin_page.pk,))
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_add_tag_to_page(self, auth_user_client, user_page, tags_list):
        url = reverse('pages-add-tags', args=(user_page.pk,))
        payload = {
            'list_tag_names': [tags_list[1].name, tags_list[2].name]
        }
        response = auth_user_client.patch(url, payload, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert set([tags_list[1].name, tags_list[2].name]).issubset(response.data['tags'])

    @pytest.mark.django_db
    def test_delete_tag_to_page(self, auth_user_client,  user_page_with_tags, tags_list):
        url = reverse('pages-delete-tags', args=(user_page_with_tags.pk,))
        payload = {
            'list_tag_names': [tags_list[3].name, tags_list[4].name]
        }
        response = auth_user_client.patch(url, payload, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert not set([tags_list[3].name, tags_list[4].name]).issubset(response.data['tags'])

    @pytest.mark.parametrize("is_to_permanent, expected", [(True, True), (False, False)],)
    @pytest.mark.django_db
    def test_admin_block_page(self, is_to_permanent, expected, auth_admin_client, user_page):
        url = reverse('pages-block', args=(user_page.pk,))
        payload = {
           'is_to_permanent': is_to_permanent,
        }
        response = auth_admin_client.patch(url, payload, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_permanent_blocked'] == expected

    @pytest.mark.django_db
    def test_user_block_page(self, auth_user_client, user_page):
        url = reverse('pages-block', args=(user_page.pk,))
        payload = {
            'is_to_permanent': False,
        }
        response = auth_user_client.patch(url, payload, format('json'))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_user_follow_page(self, auth_admin_client, admin, user_page):
        url = reverse('pages-follow', args=(user_page.pk,))
        response = auth_admin_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert admin in user_page.followers.all()

    @pytest.mark.django_db
    def test_user_unfollow_page(self, auth_admin_client, admin, user_page_with_follower):
        url = reverse('pages-unfollow', args=(user_page_with_follower.pk,))
        response = auth_admin_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert admin not in user_page_with_follower.followers.all()

    @pytest.mark.django_db
    def test_user_follow_own_page(self, auth_user_client, user, user_page):
        url = reverse('pages-unfollow', args=(user_page.pk,))
        response = auth_user_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert user not in user_page.followers.all()

    @pytest.mark.django_db
    def test_user_follow_private_page(self, auth_admin_client, admin, private_user_page):
        url = reverse('pages-follow', args=(private_user_page.pk,))
        response = auth_admin_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert admin not in private_user_page.followers.all()

    @pytest.mark.django_db
    def test_user_send_follow_request(self, auth_admin_client, admin, private_user_page):
        url = reverse('pages-send-follow-request', args=(private_user_page.pk,))
        response = auth_admin_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert admin not in private_user_page.followers.all()
        assert admin in private_user_page.follow_requests.all()

    @pytest.mark.django_db
    def test_user_unsend_follow_request(self, auth_admin_client, admin, user_private_page_with_follow_request):
        url = reverse('pages-unsend-follow-request', args=(user_private_page_with_follow_request.pk,))
        response = auth_admin_client.patch(url, {}, format('json'))

        assert response.status_code == status.HTTP_200_OK
        assert admin not in user_private_page_with_follow_request.followers.all()
        assert admin not in user_private_page_with_follow_request.follow_requests.all()

    @pytest.mark.django_db
    def test_list_follow_request(self, auth_user_client, user_private_page_with_follow_request):
        url = reverse('pages-list-follow-request', args=(user_private_page_with_follow_request.pk,))
        response = auth_user_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_accept_followers(self, auth_user_client, user_private_page_with_follow_request, admin):
        url = reverse('pages-accept-followers', args=(user_private_page_with_follow_request.pk,))
        payload = {
            'one': True,
            'user_id': admin.id
        }
        response = auth_user_client.patch(url, payload, format('json'))
        user_private_page_with_follow_request.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert admin in user_private_page_with_follow_request.followers.all()
        assert admin not in user_private_page_with_follow_request.follow_requests.all()

    @pytest.mark.django_db
    def test_reject_followers(self, auth_user_client, user_private_page_with_follow_request, admin):
        url = reverse('pages-reject-followers', args=(user_private_page_with_follow_request.pk,))
        payload = {
            'one': True,
            'user_id': admin.id
        }
        response = auth_user_client.patch(url, payload, format('json'))
        user_private_page_with_follow_request.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert admin not in user_private_page_with_follow_request.followers.all()
        assert admin not in user_private_page_with_follow_request.follow_requests.all()

