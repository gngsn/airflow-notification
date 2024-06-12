def test_stub(mocker):
    def foo(on_something):
        on_something('foo', 'bar')

    stub = mocker.stub(name='on_something_stub')
    run()
    foo(stub)
    stub.assert_called_once_with('foo', 'bar')
