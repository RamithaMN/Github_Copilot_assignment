from scripts.mcp_failure_simulation import run_scenarios


def test_failure_harness_stops_on_slow_outage_and_malformed_responses():
    results = run_scenarios()

    assert [result["scenario"] for result in results] == ["slow", "outage", "malformed"]
    assert all(result["status"] == "UNKNOWN" for result in results)
    assert all(result["write_attempted"] is False for result in results)
    assert "timeout" in results[0]["decision"]
    assert "unavailable" in results[1]["decision"]
    assert "malformed" in results[2]["decision"]
