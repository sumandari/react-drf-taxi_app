from urllib import response
from venv import create
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import AccessToken

from taxi.routing import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}


@database_sync_to_async
def create_user(username, password, group='rider'):
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    user_group, _ = Group.objects.get_or_create(name=group)
    user.groups.add(user_group)
    user.save()

    access = AccessToken.for_user(user)
    return user, access


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'passW0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}')
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'passW0rd'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}')
        await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'Test! Cross my finger.'
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'passW0rd', 'test'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}')
        await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'Test! Cross my finger.'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('test', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'passw0rD', 'driver'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'Test! Cross my finger.'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('drivers', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_request_trip(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'test.user@example.com', 'pAssw0rd', 'rider'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.connect()
        await communicator.send_json_to({
            'type': 'create.trip',
            'data': {
                'pick_up_address': '123 Main Street',
                'drop_off_address': '456 Piney Road',
                'rider': user.id,
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')
        assert response_data['id'] is not None
        assert response_data['pick_up_address'] == '123 Main Street'
        assert response_data['drop_off_address'] == '456 Piney Road'
        assert response_data['status'] == 'REQUESTED'
        assert response_data['rider']['username'] == user.username
        assert response_data['driver'] is None
        await communicator.disconnect()

    async def test_create_trip_group(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'test.user@example.com',  'password', 'rider'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        await communicator.connect()

        # send a ride request
        await communicator.send_json_to({
            'type': 'create.trip',
            'data': {
                'pick_up_address': '123 Main Street',
                'drop_off_address': '456 Piney Road',
                'rider': user.id

            }
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')

        # send a message to trip group
        message = {
            'type': 'echo.message',
            'data': 'This is a test from rider'
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send(response_data['id'], message=message)

        response = await communicator.receive_json_from()
        assert response == message

        await communicator.disconnect()
