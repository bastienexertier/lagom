import inspect

import pytest

from lagom import Container, magic_bind_to_container, injectable


class Something:
    pass


def test_partial_application_async_functions_pass_iscoroutinefunction(
    container: Container,
):
    @magic_bind_to_container(container)
    async def example_async_function(message: str) -> str:
        return message

    assert inspect.iscoroutinefunction(example_async_function)


def test_partial_application_async_functions_with_shared_pass_iscoroutinefunction(
    container: Container,
):
    @magic_bind_to_container(container, shared=[Something])
    async def example_async_function(message: str) -> str:
        return message

    assert inspect.iscoroutinefunction(example_async_function)


@pytest.mark.asyncio
async def test_calling_async_partials_works_as_expected(container: Container):
    @magic_bind_to_container(container)
    async def example_async_function(message: str) -> str:
        return message

    assert await example_async_function("test") == "test"


@pytest.mark.asyncio
async def test_calling_async_partials_on_a_object_works_as_expected(
    container: Container,
):
    class Thingy:
        async def example_async_function(
            self, message: str, something: Something = injectable
        ) -> str:
            assert isinstance(something, Something)
            return message

    thing = Thingy()
    bound_thing = container.partial(thing.example_async_function)
    assert await bound_thing("test") == "test"


@pytest.mark.asyncio
async def test_calling_async_partials_works_as_expected_with_shared_too(
    container: Container,
):
    @magic_bind_to_container(container, shared=[Something])
    async def example_async_function(message: str) -> str:
        return message

    assert await example_async_function("test") == "test"
