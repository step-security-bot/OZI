# noqa: INP001
"""Unit and fuzz tests for ``ozi-fix`` utility script"""
# Part of ozi.
# See LICENSE.txt in the project root for details.
import argparse
import os
import pathlib
import typing
from copy import deepcopy

import pytest
from hypothesis import given
from hypothesis import strategies as st

import ozi.fix
import ozi.new
from ozi.assets.structure import root_files, test_files, source_files
from ozi.fix import env

bad_namespace = argparse.Namespace(
    strict=False,
    verify_email=True,
    name='OZI-phony',
    author='',
    email='noreply@oziproject.dev',
    homepage='foobar',
    summary='A' * 512,
    copyright_head='',
    license_expression='CC0-1.0',
    license='CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    license_id='ITWASAFICTION',
    license_exception_id='WEMADEITUP',
    topic=['Utilities'],
    status='7 - Inactive',
    environment='Other Environment',
    framework='Pytest',
    audience='Other Audience',
    ci_provider='github',
    fix='',
    add=['ozi.phony'],
    remove=['ozi.phony'],
)


@pytest.fixture()
def bad_project(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Fixture to wrap the ``ozi-new project`` functionality."""
    fn = tmp_path_factory.mktemp('project_')
    namespace = deepcopy(bad_namespace)
    namespace.target = fn
    with pytest.warns(RuntimeWarning):
        ozi.new.new_project(namespace)
    return fn


@pytest.mark.parametrize(
    'key',
    ['Name', 'Version', 'Metadata-Version', 'Summary', 'License-Expression', 'License-File'],
)
def test_report_missing_required(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing requirements"""
    with bad_project.joinpath('PKG-INFO').open() as f:
        content = f.read()
    with bad_project.joinpath('PKG-INFO').open('w') as f:
        content = content.replace(key, '')
        f.write(content)
    with pytest.raises(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', [i for i in root_files if i not in ['PKG-INFO']])
def test_report_missing_required_root_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files"""
    os.remove(bad_project.joinpath(key))
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', ['PKG-INFO'])
def test_report_missing_required_pkg_info_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files"""
    os.remove(bad_project.joinpath(key))
    with pytest.raises((SystemExit, RuntimeWarning)):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', test_files)
def test_report_missing_required_test_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files"""
    os.remove(bad_project.joinpath('tests') / key)
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@pytest.mark.parametrize('key', source_files)
def test_report_missing_required_source_file(bad_project: pathlib.Path, key: str) -> None:
    """Check that we warn on missing files"""
    os.remove(bad_project.joinpath('ozi_phony') / key)
    with pytest.warns(RuntimeWarning):
        ozi.fix.report_missing(bad_project)


@given(
    type=st.just('target'),
    target=st.text(),
    operation=st.text(),
    sources=st.lists(st.text()),
    subdir=st.just(''),
    target_type=st.just('executable'),
)
def test_fuzz_RewriteCommand(  # noqa: DC102
    type: str,
    target: str,
    operation: str,
    sources: typing.List[str],
    subdir: str,
    target_type: str,
) -> None:
    ozi.fix.RewriteCommand(
        type=type,
        target=target,
        operation=operation,
        sources=sources,
        subdir=subdir,
        target_type=target_type,
    )


@given(
    target=st.just('.'),
    name=st.text(),
    fix=st.sampled_from(('test', 'source', 'root')),
    commands=st.lists(st.dictionaries(keys=st.text(), values=st.text())),
)
def test_fuzz_Rewriter(  # noqa: DC102
    target: str, name: str, fix: str, commands: typing.List[typing.Dict[str, str]]
) -> None:
    ozi.fix.Rewriter(target=target, name=name, fix=fix, commands=commands)


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__dir(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo/']
    assert len(rewriter.commands) == 2


def test_Rewriter_bad_project__iadd__bad_fix(  # noqa: DC102
    bad_project: pytest.FixtureRequest,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix='')
    with pytest.warns(RuntimeWarning):
        rewriter += ['foo/']
    assert len(rewriter.commands) == 0


def test_Rewriter_bad_project__isub__bad_fix(  # noqa: DC102
    bad_project: pytest.FixtureRequest,
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix='')
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__non_existing_child(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    with pytest.raises(RuntimeWarning):
        rewriter -= ['foo/']
    assert len(rewriter.commands) == 0


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__child(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').mkdir()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').mkdir()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').mkdir()
    rewriter -= ['foo/']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__python_file(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo.py').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo.py').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo.py').touch()
    rewriter -= ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__isub__file(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals = env.globals | {'project': vars(bad_namespace)}
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    if fix == 'root':
        pathlib.Path(str(bad_project), 'foo').touch()
    elif fix == 'source':
        pathlib.Path(str(bad_project), 'ozi_phony', 'foo').touch()
    elif fix == 'test':
        pathlib.Path(str(bad_project), 'tests', 'foo').touch()
    rewriter -= ['foo']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__file(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals.update({'project': vars(bad_namespace)})
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo.py']
    assert len(rewriter.commands) == 1


@pytest.mark.parametrize('fix', ['test', 'root', 'source'])
def test_Rewriter_bad_project__iadd__non_python_file(  # noqa: DC102
    bad_project: pytest.FixtureRequest, fix: str
) -> None:
    env.globals.update({'project': vars(bad_namespace)})
    rewriter = ozi.fix.Rewriter(target=str(bad_project), name='ozi_phony', fix=fix)
    rewriter += ['foo']
    assert len(rewriter.commands) == 1


header = """.. OZI
  Classifier: License-Expression :: Apache-2.0 WITH LLVM-exception
  Classifier: License-File :: LICENSE.txt
"""


def test_preprocess_warns_non_existing_target() -> None:  # noqa: DC102
    namespace = deepcopy(bad_namespace)
    namespace.target = 'temp/foobar'
    with pytest.warns(RuntimeWarning):
        ozi.fix.preprocess(namespace)


def test_preprocess_warns_file_target() -> None:  # noqa: DC102
    namespace = deepcopy(bad_namespace)
    namespace.target = 'temp/foobar.txt'
    pathlib.Path(namespace.target).touch()
    with pytest.warns(RuntimeWarning):
        ozi.fix.preprocess(namespace)


def test_preprocess_existing_target() -> None:  # noqa: DC102
    namespace = deepcopy(bad_namespace)
    namespace.target = '.'
    namespace = ozi.fix.preprocess(namespace)
    assert 'ozi.phony' not in namespace.add
    assert 'ozi.phony' not in namespace.remove


@given(add_items=st.lists(st.text()), remove_items=st.lists(st.text()))
def test_fuzz_preprocess_existing_target(  # noqa: DC102
    add_items: typing.List[str], remove_items: typing.List[str]
) -> None:
    namespace = deepcopy(bad_namespace)
    namespace.add.extend(add_items)
    namespace.remove.extend(remove_items)
    namespace.target = '.'
    namespace = ozi.fix.preprocess(namespace)
    assert 'ozi.phony' not in namespace.add
    assert 'ozi.phony' not in namespace.remove


@given(payload=st.text().map(header.__add__), as_message=st.booleans())
def test_fuzz_pkg_info_extra(payload: str, as_message: bool) -> None:  # noqa: DC102
    ozi.fix.pkg_info_extra(payload=payload, as_message=as_message)


@given(target=st.just('.'), strict=st.booleans(), use_tap=st.booleans())
def test_fuzz_report_missing(  # noqa: DC102
    target: pathlib.Path, strict: bool, use_tap: bool
) -> None:
    ozi.fix.report_missing(target=target)


@given(s=st.from_regex(r'^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$'))
def test_fuzz_underscorify(s: str) -> None:  # noqa: DC102
    ozi.fix.underscorify(s=s)
