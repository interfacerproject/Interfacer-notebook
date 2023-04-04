import pytest
from dpp_test import params

# def pytest_addoption(parser):
#     parser.addoption(
#         "--present", action="store_true", help="specifies whether the trace has already been calculated"
#     )
#     parser.addoption(
#         "--nb_file", action="store", default='IFServices.ipynb', help="specifies the full path to the notebook"
#     )
#     parser.addoption(
#         "--endpoint", action="store", default='http://zenflows-debug.interfacer.dyne.org/api', help="specifies the endpoint to talk to"
#     )


def pytest_addoption(parser):
    for argmt in params:
        parser.addoption(argmt['positional'][1], **argmt['params'])


@pytest.fixture
def present(request):
    return request.config.getoption("--present")


@pytest.fixture
def nb_file(request):
    return request.config.getoption("--nb_file")


@pytest.fixture
def endpoint(request):
    return request.config.getoption("--endpoint")
