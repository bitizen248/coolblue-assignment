def test_rabbit_listener(
    container,
    mock_rabbit_connection,
    mock_routing_algorithm,
    test_message
):
    """
    Test that the rabbit listener service works as expected
    """
    rabbit_service = container.rabbit_service()
    rabbit_service.start_listening()
    assert mock_rabbit_connection.is_listening
    assert mock_rabbit_connection.declared_queues == [
        {
            "queue": "cb.RoutingProblems.Problems",
            "durable": True,
        }
    ]

    mock_rabbit_connection.call_callback(
        queue="cb.RoutingProblems.Problems",
        body=test_message.encode(),
        relpy_to="cb.RoutingProblems.Solutions",
    )

    rabbit_service.stop_listening()
    assert not mock_rabbit_connection.is_listening
    assert  len(mock_rabbit_connection.messages) == 1
    message = mock_rabbit_connection.messages[0]
    assert message["exchange"] == ""
    assert message["routing_key"] == "cb.RoutingProblems.Solutions"
    assert message["properties"].correlation_id == 1
